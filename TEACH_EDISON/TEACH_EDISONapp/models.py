# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate
from django.db.models import Q
# from django.contrib.auth.backends import ModelBackend
class EmailBackend(object):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:

            username = kwargs.get(User.USERNAME_FIELD)
        try:
            try:
                user = User.objects.get(
                    email=username
                )
            except:
                user = User.objects.get(
                    phone=username
                )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
            
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        
        return is_active or is_active is None
    def get_user(self, user_id):
        try:
            user = User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials

# accounts.models.py

class UserManager(BaseUserManager):
    def create_user(self, email, phone, first_name, last_name, DOB, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            DOB=DOB
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, phone, first_name, last_name, DOB, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            DOB=DOB
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, first_name, last_name, DOB, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            DOB=DOB
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    first_name = models.CharField(
        verbose_name='first name',
        max_length=255,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=255,
        blank=True
    )
    DOB = models.CharField(
        max_length=17,
        verbose_name='Date Of Birth',
        blank=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = models.CharField(max_length=11,blank=True,unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["first_name","last_name","DOB"] # Email & Password are required by default.

    # def get_full_name(self):
    #     # The user is identified by their email address
    #     return self.email

    # def get_short_name(self):
    #     # The user is identified by their email address
    #     return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
