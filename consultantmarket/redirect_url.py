def redirect_url(request):
    my_domain = request.build_absolute_uri()
    main_domain = my_domain.split(request.get_full_path())
    if(request.session["authenticated"] == None or request.session["authenticated"] == False):
        return main_domain[0]
    return False