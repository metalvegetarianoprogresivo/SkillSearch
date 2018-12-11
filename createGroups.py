from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import django

django.setup()

practice_group, created = Group.objects.get_or_create(name='Practice Director')
ct = ContentType.objects.get_for_model(User)

sales_group, created = Group.objects.get_or_create(name='Sales')
ct = ContentType.objects.get_for_model(User)