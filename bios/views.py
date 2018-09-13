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
    return get_code(request)

def get_code(request):
    return redirect("https://intersys.my.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&redirect_uri=https%3A%2F%2Fskillssearchertest.centralus.cloudapp.azure.com%2Fbios%2F")

def get_token(code):
    url = "https://intersys.my.salesforce.com/services/oauth2/token"

    payload = "grant_type=authorization_code&redirect_uri=https%3A%2F%2Fskillssearchertest.centralus.cloudapp.azure.com%2Fbios%2F&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&client_secret=1639331975173970710&code="+code
      
    headers = {
            "content-type":"application/x-www-form-urlencoded"  
    }
    response = requests.request("POST", url, data= payload, headers = headers)
    resJson = json.loads(response.text)
    get_bios(resJson["access_token"])

    return()


def get_location(token, name):
    locations = ['Mexico Delivery Center','Central', 'West', 'East']
    url = "https://intersys.my.salesforce.com/services/data/v24.0/query?q="

    headers = {
            "authorization":"Bearer "+token
    }
    location = "No location Found"
    try:
        response = requests.request("GET", url+"SELECT KimbleOne__Resource__c.KimbleOne__BusinessUnit__r.Name FROM KimbleOne__Resource__c WHERE name = '"+name+"'", headers = headers)
        response_json=json.loads(response.text)
    except:
        location = "No location Found - 1"
    if 'No location Found' in location:
        try:
            response = requests.request("GET", url+"SELECT KimbleOne__Resource__c.KimbleOne__BusinessUnit__r.Name FROM KimbleOne__Resource__c WHERE name LIKE '%"+name+"%'", headers = headers)
            response_json=json.loads(response.text)
        except:
            location = "No location Found - 2"
    try:
        location = response_json['records'][0]['KimbleOne__BusinessUnit__r']['Name']
        if not location:
            location = "No location Found"
    except:
        location = "No location Found"
    return(location)


def get_bios(token):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    wb = load_workbook('allemployees.xlsx')
    all_links = wb['US']['B'] + wb['MDC']['B']
    all_names = wb['US']['A'] + wb['MDC']['A']
    names_links = {}
    regex = re.compile('.*.pdf')

    for consultant in range(len(all_links)):
        if all_links[consultant].value is not None and 'https' in all_links[consultant].value:
            names_links[all_names[consultant].value] = all_links[consultant].value
        else:
            pass
    
    for consultant_name, consultant_link in names_links.items():
        response = requests.get(consultant_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')  
        link = soup.find(href = regex)

        pdf_link = 'https://www.intersysconsulting.com' + link.get('href')
        pdf_file = requests.get(pdf_link, headers=headers)

        filename = 'Bio.pdf'

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
    bio, created = Bio.objects.get_or_create(name=consultant_name)
    bio.location = get_location(token, consultant_name)
    bio.url = pdf_link

    print(bio.name) #keep track of progress in command line
    template_error = 'Update Bio, standard format needed' 
                 
    try:
        name_title = re.search(r".docx(.*?) Profile ", clean_text).group(1)
    except:
        try:
            name_title = re.search(r"(.*?) Profile ", clean_text).group(1)
        except:
            name_title = template_error  
 
    job_titles = ['Senior Consultant', 'Consultant', 'Technical Lead', 'Practice Director',
    'Technical Manager', 'Delivery Lead', 'Delivery Manager']
   
    bio.title = template_error
    for title in job_titles:
        if title in name_title.title():
            bio.title = title
            break

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