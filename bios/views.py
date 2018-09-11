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
from django.core.mail import EmailMultiAlternatives


def index(request):
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return redirect("https://skillssearcher.intersysconsulting.com/")
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
    #process_documents()
    
    return get_code(request)

def get_code(request):
    return redirect("https://intersys.my.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&redirect_uri=https%3A%2F%2Fskillssearcher.intersysconsulting.com%2Fbios%2F")

def get_token(code):
    url = "https://intersys.my.salesforce.com/services/oauth2/token"

    payload = "grant_type=authorization_code&redirect_uri=https%3A%2F%2Fskillssearcher.intersysconsulting.com%2Fbios%2F&client_id=3MVG99OxTyEMCQ3i_6e.7CZ89dFfpk2X6t_CvQIU3u31aIQ1DpbJJY2naIXQLgn6n0R6OMLaih7A_Ujyx_2hW&client_secret=1639331975173970710&code="+code
      
    headers = {
            "content-type":"application/x-www-form-urlencoded"  
    }
    response = requests.request("POST", url, data= payload, headers = headers)
    resJson = json.loads(response.text)
    #print(resJson)
    #print(type(resJson))
    process_documents(resJson["access_token"])

    return()

def get_location(token, name):
    locations = ['MDC','Central', 'West', 'East']
    url = "https://intersys.my.salesforce.com/services/data/v24.0/query?q="

    headers = {
            "authorization":"Bearer "+token
    }
    try:
        response = requests.request("GET", url+"SELECT region__c FROM user WHERE name LIKE '%"+name+"%'", headers = headers)
        response_json=json.loads(response.text)
    except:
        location = "No location Found"
    try:
        location = response_json['records'][0]['Region__c']
        if not location:
            location = "No location Found"
    except:
        location = "No location Found"
    print("location ",location)
    return(location)


def send_logs():
    today = datetime.date.today()
    today=str(datetime.datetime.now())
    subject, from_email, to = 'Logs: '+today,'intersysinternalapplication@intersysconsulting.com', [request.session['mail']]
    text_content = 'This is your log until now.'
    #html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative('../logdate.txt', "text/html")
    #message.attach_file('/images/weather_map.png')
    msg.send()
    


def process_documents(token):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    '''
    excel_url = 'https://intersysconsulting.sharepoint.com/:x:/r/salesandmarketing/_layouts/15/Doc.aspx?sourcedoc=%7BEE714148-B6C1-49EA-B94A-4EA31E13A807%7D&file=1%20Consultant%20Bio%20Links.xlsx&action=default&mobileredirect=true'
    excel_user = 'internalapp@intersysconsulting.com'
    excel_pass = 'Internal2018!'

    response = requests.get(excel_url, auth=excel_user, excel_url, headers=headers)
    name = 'consultants.xlsx'

    with open(name. 'wb') as f:
        f.write(response.content)
        f.close()

    wb = load_workbook(name)
    '''
    wb = load_workbook('allemployees.xlsx')
    usa = wb['US']
    mx = wb['MDC']
    all_links = wb['US']['B'] + wb['MDC']['B']
    all_names = wb['US']['A'] + wb['MDC']['A']
    names_links = {}

    for consultant in range(len(all_links)):
        if all_links[consultant].value is not None and 'https' in all_links[consultant].value:
            names_links[all_names[consultant].value] = all_links[consultant].value
        else:
            pass

    for consultant_name, consultant_link in names_links.items():
        response = requests.get(consultant_link, headers=headers)
        filename = 'Bio.pdf'
        soup = BeautifulSoup(response.text, 'html.parser')
        regex = re.compile('.*.pdf')
        link = soup.find(href = regex)
        pdf_link = 'https://www.intersysconsulting.com' + link.get('href')
        pdf_file = requests.get(pdf_link, headers=headers)

        template_error = 'Update Bio, standard format needed' 
        with open(filename, 'wb') as f:
            f.write(pdf_file.content)
            f.close()
        
        pdf = parser.from_file(filename)
        pdf_text = pdf['content'].replace('\t','\n').replace('\n',' ').split()

        clean_text = ''

        for word in pdf_text:
            clean_text += (word + ' ')
        
        name_title = template_error               
        try:
            name_title = re.search(r".docx(.*?) Profile ", clean_text).group(1)
        except:
            pass

        if name_title is template_error:
            try:
                name_title = re.search(r"(.*?) Profile ", clean_text).group(1)
            except:
                pass
                
        bio, created = Bio.objects.get_or_create(name=consultant_name)
        print(consultant_name)
        bio.name_and_title = name_title
        bio.url = pdf_link
        bio.location = get_location(token, consultant_name)
        job_titles = ['Senior Consultant', 'Consultant', 'Technical Lead', 'Practice Director',
        'Technical Manager', 'Delivery Lead', 'Delivery Manager']

        bio.title = template_error   
        for title in job_titles:
            try: 
                if title in name_title.title():
                    bio.title = title
                    break
            except:
                pass

        profile = template_error
        try:
            profile = re.search(r" Profile (.*?)Skills ", clean_text).group(1)
        except:
            pass
        bio.profile = profile

        skills_field = template_error
        try:
            skills_field = re.search(r"Skills (.*?)Education ", clean_text).group(0)
        except:
            pass
        Skills = template_error
        try:
            skills = re.search(r"Skills ([^']*)Technical ", skills_field).group(1)
        except:
            pass
        bio.skills = skills

        technical = template_error
        try:
            technical = re.search(r"Technical(.*?)Education ", skills_field).group(1)
        except:
            pass
        bio.technical_skills = technical
            
        education = template_error
        try:
            education = re.search(r" Education (.*?) Certifications ", clean_text).group(1)
        except:
            pass
        if education is template_error:
            try:
                education = re.search(r" Education (.*?) Experience ", clean_text).group(1)
            except:
                pass
        bio.education = education

        experience = template_error
        try:
            experience = re.search(r" Experience ([^']*) ", clean_text).group(1)
        except:
            pass
        bio.experience = experience

        bio.save()

