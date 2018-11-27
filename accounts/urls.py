#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path,include,reverse_lazy
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('send_login_email', views.send_login_email, name='send_login_email'),
    path('login', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
]