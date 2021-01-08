from . import views
from django.urls import path, include

urlpatterns = [
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('school/<int:id>', views.school, name='school'),
    path('begin_quiz/<int:id>', views.begin_quiz, name='begin_quiz'),
    path('quiz', views.quiz, name='quiz'),
    path('submit_answer', views.submit_answer, name='submit_answer'),
    path('get_results', views.get_results, name='get_results'),
]