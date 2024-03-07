from .models import Proposal
from django import forms


class ProposalForm(forms.ModelForm):
    selected_time = forms.TimeField(widget=forms.HiddenInput())
    selected_day = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Proposal
        fields = ['selected_time', 'selected_day']

    def __init__(self, *args, **kwargs):
        selected_day = kwargs.pop('selected_day', None)
        super().__init__(*args, **kwargs)

        if selected_day:
            self.fields['selected_day'].initial = selected_day  # Устанавливаем начальное значение для selected_day
