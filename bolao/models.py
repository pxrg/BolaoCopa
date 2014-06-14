# coding: utf-8

from django.db import models
from django.conf import settings

class Selecao(models.Model):
	nome = models.CharField(
		max_length=50,verbose_name=u'Nome',
		unique=True, null=False)
	img = models.URLField(verbose_name=u'Link Imagem')

	def __unicode__(self):
		return "%s"%self.nome

	class Meta:
		verbose_name = u'Seleção'
		verbose_name_plural = u'Seleções'

class Grupo(models.Model):
	nome = models.CharField(
		max_length=50,verbose_name=u'Nome',
		unique=False, null=False)
	exibir = models.BooleanField(verbose_name=u'Exibir',default=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		ordering=['nome']


class Jogo(models.Model):
	time_a = models.ForeignKey('Selecao', related_name='time_a',
	 verbose_name=u'Time A', null=False, blank=False)
	time_b = models.ForeignKey('Selecao', related_name='time_b',
		verbose_name=u'Time B', null=False, blank=False)
#	resultado = models.OneToOneField(Resultado,
#		verbose_name=u'Resultado', null=True, blank=True)
	grupo = models.ForeignKey('Grupo',
		verbose_name=u'Grupo', null=False, blank=False)

	def __unicode__(self):
		return "%s - %s X %s"%(
			self.grupo.nome,
			self.time_a.nome,
			self.time_b.nome)

	class Meta:
		ordering=['grupo','time_a']

class Pontuacao(models.Model):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
	#usuario = models.OneToOneField(settings.AUTH_USER_MODEL, null=False)
	pontos = models.IntegerField()	

	def __unicode__(self):
		return "%s --> %d pts"%(self.usuario, self.pontos)

	class Meta:
		ordering = ['usuario']
		verbose_name = u'Pontuação'
		verbose_name_plural = u'Pontuações'


class Placar(models.Model):
	gols_time_a = models.PositiveIntegerField(
		verbose_name=u'Resultado Time A', default=0)
	gols_time_b = models.PositiveIntegerField(
		verbose_name=u'Resultado Time B', default=0)
	jogo = models.ForeignKey('Jogo', null=False, blank=False)

	def __unicode__(self):
		return "%s - %s  (%d) X %s  (%d)"%(
			self.jogo.grupo,
			self.jogo.time_a.nome,
			self.gols_time_a,
			self.jogo.time_b.nome,
			self.gols_time_b)

	class Meta:
		ordering = ['jogo']

class Resultado(Placar):
	vencedor = models.CharField(
		max_length=60,verbose_name='Vencedor',
		blank=True,default='------')

	def __unicode__(self):
		return "%s - %s  (%d) X %s  (%d) : Vencedor: %s"%(
			self.jogo.grupo,
			self.jogo.time_a.nome,
			self.gols_time_a,
			self.jogo.time_b.nome,
			self.gols_time_b, 
			self.vencedor)

	class Meta:
		verbose_name = u'Resultado'
		verbose_name_plural = u'Resultados'

class Aposta(Placar):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __unicode__(self):
		return "%s --> %s "%(self.usuario, super(Aposta, self).__unicode__())

	def get_absolute_url(self):
		return '/admin/aposta/'

	class Meta:
		ordering = ['usuario','jogo']
		permissions = (
			('gerar_aposta', 'Poder visualizar e gerar aposta'),
			)


