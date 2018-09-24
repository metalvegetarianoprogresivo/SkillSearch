from django.contrib import admin
from .models import Bio, EmailAuth

admin.site.register([Bio, EmailAuth])
