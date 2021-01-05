from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class Extendedusers(models.Model):
	user = models.OneToOneField(User, primary_key=True,
	on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255, default='')
	email = models.EmailField(verbose_name='email', 
	max_length=60, default='')
	school_name = models.CharField(max_length=255, default='')
	is_school = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	# Validate entered email
	def email_validate(self, email):
		if Extendedusers.objects.filter(email=email):
			return False
		else:
			try:
				validate_email(email)
			except ValidationError as e:
				# Inappropriate email
				return False
			else:
				# Email as expected
				return True
