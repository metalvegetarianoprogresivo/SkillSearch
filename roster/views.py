from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
import os
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
from django.contrib import messages
from search.views import get_availability
from consultantmarket import redirect_url
from django.contrib.auth.models import User
@require_POST
@csrf_exempt

def get_roster_bios(request):
    roster = request.session.setdefault('roster', [])
    response = {
        'bios': roster
    }
    try:
        today = datetime.date.today() 
        f = open ('../logdate.txt','a')
        today="date :"+str(datetime.datetime.now())+"    "+str(request.session['mail'])+"    "+"roster"
        f.write(today+"\n")
        f.close()
    except:
        pass
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
    loged_in = redirect_url.redirect_url(request)
    if loged_in:
       return redirect(loged_in)
    
    roster = request.session.get('roster')
    bios = Bio.objects.filter(pk__in=roster).order_by('name')
    consultant = {
            'bios': []
            }
    #list_bios = []
    #list_assignments = []
    total_cost = 0
    for bio in bios:
        total_cost += bio.cost
        print("cost "+str(total_cost))
        consultant['bios'].append(
                {
                    'bio':{
                        'data':bio,
                        'assignments':get_availability(bio)
                        }
                })
        #list_assignments.append(get_availability(bio))
        #assignments.append(get_availability(bio))
        #print(type(availability),type(days_until_available),type(utilisation),type(projects))
        #print(availability,days_until_available,utilisation,projects)
        #print("---get details")
        #print(type(bio))
        #print(dir(bio))
        #for assi in bio.assignments.all():
        #    print(dir(assi))
        ##print("---get details")
    #print(type(list_assignments[0]))
    context = {
        'title': 'Roster selected',
        'bios': bios,
        'consultant': consultant,
        'total_cost': total_cost,
        'total_consultants': len(consultant['bios'])
        }
        

    return render(request, 'roster/detail.html', context)


def send_roster(request):

    loged_in = redirect_url.redirect_url(request)
    if loged_in:
       return redirect(loged_in)    
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
            
            message += '\nGreetings from the Skills Searcher Team.'
            subject = 'Roster for {}'.format(project_title)
            from_mail = 'intersysinternalapplication@intersysconsulting.com'
            to_mail = [request.session['mail']]
            response = send_mail(subject, message, from_mail, to_mail, fail_silently=False)
            if response:
                print('sent succesfully')
                messages.success(request,"The email was sent successfully")
            return HttpResponseRedirect('/roster/detail')
    else:
        form = sendForm()
    #return render(request, 'roster/detail.html', {'form': form})
