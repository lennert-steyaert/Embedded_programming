import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################
# This file contains the models directly mapped into the database
#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################


##################################################
# Device object for on arduino/pi/beaglebone/ESP32
##################################################

class Device(models.Model):
    name = models.CharField(max_length=100)                 # Unique name from device
    lastSync = models.DateTimeField()                       # Last sync timestamp with the device
    lastMessageAccepted = models.BooleanField(default=True) # Last message is accepted = True
    img = models.ImageField(upload_to='pics')
    #########
    # Device has multiple IO table relationship
    #########
    # Add passwordhash
    # JWT token for accessing the API

############################################################################
# Stands for physical IO on a µc / computer (pi/beaglebone etc) !!SUBCLASS!!
############################################################################

class Type(models.TextChoices):
    INPUT = 'I',                     #INPUT
    OUTPUT = 'O',                   #OUTPUT
    I2C_TMP102 = 'JR', 'I2C_TMP102' #TMP102

class IO(models.Model):
    pin = models.CharField(max_length=10) 
    type = models.CharField(max_length=2,choices=Type.choices)          # Stand for the type of the IO described in class Type
    stateInteger = models.IntegerField(default=0)                       # If the type had an integer value this field represent that value
    stateText = models.CharField(max_length=32)                         # If the type had a string value this field represent that value
    stateDecimal = models.DecimalField(max_digits=20, decimal_places=2) # If the type had an decimal value this field represent that value
    device = models.ForeignKey(Device, on_delete=models.CASCADE)        # I am a IO and I belong to a device...

############################################################################################################################
# User stuff below (https://medium.com/analytics-vidhya/django-rest-api-with-json-web-token-jwt-authentication-69536c01ee18)
############################################################################################################################

class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    '''
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "login"

class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"