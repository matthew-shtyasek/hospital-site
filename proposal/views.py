from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from .models import Proposal, WorkDaysSchedule, Post
from .forms import ProposalForm
from datetime import datetime, timedelta

def count_intervals(start_time, end_time):
    return int((end_time - start_time).seconds / 60 / 20)

def generate_time(start_time, iteration):
    return start_time + timedelta(minutes=20 * iteration)

def get_available_time_slots(work_days_schedule, doctor, user):
    busy_times = []

    for schedule in work_days_schedule:
        start_time = schedule.schedule.datetime_start
        end_time = schedule.schedule.datetime_end
        intervals = count_intervals(start_time, end_time)
        all_times = [generate_time(start_time, i) for i in range(intervals)]

        busy_times.extend(Proposal.objects.filter(type=doctor, visit_time__in=all_times, user=user).values_list('visit_time', flat=True))

    available_time_slots = [time for time in all_times if time not in busy_times]
    return available_time_slots

def proposal(request, doctor_id):
    doctor = get_object_or_404(Post, pk=doctor_id)
    work_days_schedule = WorkDaysSchedule.objects.filter(doctor=doctor)

    # Получаем доступные временные слоты для текущего дня
    available_time_slots = get_available_time_slots(work_days_schedule, doctor, request.user)

    proposals = Proposal.objects.filter(user=request.user, type=doctor)

    if request.method == 'POST':
        form = ProposalForm(doctor, work_days_schedule, request.POST)
        if form.is_valid():
            with transaction.atomic():
                selected_time = form.cleaned_data['selected_time']

                if Proposal.objects.filter(type=doctor, visit_time=selected_time, user=request.user).exists():
                    messages.error(request, 'Этот временной слот уже занят.')
                else:
                    proposal = form.save(commit=False)
                    proposal.user = request.user
                    proposal.type = doctor
                    proposal.visit_time = selected_time
                    proposal.save()

                    # Обновление списка доступных временных слотов
                    work_days_schedule = WorkDaysSchedule.objects.filter(doctor=doctor)
                    available_time_slots = get_available_time_slots(work_days_schedule, doctor, request.user)

                    messages.success(request, 'Заявка успешно отправлена и время забронировано.')

                    # Передаем обновленные временные слоты в форму
                    form.update_time_slot_queryset(work_days_schedule)

                    return redirect(reverse('proposal', args=(doctor_id,)))
    else:
        form = ProposalForm(doctor, work_days_schedule)

    # Обновление списка занятых временных слотов
    busy_times = Proposal.objects.filter(type=doctor, visit_time__in=available_time_slots, user=request.user).values_list('visit_time', flat=True)

    context = {'form': form, 'user': request.user, 'time_slots': available_time_slots, 'proposals': proposals, 'busy_times': busy_times}
    return render(request, 'proposal.html', context)
