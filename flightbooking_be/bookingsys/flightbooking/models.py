from django.db import models
import uuid
from authapp.models import CustomUser
from datetime import datetime

class FlightStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.status_id
    

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)

    def __str__(self):
        return self.location_id
        

class Flight(models.Model):
    flight_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departure_time = models.DateTimeField(default=datetime.now)
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="starting_point")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="ending_point")
    seat_count = models.PositiveIntegerField(default=60)
    booked_seats = models.PositiveIntegerField(default=0)
    flight_status = models.ForeignKey(FlightStatus, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.flight_number)


class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    booking_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.booking_id)