from django import forms
from .models import Category, Event, Participant


class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter category description (optional)',
                'rows': 4
            }),
        }
    
    def clean_name(self):
        """Validate category name"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 3:
                raise forms.ValidationError('Category name must be at least 3 characters long.')
        return name


class EventForm(forms.ModelForm):
    """Form for creating and updating events"""
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter event name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter event description',
                'rows': 5
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter event location'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
        }
    
    def clean_name(self):
        """Validate event name"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 5:
                raise forms.ValidationError('Event name must be at least 5 characters long.')
        return name
    
    def clean_description(self):
        """Validate event description"""
        description = self.cleaned_data.get('description')
        if description:
            description = description.strip()
            if len(description) < 10:
                raise forms.ValidationError('Event description must be at least 10 characters long.')
        return description
    
    def clean_location(self):
        """Validate event location"""
        location = self.cleaned_data.get('location')
        if location:
            location = location.strip()
            if len(location) < 3:
                raise forms.ValidationError('Location must be at least 3 characters long.')
        return location


class ParticipantForm(forms.ModelForm):
    """Form for creating and updating participants"""
    
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter participant name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter email address'
            }),
            'events': forms.CheckboxSelectMultiple(attrs={
                'class': 'mr-2'
            }),
        }
    
    def clean_name(self):
        """Validate participant name"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 3:
                raise forms.ValidationError('Participant name must be at least 3 characters long.')
        return name
    
    def clean_email(self):
        """Validate email address"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            # Check if email already exists (for new participants)
            if not self.instance.pk:
                if Participant.objects.filter(email=email).exists():
                    raise forms.ValidationError('A participant with this email already exists.')
        return email
