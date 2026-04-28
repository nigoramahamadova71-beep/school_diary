from .models import *
from rest_framework import serializers

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'student_class', 'avatar']

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'student_class', 'avatar']
        read_only_fields = ['id']
        
        
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            'id',
            'subject',
            'date',
            'start_time',
            'end_time',
            'classroom',
            'teacher',
            'class_name'
        ]
        
class GradesSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Grades
        fields = [
            'id',
            'subject',
            'subject_name',
            'student_name',
            'student',
            'grade',
            'date',
            'lesson_topic'
        ]
        
        
class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Attendance
        fields = [
            'id',
            'subject',
            'subject_name',
            'student_name',
            'student',
            'attendance',
            'date'
        ]
        
class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    class Meta:
        model = Payment
        fields = [
            'id',
            'student_name',
            'student',
            'date_pay',
            'month',
            'paid'
        ]