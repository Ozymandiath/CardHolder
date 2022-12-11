from django import forms


class GeneratorForm(forms.Form):
    END_DATE_CHOICES = [
        ('Year', '1  год'),
        ('Six-months', '6 месяцев'),
        ('Month', '1 месяц'),
    ]
    series = forms.IntegerField(max_value=9999, min_value=1, label="Серия")
    end_date = forms.ChoiceField(choices=END_DATE_CHOICES, label="Дата окончания")
    count_card = forms.IntegerField(min_value=1, label="Кол-во карт", required=True)
