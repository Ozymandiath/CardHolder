from django import forms

from .models import Card


class GeneratorForm(forms.Form):
    END_DATE_CHOICES = [
        ('Year', '1  год'),
        ('Six-months', '6 месяцев'),
        ('Month', '1 месяц'),
    ]
    series = forms.IntegerField(max_value=9999, min_value=1, label="Серия")
    end_date = forms.ChoiceField(choices=END_DATE_CHOICES, label="Дата окончания")
    count_card = forms.IntegerField(min_value=1, label="Кол-во карт", required=True)


class SearchForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            "series",
            "number",
            "release_date",
            "end_date",
            "status"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['series'].required = False
        self.fields['number'].required = False
        self.fields['release_date'].required = False
        self.fields['end_date'].required = False
        self.fields['status'].required = False
        self.fields['status'].value = True
