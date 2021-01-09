from django.db import models
from accounts.models import Extendedusers


class Quiz(models.Model):
	user = models.ForeignKey(Extendedusers, on_delete=models.CASCADE)
	quiz_title = models.CharField(max_length=100, null=True)
	pub_date = models.DateTimeField(null=True, blank=True)
	start_time = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.quiz_title
	
class Questions(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = models.CharField(max_length=1000, null=True)
	option1 = models.CharField(max_length=1000, null=True)
	option2 = models.CharField(max_length=1000, null=True)
	option3 = models.CharField(max_length=1000, null=True)
	is_correct = models.CharField(max_length=1000, null=True)

class Answers(models.Model):
	user_key = models.ForeignKey(Extendedusers, on_delete=models.CASCADE)
	question_key = models.IntegerField(null=False)
	user_answer = models.CharField(max_length=1000, null=True)
	is_submitted = models.BooleanField(default=False)
	