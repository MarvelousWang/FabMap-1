from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    class Meta:
        verbose_name = "用户信息"  # 设置UserProfle这个类的别名
        verbose_name_plural = verbose_name  # 设置别名的复数形式

    def __str__(self):
        return self.username  # 当使用print打印时, 把继承的username字段打印出来
