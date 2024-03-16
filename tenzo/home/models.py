from django.db import models

class Contact(models.Model):

    full_name = models.CharField(max_length=100,null=False)
    email = models.EmailField(null=False)
    phone_number = models.CharField(max_length=10,null=False)
    message = models.TextField(null=False)

    def __str__(self):
        return self.full_name
    


