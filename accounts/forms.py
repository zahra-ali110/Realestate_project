from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Property, PropertyImage
from .models import CustomUser   # ✅ add this import

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser   # ✅ use your custom user model
        fields = ["email", "password1", "password2"]

# Property form (main data)
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "property_type",
            "listing_type",
            "price",
            "bedrooms",
            "bathrooms",
            "area",
            "year_built",
            "description",
            "full_address",
            "city",
            "state",
            "swimming_pool",
            "garage",
            "garden",
            "balcony",
            "contact_name",
            "contact_email",
            "contact_phone",
        ]


# ✅ Fix: Custom widget that really supports multiple files
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# PropertyImage form (uses MultiFileInput)
class PropertyImageForm(forms.ModelForm):
    image = forms.ImageField(widget=MultiFileInput(attrs={"multiple": True}))

    class Meta:
        model = PropertyImage
        fields = ["image"]
