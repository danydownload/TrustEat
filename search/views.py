import operator
from django.shortcuts import render
from .forms import SearchForm
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from user.models import Recensione
from localManagement.models import *
from order.views import db_order_consistance
from accounts.models import User
from order.models import OrdineInAttesa


class Ricerca(ListView):
    form = SearchForm()
    model = Localita
    form_class = SearchForm
    template_name = 'search/index.html'
    ordered = []
    pos = ''

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        db_order_consistance()
        form = SearchForm()

        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_superuser):
            location = User.objects.get(username=request.user).cap
            self.sorting(Locale.objects.filter(cap=Localita.objects.get(cap=location)).all())
            form = SearchForm(initial={'Position': Localita.objects.get(cap=location), 'Tag': None}, )
            self.pos = Localita.objects.get(cap=location).nome_localita
        else:
            self.sorting(Locale.objects.all())
        if request.method == 'GET':
            form = SearchForm(request.GET or None)
            if form.is_valid():
                location = form.cleaned_data['Position']
                print('località selezionata: ' + str(location))
                if location is not None:
                    self.sorting(Locale.objects.filter(cap=Localita.objects.get(nome_localita=location)).all())
                    self.pos = location
                else:
                    self.sorting(Locale.objects.all())
                    self.pos = ''
                tags = list(form.cleaned_data['Tag'].values_list('nome_tag'))
                if tags:
                    tmp = []
                    for loc in self.ordered:
                        c = 0
                        for sl in list(
                                Tag.objects.filter(locale_tag__cod_locale=loc['local'].pk).values_list('nome_tag')):
                            if sl in tags:
                                c += 1
                        if c == len(tags):
                            tmp.append(loc)
                    self.ordered = tmp
        context = {'locals': self.ordered[:15], 'SearchForm': form,
                   'location': self.pos, 'location_len': len(str(self.pos))}
        return render(request, self.template_name, context)

    def sorting(self, locals_list):
        self.ordered = []
        for local in locals_list:
            voti = Recensione.objects.filter(cod_locale=local)
            n_rec = vote = 0
            if voti.count():
                for el in voti:
                    if el.voto in range(6):
                        vote += el.voto
                        n_rec += 1
            if n_rec:
                vote = vote / n_rec
            else:
                vote = 0
            f = ""
            for foto in FotoLocale.objects.filter(cod_locale=local):
                f = foto.foto_locale.url

            self.ordered.append({'local': local, 'voto': str(round(vote, 2)).replace('.', ','), 'n_rec': n_rec,
                                 'foto': f})
            self.ordered.sort(key=operator.itemgetter('n_rec'), reverse=True)
            self.ordered.sort(key=operator.itemgetter('voto'), reverse=True)
