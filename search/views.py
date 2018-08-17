from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from bios.models import Bio
from django.shortcuts import redirect

def search(request):
    '''
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
                return redirect("https://skillsearch.westeurope.cloudapp.azure.com/")
    '''
    try:
        q = request.GET["q"]
    except:
        raise Http404
    result_set = []
    tags = list(map(lambda word: word.strip().lower(), q.split(",")))
    for bio in Bio.objects.all():
        count = 0
        skills = list(map(
            lambda ts: ts.name_and_title.lower(), bio.technical_skills.all()
        ))
        capabilities = list(map(
            lambda c: c.name_and_title.lower(), bio.capabilities.all()
        ))
        print(skills)
        print(type(skills))
        for tag in tags:
            count += (tag in capabilities) or (tag in skills)
        if count:
            result_set.append((count, bio))
    # TODO: uncomment next lines when loggin implementation
    """
    if request.session.get('logged'):
        pass
    else:
        raise Http404
    """
    result_set = sorted(result_set, key=lambda x:(-x[0], x[1]))
    paginator = Paginator(result_set, 10)
    page = request.GET.get('page')
    bios = paginator.get_page(page)
    context = {
        "title": "Search results",
        "bios": bios,
        "tags": tags,
        "q": q,
        "roster": request.session.setdefault('roster', [])
    }
    return render(request, "search/search.html", context)
