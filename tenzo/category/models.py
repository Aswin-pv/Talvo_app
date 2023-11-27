from django.db import models
from django.utils.text import slugify



class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)   
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





