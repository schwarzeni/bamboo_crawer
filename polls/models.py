from django.db import models


# Create your models here.

class Bamboo(models.Model):
    id = models.IntegerField(max_length=11, primary_key=True, null=False)
    url = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=1000, null=False)
    publish_time = models.CharField(max_length=20, null=False)
    source_from = models.CharField(max_length=20, null=False)
    click_times = models.IntegerField(max_length=11, null=False)
