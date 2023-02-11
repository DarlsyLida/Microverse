
from calendar import month
from email.policy import default
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now


# from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, national_ID, phone_number,  password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not national_ID:
            raise ValueError('The given phone_number must be set')
        # email = self.normalize_email(email)
        user = self.model(national_ID=national_ID, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, national_ID,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(national_ID,  password, **extra_fields)

    def create_superuser(self, national_ID,  password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)
        phone_number = "ass@cs.com"        
      
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(national_ID, phone_number,  password, **extra_fields)



class CustomUser(AbstractUser):
    USER_TYPE = (("Admin", "Admin"), ("Customer", "Customer"), ("Employee", "Employee"))
    gender_type = (('Female', 'Female'), ('Male', 'Male'), ('Unknown', 'Unknown'))
    
    username = None
    national_ID = models.CharField(max_length=16, blank = True, unique=True)
    phone_number = models.CharField(max_length=16, blank = True, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(default="Customer", choices=USER_TYPE, max_length=15)
    gender = models.CharField(default="Male", choices=gender_type, max_length=15)
    # user_type = models.CharField(default="Client", choices=USER_TYPE, max_length=7)
    USERNAME_FIELD='national_ID'
    # EMAIL_FIELD = 'national_ID'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Reference(models.Model):
    """Generate unique reference numbers for other models.

    The only purpose of this model is to generate unique reference numbers.
    """

    # Django models need at least 1 field
    created_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate(cls, prefix: str) -> str:
        """Generate a unique reference number prefixed with the provided prefix.

        For example, you could generate an invoice number as follows:

        Reference.generate(prefix="INV") # INV-000001 etc.
        """

        instance = cls.objects.create()
        suffix = f"{instance.pk}".zfill(6)
        return f"{prefix}-{suffix}"


class BankAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    available_amount = models.FloatField()
    date_created = models.DateTimeField('date created', auto_now_add=True)

    def __str__(self):
        return self.account_no


class Card(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    status = models.IntegerField(default=0) 
    card_no=models.CharField(max_length=100,blank=True) 
    date_created = models.DateTimeField('date created', auto_now_add=True)
    expiry_date=models.DateTimeField()


    def __str__(self):
        return self.card_no

trans_type = (('withdrawal','withdrawal'), ('top up', 'top up'))
class Transaction(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    transtaction_type = models.CharField( choices=trans_type, max_length=15)

    def __str__(self):
        return self.code