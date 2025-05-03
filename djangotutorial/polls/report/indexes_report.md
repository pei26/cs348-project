# Indexes Report

The following indexes have been added to support fast filtering and lookups in both the
CRUD interfaces and the reporting feature.

| Index Name                         | Table / Columns                    | Supported Query or Report                                                                                      | Code Location                                 | Benefit                                                          |
|------------------------------------|------------------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------|------------------------------------------------------------------|
| `polls_student_name_idx`           | `polls_student(name)`              | `Student.objects.all()`<br>Populating the “Organizers” dropdown in Create/Edit Meeting                            | `views.create_meeting`<br>`views.edit_meeting` | Fast lookup and sorting of students by name                      |
| `polls_club_name_idx`              | `polls_club(name)`                 | `Club.objects.all()`<br>Populating the “Club” dropdown in Create/Edit Meeting and Report                         | `views.create_meeting`<br>`views.meeting_report`| Speeds up retrieval of club list for UI controls                 |
| `polls_room_building_idx`          | `polls_room(building)`             | `Room.objects.all()`<br>Populating the “Room” dropdown in Create/Edit Meeting and Report                         | same as above                                 | Improves filtering rooms by building                             |
| `polls_room_number_idx`            | `polls_room(number)`               | same as above                                                                                                     |                                               | Improves filtering rooms by room number                          |
| `polls_meeting_date_idx`           | `polls_meeting(date)`              | `Meeting.objects.filter(date__range=(start, end))`<br>Raw SQL date-range filter in Report                        | `views.meeting_report`                       | Speeds up date-range filtering in reports                        |
| `polls_meeting_club_id_idx`        | `polls_meeting(club_id)`           | `Meeting.objects.filter(club_id=club_id)`<br>Raw SQL club filter in Report                                       | `views.meeting_report`                       | Speeds up filtering by selected club                             |
| `polls_meeting_room_id_idx`        | `polls_meeting(room_id)`           | `Meeting.objects.filter(room_id=room_id)`<br>Raw SQL room filter in Report                                       | `views.meeting_report`, `views.list_meetings`| Speeds up filtering by selected room                             |
| `meet_date_club_idx`               | `polls_meeting(date, club)`        | Raw SQL combined filter: `WHERE date BETWEEN %s AND %s AND club_id = %s` in Report                               | `views.meeting_report`                       | Optimizes multi‑column filtering on date + club                  |
| `meet_date_room_idx`               | `polls_meeting(date, room)`        | Raw SQL combined filter: `WHERE date BETWEEN %s AND %s AND room_id = %s` in Report                               | `views.meeting_report`                       | Optimizes multi‑column filtering on date + room                  |
| `polls_meetingorganizer_meeting_id_idx` | `polls_meetingorganizer(meeting_id)` | Retrieving all organizers for a meeting (`meeting.meetingorganizer_set.all()`)                                  | `views.meeting_detail`, `views.edit_meeting` | Speeds up lookups of organizers by meeting                       |

---

### Notes

- **ForeignKey Indexes:**  
  Django automatically indexes all foreign-key fields. We’ve also explicitly set `db_index=True` on the model fields above to make our intent clear.

- **Composite Indexes:**  
  The `(date, club)` and `(date, room)` composite indexes are crucial for the performance of the reporting filters when both date-range and club/room are selected.

- **Usage:**  
  After adding these indexes to your `models.py`, run:
  ```bash
  python manage.py makemigrations polls
  python manage.py migrate
