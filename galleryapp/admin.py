from django.contrib import admin

from galleryapp.models import CustomUser, Album


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_number', 'email',)
    list_display_links = ('id', 'email', 'email')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'original_price', 'offer_price', 'user')
