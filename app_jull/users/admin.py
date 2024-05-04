from django.contrib import admin


from .models import CustomUser, Profile, Contact


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Contact)
