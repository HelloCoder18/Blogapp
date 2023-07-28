"""
URL configuration for Baseapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import SignupView, LoginView, ViewPostView, EditPostView, AddBlogView, LogoutBlogView,IndexView
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
     path('blog/', IndexView.as_view(), name='index'),
 path('signup/', SignupView.as_view(), name='signup'),
 path('login/', LoginView.as_view(), name='login'),
    path('blog/<int:id>/', ViewPostView.as_view(), name='viewpost'),
     path('blog/edit/<int:id>/', EditPostView.as_view(), name='editpost'),
    path('blog/add/', AddBlogView.as_view(), name='addblog'),
    path('logout/', LogoutBlogView.as_view(), name='logoutblog'),

    # path('',views.login,name="login"),
    # path('login/',views.login,name="login"),
    # path('blog/<int:id>/',views.viewpost,name="viewpost"),
    # path('blog/edit/<int:id>/',views.editpost,name="editpost"),
    # path('blog/',views.home.index,name="blogs"),
    # path('blog/add/',views.addblog,name="add"),
    # path('logout/',views.logoutblog,name="logout"),
    # path('signup/', views.signup, name='signup'),
]
