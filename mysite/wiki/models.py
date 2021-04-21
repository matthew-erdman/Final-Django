from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Entry(models.Model):
	entry_title = models.CharField(max_length=100)
	entry_text = models.CharField(max_length=5000)
	#entry_author = models.ForeignKey(User, on_delete=models.CASCADE)
	entry_date = models.DateTimeField(auto_now_add=True)
	entry_updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		if len(self.entry_title) > 28:
			return self.entry_title[:25] + '...'
		else:
			return self.entry_title


class Comment(models.Model):
	comment_text = models.CharField(max_length=500)
	comment_date = models.DateTimeField('date published')
	def __str__(self):
		if len(self.comment_text) > 28:
			return self.comment_text[:25] + '...'
		else:
			return self.comment_text
