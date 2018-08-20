from django.contrib import admin
from .models import Bio, CapabilityExpertise, Technical, EmailAuth

admin.site.register([Bio, CapabilityExpertise, Technical, EmailAuth])
