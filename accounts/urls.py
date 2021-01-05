from . import views
from django.urls import path, include

urlpatterns = [
	path('signup/<str:cli>/', views.signup, name='signup'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
]
