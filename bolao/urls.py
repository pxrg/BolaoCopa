from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bolao_copa.views.home', name='home'),
    url(r'rank/$', 'bolao.views.listar_pontos', name='pontos'),
    url(r'jogos/$', 'bolao.views.listar_jogos', name='jogos'),
    url(r'apostas/$', 'bolao.views.gerar_aposta', name='apostas'),
    url(r'selecoes/$', 'bolao.views.listar_selecoes', name='selecoes'),
)
