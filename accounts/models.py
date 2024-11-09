from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self,email, name, password):
        user = self.create_user(email, name, password)
        
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    phone = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    top_seller = models.BooleanField(default=False)
    date_hired = models.DateTimeField(default=datetime.now, blank=True)
    email_optional = models.EmailField(max_length=255, blank = True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email




class Testimonial(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    content = models.TextField()
    testimonial_type_choices = [
        ('OWNER', 'Owner'),
        ('Tenant', 'Tenant'),
        ('Buyer', 'Buyer')
    ]
    testimonial_type = models.CharField(max_length=10, choices=testimonial_type_choices)
    creation_time = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return f"{self.user.name} - {self.creation_time}"

    def save(self, *args, **kwargs):
        # If user is not set, set it to the current user
        if not self.user_id:
            self.user = UserAccount.objects.get(pk=your_current_user_id)
        super(Testimonial, self).save(*args, **kwargs)