from django.db import models
from accounts.models import Extendedusers


class Quiz(models.Model):
	user_school = models.ForeignKey(Extendedusers, on_delete=models.CASCADE)
	quiz_title = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.quiz_title
		
class Questions(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = models.CharField(max_length=1000, null=True)
	option1 = models.CharField(max_length=1000, null=True)
	option2 = models.CharField(max_length=1000, null=True)
	option3 = models.CharField(max_length=1000, null=True)
	is_correct = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.question