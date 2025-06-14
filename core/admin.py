from django.contrib import admin
from .models import Dog, ForumComment, ForumRoom, ClubMembership, ClubForumComment, ClubForumRoom
# Register your models here.

admin.site.register(Dog)
admin.site.register(ForumRoom)
admin.site.register(ForumComment)
admin.site.register(ClubMembership)
admin.site.register(ClubForumRoom)
admin.site.register(ClubForumComment)
