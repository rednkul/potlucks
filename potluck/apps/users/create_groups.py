from django.contrib.auth.models import Group


manager_group, created = Group.objects.get_or_create(name='Manager')