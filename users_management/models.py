from datetime import datetime

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(verbose_name='USER ID', max_length=7, validators=[MinLengthValidator(7)], unique=True, null=False, 
                                blank=False, primary_key=True, db_column='user_id')
    phone_number = models.CharField(verbose_name='Phone number', null=True, blank=True, max_length=14, db_column='phone_number')

    USERNAME_FIELD = 'username'

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'
    

class UserGroup(models.Model):
    group_id = models.BigAutoField(verbose_name='Group ID', db_column='group_id', primary_key=True)
    name = models.CharField(verbose_name='Group name', max_length=50, unique=True, db_column='name', null=False, blank=False, 
                            error_messages={'unique': 'group name already exists'})
    date_created = models.DateTimeField('Date created', db_column='date_created', default=datetime.now())
    users = models.ManyToManyField(User, through='Membership', through_fields=('user_group', 'user'), related_name='members')
    permisions = models.ManyToManyField(Permission, through='UserGroupPermission', through_fields=('group', 'permission'), related_name='permissions')

    def __str__(self) -> str:
        return f'Group: {self.name}'

    class Meta:
        db_table = 'groups'
        verbose_name = _('group')
        verbose_name_plural = _('groups')


class Membership(models.Model):
    membership_id = models.BigAutoField(verbose_name='Membership Id', db_column='membership_id', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='group_members')
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, db_column='group_id', related_name='user_groups')
    date_joined = models.DateTimeField('Date joined group', default=datetime.now(), db_column='date_joined')

    class Meta:
        db_table = 'groups_members'
        verbose_name = _('group member')
        verbose_name_plural = _('group members')

    def __str__(self) -> str:
        return f'{self.user} belongs to {self.user_group} group'


class UserGroupPermission(models.Model):
    group_permission_id = models.BigAutoField(verbose_name='Group permission Id', db_column='group_permission_id', primary_key=True)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name='group_permissions', db_column='group_id')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_groups', db_column='permission_id')
    date_added = models.DateTimeField('Date added', db_column='date_added', default=datetime.now())

    def __str__(self) -> str:
        return f'{self.group} with permission {self.permission.codename}'

    class Meta:
        db_table = 'user_group_permissions'
        verbose_name = _('group permission')
        verbose_name_plural = _('group permissions')
    
