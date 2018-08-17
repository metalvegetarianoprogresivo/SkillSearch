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
        '''
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return redirect("https://skillsearch.westeurope.cloudapp.azure.com/")
        '''
        context = {
        'title':'Update the bios'
        }
        return render(request, 'bios/index.html', context)

def get_documents(request):
        process_documents()
        context = {
        'title':'Updated bios'
        }
        return redirect('index', context)

def process_documents():
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

        wb = load_workbook("1 Consultant Bio Links.xlsx")
        usa = wb['US']
        mx = wb['MDC']
        all_links = wb['US']['B'] + wb['MDC']['B']
        links = []

        for link in all_links:
                if link.value is not None and 'https' in link.value:
                        links.append(link.value)
                else:
                        pass

        for url in links:

                response = requests.get(url,headers=headers)
                name = 'Bio.pdf'
                soup = BeautifulSoup(response.text, 'html.parser')

                regex = re.compile('.*.pdf')
                link = soup.find(href = regex)
                pdf_link = 'https://www.intersysconsulting.com' + link.get('href')
                pdf_file = requests.get(pdf_link, headers=headers)

                with open(name, 'wb') as f:
                        f.write(pdf_file.content)
                        f.close()

                pdf = parser.from_file(name)
                pdf_text = pdf['content'].replace('\t','\n').replace('\n',' ').split()
                clean_text = ''

                for word in pdf_text:
                        clean_text += (word + ' ')
                name_title = None
                        
                try:
                        name_title = re.search(r".docx(.*?) Profile ", clean_text).group(1)
                except:
                        pass


                if name_title is None:
                        try:
                                name_title = re.search(r"(.*?) Profile ", clean_text).group(1)
                                print(name_title)
                        except:
                                pass

                bio, created = Bio.objects.get_or_create(name_and_title=name_title)

                try:
                        profile = re.search(r" Profile (.*?)Skills ", clean_text).group(1)
                except:
                        pass
                bio.profile = profile

                try:
                        skills_field = re.search(r"Skills (.*?)Education ", clean_text).group(0)
                except:
                        pass
                try:
                        skills = re.search(r"Skills ([^']*)Technical ", skills_field).group(1)
                except Exception as e:
                        skills=""

                bio.skills = skills

                try:
                        technical = re.search(r"Technical(.*?)Education ", skills_field).group(1)
                except:
                        technical = ""
                
                bio.technical_skills = technical
                
                education = None

                try:
                        education = re.search(r" Education (.*?) Certifications ", clean_text).group(1)
                except:
                        pass

                if education is None:
                        try:
                                education = re.search(r" Education (.*?) Experience ", clean_text).group(1)
                        except:
                                pass

                bio.education = education
                bio.save()

