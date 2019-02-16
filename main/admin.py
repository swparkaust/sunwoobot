from django.contrib import admin

from .models import (Group, Lazylet_Set, Lazylet_Term, Log, Mail, User,
                     WordChain_Match, WordChain_Player, WordChain_Word)

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Mail)
admin.site.register(Log)
admin.site.register(Lazylet_Set)
admin.site.register(Lazylet_Term)
admin.site.register(WordChain_Match)
admin.site.register(WordChain_Player)
admin.site.register(WordChain_Word)
