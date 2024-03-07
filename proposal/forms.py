from .models import Proposal
from django import forms


class ProposalForm(forms.ModelForm):
    selected_time = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    selected_day = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Proposal
        fields = ['selected_time', 'selected_day']

    def __init__(self, *args, **kwargs):
        work_days_schedule = kwargs.pop('work_days_schedule', None)
        selected_day = kwargs.pop('selected_day', None)
        super().__init__(*args, **kwargs)

        if work_days_schedule and selected_day:
            time_choices = [
                (schedule.schedule.datetime_start, schedule.schedule.datetime_start.strftime("%Y-%m-%d %H:%M"))
                for schedule in work_days_schedule.filter(day__date=selected_day)
            ]
            self.fields['selected_time'].widget = forms.Select(choices=[('', '--- Выберите время ---')] + time_choices)
            self.fields['selected_day'].initial = selected_day  # Устанавливаем начальное значение для selected_day

        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'