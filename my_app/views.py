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
            data = request.data,
            partial = True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        student_class = data.get('student_class')
        
        if username is None or password is None or email is None:
            return Response({'message': 'Нужен и логин, и пароль'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_exist = Users.objects.filter(username=username).exists()
        email_exist = Users.objects.filter(email=email).exists()
        
        if user_exist:
            return Response({'message': "Пользователь уже существует"}, status=status.HTTP_400_BAD_REQUEST)
        if email_exist:
            return Response({'message': "E-mail уже существует"}, status=status.HTTP_400_BAD_REQUEST)
        
        hashed_password= make_password(password)
        
        user = Users.objects.create(
            username= username, 
            email = email,
            password = hashed_password,
            student_class = student_class 
            )
        user.save()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        
        print(access_token)
        print(refresh_token)
        return Response(
            {
            "message": "Регистрация прошла успешна",
            "access_token": str(access_token), 
            "refresh_token": str(refresh_token)
            }, 
            status=status.HTTP_201_CREATED
            )

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'message': 'Нужен и email, и пароль'},
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
        user = request.user
        # print(f"Попытка логина: {request.data}")
        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class GetSchedule(APIView):
    def get(self, request):
        student_class = request.query_params.get('student_class', None)
        
        if not student_class:
            return Response(
            {"error": "Не передан параметр student_class"},
            status=status.HTTP_400_BAD_REQUEST
            )     
        schedule_student = Schedule.objects.filter(class_name=student_class).order_by('start_time')
        print(schedule_student)   
        serializer = ScheduleSerializer(schedule_student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class GetGrades(APIView):
    def get(self, request):
        username = request.query_params.get('username', None)
        
        if not username:
            return Response(
            {"error": "Не передан параметр username"},
            status=status.HTTP_400_BAD_REQUEST
            )     
        grades_student = Grades.objects.filter(student__username=username).order_by('date')
        print(request)   
        serializer = GradesSerializer(grades_student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    
class GetAttendance(APIView):
    def get(self, request):
        username = request.query_params.get('username', None)
        
        if not username:
            return Response(
            {"error": "Не передан параметр username"},
            status=status.HTTP_400_BAD_REQUEST
            )     
        attendance_student = Attendance.objects.filter(student__username=username).order_by('date')
        print(attendance_student)   
        serializer = AttendanceSerializer(attendance_student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class GetPayment(APIView):
    def get(self, request):
        username = request.query_params.get('username', None)
        
        if not username:
            return Response(
            {"error": "Не передан параметр username"},
            status=status.HTTP_400_BAD_REQUEST
            )     
        payment_student = Payment.objects.filter(student__username=username).order_by('month')
        print(payment_student)   
        serializer = PaymentSerializer(payment_student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Нужно подключить simplejwt.token_blacklist
        except Exception:
            return Response({'error': 'Неверный refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'}, status=status.HTTP)