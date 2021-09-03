from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from users.models import User

admin.site.register(ContentType)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
