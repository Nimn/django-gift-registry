from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from gift_registry.forms import GiverForm
from gift_registry.models import Gift, Giver, Event


def get_event_name(slug=None):
    lbl = settings.GIFT_REGISTRY_SETTINGS['EVENT_NAME']
    if not slug:
        return lbl
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return lbl
    return event.name


class GiftListView(ListView):
    """Show all live gifts."""

    def get_queryset(self):
        queryset = Gift.objects.filter(live=True,
                                       event__slug=self.args[0])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GiftListView, self).get_context_data(**kwargs)
        context['event_name'] = get_event_name(self.args[0])
        return context


class ThanksGiven(TemplateView):
    template_name = "gift_registry/thanks_given.html"

    def get_context_data(self, **kwargs):
        context = super(ThanksGiven, self).get_context_data(**kwargs)
        context["event"] = self.args[0]
        return context


class ThanksCancel(TemplateView):
    template_name = "gift_registry/thanks_cancel.html"

    def get_context_data(self, **kwargs):
        context = super(ThanksCancel, self).get_context_data(**kwargs)
        context["event"] = self.args[0]
        return context


def home(request):
    q = Event.objects.filter(gifts__live=True)
    events = []
    for event in q.all():
        events.append([event.slug, event.name])
    context = {}
    context['event_name'] = get_event_name()
    context["events"] = events
    return render(request, "gift_registry/home.html", context=context)


def detail(request, id):
    """Show details of a particular gift."""
    gift = get_object_or_404(Gift, pk=id)
    giver = Giver(gift_id=id)
    bookable = True
    if request.method == 'POST':
        giver_form = GiverForm(request.POST)
        if not gift.bookable():
            bookable = False
        elif giver_form.is_valid():
            giver_form.save()
            return redirect('thanks_given', gift.event.slug)
        return render(
            request, 'gift_registry/gift_detail.html',
            context={'object': gift,
                     "bookable": bookable,
                     'giver_form': giver_form})
    else:
        return render(
            request, 'gift_registry/gift_detail.html',
            context={'object': gift,
                     "bookable": bookable,
                     'giver_form': GiverForm(instance=giver)})


def cancel(request, giver_id, key):
    giver = get_object_or_404(Giver, id=giver_id)
    if giver.secret_key() != key:
        raise PermissionDenied
    gift = giver.gift

    giver.delete()
    return redirect('thanks_cancel', gift.event.slug)
