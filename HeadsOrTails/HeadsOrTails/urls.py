from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from HeadsOrTailsAPI.views import sign_up_in

urlpatterns = [
    url(r'^login/$', sign_up_in, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'home.html'}, name='logout'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^games/$', TemplateView.as_view(template_name='home.html'), name='games'),
    url(r'^games/id/$', TemplateView.as_view(template_name='game.html'), name='game'),
    url(r'^admin/', admin.site.urls),
]