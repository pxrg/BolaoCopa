from django.shortcuts import render
from django.http import HttpResponse
from models import Selecao, Grupo, Jogo, Pontuacao, Aposta
from django.contrib.auth.decorators import login_required
import re
from forms import ApostaForm

@login_required
def listar_selecoes(request, template='selecoes.html'):
	times = Selecao.objects.all()
	return render(request, template, {'selecoes':times})

@login_required
def listar_jogos(request, template='jogos.html'):
	grupos = Grupo.objects.filter(exibir=True)
	jogos = Jogo.objects.all()
	return render(request, template, {'grupos':grupos, 'jogos':jogos})

@login_required
def listar_pontos(request, template='ranking.html'):
	pontos = Pontuacao.objects.order_by('-pontos')
	return render(request, template, {'pontos':pontos})

@login_required
def gerar_aposta(request, template='apostas.html'):
	user = request.user
	if user.id != None:
		if request.method == "POST":
			apostas_itens = _process_post(request)
			for ap in apostas_itens.values():
				ap.save()
			return HttpResponse('Apostas Salvas com sucesso!')
			
		apostas = {}
		grupos = Grupo.objects.filter(exibir=True)
		jogos = [jg[0] for jg in Jogo.objects.values_list('id')]
		apostas = []
		for jg_id in jogos:
			ap = Aposta.objects.get_or_create(usuario_id = user.id, jogo_id=jg_id)
			apostas.append(ApostaForm(instance=ap[0]))

		context = {
			'grupos':grupos,
			'form':apostas,
		}
		return render(request, template,context)
	return HttpResponse('E necessario logar para visualizar')

@login_required
def _process_post(request):
	apostas = {}
	for key,item  in request.POST.items():
		id = re.sub('[^\d]', '', key)
		if id != '':
			if not apostas.has_key(id):
				apostas[id] = Aposta(usuario_id=request.user.id)
			attr = re.sub('[\d\[\]]', '', key)
			apostas[id].__setattr__(attr, int(item))
	return apostas

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

class GerarAposta(CreateView):
	model = Aposta
	template_name = 'apostas.html'
	success_url = '/'

	def get_context_data(self, **kargs):
		context = super(GerarAposta, self).get_context_data(**kargs)
		user = context.get('user')
		context['grupos'] = Grupo.objects.all()
		context['apostas'] = Aposta.objects.get(usuario_id = user.id)
		return context

	def form_valid(self, form):
		aposta = form.save(commit=False)
		aposta.usuario = self.request.user
		aposta.save()
		return super(GerarAposta, self).form_valid(self, form)

	def post(self, request, **kargs):
		apostas = self.process_post(request)
		for e in apostas.values():
			print e.save()
		return HttpResponse('Apostas Realizadas')

	def process_post(self, request):
		apostas = {}
		for key,item  in request.POST.items():
			id = re.sub('[^\d]', '', key)
			if id != '':
				if not apostas.has_key(id):
					apostas[id] = Aposta()
					apostas[id].usuario_id = request.user.id
				attr = re.sub('[\d\[\]]', '', key)
				apostas[id].__setattr__(attr, int(item))
		return apostas

