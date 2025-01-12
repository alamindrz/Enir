from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    
    path('', views.home, name='home'),
    
    path('signup/', views.signup_view, name='signup'),

    path('profile/<int:user_id>', views.profile_view, name='profile_view'),
    
    path('edit-profile/<int:user_id>', views.edit_profile, name='edit_profile'),
]