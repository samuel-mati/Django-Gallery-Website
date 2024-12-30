from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    def __str__(self):
        return self.username 
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category (e.g., Nature, Architecture)
    description = models.TextField(blank=True, null=True)  # Optional description for the category

    def __str__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=255)  # The name of the image
    description = models.TextField()  # A description of the image
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    image_file = models.ImageField(upload_to='images/')  # The actual image file
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the image was uploaded

    def __str__(self):
        return self.name
    

class ImageDownload(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    date_downloaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Download of {self.image.name} on {self.date_downloaded}"


class ImageLike(models.Model): 
    image = models.ForeignKey('Image', on_delete=models.CASCADE) 
    likes = models.PositiveIntegerField(default=0) 
    
    def __str__(self):
        return f"Likes: {self.likes} for {self.image.name}"