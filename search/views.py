import os
import math
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
    projects=[]
    tags = list(map(lambda word: word.strip().lower(), q.split(' ')))

    consultant_skills = {}
    global_skill_count = {}
    global_count = 0
    bios = Bio.objects.all()

    for bio in bios:
        consultant_skills[bio.name] = {}
        for tag in tags:
            profile = get_profile(bio)
            skills = get_skills(bio)
            experience = get_experience(bio)

            consultant_skills[bio.name].update({tag:{'skill_ocurrence': get_skill_ocurrence(tag, bio), 'flags':{'profile':tag in profile,
            'skills':tag in skills,
            'experience':tag in experience}}})

    for tag in tags:
        global_skill_count[tag] = 0

        for bio in bios:
            global_skill_count[tag] += consultant_skills[bio.name][tag]['skill_ocurrence']

        global_count += global_skill_count[tag]

    weights = {}
    for tag in tags:
        weights[tag] = global_skill_count[tag]/global_count

    for bio in bios:
        total = 0
        skills = []
        for tag in tags:
            total += consultant_skills[bio.name][tag]['skill_ocurrence']
            if consultant_skills[bio.name][tag]['skill_ocurrence']:
                skills += tag
        if total:
            availability, days_until_available, utilisation, projects = get_availability(bio)
            w_A = 40
            w_V = 35
            w_I = 25
            relevance_funct = w_A*utilisation
            for tag in tags:
                relevance_funct += w_V*weights[tag]*(consultant_skills[bio.name][tag]['skill_ocurrence']>0) 
                relevance_funct += w_I*weights[tag]*(1/6)*consultant_skills[bio.name][tag]['flags']['experience']
                relevance_funct += w_I*weights[tag]*(3/6)*consultant_skills[bio.name][tag]['flags']['profile']
                relevance_funct += w_I*weights[tag]*(2/6)*consultant_skills[bio.name][tag]['flags']['skills']

            result_set.append((skills, len(skills), total, bio, availability, days_until_available, 100-utilisation, projects, utilisation, relevance_funct))

    result_set = sorted(result_set, key=lambda x:(-x[-1], x[5], -x[6], -x[1], -x[2], x[3]))
    #get relevance intead of sorted
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

def get_skill_ocurrence(tag, bio):
    fields = get_fields(bio)
    skill_ocurrence = 0

    for word in fields:
        if tag == word:
            skill_ocurrence += 1
    
    return skill_ocurrence

def get_availability(bio):
    projects = list(filter(lambda x: (x.p3_end - date.today()).days > 0, bio.assignments.all()))
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

            if project.utilisation >= 100:
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
        elif days_until_available <= 30:
            availability = 'Available in {} days'.format(days_until_available)
        else:      
            availability = 'Commited until {}'.format(shown_date)

    return availability, days_until_available, total_utilisation,projects



def get_fields(bio):
    names = bio.name.lower().split()

    fields = names + get_skills(bio) + get_experience(bio) + get_profile(bio)

    return fields 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

def get_skills(bio):
    skills = bio.skills.lower().replace('/',' ').split()
    tech_skills = bio.technical_skills.lower().replace('/',' ').split()
    
    all_skills = skills + tech_skills 

    return all_skills


def get_experience(bio):
    experience = bio.experience.lower().replace('/',' ').split()
    
    return experience


def get_profile(bio):
    profile = bio.profile.lower().replace('/',' ').split()

    return profile    

#deprecate?
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