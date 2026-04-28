from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    student_class = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="media/avatars/", default="media/default.webp")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} - {self.email} {self.student_class}"

class Schedule(models.Model):
    subject = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.IntegerField()
    teacher = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['start_time']  # сортировка по времени
    
    def __str__(self):
        return f"{self.subject} - {self.date} {self.start_time}"
    
class Subjects(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    
class Grades(models.Model):
    student = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    
    grade = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    lesson_topic = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.grade}"
    
class Attendance(models.Model):
    student = models.ForeignKey("Users", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    date = models.DateField()
    attendance = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.attendance}"
    
    
class Payment(models.Model):
    MONTH_CHOICES = [
        ('jan', 'Январь'),
        ('feb', 'Февраль'),
        ('mar', 'Март'),
        ('apr', 'Апрель'),
        ('may', 'Май'),
        ('jun', 'Июнь'),
        ('jul', 'Июль'),
        ('aug', 'Август'),
        ('sep', 'Сентябрь'),
        ('oct', 'Октябрь'),
        ('nov', 'Ноябрь'),
        ('dec', 'Декабрь'),
    ]
    student = models.ForeignKey("Users", on_delete=models.CASCADE)
    date_pay = models.DateField(blank=True, null=True)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.username} - {self.month} - {self.paid}"