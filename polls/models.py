from django.db import models
from django.contrib.postgres.fields import ArrayField

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

class IO(models.Model):
    class Type(models.TextChoices):
        INPUT = 'I',                     #INPUT
        OUTPUT = 'O',                   #OUTPUT
        I2C_TMP102 = 'JR', 'I2C_TMP102' #TMP102
    type = models.CharField(max_length=2,choices=Type.choices)          # Stand for the type of the IO described in class Type
    stateInteger = models.IntegerField(default=0)                       # If the type had an integer value this field represent that value
    stateText = models.CharField(max_length=32)                         # If the type had a string value this field represent that value
    stateDecimal = models.DecimalField(max_digits=20, decimal_places=2) # If the type had an decimal value this field represent that value
    device = models.ForeignKey(Device, on_delete=models.CASCADE)        # I am a IO and I belong to a device...