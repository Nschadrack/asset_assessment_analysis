from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from users_management.views import get_user, get_user_by_email, find_group_by_name
from users_management.models import *


def index(request):

    return render(request, "account/index.html")


def create_account(request):
    username = request.POST["username"].strip().upper().replace("_", "")
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
    return redirect("account:index")


def login_user(request):
    username = request.POST["username"].strip().upper().replace("_", "")
    password = request.POST["password"].strip()

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("dashboard:overall")
    else:
        print("\\n\nINVALID CREDENTIALS\n\n")
    
    return redirect("account:index")
    
@login_required(login_url="account:index", redirect_field_name="redirect_to")
def logout_user(request):
    logout(request)
    return redirect("account:index")

        

    


