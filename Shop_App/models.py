from django.db import models
from PIL import Image
from django.db.models.fields.related import ForeignKey

class CategoryGroup(models.Model):
    group_name = models.CharField(max_length=40)

    def __str__(self):
        return "Category group for " + self.group_name

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=40, blank = False)
    group_name = ForeignKey(CategoryGroup, blank = False, on_delete=models.CASCADE)
    category_description = models.TextField()

    def serialize(self, *args, **kwargs):
        return {
            "category_name": self.category_name,
            "group_name": self.group_name.group_name,
            "category_description": self.category_description
        }


    def __str__(self):
        return "Category " + self.category_name

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    creation_date = models.DateField(auto_now=True)
    price = models.FloatField(blank=False)
    image = models.ImageField(default="default3.jpg")
    is_vege = models.BooleanField(default=False)
    category = models.ManyToManyField(ProductCategory)

    def serialize(self,*args,**kwargs):
        qs_cat = self.category.all()
        cat_keys = []
        cat_vals = []

        #for each product the category and its group need to be serialized
        i = 0
        for q in qs_cat:
            cat_keys.append(i)
            i = i+1
            cat_vals.append({
                "category_name" : q.category_name,
                "group_name" : q.group_name.group_name
            })

        category=dict(zip(cat_keys,cat_vals))

        return {
            "name" : self.name,
            "description" : self.description,
            "creation_date" : self.creation_date,
            "price" : self.price,
            "image" : self.image.url,
            "is_vege" : self.is_vege,
            "category" : category,
        }

    def __str__(self):
        return "Pr-"+self.name+" "+str(self.creation_date.day)+ "-" +str(self.creation_date.month)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        print(self.category)

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

