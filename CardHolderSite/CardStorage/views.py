import datetime
import random

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone, dateformat
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import GeneratorForm, SearchForm, TransactionForm
from .models import Card, CardTransaction


class Storage(ListView):
    template_name = "CardStorage/list_card.html"
    model = Card
    context_object_name = "cards"
    form = SearchForm

    def get_queryset(self):
        series = Q(series=self.request.GET.get('series')) if self.request.GET.get('series') else Q()
        number = Q(number__icontains=self.request.GET.get('number')) if self.request.GET.get('number') else Q()
        release_date = Q(release_date__gte=self.request.GET.get('release_date')) if self.request.GET.get(
            'release_date') else Q()
        end_date = Q(end_date__lte=self.request.GET.get('end_date')) if self.request.GET.get('end_date') else Q()
        status = Q(status=self.request.GET.get('status')) if self.request.GET.get('status') else Q()
        if len(self.request.GET):
            object_list = self.model.objects.filter(series & number & release_date & end_date & status)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for i in context["cards"]:
            if i.status == True:
                i.status = "Активна"
            elif i.status == False:
                i.status = "Просрочена"
        context["form"] = self.form()
        return context


class ProfileCard(View):
    template_name = "CardStorage/profile.html"
    form_class = TransactionForm

    def get(self, request, pk):
        transactions = CardTransaction.objects.filter(card_id=pk)
        card = Card.objects.get(pk=pk)
        form = self.form_class()
        if card.status == True:
            card.status = "Активна"
        elif card.status == False:
            card.status = "Просрочена"

        context = {
            "card": card,
            "transactions": transactions,
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            date_use = form.cleaned_data["date_use"]
            amount = form.cleaned_data["amount"]
            CardTransaction.objects.create(card_id=Card.objects.get(pk=pk), date_use=date_use, amount=amount)

            return redirect("profile", pk)



class GeneratorCard(View):
    form_class = GeneratorForm
    template_name = "CardStorage/generator_card.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            number_list = list("0123456789")
            time_now = dateformat.format(timezone.now(), 'Y-m-d H:i')
            release_date = datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M')
            if form.cleaned_data["end_date"] == "Year":
                end_date = release_date + relativedelta(year=1)
            elif form.cleaned_data["end_date"] == "Six-months":
                end_date = release_date + relativedelta(months=6)
            elif form.cleaned_data["end_date"] == "Month":
                end_date = release_date + relativedelta(months=1)

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
