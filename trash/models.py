from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class register(models.Model):
#     user=models.OneToOneField(User, on_delete = models.CASCADE)


#     def __str__(self) -> str:
#         return self.user.username

class Areas(models.Model):

    area_name = models.CharField(max_length=20)

    def __str__(self):
        return self.area_name

    def housecount(self):
        houses = Houses.objects.filter(area = self)
        return houses.count()+1




class Collector(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    is_admin  = models.BooleanField(default=False)
    is_real  = models.BooleanField(default=False)
    area_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

class Houses(models.Model):

    area = models.ForeignKey(Areas, on_delete = models.CASCADE)
    house_name = models.CharField(max_length=20)
    house_address = models.CharField(max_length=50, blank=True)
    is_completed = models.CharField(max_length=50, default='Not Completed')
    collector = models.ForeignKey(Collector, on_delete=models.DO_NOTHING, default=None, null=True,blank=True)


    def __str__(self) -> str:
        return self.house_name


# Here we connect Collector with User using ONeToOneField