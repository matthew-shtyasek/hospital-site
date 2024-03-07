from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Proposal, WorkDaysSchedule, Post, Days
from .forms import ProposalForm

def count_intervals(start_time, end_time):
    # Функция возвращает количество временных слотов
    return int((end_time - start_time).seconds / 60 / 20)

def generate_time(start_time, iteration):
    # Генерация времени с учетом интервала в 20 минут
    return start_time + timedelta(minutes=20 * iteration)

def get_available_time_slots(doctor, user, selected_day=None):
    # Получение доступных временных слотов для записи к врачу
    busy_times = Proposal.objects.filter(type=doctor, user=user).values_list('visit_time', flat=True)
    all_times = []

    work_days_schedule = WorkDaysSchedule.objects.filter(doctor=doctor)

    for schedule in work_days_schedule:
        start_time = schedule.schedule.datetime_start
        end_time = schedule.schedule.datetime_end

        if selected_day and schedule.day.date != selected_day:  # Фильтрация
            # Пропускаем временные интервалы, не относящиеся к выбранному дню
            continue

        # Генерируем слоты и исключаем те которые уже заняты
        intervals = count_intervals(start_time, end_time)
        all_times.extend([generate_time(start_time, i) for i in range(intervals)])

    available_time_slots = [time for time in all_times if time not in busy_times]
    return available_time_slots

def proposal(request, doctor_id):
    doctor = get_object_or_404(Post, pk=doctor_id)
    proposals = Proposal.objects.filter(user=request.user, type=doctor)

    if request.method == 'POST':
        form = ProposalForm(data=request.POST)
        if form.is_valid():
            selected_time = form.cleaned_data['selected_time']
            selected_day = form.cleaned_data['selected_day']

            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.type = doctor
            proposal.visit_time = selected_time
            proposal.save()

            return redirect(reverse('proposal', args=(doctor_id,)) + f'?selected_day={selected_day}')
    else:
        # Отображение формы для выбора дня и времени записи
        selected_day = request.GET.get('selected_day')
        work_days_schedule = WorkDaysSchedule.objects.filter(doctor=doctor)

        form = ProposalForm(work_days_schedule=work_days_schedule, selected_day=selected_day)

    # доступные временные слоты для бронирования
    available_time_slots = get_available_time_slots(doctor, request.user, selected_day)
    #  извлекаем временные слоты, которые уже заняты пользователем
    busy_times = Proposal.objects.filter(type=doctor, visit_time__in=available_time_slots, user=request.user).values_list('visit_time', flat=True)
    days = Days.objects.all()

    context = {'form': form, 'user': request.user, 'time_slots': available_time_slots, 'proposals': proposals, 'busy_times': busy_times, 'days': days, 'selected_day': selected_day}
    return render(request, 'proposal.html', context)