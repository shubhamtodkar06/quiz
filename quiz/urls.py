# quiz/urls.py
from django.urls import path
from .views import StartQuizView, SubmitQuizView, QuizHistoryView, quiz

urlpatterns = [
    path('start/', StartQuizView.as_view(), name='start_quiz'),
    path('submit/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('history/', QuizHistoryView.as_view(), name='quiz_history'),
    path('', quiz, name = "quiz")
]