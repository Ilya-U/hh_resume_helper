from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Resume
from .serializers import ResumeListSerializer, ResumeStatusSerializer
from .forms import SignUpForm, LoginForm

class ResumeListView(generics.ListAPIView):
    """
    GET /api/resumes/
    Возвращает список всех резюме с id и базовой информацией
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeListSerializer


class ResumeStatusUpdateView(APIView):
    """
    PATCH /api/resumes/{id}/status/
    Принимает id резюме и новый статус, обновляет статус
    """

    def patch(self, request, resume_id):
        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            raise NotFound(detail=f'Резюме с id={resume_id} не найдено')

        # Валидация входных данных
        serializer = ResumeStatusSerializer(resume, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что статус передан
        if 'status' not in request.data:
            return Response(
                {'status': 'Это поле обязательно'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response({
            'message': 'Статус успешно обновлён',
            'resume': ResumeListSerializer(resume).data
        }, status=status.HTTP_200_OK)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # Проверяем учетные данные
            if user is not None:
                login(request, user)     # Выполняем вход
                return redirect('/')  # Перенаправляем на главную страницу
    return render(request, 'login.html', {'form': form})