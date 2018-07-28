from django.contrib import admin
from .models import Bio, CapabilityExpertise, Technical

admin.site.register([Bio, CapabilityExpertise, Technical])
