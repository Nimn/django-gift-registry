from django.contrib import admin
from gift_registry.models import Gift, Giver, Event, GiftCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    prepopulated_fields = {"slug": ("name",)}


class GiftAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'one_only', 'live')
    list_filter = ('live',)


class GiverAdmin(admin.ModelAdmin):
    list_display = ('email', )
    exclude = ('gift',)


admin.site.register(Event, EventAdmin)
admin.site.register(Gift, GiftAdmin)
admin.site.register(Giver, GiverAdmin)
admin.site.register(GiftCategory, CategoryAdmin)
