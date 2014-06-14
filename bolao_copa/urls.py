from django.conf.urls import patterns, include, url
from django.contrib import admin
from bolao.views import gerar_aposta, listar_pontos
from chat.views import chat_room
from django.shortcuts import redirect

def admin_index(request):
    return redirect('admin/')

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bolao_copa.views.home', name='home'),
    url(r'^$',admin_index),
    url(r'^bolao/', include('bolao.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^apostas/$', admin.site.admin_view(gerar_aposta)),
            (r'^ranking/$', admin.site.admin_view(listar_pontos)),
            (r'^chat/$', admin.site.admin_view(chat_room)),
        )
        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls