from django.contrib import admin
from . models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice
# Register your models here.

admin.site.register(Variant)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'sku' : ('title', )}
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)