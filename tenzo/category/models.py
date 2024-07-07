from user.models import User
from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    slug = models.SlugField(max_length=100,unique=True, blank=True, null=True)   
    category_image = models.ImageField(upload_to='category/', null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    #automatically generate a slug using slugify
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=False)
    subcategory_title = models.CharField(max_length=255,null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True) 
    charge = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.CharField(max_length=255,blank=True)
    employee_count = models.IntegerField(null=False, blank=False)
    sub_category_image = models.ImageField(upload_to='sub_category/', null=True, blank=True)

    class Meta:
        verbose_name = 'sub_category'
        verbose_name_plural = 'sub_categories'

    def save(self, *args, **kwargs):
        if self.slug is None:
            #GENERATE A UNIQUE IDENTIFIER
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{slugify(self.subcategory_title)}-{unique_id}"
        super().save(*args, **kwargs)    

    def __str__(self):
        return self.subcategory_title

# product review
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rating = models.FloatField()
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


    

