from django.urls import path 

from .views import *

app_name = 'users_management'

urlpatterns = [ 
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/<str:user_id>/', UserDetail.as_view(), name='user-detail'),
    path('users/<str:user_id>/<str:update_or_delete>/', UserDetail.as_view(), name='user-detail-update'),

    path('groups/', GroupsList.as_view(), name='groups-list'),
    path('groups/<int:group_id>/', GroupDetail.as_view(), name='group-detail'),
    path('groups/<int:group_id>/<str:update_or_delete>/', GroupDetail.as_view(), name='group-update-detail'),

    path('group/<int:group_id>/membership/', MembershipView.as_view(), name='membership'),
    path('group/<int:group_id>/member/<str:user_id>/', MembershipView.as_view(), name='add-member'),
    path('group/<int:group_id>/member/<str:user_id>/<str:remove_member>/', MembershipView.as_view(), name='remove-member'),

    path('group-permissions-assignment/<int:group_id>/', GroupPermissionList.as_view(), name='group-permissions'),
    path('group-permissions-assignment/<int:group_id>/remove-permission/<int:permission_id>/', GroupPermissionList.as_view(), name='remove-group-permissions'),
]