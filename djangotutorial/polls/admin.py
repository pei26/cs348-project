from django.contrib import admin
from .models import Club, Room, Student, Meeting, MeetingOrganizer

admin.site.register(Club)
admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Meeting)
admin.site.register(MeetingOrganizer)