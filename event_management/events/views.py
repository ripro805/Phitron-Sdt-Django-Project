from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import date
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm


# ==================== Category Views ====================

def category_list(request):
    """Display list of all categories"""
    # Optimized: prefetch related events to avoid N+1 queries
    categories = Category.objects.prefetch_related('events').all()
    context = {
        'categories': categories,
        'title': 'Categories'
    }
    return render(request, 'events/category_list.html', context)


def category_detail(request, pk):
    """Display details of a specific category"""
    # Optimized: prefetch events to avoid additional queries
    category = get_object_or_404(Category.objects.prefetch_related('events'), pk=pk)
    events = category.events.all()
    context = {
        'category': category,
        'events': events,
        'title': f'Category: {category.name}'
    }
    return render(request, 'events/category_detail.html', context)


def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('events:category_detail', pk=category.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Create Category',
        'button_text': 'Create Category'
    }
    return render(request, 'events/category_form.html', context)


def category_update(request, pk):
    """Update an existing category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('events:category_detail', pk=category.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': f'Update Category: {category.name}',
        'button_text': 'Update Category'
    }
    return render(request, 'events/category_form.html', context)


def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('events:category_list')
    
    context = {
        'category': category,
        'title': f'Delete Category: {category.name}'
    }
    return render(request, 'events/category_confirm_delete.html', context)


# ==================== Event Views ====================

def event_list(request):
    """Display list of all events with optimized queries, filters, and search"""
    # Optimized: select_related for category (ForeignKey), prefetch_related for participants (ManyToMany)
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants')
    )
    
    # Get filter parameters from GET request
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('search', '').strip()
    
    # Apply search filter (event name or location)
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    
    # Apply category filter
    if category_id:
        events = events.filter(category_id=category_id)
    
    # Apply date range filters
    if start_date:
        events = events.filter(date__gte=start_date)
    
    if end_date:
        events = events.filter(date__lte=end_date)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_id,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'title': 'Events'
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """Display details of a specific event"""
    # Optimized: select_related for category, prefetch_related for participants
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        pk=pk
    )
    context = {
        'event': event,
        'title': event.name
    }
    return render(request, 'events/event_detail.html', context)


def event_create(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('events:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'title': 'Create Event',
        'button_text': 'Create Event'
    }
    return render(request, 'events/event_form.html', context)


def event_update(request, pk):
    """Update an existing event"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect('events:event_detail', pk=event.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'title': f'Update Event: {event.name}',
        'button_text': 'Update Event'
    }
    return render(request, 'events/event_form.html', context)


def event_delete(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Event "{event_name}" deleted successfully!')
        return redirect('events:event_list')
    
    context = {
        'event': event,
        'title': f'Delete Event: {event.name}'
    }
    return render(request, 'events/event_confirm_delete.html', context)


# ==================== Participant Views ====================

def participant_list(request):
    """Display list of all participants"""
    # Optimized: prefetch events to avoid N+1 queries when counting registered events
    participants = Participant.objects.prefetch_related('events').all()
    context = {
        'participants': participants,
        'title': 'Participants'
    }
    return render(request, 'events/participant_list.html', context)


def participant_detail(request, pk):
    """Display details of a specific participant"""
    # Optimized: prefetch events with their categories to avoid N+1 queries
    participant = get_object_or_404(
        Participant.objects.prefetch_related('events__category'),
        pk=pk
    )
    context = {
        'participant': participant,
        'title': participant.name
    }
    return render(request, 'events/participant_detail.html', context)


def participant_create(request):
    """Create a new participant"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.name}" created successfully!')
            return redirect('events:participant_detail', pk=participant.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ParticipantForm()
    
    context = {
        'form': form,
        'title': 'Create Participant',
        'button_text': 'Create Participant'
    }
    return render(request, 'events/participant_form.html', context)


def participant_update(request, pk):
    """Update an existing participant"""
    participant = get_object_or_404(Participant, pk=pk)
    
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.name}" updated successfully!')
            return redirect('events:participant_detail', pk=participant.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ParticipantForm(instance=participant)
    
    context = {
        'form': form,
        'participant': participant,
        'title': f'Update Participant: {participant.name}',
        'button_text': 'Update Participant'
    }
    return render(request, 'events/participant_form.html', context)


def participant_delete(request, pk):
    """Delete a participant"""
    participant = get_object_or_404(Participant, pk=pk)
    
    if request.method == 'POST':
        participant_name = participant.name
        participant.delete()
        messages.success(request, f'Participant "{participant_name}" deleted successfully!')
        return redirect('events:participant_list')
    
    context = {
        'participant': participant,
        'title': f'Delete Participant: {participant.name}'
    }
    return render(request, 'events/participant_confirm_delete.html', context)


# ==================== Home View (Dashboard) ====================

def home(request):
    """Dashboard with statistics and filtered event list"""
    
    # Get filter parameter from request.GET (default: 'today')
    filter_param = request.GET.get('filter', 'today')
    
    # Get today's date
    today = date.today()
    
    # Calculate overall statistics
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    
    # Calculate upcoming and past events counts
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    
    # Optimized: Base queryset with select_related for ForeignKey and prefetch_related for ManyToMany
    base_queryset = Event.objects.select_related('category').prefetch_related('participants')
    
    # Filter events based on the filter parameter
    if filter_param == 'today':
        # Events happening today
        events = base_queryset.filter(date=today).order_by('time')
        filter_label = "Today's Events"
    elif filter_param == 'upcoming':
        # Events from today onwards (including today)
        events = base_queryset.filter(date__gte=today).order_by('date', 'time')
        filter_label = "Upcoming Events"
    elif filter_param == 'past':
        # Events before today
        events = base_queryset.filter(date__lt=today).order_by('-date', '-time')
        filter_label = "Past Events"
    elif filter_param == 'all':
        # All events
        events = base_queryset.all().order_by('-date', '-time')
        filter_label = "All Events"
    else:
        # Default to today if invalid filter
        events = base_queryset.filter(date=today).order_by('time')
        filter_label = "Today's Events"
        filter_param = 'today'
    
    # Annotate events with participant count
    events = events.annotate(participant_count=Count('participants'))
    
    # Get recent categories
    recent_categories = Category.objects.all()[:5]
    
    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'events': events,
        'filter_param': filter_param,
        'filter_label': filter_label,
        'recent_categories': recent_categories,
        'title': 'Dashboard - Event Management System'
    }
    return render(request, 'events/home.html', context)
