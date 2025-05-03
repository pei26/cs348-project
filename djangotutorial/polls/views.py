from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Meeting, Student
from .forms import MeetingForm
from django.db import connection
from .models import Meeting, Club, Room
import datetime

def index(request):
    return render(request, 'polls/index.html')

def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                meeting = form.save()
                # Retrieve selected organizers (assumes your template sends a list of student IDs)
                organizers_ids = request.POST.getlist('organizers')
                for stud_id in organizers_ids:
                    meeting.meetingorganizer_set.create(student_id=stud_id)
            return redirect('meeting_detail', meeting_id=meeting.id)
    else:
        form = MeetingForm()
    # Get students for the organizer selection dropdown
    students = Student.objects.all()
    return render(request, 'polls/meeting_form.html', {'form': form, 'students': students})

def meeting_detail(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    organizers = meeting.meetingorganizer_set.all()
    return render(request, 'polls/meeting_detail.html', {'meeting': meeting, 'organizers': organizers})

def meeting_report(request):
    # Retrieve filter parameters from GET request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    club_id = request.GET.get('club')
    room_id = request.GET.get('room')
    
    filters = {}
    if start_date and end_date:
        filters['date__range'] = (start_date, end_date)
    if club_id:
        filters['club_id'] = club_id
    if room_id:
        filters['room_id'] = room_id
    
    meetings = Meeting.objects.filter(**filters)
    
    # Example of a prepared statement to get basic statistics:
    stats = None
    if start_date and end_date:
        with connection.cursor() as cursor:
            query = """
                SELECT AVG(duration) AS avg_duration,
                       AVG(invited_count) AS avg_invited,
                       AVG(accepted_count) AS avg_accepted
                FROM polls_meeting
                WHERE date BETWEEN %s AND %s
            """
            params = [start_date, end_date]
            if club_id:
                query += " AND club_id = %s"
                params.append(club_id)
            if room_id:
                query += " AND room_id = %s"
                params.append(room_id)
            cursor.execute(query, params)
            stats = cursor.fetchone()
    if stats and stats[0] is not None:
        avg_microseconds = stats[0]  # average duration in microseconds
        # Convert microseconds to a timedelta
        avg_timedelta = datetime.timedelta(microseconds=avg_microseconds)
        # Format the timedelta as HH:MM:SS
        formatted_duration = str(avg_timedelta)
    
    clubs = Club.objects.all()
    rooms = Room.objects.all()
    return render(request, 'polls/report.html', {
        'meetings': meetings,
        'stats': stats,
        'clubs': clubs,
        'rooms': rooms,
        'start_date': start_date,
        'end_date': end_date,
        'selected_club': club_id,
        'selected_room': room_id
    })

def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            with transaction.atomic():
                meeting = form.save()
                meeting.meetingorganizer_set.all().delete()
                organizers_ids = request.POST.getlist('organizers')
                for stud_id in organizers_ids:
                    meeting.meetingorganizer_set.create(student_id=stud_id)
            return redirect('meeting_detail', meeting_id=meeting.id)
    else:
        form = MeetingForm(instance=meeting)
    
    students = Student.objects.all()
    selected_organizers = meeting.meetingorganizer_set.values_list('student_id', flat=True)
    
    return render(request, 'polls/edit_meeting.html', {
        'form': form,
        'students': students,
        'selected_organizers': selected_organizers,
        'meeting': meeting
    })

def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        meeting.delete()
        return redirect('list_meetings')
    return render(request, 'polls/delete_meeting.html', {'meeting': meeting})

def list_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'polls/meeting_list.html', {'meetings': meetings})