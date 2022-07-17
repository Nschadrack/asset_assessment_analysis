from rest_framework import serializers

from .models import *
from django.contrib.auth.models import Permission


def return_model_fields(model):
    fields = [field.name for field in model._meta.get_fields()]
    return fields 


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = return_model_fields(User)


    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        #['url', 'logentry', 'members', 'group_members', 'password', 'last_login', 'is_superuser', 'first_name', 'last_name', 'email', 
        # 'is_staff', 'is_active', 'date_joined', 'username', 'phone_number', 'groups', 'user_permissions']
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        
        instance.save()
        return instance 


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = return_model_fields(UserGroup)
    
    def create(self, validated_data):
        return UserGroup.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        #['url', 'user_groups', 'group_permissions', 'group_id', 'name', 'date_created', 'users', 'permisions']
        instance.name = validated_data.get("name", instance.name)

        instance.save()
        return instance
