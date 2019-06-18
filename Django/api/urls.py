from django.urls import path
from api import views

urlpatterns = [
    path('rules/', views.ListAllRules.as_view(), name="rules-all"),
    path('children/<str:inCode>/',
         views.ListChildrenOfCode.as_view(), name="children-of-code"),
    path('family/<str:inCode>/', views.Family.as_view(), name="family-of-code"),
    path('codeDescription/<str:inCode>/',
         views.SingleCodeDescription.as_view(), name="single-code"),
    path('requestRules/<str:inCodes>/',
         views.ListRequestedRules.as_view(), name="rules-specific"),
    path('matchDescription/<str:descSubstring>/',
         views.ListMatchingDescriptions.as_view(), name="match-description"),
    path('ancestors/<str:inCode>/',
         views.ListAncestors.as_view(), name="ancestors-of-code"),
    path('codeAutosuggestions/<str:matchString>/',
         views.ListCodeAutosuggestions.as_view(), name="code-autosuggestions"),
    path('codeUsed/<str:inCodes>/', views.CodeUsed.as_view(), name="code-used"),
    path('codeBlockUsage/', views.ListCodeBlockUsage.as_view(),
         name="code-block-usage"),
    path('modifyRule/', views.ModifyRule.as_view(), name="modify-rule")
]
