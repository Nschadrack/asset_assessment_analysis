from django.urls import path
from .views import *

app_name = "all_staff"
urlpatterns = [
    path("general/board/", general_board, name="general-board"),
    path("general/board/computers/", user_computers_list, name="user-computers"),
]
