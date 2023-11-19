from django import forms
from .models import Count

class AddCountForm(forms.ModelForm):
    COUNT_STATUS_CHOICES = [
        ("Pending Count", "Pending Count"),
        ("Pending Review", "Pending Review"),
        ("Completed", "Completed"),
    ]
    
    tag = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Tag #", "class":"form-control"}), label="")
    name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Item Name", "class":"form-control"}), label="")
    subinv = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Subinventory", "class":"form-control"}), label="")
    location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Location", "class":"form-control"}), label="")
    uom = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "UOM", "class":"form-control"}), label="")
    quantity = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Quantity", "class":"form-control"}), label="")
    status = forms.ChoiceField(required=False, choices=COUNT_STATUS_CHOICES, widget=forms.Select(attrs={"class": "form-control"}), label="")

    class Meta:
        model = Count
        exclude = ('modified_by', 'created_by', 'first_count', 'second_count', 'third_count', 'fourth_count', 'fifth_count', 'assigned_to', 'locked')

    def __init__(self, *args, **kwargs):
        # Get the user from the keyword arguments
        user = kwargs.pop('user', None)
        super(AddCountForm, self).__init__(*args, **kwargs)

        # Store the user as an instance variable
        self.user = user

    def save(self, commit=True):
        instance = super(AddCountForm, self).save(commit=False)
        # Set the 'created_by' field to the current user
        instance.created_by = self.user
        instance.modified_by = self.user
        if commit:
            instance.save()
        return instance

class CountEntryForm(forms.Form):
    location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "", "class":"form-control-sm"}), label="")
    value = forms.DecimalField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "", "class":"form-control-sm"}), label="")

class CountUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
    )