from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
    #path('contact/', views.contact, name='contact'),
    #path('about/', views.about, name='about'),
    #path('blog/', views.blog, name='blog'),
    #path('new_post/', views.new_post.as_view(), name='new_post'),
    #path('view_vol_posts/', views.view_vol_posts.as_view(), name='view_vol_posts'),
    #path('view_individual_post/<int:pk>', views.view_individual_post.as_view(), name='view_individual_post'),
    #path('view_all_orgs/',views.view_all_orgs.as_view(), name='view_all_orgs'),
    #path('view_org/<int:pk>', views.view_org.as_view(), name='view_org'),
    #path('application/<int:pk>', views.application.as_view(), name='application'),
    #path('edit_np_profile/<int:pk>', views.edit_np_profile.as_view(), name='edit_np_profile'),
    #path('success/', views.success, name='success'),
    #path('success_submitted/', views.success_submit, name='success_submit'),
    #path('feedback/', views.feedback.as_view(), name='feedback'),
    #path('edit_vol_post/<int:pk>', views.edit_vol_post.as_view(), name='edit_vol_post'),
    #path('edit_np_user_profile/<int:pk>', views.edit_np_user_profile.as_view(), name = 'edit_np_user_profile'),