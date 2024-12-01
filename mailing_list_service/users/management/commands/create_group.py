from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create a group
        group = Group.objects.create(name='manager')

        # Assign a permission to the group
        permission = Permission.objects.get(codename="manager_permissions")
        group.permissions.add(permission)

        # Save the group
        group.save()
