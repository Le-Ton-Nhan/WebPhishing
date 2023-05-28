# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# ctr + k + c: comment, ctr + k + u: uncomment
from django.db import models
from django.contrib.auth.models import User


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has on_delete set to the desired behavior.
#   * Remove managed = False lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# ctr + k + c: comment, ctr + k + u: uncomment
from django.db import models
from django.contrib.auth.models import User

class static_result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    prediction = models.TextField()
    conf_score = models.TextField()
class dynamic_result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    brand_name = models.TextField()
    prediction = models.TextField()
    conf_score = models.TextField()
    img_path = models.TextField()

class final_result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_id = models.AutoField(primary_key=True)
    url = models.TextField() 
    time = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    prediction_final = models.TextField()
    conf_score = models.TextField()
    vt_score = models.TextField(default="None")





