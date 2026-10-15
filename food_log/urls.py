from django.urls import path
from food_log.views import SignUpView,GetMeView,FoodLogListCreateView,FoodLogRetrieveUpdateDeleteView,ObtainAuthToken,FoodLogSummaryView
from food_log.views import DietPlanView


urlpatterns=[
    path("register/",SignUpView.as_view()),
    path("me/",GetMeView.as_view()),
    path("food_log/",FoodLogListCreateView.as_view()),
    path("food_log/<int:pk>/",FoodLogRetrieveUpdateDeleteView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    path("food_log/summary/",FoodLogSummaryView.as_view()),
    path("food_log/dietplan/",DietPlanView.as_view())


]
