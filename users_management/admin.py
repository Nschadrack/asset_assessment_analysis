from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
from .serializers import return_model_fields

admin.site.register(User)
admin.site.register(UserGroup)
admin.site.register(UserGroupPermission)
admin.site.register(Membership)

# perms = Permission.objects.all()
# return_model_fields(UserGroup)
# return_model_fields(UserGroup)
# print(f"\n\n{UserGroup.objects.first().user_groups.all()}\n\n")

# print("\n\nPERMISSIONS\n----------------------\n")
# for perm in perms:
#     print(f"ID: {perm.id}\nName: {perm.name}\nCode: {perm.codename}\n\n")
