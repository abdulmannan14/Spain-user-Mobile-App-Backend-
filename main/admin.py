from django.contrib import admin

# Register your models here.
from . import models as main_models

admin.site.register(main_models.UserDetails)
