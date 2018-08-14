from django.shortcuts import render
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import requests
import json
# Use this just as example
@csrf_exempt
def index(request):
    request.session['authenticated'] = False
    
    '''
    print(dir(request))
    print("------POST") 
    '''
    print(dir(request.POST))
    
    '''
    print("-----")
    print(request.POST.keys())
    print("---")
    print(dir(request.GET))
    print("--GTE")
    print(request.GET.keys())
    '''
    print("LLaves y valores")
    for key, val in request.POST.items():
        print(key+"--"+val+"\n")
    proxyURL = getURL()
    #if(request.session['authenticated'] == False):
    #    return redirect(proxyURL)
    #full_path = request.get_full_path()
    #current_path = full_path[full_path.index('/', 1):]
    #print(full_path)
    #if request.GET.get('access_token'):
    #    message = 'You submitted: %r' % request.GET['access_token']
    #else:
    #    message = 'You submitted nothing!'
    #print(message)
    #print(access_token)
    """
    Landing page
    """
    context = {
        "title" : "Home"
    }
    return render(request, "templates/index.html", context)

def getURL():
    url = "https://simple-sign-on.azurewebsites.net/auth"

    payload = {
            "id": "a67b9eaf-4a58-40b9-be6d-e7b597d8c004",
            "secret": "ibGJSG864$ezaovEBW02]#%",
            "scope": ["openid", "profile", "User.Read"],
            "redirect": "https://skillsearch.westeurope.cloudapp.azure.com/",
            "response": "form_post"
            }
    headers = {

  'Content-Type': "application/json",

  'Cache-Control': "no-cache",

  'Postman-Token': "f033541d-4878-479a-9ac3-892522403736"
    }
    response = requests.request("POST", url, data= json.dumps(payload), headers=headers)
    print(response.text)
