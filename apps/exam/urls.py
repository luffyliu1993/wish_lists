from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$',views.index),
    url(r'^login$',views.login_check),
    url(r'^register$',views.register),
    url(r'^dashboard$',views.show_dashboard),
    url(r'^wish_items/create$',views.add_item),
    url(r'^add_item$',views.process_add),
    url(r'^logout$',views.logout),
    url(r'^wish_items/(?P<item_id>\d+?)$',views.show_item),
    url(r'^add_wish/(?P<item_id>\d+?)$',views.add_wish),
    url(r'^delete/(?P<item_id>\d+?)$',views.delete),
    url(r'^remove_wish/(?P<item_id>\d+?)$',views.remove_wish)
]
