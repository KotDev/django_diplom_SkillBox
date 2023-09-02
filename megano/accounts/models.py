from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to="app_users/avatars/user_avatars/",
        default="app_users/avatars/default-avatar.jpg",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")
    objects = models.Manager()

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    @classmethod
    def get_default(cls):
        avatar, _ = cls.objects.get_or_create(
            src="app_users/avatars/default-avatar.jpg"
        )
        return avatar.pk


class Profile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
        default=Avatar.get_default,
    )
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="Почта")
    objects = models.Manager()

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"{self.user.username} - {self.fullName}"
