from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from bios.models import Bio
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from consultantmarket.views import index
from .forms import sendForm
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
        return redirect("https://skillssearcher.intersysconsulting.com/")
    
    roster = request.session.get('roster')
    bios = Bio.objects.filter(pk__in=roster).order_by('name')

    context = {
        'title': 'Roster selected',
        'bios': bios,
    }

    return render(request, 'roster/detail.html', context)


def send_roster(request):
    
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return redirect("https://skillssearcher.intersysconsulting.com/")
    
#confirm from_mail in 'consultantmarket/settings.py'
    if request.method == 'POST':
        form = sendForm(request.POST)
        
        if form.is_valid():
            roster = request.session.get('roster')
            bios = Bio.objects.filter(pk__in=roster).order_by('name')
            
            project_title = form.cleaned_data['title']
            name = request.session['displayName']
            message = 'Hello {},\n\nYour roster for the project {} is the following.\nPlease feel free to select on the links of each consultant to see their bios.\n\nRoster:\n'.format(name, project_title)
            
            for bio in bios:
                message += '{}:\n\t{}\n'.format(bio.name,bio.url)
            
            message += '\nGreetings from the Skill Search Team.'
            subject = 'Roster for {}'.format(project_title)
            from_mail = 'internalapp@intersysconsulting.com'
            to_mail = [request.session['mail']]
            response = send_mail(subject, message, from_mail, to_mail, fail_silently=False)
            if response:
                print('sent succesfully')
              
                messages.success(request,"The email was sended successfully")
            return HttpResponseRedirect('/roster/detail')
    else:
        form = sendForm()
    return render(request, 'roster/detail.html', {'form': form})
