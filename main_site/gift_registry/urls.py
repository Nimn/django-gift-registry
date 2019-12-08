from django.conf.urls import url

from gift_registry import views

urlpatterns = [
    url(r'^$', views.home, name='gift_home'),
    url(r'^([-a-z0-9]+)/$', views.GiftListView.as_view(), name='gift_list'),
    url(r'^gift/(\d+)/$', views.detail, name="gift_detail"),
    url(r'^gift/(\d+)/cancel/(.+)/$', views.cancel, name="gift_cancel"),
    url(r'^([-a-z0-9]+)/thanks-given/$', views.ThanksGiven.as_view(),
        name='thanks_given'),
    url(r'^([-a-z0-9]+)/thanks-cancel/$', views.ThanksCancel.as_view(),
        name='thanks_cancel'),
]
