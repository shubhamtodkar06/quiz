from django.db import models
from django.contrib.auth.models import User
import random

class QuizQuestion(models.Model):
    question_text = models.TextField()
    options = models.JSONField()  # Store options as a JSON list or dictionary
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text[:50] + "..."

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(QuizQuestion)
    user_answers = models.JSONField(default=dict)  # Store user's answers as {question_id: answer}
    score = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"

    def calculate_score(self):
        score = 0
        for question in self.questions.all():
            user_answer = self.user_answers.get(str(question.id))
            if user_answer and user_answer.lower() == question.correct_answer.lower():
                score += 1
        self.score = score
        self.save()
        return self.score

def get_random_quiz_questions(num_questions=10):
    total_questions = QuizQuestion.objects.count()
    if total_questions < num_questions:
        return random.sample(list(QuizQuestion.objects.all()), total_questions)
    else:
        return random.sample(list(QuizQuestion.objects.all()), num_questions)