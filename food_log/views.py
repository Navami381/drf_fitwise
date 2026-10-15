from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken


from food_log.serializers import UserSerializer,MealSerializer
from food_log.models import Meal
from food_log.permissions import IsOwner
from food_log.ai_server import get_diet_plan

from datetime import datetime

# Create your views here.
class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            instance=User.objects.create_user(**cleaned_data)
            serializer_instance=UserSerializer(instance)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class GetMeView(APIView):
    authentication_classes=[authentication.TokenAuthentication] #Only authenticated users can access this view.
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        auth_user=request.user
        instance=User.objects.get(username=auth_user)  #this searches the User table and gets the user whose username matches auth_user.
        serializer_instance=UserSerializer(instance)  #User object to json data
        return Response(data=serializer_instance.data)

class FoodLogListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        instance=Meal.objects.filter(owner=request.user)
        serializer_instance=MealSerializer(instance,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=MealSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class FoodLogRetrieveUpdateDeleteView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    #permission_classes=[permissions.IsAuthenticated]
    permission_classes=[IsOwner]
    def get(self,request,pk=None):
        #instance=Meal.objects.get(id=pk)
        instance=get_object_or_404(Meal,id=pk)
        self.check_object_permissions(request,instance)
        serilaizer_instance=MealSerializer(instance)
        return Response(data=serilaizer_instance.data)

    def put(self,request,pk=None):
        form_data=request.data
        serializer_instance=MealSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


    def delete(self,request,pk=None):
        instance=get_object_or_404(Meal,id=pk)
        self.check_object_permissions(request,instance)
        instance.delete()
        return Response(data={"message":"deleted.."})


class FoodLogSummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request):
        #todays summary
        response_data={"todays_total_calorie":0}
        
        cur_date=timezone.localdate()     

        todays_food_log=Meal.objects.filter(owner=request.user,created_at__date=cur_date)
        
        if todays_food_log:
            todays_total_calorie=todays_food_log.values("calorie").aggregate(total=Sum("calorie")).get("total")
            meal_type_summary=todays_food_log.values("meal_type").annotate(total=Sum("calorie"))
            response_data={"todays_total_calorie":todays_total_calorie,
                           "meal_type_summary":meal_type_summary
                           }
            
        #montly summary
        cur_month=datetime.now().month
        cur_year=datetime.now().year

        monthly_food_log=Meal.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_food_log:
            monthly_total=monthly_food_log.values("calorie").aggregate(total=Sum("calorie")).get("total")
            monthly_meal_calorie=monthly_food_log.values("meal_type").annotate(total=Sum("calorie"))
            response_data["monthly_total"]=monthly_total
            response_data["monthly_meal_calorie"]=monthly_meal_calorie

        return Response(data=response_data)

class DietPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        response_data={"monthly_total":0}

        cur_month=datetime.now().month
        cur_year=datetime.now().year

        monthly_food_log=Meal.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        if monthly_food_log:
            monthly_total=monthly_food_log.values("calorie").aggregate(total=Sum("calorie")).get("total")
            monthly_meal_summary=monthly_food_log.values("meal_type").annotate(total=Sum("calorie"))
            response_data["monthly_total"]=monthly_total
            response_data["monthly_meal_summary"]=monthly_meal_summary

            get_diet_plan(response_data)

        return Response(data=response_data)
