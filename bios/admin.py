from django.contrib import admin
from .models import Bio, EmailAuth ,Projects , Rosters

admin.site.register([Bio, EmailAuth ,Projects , Rosters])
