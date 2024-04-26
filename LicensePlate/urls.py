from django.urls import path
from .views import CheckAndAddRecordView

urlpatterns = [
    path('check_and_add_record/', CheckAndAddRecordView.as_view(), name='check_and_add_record'),
]