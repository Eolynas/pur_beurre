from django.contrib import admin
from django.core.management import call_command
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

from product.models import Product, Category


@admin.action(description='import all product from api open food fact')
def import_products(modeladmin, request, queryset):
    call_command('insert_data_api')


class ProductAdmin(admin.ModelAdmin):
    actions = [import_products]
    list_display = ['name', 'nutriscore']
    list_filter = ['nutriscore']

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'import_products':
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Product.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(ProductAdmin, self).changelist_view(request, extra_context)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)