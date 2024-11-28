from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StressParameters
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load the trained model and scaler
MODEL_PATH = 'detection/ml/models/stress_model.h5'
SCALER_PATH = 'detection/ml/models/scaler.pkl'

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def index(request):
    """Home page view"""
    return render(request, 'index.html')

def login_view(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('parameters')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def signup_view(request):
    """Signup view with password validation"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    
    return render(request, 'signup.html')

@login_required
def parameter_entry(request):
    """View to enter stress parameters; requires login"""
    if request.method == 'POST':
        # Retrieve form data
        snoring_rate = request.POST.get('snoring_rate')
        respiratory_rate = request.POST.get('respiratory_rate')
        body_temp = request.POST.get('body_temp')
        limb_movement = request.POST.get('limb_movement')
        blood_oxygen = request.POST.get('blood_oxygen')
        eye_movement = request.POST.get('eye_movement')
        sleep_hours = request.POST.get('sleep_hours')
        heart_rate = request.POST.get('heart_rate')

        # Save the data to the database
        stress_params = StressParameters(
            user=request.user,  # Associate the current user with the entry
            snoring_rate=float(snoring_rate) if snoring_rate else 0,
            respiratory_rate=float(respiratory_rate) if respiratory_rate else 0,
            body_temperature=float(body_temp) if body_temp else 0,
            limb_movement=float(limb_movement) if limb_movement else 0,
            blood_oxygen=float(blood_oxygen) if blood_oxygen else 0,
            eye_movement=float(eye_movement) if eye_movement else 0,
            sleep_hours=float(sleep_hours) if sleep_hours else 0,
            heart_rate=float(heart_rate) if heart_rate else 0,
        )
        stress_params.save()

        # Prepare the input data for prediction
        input_data = [
            stress_params.snoring_rate,
            stress_params.respiratory_rate,
            stress_params.body_temperature,
            stress_params.limb_movement,
            stress_params.blood_oxygen,
            stress_params.eye_movement,
            stress_params.sleep_hours,
            stress_params.heart_rate
        ]
        
        # Normalize and predict stress level using the trained model
        input_data = np.array(input_data).reshape(1, -1)
        scaled_data = scaler.transform(input_data)
        prediction = model.predict(scaled_data)

        # Interpret the result
        if prediction[0][0] > 0.5:  # Assuming sigmoid activation in the output layer
            stress_level = "Detected"
        else:
            stress_level = "Not Detected"

        # Save the predicted stress level to the database
        stress_params.stress_level = stress_level
        stress_params.save()

        # Redirect to results page with stress level as a part of the URL
        return redirect('results', stress_level=stress_level)  # Pass the stress_level as an argument

    return render(request, 'parameter_entry.html')


@login_required
def results(request, stress_level):
    """Results page view"""
    # Get the most recent entry for the logged-in user
    latest_parameters = StressParameters.objects.filter(user=request.user).last()

    # If no parameters are found, display a message
    if not latest_parameters:
        messages.error(request, 'No parameters found for your account.')
        return redirect('parameters')  # Redirect back to parameter entry page if no data

    return render(request, 'results.html', {
        'stress_level': stress_level,  # Use the stress level passed from the URL
        'parameters': latest_parameters
    })


def about(request):
    """About page view"""
    return render(request, 'about.html')

def how_to_use(request):
    """How to use page view"""
    return render(request, 'how_to_use.html')
