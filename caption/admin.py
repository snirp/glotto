from .models import Language, Artist, Item, Youtube, Line, Translation, Linetrans, Member, Playlist
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'


class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PlaylistItemsInline(admin.TabularInline):
    model = Playlist.items.through


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'language', 'item_count', 'follower_count', )
    inlines = (PlaylistItemsInline,)

admin.site.register(Playlist, PlaylistAdmin)


class TranslationsInline(admin.TabularInline):
    model = Translation


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
    inlines = (TranslationsInline,)

admin.site.register(Language, LanguageAdmin)


class LinetransInline(admin.TabularInline):
    model = Linetrans


class TranslationAdmin(admin.ModelAdmin):
    list_display = ('title', 'item', 'language', )
    list_filter = ('language', 'item', )
    #inlines = (LinetransInline, )

admin.site.register(Translation, TranslationAdmin)

admin.site.register(Linetrans)


class ArtistItemsInline(admin.TabularInline):
    model = Item.artists.through


class ArtistAdmin(admin.ModelAdmin):
    inlines = (ArtistItemsInline, )

admin.site.register(Artist, ArtistAdmin)


class LineAdmin(admin.ModelAdmin):
    list_display = ('text', 'item', 'number', 'cue_in', 'stanza', )
    list_filter = ('item__language', 'item', )
    inlines = (LinetransInline, )

admin.site.register(Line, LineAdmin)


class LinesInline(admin.TabularInline):
    model = Line


class YoutubeAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'first_artist', 'language', )
    list_filter = ('language', )
    inlines = (LinesInline, TranslationsInline, )

admin.site.register(Youtube, YoutubeAdmin)
