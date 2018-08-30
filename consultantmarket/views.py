from django.shortcuts import render
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.shortcuts import redirect
from bios.models import EmailAuth
# Use this just as example
@csrf_exempt

def index(request):
    '''
    print(EmailAuth.objects.all())
    urlProfile="https://graph.microsoft.com/v1.0/me/"
    #if(request.session.get('authenticateid')):     
    request.session['authenticated'] = False
    proxyURL = getURL()
    if(request.POST.keys()):
        access_tok=request.POST['access_token']
        user=(getData(access_tok,urlProfile))
        request.session['displayName'] = user['displayName']
        request.session['mail'] =user['mail']
        print("POST")
        query = EmailAuth.objects.all()
        access = False
        for obj in query:
            print(request.session['mail']+"  "+obj.email)
            if(request.session['mail'] == obj.email):
                print("youhaveaccess")
                request.session['authenticated'] = True
                access = True
        if(access == False):
            return redirect('noAccess')
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
    #assert(False, request.session['authenticated'])
    return render(request, "templates/index.html", context)
  
def noAccess(request):
    return render(request, "templates/noaccess.html")

def credits(request):
    return render(request, "templates/credits.html")

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
            "redirect": "https://skillssearcher.intersysconsulting.com/",
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
    return redirect("https://login.microsoftonline.com/common/oauth2/logout?post_logout_redirect_uri=https://skillssearcher.intersysconsulting.com/")
