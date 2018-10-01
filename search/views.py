import os
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from bios.models import Bio, Assignments
from django.shortcuts import redirect
from datetime import datetime, date

def search(request):
    
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return redirect("https://skillssearcher.intersysconsulting.com/")
    
    try:
        q = request.GET["q"]
    except:
        raise Http404
    
    send_log(request.session['mail'])

    q = q.replace(', ', ' ').replace(',',' ')
    result_set = []
    tags = list(map(lambda word: word.strip().lower(), q.split(' ')))

    for bio in Bio.objects.all():
        fields = get_fields(bio)
        total_count, skills = get_skills_found(tags, fields)

        if total_count:
            availability, days_until_available, utilisation = get_availability(bio)
            result_set.append((skills, len(skills), total_count, bio, availability, days_until_available, 100-utilisation))

    result_set = sorted(result_set, key=lambda x:(x[5],-x[6], -x[1], -x[2], x[3]))

    paginator = Paginator(result_set, 10)
    page = request.GET.get('page')
    bios = paginator.get_page(page)

    context = {
        "title": "results",
        "bios": bios,
        "tags": tags,
        "q": q,
        "roster": request.session.setdefault('roster', []),
        "max" : len(result_set)
    }

    return render(request, "search/search.html", context)


def get_availability(bio):
    projects = list(filter(lambda x: (x.p3_end > date.today()), bio.assignments)) 
    total_utilisation = 0
    shown_date = date(3000, 12, 31)
    shown_date_100 = date(1995, 4, 11)
    project_at_100 = False
    
    if len(projects) is 0:
        days_until_available = -1
        availability = 'Available'

    else:
        for project in projects:
            total_utilisation += project.utilisation

            if project.utilisation >= 100
                if project.p3_end > shown_date_100:
                    shown_date_100 = project.p3_end
                    project_at_100 = True
            else:
                if project.p3_end < shown_date:
                    shown_date = project.p3_end
        
        if project_at_100 is True:
            shown_date = shown_date_100

        time_delta = shown_date - date.today()
        days_until_available = time_delta.days

        if total_utilisation < 100:
            days_until_available = 0
            availability = 'Available at {}%'.format(100 - total_utilisation)
        if days_until_available <= 30:
            availability = 'Available in {} days'.format(days_until_available)
        else:      
            availability = 'Busy until {}'.format(shown_date)

    return availability, days_until_available, total_utilisation


def get_fields(bio):
    names = bio.name.lower().split()
    skills = bio.skills.lower().replace('/',' ').split()
    tech_skills = bio.technical_skills.lower().replace('/',' ').split()
    profile = bio.profile.lower().replace('/',' ').split()
    experience = bio.experience.lower().replace('/',' ').split()

    fields = names + profile + skills + tech_skills + experience

    return fields


def get_skills_found(tags, fields):
    total_count = 0
    diff_skill_flag = False 
    skills = {}
    
    for tag in tags:
        skill_count = 0 
        for word in fields:
            if word == tag:
                diff_skill_flag = True
                total_count += 1
                skill_count += 1
        if diff_skill_flag is True:
            skills[tag.title()] = skill_count
            diff_skill_flag = False

    return total_count, skills


def send_log(mail):   
    f = open('../logdate.txt','a')
    today= "date: {}    {}    search".format(datetime.today(), mail)
    f.write(today+"\n")
    f.close()

