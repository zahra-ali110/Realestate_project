from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PropertyForm
from .models import Property


def index(request):
    # Get top 3 properties with highest price
    top_properties = Property.objects.all().order_by('-price')[:3]
    return render(request, "account/index.html", {"top_properties": top_properties})



# User Signup
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "account/signup.html", {"form": form})


# User Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {"form": form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PropertyForm
from .models import PropertyImage

@login_required
def post_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()

            # Save multiple images (make sure input name="images")
            for img in request.FILES.getlist("images"):
                PropertyImage.objects.create(property=property_instance, image=img)

            messages.success(request, "✅ Your property has been posted successfully!")
            return redirect("properties")  # redirect to property list
        else:
            print("❌ Form errors:", form.errors)  # Debugging
    else:
        form = PropertyForm()

    return render(request, "account/post_property.html", {"form": form})

def properties_page(request):
    properties = Property.objects.all()

    # Filters
    location = request.GET.get("location")
    property_type = request.GET.get("type")
    price = request.GET.get("price")
    sort = request.GET.get("sort")

    if location:
        properties = properties.filter(city__iexact=location)

    if property_type:
        properties = properties.filter(property_type__iexact=property_type)

    if price:
        if "-" in price:
            low, high = price.split("-")
            properties = properties.filter(price__gte=int(low), price__lte=int(high))
        elif "+" in price:
            low = price.replace("+", "")
            properties = properties.filter(price__gte=int(low))

    # Sorting
    if sort == "price-low":
        properties = properties.order_by("price")
    elif sort == "price-high":
        properties = properties.order_by("-price")
    elif sort == "size":
        properties = properties.order_by("-area")
    else:  # newest
        properties = properties.order_by("-created_at")

    return render(request, "account/properties.html", {"properties": properties})


# Pfrom django.shortcuts import render, get_object_or_404
from .models import Property
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    images = property_obj.images.all()
    first_image_url = images[0].image.url if images else None

    # Fetch similar properties (same city, same property_type)
    similar_properties = Property.objects.filter(
        city=property_obj.city,
        property_type=property_obj.property_type
    ).exclude(id=property_obj.id)[:3]  # limit to 3

    return render(request, "account/property_detail.html", {
        "property": property_obj,
        "images": images,
        "first_image_url": first_image_url,
        "similar_properties": similar_properties,
    })



@login_required
def profile(request):
    return render(request, "account/profile.html")
@login_required
def profile(request):
    user = request.user
    properties = Property.objects.filter(user=user)
    return render(request, "account/profile.html", {
        "user": user,
        "properties": properties,
        "listed_count": properties.count(),
        "rating": 4.8,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Property
from .forms import PropertyForm  # you must have a PropertyForm in forms.py
@login_required
def edit_property(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, user=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        files = request.FILES.getlist('images')  # get new uploaded images

        if form.is_valid():
            updated_property = form.save(commit=False)

            # Save all features (checked or unchecked)
            features = [
                'swimming_pool', 'garage', 'garden', 'fireplace',
                'central_ac', 'security_system', 'balcony', 'parking', 'smart_home'
            ]
            for feature in features:
                setattr(updated_property, feature, bool(request.POST.get(feature)))

            updated_property.save()

            # Save new images if uploaded
            for f in files:
                PropertyImage.objects.create(property=updated_property, image=f)

            messages.success(request, "✅ Property updated successfully!")
            return redirect('profile')
    else:
        form = PropertyForm(instance=property_obj)

    existing_images = property_obj.images.all()
    return render(request, 'account/post_property.html', {
        'form': form,
        'editing': True,
        'property': property_obj,
        'existing_images': existing_images
    })



@login_required
def delete_property(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, user=request.user)
    property_obj.delete()
    messages.success(request, "Property deleted successfully!")
    return redirect('profile')


@login_required
def delete_property_image(request, image_id):
    image = get_object_or_404(PropertyImage, id=image_id, property__user=request.user)
    property_id = image.property.id
    image.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect('edit_property', property_id=property_id)


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def edit_username(request):
    if request.method == "POST":
        new_username = request.POST.get("username")
        if new_username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, "Username updated successfully!")
        else:
            messages.error(request, "Username cannot be empty.")
    return redirect('profile')  # Redirect back to profile page
