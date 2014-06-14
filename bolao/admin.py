# coding: utf-8

from django.conf.urls import patterns
from django.contrib import admin

from models import Selecao, Jogo, Grupo, \
Resultado, Aposta, Pontuacao
from views import gerar_aposta, listar_pontos

class ApostaAdminForm(admin.ModelAdmin):
	model = Aposta
	list_display = ('aposta','usuario', 'jogo')
	list_filter = ['usuario__username','jogo__grupo__nome',]

	search_fields = ['usuario__username','jogo__grupo__nome',]

admin.site.register(Selecao)
admin.site.register(Grupo)
admin.site.register(Jogo)
admin.site.register(Resultado)
admin.site.register(Aposta, ApostaAdminForm)
admin.site.register(Pontuacao)
