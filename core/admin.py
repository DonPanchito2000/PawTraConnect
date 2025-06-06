from django.contrib import admin
from .models import Dog, ForumComment, ForumRoom, ClubMembership
# Register your models here.

admin.site.register(Dog)
admin.site.register(ForumRoom)
admin.site.register(ForumComment)
admin.site.register(ClubMembership)
