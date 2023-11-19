from django.shortcuts import render, redirect
from .models import Count
from .forms import AddCountForm, CountEntryForm, CountUploadForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import pandas as pd
from django.db.models import F, Q
from django.utils import timezone
from django.contrib.auth.decorators import permission_required, user_passes_test
import csv
from collections import defaultdict
from django.db import transaction

PENDING_COUNT = 'Pending Count'
PENDING_REVIEW = 'Pending Review'
COMPLETED = 'Completed'

def check_permission(user, group_names):
    return user.is_authenticated and user.groups.filter(Q(name__in=group_names)).exists()

def redirect_to_home(request):
    redirect_to_home(request)

def home(request):
    return render(request, 'imx_home.html')

def view_counting(request):
    if request.user.is_authenticated:
        counts = Count.objects.filter(status=PENDING_COUNT)
        return render(request, 'imx_counting.html', {"counts": counts})
    else:
        redirect_to_home(request)
    
def generate_counts(request):
    if request.user.is_authenticated:
        if not check_permission(request.user, ['IC Clerk', 'IC Manager']):
            messages.error(request, "You do not have permission to access this page.")
            return render(request, 'imx_counting.html')
        if request.method == "POST":
            form_upload = CountUploadForm(request.POST, request.FILES)
            form_manual = AddCountForm(request.POST, user=request.user)

            if 'file' in request.FILES:
                # Handle file upload
                if form_upload.is_valid():
                    uploaded_file = request.FILES['file']
                    if uploaded_file.name.endswith(('.xls', '.xlsx')):
                        df = pd.read_excel(uploaded_file)
                        records = []

                        for index, row in df.iterrows():
                            record = Count(
                                tag=row['Tag'],
                                name=row['Item'],
                                subinv=row['Subinventory'],
                                location=row['Locator'],
                                uom=row['UOM'],
                                quantity=row['Qty'],
                                created_by=request.user,
                                status=PENDING_COUNT
                            )

                            records.append(record)

                        Count.objects.bulk_create(records)

                        messages.success(request, f"{len(records)} records created successfully")
                    else:
                        messages.error(request, "Invalid file format. Please upload a CSV or Excel file.")
            elif form_manual.is_valid():
                form_manual.save()
                messages.success(request, "Count/s generated successfully")

        form_upload = CountUploadForm()
        form_manual = AddCountForm(user=request.user)
    else:
        redirect_to_home(request)

    return render(request, 'imx_generate_counts.html', {"form_upload": form_upload, "form_manual": form_manual})

def review_counts(request):
    if request.user.is_authenticated:
        if not check_permission(request.user, ['IC Clerk', 'IC Manager']):
            messages.error(request, "You do not have permission to access this page.")
            return render(request, 'imx_counting.html') 
        counts = Count.objects.all()
        return render(request, 'imx_review_counts.html', {'counts': counts})
    else:
        redirect_to_home(request)
    
def review_counts_filtered(request, filter):
    if filter == 'all':
        counts = Count.objects.all()
    elif filter == 'pending_count':
        counts = Count.objects.filter(status=PENDING_COUNT)
    elif filter == 'pending_review':
        counts = Count.objects.filter(status=PENDING_REVIEW)
    elif filter == 'completed':
        counts = Count.objects.filter(status=COMPLETED)
    else:
        # Handle the case when an invalid filter value is provided.
        # You can return an empty queryset or handle it differently as needed.
        counts = Count.objects.none()  # This will result in an empty queryset.

    return render(request, 'imx_review_counts.html', {'counts': counts})

def get_next_pending_count(pk):
    try:
        next_count = Count.objects.filter(status='Pending Count', pk__gt=pk).order_by('pk').first()
        print("Counts found!")
        return next_count
    except Count.DoesNotExist:
        print("No Counts!")
        return None

def count_detail(request, pk):
    if not check_permission(request.user, ['IC Counter', 'IC Clerk', 'IC Manager']):
        messages.error(request, "You do not have permission to access this page.")
        return render(request, 'imx_counting.html') 

    try:
        count = Count.objects.get(pk=pk, status='Pending Count')
    except Count.DoesNotExist:
        return JsonResponse({'count_found': False})

    # Assuming the tag has the format "COLL-001", split it at the "-" to get the group key
    group_key = count.tag.split("-")[0]

    # Retrieve all counts with the same group key
    counts_in_group = Count.objects.filter(tag__startswith=group_key, status='Pending Count')

    count_entry_form = CountEntryForm(request.POST or None)

    if request.method == 'POST':
        if count_entry_form.is_valid():
            location = count_entry_form.cleaned_data['location']
            value = count_entry_form.cleaned_data['value']

            if location == count.location:
                if count.first_count is None:
                    count.first_count = value
                elif count.second_count is None:
                    count.second_count = value
                elif count.third_count is None:
                    count.third_count = value
                elif count.fourth_count is None:
                    count.fourth_count = value
                elif count.fifth_count is None:
                    count.fifth_count = value

                count.status = PENDING_REVIEW
                count.modified_by = request.user

                count.save()

                # Find the next count within the same group
                next_count = counts_in_group.filter(pk__gt=pk).order_by('pk').first()

                if next_count:
                    return redirect('count_detail', pk=next_count.pk)
                else:
                    messages.success(request, "No more counts in this batch.")
                    return render(request, 'imx/imx_counting.html', {"count": count})

    previous_count = counts_in_group.filter(pk__lt=pk).order_by('-pk').first()
    next_count = counts_in_group.filter(pk__gt=pk).order_by('pk').first()

    return render(request, 'imx_count_entry.html', {'count': count, 'previous_count': previous_count, 'next_count': next_count, 'count_entry_form': count_entry_form})

def count_approval(request, pk):
    if request.user.is_authenticated:
        if not check_permission(request.user, ['IC Manager', 'IC Clerk']):
            messages.error(request, "You do not have permission to access this page.")
            return render(request, 'imx_counting.html') 
        count_record = Count.objects.get(id=pk)
        count_history = count_record.history.all()  # Retrieve all historical versions
        return render(request, 'imx_count_approval.html', {'count_record': count_record, 'count_history': count_history})
    
    else:
        redirect_to_home(request)
    
def approve_count(request, pk):
    if request.user.is_authenticated:
        count = Count.objects.get(id=pk)
        count.status = COMPLETED
        count.modified_by = request.user
        count.save()

        messages.success(request, "Count completed successfully")
        return redirect('review_counts')
    else:
        redirect_to_home(request)
    
def initiate_recount(request, pk):
    if request.user.is_authenticated:
        count = Count.objects.get(id=pk)
        count.status = PENDING_COUNT
        count.modified_by = request.user
        count.save()

        messages.success(request, "Status updated successfully")
        return redirect('review_counts')
    else:
        redirect_to_home(request)
    
def export_data(request):
    data = Count.objects.all()

    # Create an HTTP response with the appropriate content type for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    # Create a CSV writer and write the data to the response
    writer = csv.writer(response)
    writer.writerow(['Name', 'Quantity'])  # CSV header row

    for item in data:
        writer.writerow(item['name'], item['quantity'])

    return response