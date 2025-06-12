from django.db import models
from django.contrib.auth.models import User

class StressParameters(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Now, the field is non-nullable
    snoring_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    body_temperature = models.FloatField()
    limb_movement = models.FloatField()
    blood_oxygen = models.FloatField()
    eye_movement = models.FloatField()
    sleep_hours = models.FloatField()
    heart_rate = models.FloatField()
    stress_level = models.CharField(max_length=50, null=True, blank=True)  # Optional field for predicted stress level

    def __str__(self):
        return f"StressParameters ID {self.id} for {self.user.username}"  # Display an identifier with the username in the admin panel
