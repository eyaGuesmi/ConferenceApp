<<<<<<< HEAD
=======

>>>>>>> df5daa56f74cd80f69add844502b78735ab8bc6a
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns =[
    path( "register/", views.register , name="register"),
    path('login',LoginView.as_view(template_name="login.html"),name="login"),
    path('logout/',views.logout_view,name="logout")
<<<<<<< HEAD
]
=======
]
>>>>>>> df5daa56f74cd80f69add844502b78735ab8bc6a
