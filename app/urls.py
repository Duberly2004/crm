from django.urls import path,include
from app.views import getUser,index,LoginView,SignupView,change_password
urlpatterns = [
    path('',index),
    path('user',getUser),
    path('auth/login',LoginView.as_view()),
    path('auth/signup',SignupView.as_view(),name="signup"),
    path('auth/changepassword',change_password,name="changepassword"),#Solicitar un token para restablecer la contraseña
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
