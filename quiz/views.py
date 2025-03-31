# quiz/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import QuizQuestion, QuizAttempt, get_random_quiz_questions
from .serializers import QuizQuestionSerializer, SubmitQuizSerializer, QuizAttemptSerializer
from django.utils import timezone
from django.shortcuts import render

class StartQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = get_random_quiz_questions(num_questions=10)
        serializer = QuizQuestionSerializer(questions, many=True)
        return Response(serializer.data)

class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubmitQuizSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            answers = serializer.validated_data['answers']
            questions = QuizQuestion.objects.filter(id__in=answers.keys())
            if len(questions) != len(answers):
                return Response({"error": "Invalid question IDs in answers."}, status=status.HTTP_400_BAD_REQUEST)

            quiz_attempt = QuizAttempt.objects.create(user=user)
            quiz_attempt.questions.set(questions)
            quiz_attempt.user_answers = answers
            score = quiz_attempt.calculate_score()
            quiz_attempt.end_time = timezone.now()
            quiz_attempt.save()

            attempt_serializer = QuizAttemptSerializer(quiz_attempt)
            return Response(attempt_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-start_time')
        serializer = QuizAttemptSerializer(quiz_attempts, many=True)
        return Response(serializer.data)

def quiz(request):
    return render(request, 'quiz_page.html')


