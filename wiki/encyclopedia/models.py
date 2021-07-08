from django.db import models
from django.urls import reverse

# Create your models here.

# class Entry(models.Model):
#     entry_title         = models.Charfield(max_length=120)
#     description         = models.TextField(blank=True, null=True)

#     def get_absolute_url(self):
#         return reverse("encyclopedia:entry", kwargs={"entry":self.entry_title})