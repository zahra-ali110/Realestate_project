from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # show ALL fields in list view
    list_display = [field.name for field in Property._meta.fields]

    # make all fields searchable (for text-based search)
    search_fields = [field.name for field in Property._meta.fields 
                     if field.get_internal_type() in ("CharField", "TextField")]

    # filter by any Date/Boolean/Choice fields
    list_filter = [field.name for field in Property._meta.fields 
                   if field.get_internal_type() in ("DateField", "DateTimeField", "BooleanField")]

