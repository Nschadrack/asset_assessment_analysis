from tokenize import group
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *


def get_user(username):
        try:
            return User.objects.get(pk=username)
        except:
            return None

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def find_group_by_name(group_name):
    return UserGroup.objects.filter(name=group_name).first()


class UsersList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        users =  User.objects.all().order_by('-date_joined')
        context = {
            "users": users,
        }
        return render(request, "users_management/users_list.html", context)

    def post(self, request, *args, **kwargs):
        username = request.POST["username"].strip().upper().replace("_","")
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        email = request.POST["email"].strip()
        phone_number = request.POST["phone_number"].strip()
        password = request.POST["password"].strip()
        password2 = request.POST["password2"].strip()

        error_messages = {}
        if get_user(username):
            error_messages["username"] = f"User with username: {username} already exists"
        else:
            if not username[0].isidentifier() or not username[1].isidentifier():
                error_messages["username"] = f"{username} must be starts with 2 letters"
        if len(first_name) > 40:
            error_messages["first_name"] = "First name cannot exceed 40 characters"
        
        if len(last_name) > 40:
            error_messages["last_name"] = "Last name cannot exceed 40 characters"
        
        if not phone_number.startswith("250"):
            error_messages["phone_number"] = f"Phone number must start with 250"
        
        if get_user_by_email(email):
            error_messages["email"] = f"user with email: {email} already exists"
        else:
            if not email.endswith("@equitybank.co.rw"):
                error_messages["email"] = f"This {email} is not valid, use work email offered by equitybank"

        if password != password2:
            error_messages["password"] = "Password fields must match"
        
        if error_messages.keys():
            print("\n\nInvalid data\n\n", error_messages, "\n\n")
        else:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone_number=phone_number)
            user.set_password(password)
            user.is_active = True
            user.save()
            group = find_group_by_name("All Staffs")
            if not group:
                group = UserGroup(name="All Staffs")
                group.save()
            
            membership = Membership(user=user, user_group=group)
            membership.save()
        return redirect("users_management:users-list")


class UserDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, user_id, update_or_delete=None, *args, **kwargs):
        user = get_user(user_id)
        user_groups_num = Membership.objects.filter(user=user).all().count()
        if user:
            user_groups = Membership.objects.filter(user=user).all().order_by("-date_joined")
            context = {
                "user": user,
                "user_groups_num": user_groups_num,
                "user_groups": user_groups
            }

            if update_or_delete == "update":
                return render(request, "users_management/user-update-form.html", context)
            elif update_or_delete == "confirm_delete":
                context = {
                    "category": "user",
                    "user_group": user,
                    "user_group_id": user.username,
                    "list_url": "users_management:users-list",
                    "delete_url_name": "users_management:user-detail-update",
                    "cancel_url_name": "users_management:user-detail"
                }
                return render(request, "users_management/asking-delete-confirmation.html", context)
            elif update_or_delete == "delete":
                if self.delete(request, user_id):
                    #some message
                    pass
                return redirect("users_management:users-list")
            else:
                return render(request, "users_management/user-details.html", context)
        else:
            return render(request, "users_management/users_list.html", context)

    def post(self, request, user_id, update_or_delete="update", *args, **kwargs):
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        email = request.POST["email"].strip()
        phone_number = request.POST["phone_number"].strip()

        error_messages = {}
        if len(first_name) > 40:
            error_messages["first_name"] = "First name cannot exceed 40 characters"

        if len(last_name) > 40:
            error_messages["last_name"] = "Last name cannot exceed 40 characters"

        if not phone_number.startswith("250"):
            error_messages["phone_number"] = f"Phone number must start with 250"

        if not email.endswith("@equitybank.co.rw"):
            error_messages["email"] = f"This {email} is not valid, use work email offered by equitybank"

        if error_messages.keys():
            print("\n\nInvalid data\n\n", error_messages, "\n\n")
        else:
            user = get_user(user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.save()
            
            return HttpResponseRedirect(reverse("users_management:user-detail", args=(user.username,)))
    
    def delete(self, request, user_id, update_or_delete="delete", *args, **kwargs):
        user = get_user(user_id)
        if user:
            user.delete()
            return True 
        return False


class GroupsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        groups = UserGroup.objects.all().order_by('-date_created')
        context = {
            "groups": groups,
        }
        return render(request, "users_management/groups-list.html", context)
        

    def post(self, request, *args, **kwargs):
        name = request.POST["name"].strip()
        group = find_group_by_name(name)
        error_messages = {}
        if group:
            error_messages["name"] = f"Group with name: {name} already exists"
        else:
            if len(name) > 50 or len(name) < 2:
                error_messages["name"] = "Group name must at least two characters and maximum 50 characters"

        if error_messages.keys():
            pass
        else:
            group = UserGroup(name=name)
            group.save()
        
        return redirect("users_management:groups-list")



class GroupDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, group_id, update_or_delete=None, *args, **kwargs):
        group = UserGroup.objects.get(pk=group_id)
        group_members = Membership.objects.filter(user_group=group).order_by("-date_joined")
        group_permissions = UserGroupPermission.objects.filter(group=group)
        group_permissions_num = len(group_permissions)
        group_members_num = len(group_members)
        context = {
            "group": group,
            "group_members_num":group_members_num,
            "group_members": group_members,
            "group_permissions": group_permissions,
            "group_permissions_num": group_permissions_num
        }
        if update_or_delete == "update":
            if group.name.lower() == "all staffs":
                return redirect("users_management:groups-list")
            return render(request, "users_management/group-update-form.html", context)
        elif update_or_delete == "confirm_delete":
            if group.name.lower() == "all staffs":
                return redirect("users_management:groups-list")
            context = {
                "category": "group",
                "user_group": group,
                "user_group_id": group.group_id,
                "list_url": "users_management:groups-list",
                "delete_url_name": "users_management:group-update-detail",
                "cancel_url_name": "users_management:group-detail"
            }
            return render(request, "users_management/asking-delete-confirmation.html", context)
        elif update_or_delete == "delete":
            if group.name.lower() == "all staffs":
                return redirect("users_management:groups-list")
            if self.delete(request, group_id):
                #some messages
                pass
            return redirect("users_management:groups-list")
        return render(request, "users_management/group-details.html", context)

    def post(self, request, group_id, update_or_delete="update", *args, **kwargs):
        name = request.POST["name"].strip()
        error_messages = {}
        if len(name) > 50 or len(name) < 2:
            error_messages["name"] = "Group name must at least two characters and maximum 50 characters"

        if error_messages.keys():
            pass
        else:
            group = UserGroup.objects.get(pk=group_id)
            group.name = name
            group.save()

        return HttpResponseRedirect(reverse("users_management:group-detail", args=(group.group_id,)))
    
    def delete(self, request, group_id, update_or_delete="delete", *args, **kwargs):
        group = UserGroup.objects.get(pk=group_id)
        if group:
            group.delete()
            return True 
        return False


class MembershipView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    """
    The view for:
        1. adding user in group
        2. removing user from group
        3. adding group to user
        4. removing group from user
    """ 
    def get(self, request, group_id, user_id=None, remove_member=None, *args, **kwargs):
        group = UserGroup.objects.get(pk=group_id)
        current_membership = Membership.objects.filter(user_group=group)
        current_members = [membership.user.username for membership in current_membership]
        not_members = User.objects.all().exclude(username__in=current_members)
        context = {
            "not_members": not_members,
            "group_members_num_to_add": len(not_members),
            "group": group
        }
        if user_id and remove_member is None:
            user_to_add = User.objects.get(pk=user_id)
            if not Membership.objects.filter(user=user_to_add, user_group=group).first():
                add_membership = Membership(user=user_to_add, user_group=group)
                add_membership.save()
            else:
                #user already exists, some message
                pass
        elif remove_member:
            if group.name != "All Staffs":
                user_to_remove = User.objects.get(pk=user_id)
                remove_membership = Membership.objects.filter(user=user_to_remove, user_group=group)
                remove_membership.delete()
            else:
                #user cannot be removed from this group
                pass
        else:
            return render(request, "users_management/add-group-member.html", context)
        return HttpResponseRedirect(reverse("users_management:group-detail", args=(group.group_id,))) 


class PermissionsList(LoginRequiredMixin, View):
    def get(self, request, format=None):
        pass 


class PermissionDetail(LoginRequiredMixin, View):
    def get_object(self, permission_id):
        pass 

    def get(self, request, permission_id, format=None):
        pass 

    def delete(self, request, permission_id, group_id, format=None):
        """
        The method for removing permission from a certain group
        """
        pass


class GroupPermissionList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, group_id, permission_id=None, *args, **kwargs):
        group = UserGroup.objects.get(pk=group_id)
        existing_permissions = UserGroupPermission.objects.filter(group=group)
        existing_permissions_ids = [perm.permission.id for perm in existing_permissions]
        permissions_not_added = Permission.objects.all().exclude(id__in=existing_permissions_ids)
        context = {
            "permissions_not_added": permissions_not_added,
            "group_permissions_num_to_add": len(permissions_not_added),
            "group": group
        }
        if permission_id is not None:
            if group.name == "All Staffs":
                #some messages, you're not allowed remove permissions on this group
                pass 
            else:
                if self.delete(request, group_id, permission_id, *args, **kwargs):
                    #deleted successfuly
                    pass
                else:
                    pass
                    #was not deleted successfully
            return HttpResponseRedirect(reverse("users_management:group-detail", args=(group_id,)))
        return render(request, "users_management/add-group-permission.html", context)

    def post(self, request, group_id, permission_id=None, *args, **kwargs):
        """
        The method for assigning permissions to the group
        it will take list of permissions from requets to be added, loop throuhg all permissions
        and add them
        """
        permissions_to_add_ids = [int(v[0]) for v in dict(request.POST).values() if v[0].isdigit()]
        permissions_to_add = Permission.objects.filter(pk__in=permissions_to_add_ids)
        group = UserGroup.objects.get(pk=group_id)
        if group.name == "All Staffs":
            # no add permissions allowed to this group
            pass
        else:
            for perm in permissions_to_add:
                if not UserGroupPermission.objects.filter(group=group, permission=perm).first():# if permission not added yet
                    group_permission = UserGroupPermission(group=group, permission=perm)
                    group_permission.save()
        
        return HttpResponseRedirect(reverse("users_management:group-detail", args=(group_id,)))

    def delete(self, request, group_id, permission_id, *args, **kwargs):
        """
        The method for removing permissions from the group
        It will take list of permissions from request and remove them
        """
        try:
            group = UserGroup.objects.get(pk=group_id)
            permission = Permission.objects.get(pk=permission_id)
            remove_permission = UserGroupPermission.objects.filter(group=group, permission=permission)
            remove_permission.delete()
            return True
        except:
            return False




