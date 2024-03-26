from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),

    
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('photos/', views.photos, name='photos'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('settings/', views.settings, name='settings'),
]
