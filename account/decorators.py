from django.shortcuts import redirect
from users_management.models import Membership


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated:
            print(f"\n\nIN THE authenticated_user: {current_user}\n\n")
            memberships_num = Membership.objects.filter(user=current_user).all().count()
            if memberships_num > 0:
                return redirect("dashboard:overall") 
            else:
                return redirect("all_staff:general-board") 
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
