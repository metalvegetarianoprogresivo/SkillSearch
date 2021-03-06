import json
import os
import requests
import re

from django.shortcuts import redirect, render, reverse
from django.conf import settings
from bs4 import BeautifulSoup
from tika import parser
from .models import Bio, Assignments
from datetime import datetime, date
import urllib.parse
from django.conf import settings
from consultantmarket import redirect_url
from django.contrib.auth.models import User

def index(request):
    print("entro al index ")
    
    loged_in = redirect_url.redirect_url(request)
    if loged_in:
        print(loged_in)
        return redirect(loged_in)

    request.session['my_domain'] = redirect_url.read_main_url()
    request.session["my_domain"] = urllib.parse.quote_plus(request.session["my_domain"])
    if("code" in request.GET.keys()):
        print("entro a code")
        get_token(request, request.GET.get("code"))
    
    return render(request, 'bios/index.html')

    try:
        today = datetime.date.today() 
        f = open ('../logdate.txt','a')
        today="date :"+str(datetime.datetime.now())+"    "+str(request.session['mail'])+"    "+"bio"
        f.write(today+"\n")
        f.close()
    except: 
        pass

      
def get_documents(request):
    if settings.FAKE_DATA:
        return redirect(redirect_url.read_main_url()+"bios/?code=32ewadfsghtyu678iuyhkj==")
    else:
        try:
            url_redirect = "https://intersys.my.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&redirect_uri="+request.session["my_domain"]+"bios%2F"
        except:
            return redirect(redirect_url.read_main_url())
        
    print(url_redirect)
    return redirect(url_redirect)


def get_token(request, code):
    sufix = "/services/oauth2/token"
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else:
        url = "https://intersys.my.salesforce.com"+sufix

    payload = "grant_type=authorization_code&redirect_uri="+request.session["my_domain"]+"bios%2F&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&client_secret=1639331975173970710&code="+code
    headers = {"content-type":"application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data= payload, headers = headers)
    resJson = json.loads(response.text)
    print(resJson)
    try:
        get_bios(resJson["access_token"])
    except:
        return redirect(redirect_url.read_main_url())


def get_location(token, name):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer "+token}
    location = "No location Found"

    try:
        response = requests.request("GET", url+"SELECT KimbleOne__Resource__c.KimbleOne__BusinessUnit__r.Name FROM KimbleOne__Resource__c WHERE name = '"+name+"'", headers = headers)
        response_json=json.loads(response.text)
        try:
            location = response_json['records'][0]['KimbleOne__BusinessUnit__r']['Name']
            if location is None:
                location = "No location Found"
        except:
            pass
    except:
        pass  

    return(location)


def get_name_link(token):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer " + token}
    names_link = {}

    response = requests.request("GET", url+"SELECT Name,KimbleOne__Resource__c.Resource_Bio__r.Bio_Url__c FROM KimbleOne__Resource__c WHERE KimbleOne__ResourceType__c = 'a7J0c000002VD4LEAW' AND KimbleOne__Grade__c != 'a5G0c000000g2IXEAY' AND KimbleOne__StartDate__c <= TODAY AND KimbleOne__EndDate__c = Null", headers = headers)
    consultants=json.loads(response.text)
    
    if (consultants.get('records')):
        for consultant in consultants.get('records'):
            if consultant.get('Resource_Bio__r'):
                if consultant['Resource_Bio__r'].get('Bio_Url__c') is not None:
                    names_link[consultant['Name']] = consultant['Resource_Bio__r']['Bio_Url__c']

    from bios.models import Bio
    print('vivo')
    print(Bio.objects.all())
    records_in_db = Bio.objects.all()
    [record.delete() for record in records_in_db if record.name not in [y.get('Name') for y in [x for x in consultants.get('records')] if y.get('Name')]]

    return names_link


def get_title(token, name):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer " + token}

    try:
        response = requests.request("GET", url+"SELECT KimbleOne__Resource__c.KimbleOne__Grade__r.Name FROM KimbleOne__Resource__c WHERE name = '"+name+"'", headers = headers)
        title = json.loads(response.text)
        try:
            export_title = title['records'][0]['KimbleOne__Grade__r']['Name']
        except:
            pass
    except:
        export_title = 'No title available'
    if 'MDC' in export_title:
        export_title = export_title.replace('MDC ','')

    return export_title


def get_email(token, name):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer " + token}

    response = requests.request("GET", url+"SELECT KimbleOne__Resource__c.KimbleOne__User__r.Email FROM KimbleOne__Resource__c WHERE name = '"+name+"'", headers = headers)
    email = json.loads(response.text)

    try:
        email = email['records'][0]['KimbleOne__User__r']['Email']
    except:
        email = 'No email available'

    return email


def get_cost(token, name):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer " + token}

    response = requests.request("GET", url+"SELECT KimbleOne__ActualCost__c FROM KimbleOne__Resource__c WHERE name = '"+name+"'", headers = headers)
    cost_j = json.loads(response.text)

    try:
        cost = cost_j['records'][0]['KimbleOne__ActualCost__c']
    except:
        cost = 0.0

    return cost


def get_cost_type(token, name):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer " + token}

    response = requests.request("GET", url+"SELECT KimbleOne__ActualCostUnitType__c FROM KimbleOne__Resource__c WHERE name = '"+name+"'", headers = headers)
    cost_t_j = json.loads(response.text)

    try:
        cost_t = cost_t_j['records'][0]['KimbleOne__ActualCostUnitType__c']
    except:
        cost_t = 'Unknown type'

    return cost_t


def get_assignments(token, bio):
    sufix = "/services/data/v24.0/query?q="
    if settings.FAKE_DATA:
        url = "http://fake-kimble-server:3010"+sufix
    else: 
        url = "https://intersys.my.salesforce.com"+sufix
    headers = {"authorization":"Bearer " + token}
    assignment_date = None
    response = requests.request("GET", url+"SELECT name, KimbleOne__Resource__r.Name, KimbleOne__DeliveryGroup__r.KimbleOne__Account__r.Name, KimbleOne__StartDate__c, KimbleOne__ForecastP1EndDate__c, KimbleOne__ForecastP2EndDate__c, KimbleOne__ForecastP3EndDate__c, KimbleOne__UtilisationPercentage__c FROM KimbleOne__ActivityAssignment__c WHERE KimbleOne__DeliveryGroup__c != NULL AND KimbleOne__Resource__r.Name = '"+bio.name+"'", headers = headers)
    assignments = json.loads(response.text)
    assignment_end_date = None

    try:
        decodedAssignments = assignments['records']

        for assignment in assignments['records']:
            end_date = assignment['KimbleOne__ForecastP3EndDate__c']

            if end_date is not None and (datetime.strptime(end_date, '%Y-%m-%d').date() - date.today()).days > 0:
                project = Assignments()
                project, created = Assignments.objects.get_or_create(name=assignment['Name'])
                project.start = datetime.strptime(assignment['KimbleOne__StartDate__c'], '%Y-%m-%d').date()
                try:
                    project.p1_end = datetime.strptime(assignment['KimbleOne__ForecastP1EndDate__c'], '%Y-%m-%d').date()
                except:
                    project.p1_end = None
                try:
                    project.p2_end = datetime.strptime(assignment['KimbleOne__ForecastP2EndDate__c'], '%Y-%m-%d').date()
                except:
                    project.p2_end = None
                project.p3_end = datetime.strptime(assignment['KimbleOne__ForecastP3EndDate__c'], '%Y-%m-%d').date()
                project.account_name = assignment['KimbleOne__DeliveryGroup__r']['KimbleOne__Account__r']['Name']
                project.utilisation = int(assignment['KimbleOne__UtilisationPercentage__c'])
                bio.assignments.add(project)
                project.save() 
    except:
        pass


def get_bios(token):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    names_links = get_name_link(token)
    regex = re.compile('.*.pdf')
    filename = 'Bio.pdf'

    for consultant_name, consultant_link in names_links.items():
        response = requests.get(consultant_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')  
        link = soup.find(href = regex)

        pdf_link = link.get('href')
        pdf_file = requests.get(pdf_link, headers=headers)

        with open(filename, 'wb') as f:
            f.write(pdf_file.content)
            f.close()

        pdf = parser.from_file(filename)
        pdf_text = pdf['content'].replace('\t','\n').replace('\n',' ').replace(',',' ').split()

        clean_text = ''
        for word in pdf_text:
            clean_text += (word + ' ')

        process_documents(token, consultant_name, clean_text, pdf_link)


def process_documents(token, consultant_name, clean_text, pdf_link):
    template_error = 'Update Bio, standard format needed' 

    bio, created = Bio.objects.get_or_create(name=consultant_name)
    bio.location = get_location(token, consultant_name)
    bio.url = pdf_link
    bio.title = get_title(token, bio.name)
    bio.email = get_email(token, bio.name)
    bio.cost = get_cost(token, bio.name)
    bio.cost_type = get_cost_type(token, bio.name)
    get_assignments(token, bio)

    try:
        bio.profile = re.search(r" Profile (.*?)Skills ", clean_text).group(1) 
    except:
        bio.profile = template_error

    try:
        skills_field = re.search(r"Skills (.*?)Education ", clean_text).group(0)
    except:
        skills_field = template_error

    try:
        bio.skills = re.search(r"Skills ([^']*)Technical ", skills_field).group(1)
    except:
        bio.skills = template_error

    try:
        bio.technical_skills = re.search(r"Technical(.*?)Education ", skills_field).group(1)
    except:
        bio.technical_skills = template_error

    try:
        bio.education = re.search(r" Education (.*?) Certifications ", clean_text).group(1)
    except:
        try:
            bio.education = re.search(r" Education (.*?) Experience ", clean_text).group(1)
        except:
            bio.education = template_error

    try:
        bio.experience = re.search(r" Experience ([^']*) ", clean_text).group(1)
    except:
        bio.experience = template_error

    bio.save()
