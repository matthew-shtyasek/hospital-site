from django import forms
from .models import Proposal

class ProposalForm(forms.ModelForm):
    selected_time = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Proposal
        fields = ['selected_time']

    def __init__(self, doctor, work_days_schedule, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Используйте selected_time для формирования списка значений времени
        time_choices = [(schedule.schedule.datetime_start, schedule.schedule.datetime_start.strftime("%Y-%m-%d %H:%M")) for schedule in work_days_schedule]
        self.fields['selected_time'].widget = forms.Select(choices=[('', '--- Выберите время ---')] + time_choices)

        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def update_time_slot_queryset(self, work_days_schedule):
        # Обновление списка доступных временных слотов после успешной отправки заявки
        time_choices = [(schedule.schedule.datetime_start, schedule.schedule.datetime_start.strftime("%Y-%m-%d %H:%M")) for schedule in work_days_schedule]
        self.fields['selected_time'].widget.choices = [('', '--- Выберите время ---')] + time_choices