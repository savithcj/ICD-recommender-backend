from django.urls import path
from api import views

urlpatterns = [
    path('rules/', views.ListAllRules.as_view(), name="rules-all"),
    path('codes/', views.ListAllCodes.as_view(), name="codes-all"),
    path('codes/<str:pk>/', views.CodeInformation.as_view(), name="code-information"),
    path('children/<str:pk>/', views.ListChildrenOfCode.as_view(), name="children-of-code"),
    path('family/<str:pk>/', views.Family.as_view(), name="family-of-code"),
    path('requestRules/<str:inCodes>/', views.ListRequestedRules.as_view(), name="rules-specific")
]
