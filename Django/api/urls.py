from django.urls import path
from api import views

urlpatterns = [
    path('rules/', views.ListAllRules.as_view(), name="rules-all"),
    path('codes/', views.ListAllCodes.as_view(), name="codes-all"),
    path('children/<str:pk>/', views.ListChildrenOfCode.as_view(), name="children-of-code"),
]