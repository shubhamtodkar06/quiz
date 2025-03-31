from django.contrib import admin
from .models import QuizQuestion, QuizAttempt

admin.site.register(QuizQuestion)
admin.site.register(QuizAttempt)