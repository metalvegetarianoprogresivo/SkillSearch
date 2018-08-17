import requests
import re
from bs4 import BeautifulSoup
from tika import parser
from openpyxl import load_workbook
from openpyxl import workbook


wb = load_workbook('1 Consultant Bio Links.xlsx')
usa = wb['US']
mx = wb['MDC']
all_links = wb['US']['B'] + wb['MDC']['B']
links = []
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

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
		except:
			pass
	#print('\n', name_title)
	#bio.name_title.add(name_title)
	name = bio.objects.get_or_create(name = name_title)

	try:
		profile = re.search(r" Profile (.*?)Skills ", clean_text).group(1)
	except:
		pass
	#Profile(profile)
	#print("Profile")
	#print(Profile)
	Profile = Profile.objects.get_or_create(profile = profile)

	try:
		skills_field = re.search(r"Skills (.*?)Education ", clean_text).group(0)
	except:
		pass
	try:
		skills = re.search(r"Skills ([^']*)Technical ", Skills_field).group(1)
	except:
		pass
	#bio.general_skills.add(skills)
	#print("\nSkills")
	#print(Skills)
	skills = Skills.objects.get_or_create(skills = skills)

	try:
		technical = re.search(r"Technical(.*?)Education ", Skills_field).group(1)
	except:
		pass
	#bio.technical_skills.add(technical)
	#print("\nTechnical")
	#print(Technical)
	skills = Technical.objects.get_or_create(technical = technical)

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
	#bio.education.add(education)
	#print("\nEducation")
	#print(education)
	education = Education.objects.get_or_create(education = education)


