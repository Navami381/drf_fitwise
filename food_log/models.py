from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    MEAL_TYPES = [
        ('bf', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    calorie = models.IntegerField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    serving_size = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
