from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *


class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        student_class = data.get('student_class')

        if not username or not email or not password:
            return Response(
                {'message': 'Нужны username, email и password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Users.objects.filter(username=username).exists():
            return Response(
                {'message': "Пользователь уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Users.objects.filter(email=email).exists():
            return Response(
                {'message': "E-mail уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = Users.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            student_class=student_class
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Регистрация прошла успешно",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'message': 'Нужен email и пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = Users.objects.filter(email=email).first()

        if not user:
            return Response(
                {'message': 'Пользователь не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password):
            return Response(
                {'message': 'Неверный email или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Успешный вход",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })


class GetInfoUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class GetSchedule(APIView):
    def get(self, request):
        student_class = request.query_params.get('student_class')

        if not student_class:
            return Response(
                {"error": "Не передан student_class"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = Schedule.objects.filter(class_name=student_class).order_by('start_time')
        return Response(ScheduleSerializer(data, many=True).data)


class GetGrades(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response(
                {"error": "Не передан username"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = Grades.objects.filter(student__username=username).order_by('date')
        return Response(GradesSerializer(data, many=True).data)


class GetAttendance(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response(
                {"error": "Не передан username"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = Attendance.objects.filter(student__username=username).order_by('date')
        return Response(AttendanceSerializer(data, many=True).data)


class GetPayment(APIView):
    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response(
                {"error": "Не передан username"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = Payment.objects.filter(student__username=username).order_by('month')
        return Response(PaymentSerializer(data, many=True).data)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'Необходим refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'error': 'Неверный refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'success': 'Выход успешен'},
            status=status.HTTP_200_OK
        )