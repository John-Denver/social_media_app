from django.contrib import admin
from post.models import Tag, Post, Follow, Stream, Media

# Register your models here.

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Media)
admin.site.register(Follow)
admin.site.register(Stream)
