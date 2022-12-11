import random

from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .forms import GeneratorForm
from .models import Card


class Storage(ListView):
    template_name = "CardStorage/list_card.html"
    model = Card
    context_object_name = "cards"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for i in context["cards"]:
            if i.status == True:
                i.status = "Активна"
            elif i.status == False:
                i.status = "Просрочена"
        return context


class GeneratorCard(View):
    form_class = GeneratorForm
    template_name = "CardStorage/generator_card.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            number_list = list("0123456789")
            release_date = timezone.now()
            if form.cleaned_data["end_date"] == "Year":
                end_date = release_date + relativedelta(year=1)
            elif form.cleaned_data["end_date"] == "Six-months":
                end_date = release_date + relativedelta(months=6)
            elif form.cleaned_data["end_date"] == "Month":
                end_date = release_date + relativedelta(month=1)

            for _ in range(form.cleaned_data["count_card"]):
                number = ""
                for _ in range(16):
                    number += random.choice(number_list)
                Card.objects.create(
                    series=form.cleaned_data["series"],
                    number=number,
                    release_date=release_date,
                    end_date=end_date,
                    status=True
                )
            return redirect("home")
