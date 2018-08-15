from bios.models import Bio
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@require_POST
@csrf_exempt

def get_roster_bios(request):
    roster = request.session.setdefault('roster', [])
    response = {
        'bios': roster
    }

    return JsonResponse(response)

@require_POST
@csrf_exempt
def add_to_roster(request):
    bio_id = request.POST['bio_id']
    bio = get_object_or_404(Bio, pk=bio_id)
    if bio.pk in request.session.setdefault('roster', []):
        added = False
    else:
        request.session['roster'].append(bio.pk)
        request.session.modified = True
        added = True
    response = {
        'bio': bio.pk,
        'added': added
    }

    return JsonResponse(response)

@require_POST
@csrf_exempt
def remove_from_roster(request):
    bio_id = request.POST['bio_id']
    bio = get_object_or_404(Bio, pk=bio_id)
    if bio.pk in request.session.setdefault('roster', []):
        request.session['roster'].remove(bio.pk)
        request.session.modified = True
        added = 0
    else:
        added = 0
    response = {
        'bio': bio.pk,
        'added': added
    }

    return JsonResponse(response)

def roster_detail(request):
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
                return redirect("https://skillsearch.westeurope.cloudapp.azure.com/")
    roster = request.session.get('roster')
    bios = Bio.objects.filter(pk__in=roster).order_by('name')

    context = {
        'title': 'Roster selected',
        'bios': bios,
    }

    return render(request, 'roster/detail.html', context)
