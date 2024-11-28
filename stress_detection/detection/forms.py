from django import forms

class StressPredictionForm(forms.Form):
    snoring_rate = forms.FloatField(label="Snoring Rate", min_value=0.0)
    respiratory_rate = forms.FloatField(label="Respiratory Rate", min_value=0.0)
    body_temperature = forms.FloatField(label="Body Temperature", min_value=30.0, max_value=40.0)
    limb_movement = forms.FloatField(label="Limb Movement", min_value=0.0)
    blood_oxygen = forms.FloatField(label="Blood Oxygen", min_value=0.0, max_value=100.0)
    eye_movement = forms.FloatField(label="Eye Movement", min_value=0.0)
    sleep_hours = forms.FloatField(label="Sleep Hours", min_value=0.0, max_value=24.0)
    heart_rate = forms.FloatField(label="Heart Rate", min_value=0.0)

