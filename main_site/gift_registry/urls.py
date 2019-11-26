from django.conf.urls import url
from django.views.generic import TemplateView

from gift_registry import views

urlpatterns = [
    url(r'^$', views.home, name='gift_home'),
    url(r'^(\w+)/$', views.GiftListView.as_view(), name='gift_list'),
    url(r'^gift/(\d+)/$', views.detail, name="gift_detail"),
    url(r'^gift/(\d+)/cancel/(.+)/$', views.cancel, name="gift_cancel"),
    url(r'^(\w+)/thanks-given/$', views.ThanksGiven.as_view(),
        name='thanks_given'),
    url(r'^(\w+)/thanks-cancel/$', views.ThanksCancel.as_view(),
        name='thanks_cancel'),
]
