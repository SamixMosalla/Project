from django.db import models
from django.contrib.auth.models import User
import jdatetime
from django.urls import reverse


class Category(models.Model):
    image = models.ImageField(
        upload_to="category_images/", blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    count_product = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته بندی محصولات "
        verbose_name_plural = " دسته بندی محصولات "


class NewProducts(models.Model):
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True, verbose_name='عکس محصول'
    )
    name = models.CharField(max_length=100, unique=True,
                            verbose_name='اسم محصول')
    main_price = models.IntegerField(
        default=100000, verbose_name='قیمت اصلی محصول')
    discount_price = models.IntegerField(
        default=100000, verbose_name="قیمت محصول با تخفیف")
    Short_description = models.TextField(
        max_length=800, verbose_name='توضیحات کوتاه در مورد مصحول ', default='توضیحات')
    Description = models.TextField(
        max_length=1000, verbose_name='توضیحات', default='توضیحات')
    category = models.TextField(
        max_length=500, verbose_name='دسته بندی محصول', default='خرما'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    weight = models.CharField(
        max_length=400, verbose_name='وزن', default='1 کیلوگرم ، 750 گرم ، 500 گرم')
    quality = models.CharField(
        max_length=300, verbose_name='کفیفت', default='درجه یک')
    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'pk': self.pk, 'name': self.name})

    class Meta:
        verbose_name = " محصولات جدید"
        verbose_name_plural = " محصولات جدید "


class NewWeBlog(models.Model):
    image = models.ImageField(
        upload_to='weblog_image/', blank=True, null=True
    )
    title = models.CharField(max_length=300)
    short_description = models.TextField(
        max_length=200, verbose_name='توضیح کوتاه در مورد موضوع ', default='short description')
    description = models.TextField(
        max_length=1000, verbose_name='توضیحات در مورد موضوع', default='long description')
    time = models.DateTimeField(
        auto_now_add=True
    )

    def get_created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime=self.time).strftime('%Y %B %d - %H:%M')

    def get_absolute_url(self):
        return reverse('main:blog_detail', kwargs={'pk': self.pk, 'name': self.title})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = " مطالب جدید"
        verbose_name_plural = " مطالب جدید"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(NewProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return int(self.product.discount_price) * self.quantity


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "ارتباط با ما "
        verbose_name_plural = "ارتباط با ما "


class ContactInfo(models.Model):
    management_email = models.EmailField(
        verbose_name="ایمیل مدیریت", blank=True, null=True)
    support_email = models.EmailField(
        verbose_name="ایمیل پشتیبانی", blank=True, null=True)

    management_phone = models.CharField(
        max_length=15, verbose_name="شماره تماس مدیریت", blank=True, null=True)
    support_phone = models.CharField(
        max_length=15, verbose_name="شماره تماس پشتیبانی", blank=True, null=True)

    landline_phone = models.CharField(
        max_length=15, verbose_name="شماره تلفن ثابت", blank=True, null=True)

    instagram = models.URLField(
        verbose_name="اینستاگرام", blank=True, null=True)
    whatsapp = models.URLField(verbose_name="واتساپ", blank=True, null=True)
    telegram = models.URLField(verbose_name="تلگرام", blank=True, null=True)
    twitter = models.URLField(verbose_name="توییتر", blank=True, null=True)

    address = models.TextField(verbose_name="آدرس", blank=True, null=True)

    def __str__(self):
        return 'اطلاعات تماس'

    class Meta:
        verbose_name = "اطلاعات تماس ادمین "
        verbose_name_plural = "اطلاعات تماس ادمین"


class Comment(models.Model):
    blog = models.ForeignKey(
        NewWeBlog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"

    class Meta:
        verbose_name = 'فرم دیدگاه وبلاگ'
        verbose_name_plural = "فرم دیدگاه وبلاگ"


class ProductComment(models.Model):
    product = models.ForeignKey(
        NewProducts, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField(verbose_name='دیدگاه')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # نیاز به تایید ادمین

    def __str__(self):
        return f"{self.name} - {self.product.name}"

    class Meta:
        verbose_name = " دیدگاه مرتبط به محصولات "
        verbose_name_plural = " دیدگاه مرتبط به محصولات"


class BillingInfo(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    province = models.CharField(max_length=100, verbose_name="استان")
    street = models.CharField(max_length=255, verbose_name="آدرس خیابان")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    email = models.EmailField(verbose_name="ایمیل")
    products = models.TextField(verbose_name="محصولات (نام، تعداد و قیمت)")
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="مبلغ کل")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ثبت")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = " سفارش های ثبت شده "
        verbose_name_plural = " سفارش های ثبت شده "
