from django.conf.urls import url
from django.views.generic import TemplateView

from gift_registry import views

urlpatterns = [
    url(r'^$', views.home, name='gift_home'),
    url(r'^(\w+)/$', views.GiftListView.as_view(), name='gift_list'),
    url(r'^gift/(\d+)/$', views.detail, name="gift_detail"),
    url(r'^gift/(\d+)/cancel/(.+)/$', views.cancel, name="gift_cancel"),
    url(r'^thanks-given/$', TemplateView.as_view(
        template_name='gift_registry/thanks_given.html'),
        name='thanks_given'),
    url(r'^thanks-cancel/$', TemplateView.as_view(
        template_name='gift_registry/thanks_cancel.html'),
        name='thanks_cancel'),
]
