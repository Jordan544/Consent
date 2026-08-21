from django.db import models

# Create your models here.
class students(models.Model):
  reg_number = models.CharField(max_length=26)
  fullname = models.CharField(max_length=100)
  