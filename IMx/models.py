from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
    
class Count(models.Model):
    PENDING_COUNT = 'Pending Count'
    PENDING_REVIEW = 'Pending Review'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING_COUNT, 'Pending Count'),
        (PENDING_REVIEW, 'Pending Review'),
        (COMPLETED, 'Completed'),
    ]
    
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    subinv = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Pending Count")
    first_count = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    second_count = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    third_count = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    fourth_count = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    fifth_count = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='counts_modified')
    last_modified = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_counts')
    locked = models.BooleanField(default=False)


    history = HistoricalRecords()

    def __str__(self):
        return(f"{self.tag} {self.name} {self.quantity} {self.status}")
    
    def save(self, *args, **kwargs):
        # Update the 'last_modified' field with the current timestamp
        self.last_modified = timezone.now()
        super(Count, self).save(*args, **kwargs)