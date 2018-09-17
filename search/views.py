import os
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from bios.models import Bio
from django.shortcuts import redirect
from datetime import datetime, date

def search(request):
    
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return redirect("https://skillssearcher.intersysconsulting.com/")
    
    try:
        q = request.GET["q"]
    except:
        raise Http404
    
    q = q.replace(', ', ' ').replace(',',' ')
    result_set = []
    tags = list(map(lambda word: word.strip().lower(), q.split(' ')))

    for bio in Bio.objects.all():
        days_until_available = datetime.strptime(bio.assignment_date,'%Y-%m-%d').date()  - date.today()
        if days_until_available.days <= 0:
            availability = 'Available'
        elif days_until_available.days <= 30:
            availability = 'Available within the next 30 days'
        else:      
            availability = 'Not Available'

        try:
            names = bio.name.lower().split()
            skills = bio.skills.lower().replace('/',' ').split()
            tech_skills = bio.technical_skills.lower().replace('/',' ').split()
            profile = bio.profile.lower().replace('/',' ').split()
            experience = bio.experience.lower().replace('/',' ').split()
        except:
            pass
        fields = names + profile + skills + tech_skills + experience

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
        if total_count:
            result_set.append((skills, len(skills), total_count, bio, availability))
    # TODO: uncomment next lines when loggin implementation
    """
    if request.session.get('logged'):
        pass
    else:
        raise Http404
    """
    result_set = sorted(result_set, key=lambda x:(x[4], -x[1], -x[2], x[3]))
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
    try:
        today = datetime.date.today()   
        f = open ('../logdate.txt','a')
        today="date :"+str(datetime.datetime.now())+"    "+str(request.session['mail'])+"    "+"search"
        f.write(today+"\n")
        f.close()
    except:
        pass    
    return render(request, "search/search.html", context)
