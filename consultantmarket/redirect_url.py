def redirect_url(request):
    main_domain = read_main_url()
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return main_domain[0]
    return False

def read_main_url():
    file = open("properties.txt","r").read()
    return file.splitlines()[0]
