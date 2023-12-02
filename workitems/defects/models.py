from django.db import models

# Create your models here.
class	Defects(models.Model):
							defect_id 	= models.CharField(max_length=200,	primary_key=True)
							creator = models.CharField(max_length=200)
							status	= models.CharField(max_length=200)
							team_area	= models.CharField(max_length=1000)
							created_dt = models.DateField(auto_now=False)
							modified_dt	= models.DateField(auto_now=False)
							filed_against	= models.CharField(max_length=1000)
