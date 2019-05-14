from django.urls import path
from . import views

urlpatterns = [
    path('entering/', views.entering.as_view(), name='entering'),
    path('results/', views.results.as_view(), name='results'),
]
