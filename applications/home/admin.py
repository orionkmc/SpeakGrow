# Django
from django.contrib import admin

# Apps
from applications.home.models import (UserProfile, AnonymousUser, Room)

# Other
from django_object_actions import DjangoObjectActions


class UserProfileAdmin(DjangoObjectActions, admin.ModelAdmin):
    def make_published(modeladmin, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="users.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(["Username", "First name", "Last name", "Email", "picture", "number", "short_description"])
        for q in queryset:
            writer.writerow([
                q.user.username, q.user.first_name, q.user.last_name, q.user.email, q.profile_picture.url,
                q.phone_number, q.short_description
            ])
        return response

    make_published.label = "descargar en formato csv"
    make_published.short_description = "descargar en formato csv"

    changelist_actions = ('make_published', )


class AnonymousUserAdmin(admin.ModelAdmin):
    pass


class RoomAdmin(admin.ModelAdmin):
    list_display = ('anonymousUser', 'speaker', 'created_at',)
    list_filter = ('anonymousUser', 'speaker')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AnonymousUser, AnonymousUserAdmin)
admin.site.register(Room, RoomAdmin)
