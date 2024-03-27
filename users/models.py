from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER=(
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

STATUS=(
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed'),
    ('seperated', 'Seperated'),

)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def profile(self):
        profile, created = UserProfile.objects.get_or_create(user=self)
        return profile

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER, default='other')
    status = models.CharField(max_length=20, choices=STATUS, default='other')

    occupation = models.CharField(max_length=20, blank=True, null=True)
    lives_in = models.CharField(max_length=200, null=True, blank=True)
    born_in = models.CharField(max_length=200, null=True, blank=True)

    joined = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=20, blank=True, null=True)
    photos = models.ManyToManyField('Photo',  blank=True)

    


    def __str__(self):
        return self.user.username + "'s Profile"
    

class Photo(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id}"