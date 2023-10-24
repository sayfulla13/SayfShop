from django.contrib import admin
from .models import Product , Basket
# Register your models here.

class SayfShopAdmin(admin.ModelAdmin):
    readonly_fields = ('createdDate',)

admin.site.register(Product,SayfShopAdmin)
admin.site.register(Basket )
