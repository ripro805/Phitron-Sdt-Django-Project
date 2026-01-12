from django.db import models


class Category(models.Model):
    """Model representing an event category"""
    name = models.CharField(max_length=100, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """Model representing an event"""
    name = models.CharField(max_length=200, verbose_name="Event Name")
    description = models.TextField(verbose_name="Event Description")
    date = models.DateField(verbose_name="Event Date")
    time = models.TimeField(verbose_name="Event Time")
    location = models.CharField(max_length=300, verbose_name="Location")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="events",
        verbose_name="Category"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-date', '-time']
    
    def __str__(self):
        return f"{self.name} - {self.date}"


class Participant(models.Model):
    """Model representing an event participant"""
    name = models.CharField(max_length=200, verbose_name="Participant Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    events = models.ManyToManyField(
        Event, 
        related_name="participants",
        verbose_name="Registered Events",
        blank=True
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.email})"
