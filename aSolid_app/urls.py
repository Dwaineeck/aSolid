from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^log$', views.log),
    url(r'^registration$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^jobs$', views.jobs),
    url(r'^create$', views.create),
    url(r'^add_add/(?P<id>\d+)$', views.add_add),
    url(r'^remove_add/(?P<id>\d+)$', views.remove_add),
    url(r'^jobs/(?P<id>\d+)$', views.show_user),
    url(r'^users/(?P<id>\d+)/edit$', views.edit),
    url(r'^users/(?P<id>\d+)/update$', views.update),
    url(r'^users/(?P<id>\d+)/delete$', views.destroy),
]