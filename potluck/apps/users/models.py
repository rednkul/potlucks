from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from .managers import CustomUserManager

# Authentification
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Адрес электронной почты', unique=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    date_registration = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


# Profiles
class Profile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user')
    phone_number = models.CharField("Номер телефона", max_length=15)
    patrynomic = models.CharField("Отчество", max_length=60, default='')
    post_index = models.CharField("Почтовый индекс", max_length=6)
    balance = models.PositiveIntegerField("Баланс счета", default=0, help_text="Сумма в рублях")
    finished_orders = models.PositiveSmallIntegerField("Завершенные заказы", default=0)

    def __str__(self):
        return f"{self.user.email}"

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.user.save()

