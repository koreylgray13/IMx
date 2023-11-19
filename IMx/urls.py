# 'IMx' app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='imx_home'),
    # Add other URL patterns for the 'IMx' app

    path('counting/', views.view_counting, name='view_counting'),
    path('counting/generate_counts/', views.generate_counts, name='generate_counts'),
    path('counting/review_counts/', views.review_counts, name='review_counts'),
    path('counting/review_counts/<str:filter>/', views.review_counts_filtered, name='review_counts_filtered'),
    path('counting/count_detail/<int:pk>/', views.count_detail, name='count_detail'),
    path('counting/count_approval/<int:pk>/', views.count_approval, name='count_approval'),
    path('counting/approve_count/<int:pk>/', views.approve_count, name='approve_count'),
    path('counting/initiate_recount/<int:pk>/', views.initiate_recount, name='initiate_recount'),
    path('counting/export_data/', views.export_data, name='export_data'),
]