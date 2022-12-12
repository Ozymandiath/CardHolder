from django.utils import timezone

from .models import Card

def activation_check(get_response):
    def middleware(request):
        cards = Card.objects.all()
        time_now = timezone.now()
        for card in cards:
            if time_now > card.end_date:
                Card.objects.filter(pk=card.pk).update(status=False)
        response = get_response(request)

        return response
    return middleware