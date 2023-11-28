from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    slug = models.SlugField(max_length=100,unique=True, blank=True, null=True)   
    description = models.CharField(max_length=255,blank=True)
    category_image = models.ImageField(upload_to='category/', null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default = True)
    subcategory_title = models.CharField(max_length=255,null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True) 
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



