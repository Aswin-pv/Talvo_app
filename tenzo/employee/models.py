from django.db import models
from category.models import Subcategory,Category
import uuid


class Employee(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    employee_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employee_name = models.CharField(max_length=255,null=False)
    location = models.CharField(max_length=255,null=False)
    contact_number = models.CharField(max_length=10,unique=True,null=False)
    experience = models.IntegerField()
    profile_image = models.ImageField(upload_to='employee/', null=True, blank=True)

    is_available = models.BooleanField(default=True,null=False)


    def __str__(self):
        return f"{self.employee_name}"

