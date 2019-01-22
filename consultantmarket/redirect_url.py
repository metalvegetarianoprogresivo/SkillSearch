from django.contrib.auth.models import User
from django.conf import settings

def redirect_url(request):
    main_domain = settings.MAIN_URL
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
