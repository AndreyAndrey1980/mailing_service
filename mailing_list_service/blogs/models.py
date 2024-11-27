from django.db import models
from datetime import datetime


class Blog(models.Model):
    title = models.CharField(max_length=100)
    view_count = models.IntegerField(default=0)
    publicate = models.BooleanField(default=True)
    text = models.TextField()
    create_date = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.title
