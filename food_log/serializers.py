from rest_framework import serializers

from django.contrib.auth.models import User

from food_log.models import Meal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meal
        fields="__all__"
        read_only_fields=["id","owner","created_at"]