from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *

from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self,attr):
    data = super().validate(attr)
    token = self.get_token(self.user)
    data['user'] = str(self.user)
    data['id'] = str(self.user.id)
    data['name'] = str(self.user.name)
    return data


class RealtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        exclude = ['groups', 'user_permissions']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['name', 'photo', 'phone', 'description', 'email_optional']


        def update(self, instance, validated_data):
            instance.email = validated_data.get('email', instance.email)
            instance.name = validated_data.get('name', instance.name)
            instance.photo = validated_data.get('photo', instance.photo)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.description = validated_data.get('description', instance.description)
            instance.email_optional = validated_data.get('email_optional', instance.email_optional)
            instance.save()
            return instance

class TestimonialListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Testimonial
        fields = ['user_name', 'content', 'testimonial_type', 'creation_time']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()