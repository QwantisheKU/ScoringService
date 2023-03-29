from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(default='default.png', null=True)
    date_created = models.DateTimeField(default=datetime.now)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

class Calculation(models.Model):
    LOAN_DEFAULTS = (
        ('Y', 'Да'),
        ('N', 'Нет'),
    )
    HOME_OWNERSHIPS = (
        ('RENT', 'Аренда'),
        ('MORTGAGE', 'Ипотека'),
        ('OWN', 'Собственность'),
        ('OTHER', 'Другое'),
    )
    LOAN_INTENTS = (
        ('EDUCATION', 'Образование'),
        ('MEDICAL', 'Медицина'),
        ('VENTURE', 'Инвестиции'),
        ('PERSONAL', 'Личная'),
        ('DEBTCONSOLIDATION', 'Погашение долга'),
        ('HOMEIMPROVEMENT', 'Жилищный ремонт'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person_name = models.CharField(max_length=200)
    person_age = models.IntegerField()
    person_income = models.IntegerField()
    person_home_ownership = models.CharField(max_length=30, choices=HOME_OWNERSHIPS)
    person_emp_length = models.FloatField()
    loan_intent = models.CharField(max_length=30, choices=LOAN_INTENTS)
    loan_amnt = models.IntegerField()
    loan_int_rate = models.FloatField()
    cb_person_default_on_file = models.CharField(max_length=30, choices=LOAN_DEFAULTS)
    cb_person_cred_hist_length = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.person_name
    
    class Meta:
        ordering = ['-date_created']
    
class CalculationResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    score = models.CharField(max_length=1)
    date_created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    calculation_id = models.ForeignKey(Calculation, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
    
class FeedbackForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return self.name