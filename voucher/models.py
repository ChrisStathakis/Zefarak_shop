from django.db import models

# Create your models here.



class VoucherSet(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField()
    code_length = models.IntegerField(default=12)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    offer = models.OneToOneField()