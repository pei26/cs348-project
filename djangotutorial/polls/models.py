from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name       = models.CharField(max_length=100, db_index=True)
    email      = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Club(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=100, db_index=True)
    address     = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    id           = models.AutoField(primary_key=True)
    building     = models.CharField(max_length=100, db_index=True)
    number       = models.CharField(max_length=10, db_index=True)
    max_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.building} – {self.number}"

class Meeting(models.Model):
    id             = models.AutoField(primary_key=True)
    date           = models.DateField(db_index=True)
    time           = models.TimeField()
    duration       = models.DurationField()
    description    = models.TextField(blank=True, null=True)
    club           = models.ForeignKey(Club, on_delete=models.CASCADE, db_index=True)
    room           = models.ForeignKey(Room, on_delete=models.CASCADE, db_index=True)
    invited_count  = models.IntegerField(default=0)
    accepted_count = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['date', 'club'], name='meet_date_club_idx'),
            models.Index(fields=['date', 'room'], name='meet_date_room_idx'),
        ]

    def __str__(self):
        return f"Meeting on {self.date} at {self.time}"

class MeetingOrganizer(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, db_index=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('meeting', 'student')

    def __str__(self):
        return f"{self.student.name} organizes {self.meeting}"
