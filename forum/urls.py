from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('adminamama/', admin.site.urls),
    path('api/v1/login/', views.login),
    path('api/v1/login', views.login),

    path('api/v1/reg/', views.register),
    path('api/v1/reg', views.register),


    path('api/v1/topics/', views.topics_list),
    path('api/v1/topics', views.topics_list),

    path('test', views.test1),


    path("__debug__/", include("debug_toolbar.urls")),

]
