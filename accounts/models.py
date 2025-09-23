# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="properties",
        null=True, blank=True
    )
    title = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50)
    listing_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.CharField(max_length=10, blank=True, null=True)
    bathrooms = models.CharField(max_length=10, blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    full_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    # Features
    swimming_pool = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)
    garden = models.BooleanField(default=False)
    fireplace = models.BooleanField(default=False)
    central_ac = models.BooleanField(default=False)
    security_system = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    smart_home = models.BooleanField(default=False)

    # Contact info
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    preferred_contact = models.CharField(
        max_length=20,
        choices=[("phone", "Phone"), ("email", "Email"), ("both", "Both")],
        default="both"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ New Model for property images
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="properties/")

    def __str__(self):
        return f"Image for {self.property.title}"
