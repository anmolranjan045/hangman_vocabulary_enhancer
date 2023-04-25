from django.contrib import admin
from .models import hangmanWord, hangman_Game

admin.site.register(hangmanWord)
admin.site.register(hangman_Game)
