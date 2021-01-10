from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from exams import views


urlpatterns = [
	path('admin/', admin.site.urls),
	path('accounts/', include('accounts.urls')),
	path('exams/', include('exams.urls')),
	path('', views.show_quiz, name='show_quiz'),
]
