from django.contrib.auth.models import User
from polls.models import Usuario
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		Usuario = get_user_model()
		try:
			user = Usuario.objects.get(Q(username=username)| Q(email=username))
		except Usuario.DoesNotExist:
			return None
		else:
			if user.check_password(password):
				return user
		return None