from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=32, default='Title')
    content = models.TextField(null=True)

    def __str__(self):
        return self.title


class Table(models.Model):
    show = models.SmallIntegerField(default=0)
    title = models.TextField(null=False)
    expired = models.IntegerField(default=0)
    field = models.TextField()

    def __str__(self):
        return self.title


class PostCount(models.Model):
    ip = models.TextField(default=0)
    rows = models.IntegerField(default=0)
    title = models.TextField()
    counts = models.IntegerField(default=0)
    pub_time = models.DateTimeField(null=True)
