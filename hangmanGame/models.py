from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class hangmanWord(models.Model):
    text = models.CharField(max_length=50)
    category = models.CharField(max_length=100, null=True, blank=True)
    meaning = models.TextField()
    difficulty = models.CharField(max_length=10)
    
    def __str__(self):
        return self.text

class hangman_Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)
    guessed = models.CharField(max_length=26, default="")
    status = models.CharField(max_length=20, default='IN_PROGRESS')
    game_id = models.BigAutoField(primary_key=True, auto_created=True)
    difficulty = models.CharField(max_length=10)
    mode = models.CharField(max_length=20, default='')
    
    def __str__(self):
        return self.answer + str(" ") + str(self.user)