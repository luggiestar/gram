from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'GRAMONEY'

urlpatterns = [

    path('', views.home, name="home"),
    path('user-authentication/', views.index, name="login"),
    path('get-started/', views.registration, name="registration"),
    path('user-dashboard/', views.userHome, name="user_home"),
    path('withdraw-request/', views.withdraw_request, name="withdraw_request"),
    path('withdraw-request-confirmation/<withdraw>', views.confirm_withdraw, name="confirm_withdraw"),
    path('user-registration/<invite>', views.referral_registration, name="referral_registration"),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

'''
    Password view For reseting password
------------------------------------------
1 - PasswordResetView submit email from user
2 - PasswordResetDoneView email sent successfull
3 - link to password Rest form in email
4 - Password successfully changed
'''
