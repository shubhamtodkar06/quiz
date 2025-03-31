# quiz/serializers.py
from rest_framework import serializers
from .models import QuizQuestion, QuizAttempt

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'options']  # Exclude correct_answer

class SubmitQuizSerializer(serializers.Serializer):
    answers = serializers.JSONField()  # Expected format: {question_id: user_answer}

class QuizAttemptSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = QuizAttempt
        fields = ['id', 'start_time', 'end_time', 'score', 'questions', 'user_answers']
        read_only_fields = ['id', 'start_time', 'end_time', 'score', 'questions', 'user']