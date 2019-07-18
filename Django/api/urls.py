from django.urls import path
from api import views

urlpatterns = [
    path('rules/', views.ListAllRules.as_view(), name="rules-all"),
    path('children/<str:inCode>/', views.ListChildrenOfCode.as_view(), name="children-of-code"),
    path('family/<str:inCode>/', views.Family.as_view(), name="family-of-code"),
    path('codeDescription/<str:inCode>/', views.SingleCodeDescription.as_view(), name="single-code"),
    path('requestRules/<str:inCodes>/', views.ListRequestedRules.as_view(), name="rules-specific"),
    path('requestRulesActive/<str:inCodes>/', views.ListRequestedRulesActive.as_view(), name="rules-specific-active"),
    path('matchDescription/<str:searchString>/', views.ListMatchingDescriptions.as_view(), name="match-description"),
    path('matchKeyword/<str:searchString>/', views.ListMatchingKeywords.as_view(), name="match-keyword"),
    path('ancestors/<str:inCode>/', views.ListAncestors.as_view(), name="ancestors-of-code"),
    path('codeAutosuggestions/<str:searchString>/', views.ListCodeAutosuggestions.as_view(), name="code-autosuggestions"),
    path('codeBlockUsage/', views.ListCodeBlockUsage.as_view(), name="code-block-usage"),
    path('createRule/', views.CreateRule.as_view(), name="create-rule"),
    path('ruleSearch/', views.RuleSearch.as_view(), name="rule-search"),
    path('flagRuleForReview/<str:ruleId>/', views.FlagRuleForReview.as_view(), name="flag-rule-for-review"),
    path('flaggedRules/', views.ListFlaggedRules.as_view(), name="flagged-rules"),
    path('updateFlaggedRule/<str:ruleIdAndDecision>/', views.UpdateFlaggedRule.as_view(), name="update-flagged-rule"),
    path('daggerAsterisk/<str:inCodes>/', views.DaggerAsteriskAPI.as_view(), name="dagger-asterisk"),
    path('enterLog/', views.EnterLog.as_view(), name="enter-log"),
    path('inactiveRules/', views.InactiveRules.as_view(), name="inactive-rules"),
    path('stats/', views.Stats.as_view(), name="stats"),
    path('checkCode/<str:inCode>/', views.CheckCode.as_view(), name="checkCode"),
    path('changeRuleStatus/', views.ChangeRuleStatus.as_view(), name="change-rule-status"),
]
