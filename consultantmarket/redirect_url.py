from django.contrib.auth.models import User

def redirect_url(request):
    main_domain = read_main_url()
    try:
        intersys_user = User.objects.get(email = request.session['mail'])
        request.user = intersys_user
        for group in intersys_user.groups.all():
            if "Sales" == group.name:
                return False
            if "Practice Director" == group.name:
                return False
        return main_domain+"noaccess/"
    except:
            main_domain = main_domain+"noaccess/"
    return main_domain
   
def read_main_url():
    file = open("properties.txt","r").read()
    print("leyo"+file.splitlines()[0])
    return file.splitlines()[0]
