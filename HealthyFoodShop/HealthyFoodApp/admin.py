from django.contrib import admin
from .models import *

class ProductInline(admin.TabularInline):
    model = Product
    extra=1

class ProductAdmin(admin.ModelAdmin):
    exclude = ['user',]
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        else:
            return obj.user == request.user

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    inlines = (ProductInline,)
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class ClientAdmin(admin.ModelAdmin):
    list_display = ['name','lastName']

class SaleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sale,SaleAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)