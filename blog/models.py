from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = " دنبال کنندگان خبرنامه"
        verbose_name_plural = " دنبال کنندگان خبرنامه"
