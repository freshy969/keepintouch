from django.contrib import admin

# Register your modelx here.

from .models import Contact, KITUser, Event, PublicEvent, MessageTemplate, SentMessage, SMTPSetting, CoUserGroup


class ContactAdmin(admin.ModelAdmin):

    list_display = ('first_name','last_name','active')
    
class KITUserAdmin(admin.ModelAdmin):
    
    def user_group(self, obj):
        return ", ".join(p.title for p in obj.cousergroup_set.all())
    user_group.short_description = "Groups Admin Over"
    
    list_display = ('user','parent','is_admin','user_group')

class CoUserGroupAdmin(admin.ModelAdmin):
    
    list_display = ('title','kit_admin')
    
    
admin.site.register(Event)
admin.site.register(PublicEvent)
admin.site.register(Contact, ContactAdmin)
admin.site.register(SentMessage)
admin.site.register(MessageTemplate)
admin.site.register(SMTPSetting)
admin.site.register(KITUser, KITUserAdmin)
admin.site.register(CoUserGroup, CoUserGroupAdmin)
