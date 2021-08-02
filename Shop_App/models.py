from django.db import models
from PIL import Image

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    creation_date = models.DateField(auto_now=True)
    price = models.FloatField(blank=False)
    image = models.ImageField(default="default3.jpg")

    def __str__(self):
        return "Pr-"+self.name+" "+str(self.creation_date.day)+ "-" +str(self.creation_date.month)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        MAX_WIDTH = 200
        MAX_HEIGHT = 200

        img = Image.open(self.image.path)

        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
            img.thumbnail((MAX_HEIGHT, MAX_WIDTH))
            img.save(self.image.path)

class Comment(models.Model):
    nickname = models.CharField(max_length = 30, blank = False, null= False)
    title = models.CharField(max_length = 50, blank = False, null = False, default="Comment")
    content = models.TextField(blank = False, null = False)
    creation_date = models.DateField(auto_now = True)
    rating = models.IntegerField(blank = True, null = True)
    def __str__(self):
        return "Comment by " + self.nickname + "on" + str(self.creation_date.day) + "-" +str(self.creation_date.month) + "-" +str(self.creation_date.year)

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        print("Save method called")


    def serialize(self, *args, **kwargs):
        return {
            "nickname": self.nickname,
            "title" : self.title,
            "content": self.content,
            "creation_date": self.creation_date,
            "rating": self.rating
        }