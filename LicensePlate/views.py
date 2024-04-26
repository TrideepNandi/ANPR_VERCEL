from django.shortcuts import render
from django.http import JsonResponse
from .models import LicensePlate, Record
from django.views import View

class CheckAndAddRecordView(View):
    def post(self, request, *args, **kwargs):
        license_plate_text = request.POST.get('license_plate_text')
        date = request.POST.get('date')
        time = request.POST.get('time')
        image = request.FILES.get('image')

        try:
            license_plate = LicensePlate.objects.get(license_plate_text=license_plate_text)
            Record.objects.create(license_plate=license_plate, date=date, time=time, image=image)
            return JsonResponse({'message': 'Record added successfully'})
        except LicensePlate.DoesNotExist:
            return JsonResponse({'message': 'License plate not found'}, status=404)