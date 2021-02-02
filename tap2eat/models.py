from django.db import models

# Create your models here.
class Keyfungu(models.Model):
    acc_token = models.TextField(max_length=500)

    def __str__(self):
        return self.acc_token