from django.urls import path
from .views import *

app_name = "all_staff"
urlpatterns = [
    path("general/board/", general_board, name="general-board"),
    path("general/board/computers/", user_computers_list, name="user-computers"),
    path("general/board/screens/", user_screens_list, name="user-screens"),
    path("general/board/biometrics/", user_bios_list, name="user-bios"),
    path("general/board/avaya/", user_avaya_list, name="user-avaya"),
]
