from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quote
