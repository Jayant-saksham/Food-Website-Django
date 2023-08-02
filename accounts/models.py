from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    """
        Managers are used for adding methods related to a model. For example, creating a model, filtering out the model.
        The github repository of Django includes the following set of classes as Manager classes:
            -   UserManager
            -   PermissionManager
            -   GroupManager

        And following classes are available for User
            -   AbstractUser 
            -   Permission 
            -   Group

        Please note that we are just extending the BaseUserManager here. It means that we are rewriting the UserManger class which is written in Django github.  
        To create this class I used: https://github.com/django/django/blob/main/django/contrib/auth/models.py#L136 

    """
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
            
        if not email:
            raise ValueError("The given email must be set")
        
        email = self.normalize_email(email)
       
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
 


class User(AbstractBaseUser):

    """
        'User' represents custom user.
        To create custom user we have two options. We can extend any of the following classes:
        - AbstractUser       : The AbstractUser is basically just the "User" class you're probably already used to. 
                               You can add new fields, change and remove initial fields.
                               Keep it in mind that username and email fields in the initial fields of AbstractUser class are special and only username field has Unique Constraint.

        - AbstractBaseUser   : AbstractBaseUser makes fewer assumptions and you have to tell it what field represents the username, what fields are required, and how to manage those users.
                               AbstractBaseUser only contains the authentication functionality, but no actual fields: you have to supply them when you extend this class.
                               You can see the USERNAME_FIELD is not defined and REQUIRED_FIELDS = [] in case of AbstractBaseUser
                               Note - While using AbstractBaseUser class, has_perms and has_module_params functions are compulsory to be implemented.  

    Please note that we are just extending the AbstractBaseUser here. It means that we are rewriting the AbstractUser class which is written in Django github. For reference, please
    see the django's official github repository. (Also no need to mention about password)
    To create this class I used: https://github.com/django/django/blob/main/django/contrib/auth/models.py#L136 

    """
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True) 
    username = models.CharField(max_length=50, blank = True, null = True)
    email = models.EmailField(max_length = 50, unique=True, null=True, blank = True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)


    #BooleanField
    is_staff = models.BooleanField(
        default=False,
        help_text = ("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text = ("Designates whether this user should be treated as active. "),
    )
    is_superuser =  models.BooleanField(
        default=False,
        help_text = ("Designates whether this user should be treated as admin. "),
    )

    #DateField 
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True) 
    last_login = models.DateTimeField(auto_now = True)


    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"









