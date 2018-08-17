from django.shortcuts import render
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.shortcuts import redirect

# Use this just as example
@csrf_exempt
def index(request):
    '''
    access_tok=""
    urlProfile="https://graph.microsoft.com/v1.0/me/"
    print(dir(request.POST))
    print("-----")
    print(request.POST.keys())
    print("---")
    print(dir(request.GET))
    print("--GTE")
    print(request.GET.keys())
    print("LLaves y valores")
    access_tok=request.POST['access_token']
     #   print(type(val))
    print("Hola------------------------------------------------------------------")
    print(access_tok)    
    print("Hola------------------------------------------------------------------")
    user=(getData(access_tok,urlProfile))
    request.session['displayName'] = user['displayName']
    request.session['mail'] =user['mail']
    print("Hola------------------------------------------------------------------")
    for key in request.session.keys():
        print ("key:=>" + str(request.session[key]))
    proxyURL = getURL()
    if(request.POST.keys()):
        request.session['authenticated'] = True
        print("POST")
    else:
        request.session['authenticated'] = False
        print("False")
        return redirect(proxyURL["authurl"])
   
   '''
    """
    Landing page
    """
    context = {
        "title" : "Home"
    }
    return render(request, "templates/index.html", context)

def noAccess(request):
    return render(request, "templates/noaccess.html")

def getData(ac_t,url_ac):
    r=requests.get(url_ac, headers={
        'Content-type': "application/json",

        'Authorization': "Bearer "+ac_t,
        })
    return json.loads(r.text)

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
    
    return json.loads(response.text)

def logout(request):
    request.session['authenticated'] = False
    return redirect("https://login.microsoftonline.com/common/oauth2/logout?post_logout_redirect_uri=https://skillsearch.westeurope.cloudapp.azure.com/")
