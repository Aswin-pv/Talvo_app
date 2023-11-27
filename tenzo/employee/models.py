# from django.db import models
# from category.models import Subcategory


# class Employee(models.Model):
#     subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
#     fname = models.CharField(max_length=255,null=False)
#     lname = models.CharField(max_length=255)
#     adhar_number = models.CharField(max_length=255,unique=True,null=False)
#     pan_number = models.CharField(max_length=255,unique=True,null=False)
#     contact_number = models.CharField(max_length=10,unique=True,null=False)
#     experience = models.IntegerField()


#     def __str__(self):
#         return f"{self.fname} {self.lname}"