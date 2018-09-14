import json
import datetime
import os
from django.shortcuts import redirect, render, reverse
from django.conf import settings
import requests
import re
from bs4 import BeautifulSoup
from tika import parser
from openpyxl import load_workbook
from openpyxl import workbook
from .models import Bio, Technical, Skill


def index(request):
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return redirect("https://skillssearchertest.centralus.cloudapp.azure.com/")
    if("code" in request.GET.keys()):
        get_token(request.GET.get("code"))
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
    return redirect("https://intersys.my.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&redirect_uri=https%3A%2F%2Fskillssearcher.intersysconsulting.com%2Fbios%2F")


def get_token(code):
    url = "https://intersys.my.salesforce.com/services/oauth2/token"
    payload = "grant_type=authorization_code&redirect_uri=https%3A%2F%2Fskillssearcher.intersysconsulting.com%2Fbios%2F&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&client_secret=1639331975173970710&code="+code
    headers = {"content-type":"application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data= payload, headers = headers)
    resJson = json.loads(response.text)

    get_bios(resJson["access_token"])


def get_location(token, name):
    url = "https://intersys.my.salesforce.com/services/data/v24.0/query?q="
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
    url = "https://intersys.my.salesforce.com/services/data/v24.0/query?q="
    headers = {"authorization":"Bearer " + token}
    names_link = {}

    response = requests.request("GET", url+"SELECT Name,KimbleOne__Resource__c.Resource_Bio__r.Bio_Url__c FROM KimbleOne__Resource__c WHERE KimbleOne__ResourceType__c = 'a7J0c000002VD4LEAW' AND KimbleOne__Grade__c != 'a5G0c000000g2IXEAY' AND KimbleOne__StartDate__c <= TODAY AND KimbleOne__EndDate__c = Null", headers = headers)
    consultants=json.loads(response.text)
    
    for consultant in consultants['records']:
        if consultant['Resource_Bio__r']['Bio_Url__c'] is not None:
            names_link[consultant['Name']] = consultant['Resource_Bio__r']['Bio_Url__c']
    
    return names_link


def get_title(token, name):
    url = "https://intersys.my.salesforce.com/services/data/v24.0/query?q="
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


def get_email(token,name):
    url = "https://intersys.my.salesforce.com/services/data/v24.0/query?q="
    headers = {"authorization":"Bearer " + token}

    response = requests.request("GET", url+"SELECT KimbleOne__Resource__c.KimbleOne__User__r.Email FROM KimbleOne__Resource__c WHEREname = '"+name+"'", headers = headers)
    email = json.loads(response.text)

    try:
        email = email['records'][0]['KimbleOne__User__r']['Email']
    except:
        email = 'No email available'

    return email


def get_bios(token):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    names_links = get_name_link(token)
    regex = re.compile('.*.pdf')
    filename = 'Bio.pdf'

    for consultant_name, consultant_link in names_links.items():
        response = requests.get(consultant_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')  
        link = soup.find(href = regex)

        pdf_link = 'https://www.intersysconsulting.com' + link.get('href')
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

    bio.email = get_email(token, bio.name)

    print(bio.name) #keep track of progress in command line

    title = get_title(token, bio.name)

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