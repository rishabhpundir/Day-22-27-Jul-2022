from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from ClubApp.models import Event
from templates.event_form import EventForm
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.

# Displaying all events on the homepage
def home(request):
    logged_out = None
    login_success = None
    event_deleted = None
    registered = None
    events_list = Event.objects.all().order_by('event_name')
    if 'login_success' in request.GET:
        login_success = True

    if "logged_out" in request.GET:
        logged_out = True

    if "event_deleted" in request.GET:
        event_deleted = True

    if "registered" in request.GET:
        registered = True
        
    return render(request, 'home.html', {'events':events_list, 'login_success':login_success, 'logged_out': logged_out, 'event_deleted': event_deleted, 'registered':registered})

# Add a new event to Database using Django Form 
def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/AddEvent?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_event.html', {'form':form, 'submitted':submitted})

# Get event details on a different page
def event_details(request, event_id):
    updated = False
    event = Event.objects.get(pk=event_id)
    if 'updated' in request.GET:
            updated = True
    return render(request, 'event_details.html', {'event': event, 'updated':updated})

# Search events by event names through the search bar
def search(request):
    if request.method == "POST":
        search_query = request.POST['search-bar']
        events = Event.objects.filter(event_name__contains=search_query)
        return render(request, 'search.html', {'search_query':search_query, 'events': events})
    else:
        return render(request, 'search.html', {})

# Update an existing event by editing its DB entry through Django Form
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    updated = False
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(f'/EventDetails/{event_id}?updated=True')
    return render(request, 'update_event.html', {'event': event, 'form': form})

# Delete an event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponseRedirect('/?event_deleted=True')

# Generate a txt file that has all events info
def gen_events_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=EventsList.txt'

    # Designate the Event model and loop through the DB objects (data)
    events = Event.objects.all()
    events_list = []
    for event in events:
        events_list.append(f"{event.event_name}, {event.event_date}, {event.venue}, {event.event_manager}, {event.description}, ,  ------------------------------------------------, , ")

    #Write To TextFile
    response.writelines(events_list)
    return response 

# Generate a CSV file that has all events info
def gen_events_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=EventsList.csv'

    # Create a CSV writer
    csv_writer = csv.writer(response)
    # Designate the Event model to loop through the DB objects (data)
    events = Event.objects.all()

    # Add CSV column headings
    csv_writer.writerow(["Event Name", "Event Date", "Venue", "Event Manager", "Description"])

    # Loop through Data and write To CSVFile
    for event in events:
        csv_writer.writerow([event.event_name, event.event_date, event.venue, event.event_manager, event.description])

    return response

# Generate a PDF file that has all events info
def gen_events_pdf(request):
    # Create a Byte stream buffer
    buffer = io.BytesIO()
    can = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    # Create a text object
    txt_obj = can.beginText()
    txt_obj.setTextOrigin(inch, inch)
    txt_obj.setFont('Helvetica', 12)

    # Designate the Event model and loop through the DB objects (data)
    events = Event.objects.all()

    # Loop through Data and write To PDFFile
    events_list = []
    for event in events:
        events_list.append(f"Event Name : {event.event_name}")
        events_list.append(f"Event Date : {event.event_date}")
        events_list.append(f"Venue : {event.venue}")
        events_list.append(f"Event Manager : {event.event_manager}")
        events_list.append(" ")
        events_list.append("------------------------------------------------")
        events_list.append(" ")

    for line in events_list:
        txt_obj.textLine(line)

    # Finish up saving file
    can.drawText(txt_obj)
    can.showPage()
    can.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='EventsList.pdf')
