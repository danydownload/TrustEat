from django.shortcuts import render


def contattaci(request):
    messaggio = "Per qualsiasi problema/dubbio/domanda/informazione ci potete contattare al seguente indirizzo email:"
    context = {'messaggio': messaggio}
    return render(request, 'contatti.html', context)
