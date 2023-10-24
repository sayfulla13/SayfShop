from django.db import models
from django.contrib.auth.models import User


CATEGORIS2 = (
    ('мобильные телефоны','мобильные телефоны'),
    ('телевизоры','телевизоры'),
    ('ноутбуки','ноутбуки'),
    ('компьютерные детали','компьютерные детали'),
    ('игровые приставки','игровые приставки'),
    ('наушники','наушники'),
)

class Product(models.Model):
    name = models.CharField(max_length=50)
    discription = models.TextField()
    category = models.CharField(max_length=30 ,choices=CATEGORIS2,default=CATEGORIS2[0][0])
    price = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=50)
    img = models.ImageField(upload_to='sayfshop/images' ,null=True)
    count = models.PositiveIntegerField()
    createdDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)



    def __str__(self):
        return self.name

class Basket(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)

    user = models.ForeignKey(User , on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.product.name} -- {self.user.username}'
