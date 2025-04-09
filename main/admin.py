from django.contrib import admin

# Register your models here.
from .models import Category, NewProducts, NewWeBlog, Contact, ContactInfo, Comment, ProductComment  , BillingInfo

admin.site.register(Category)
admin.site.register(NewProducts)
admin.site.register(NewWeBlog)
admin.site.register(Contact)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'management_email', 'support_email', 'management_phone', 'support_phone',
        'landline_phone', 'instagram', 'whatsapp', 'telegram', 'twitter', 'address'
    ]
    list_editable = [
        'management_email', 'support_email', 'management_phone', 'support_phone',
        'landline_phone', 'instagram', 'whatsapp', 'telegram', 'twitter', 'address'
    ]
    list_display_links = ['id']  # استفاده از 'id' به عنوان لینک


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "تأیید دیدگاه‌های انتخاب‌شده"


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'approved', 'created_at']
    list_filter = ['approved']
    search_fields = ['name', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)




@admin.register(BillingInfo)
class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'total_price', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at',)
