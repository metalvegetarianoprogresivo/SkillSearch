from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

new_group, created = Group.objects.get_or_create(name='Practice Director')
# Code to add permission to group ???
ct = ContentType.objects.get_for_model(User)

# Now what - Say I want to add 'Can add project' permission to new_group?
permission = Permission.objects.create()
new_group.permissions.add(permission)

new_group, created = Group.objects.get_or_create(name='Sales')
# Code to add permission to group ???
ct = ContentType.objects.get_for_model(User)

# Now what - Say I want to add 'Can add project' permission to new_group?
permission = Permission.objects.create(codename='view_cost',
                                   name='view_cost',
                                   content_type=ct)
new_group.permissions.add(permission)