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
    count = models.IntegerField(default=1)
    field = models.TextField()

    def __str__(self):
        return self.title


class PostCount(models.Model):
    ip = models.TextField(default=0)
    times = models.IntegerField(default=0)
    title = models.TextField()
    pub_time = models.DateTimeField(null=True)
