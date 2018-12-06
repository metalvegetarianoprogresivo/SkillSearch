from django.contrib.auth.models import User

def redirect_url(request):
    main_domain = read_main_url()
    if(request.session.get("authenticated", None) == None or request.session.get("authenticated", False) == False or request.session.get('mail', None) == None):
        return main_domain
    else:
        intersys_user = User.objects.get(email = request.session['mail'])
        request.user = intersys_user 
        return False

def read_main_url():
    file = open("properties.txt","r").read()
    print("leyo"+file.splitlines()[0])
    return file.splitlines()[0]
