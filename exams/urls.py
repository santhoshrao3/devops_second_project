from . import views
from django.urls import path, include

urlpatterns = [
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('school/<int:id>', views.school, name='school'),
    path('quiz/<int:id>', views.quiz, name='quiz'),
]