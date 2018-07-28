from django.shortcuts import render

# Use this just as example
def index(request):
    """
    Landing page
    """
    context = {
        "title" : "Home"
    }
    return render(request, "templates/index.html", context)
