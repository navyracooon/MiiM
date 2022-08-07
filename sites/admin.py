from django.contrib import admin

from .models import Meme, Tag, Language, Mi, Evaluation, TagList

admin.site.register(Meme)
admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Mi)
admin.site.register(Evaluation)
admin.site.register(TagList)

# Register your models here.
