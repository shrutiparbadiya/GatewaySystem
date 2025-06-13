from django.shortcuts import render, redirect
from .models import Vehicle
from .forms import VehicleForm
from django.contrib.auth.decorators import login_required
from .plate_detection_image import plate_detection
from django.contrib.auth import login,  authenticate, logout
from .forms import SignupForm, LoginForm
from django.core.files.storage import default_storage

@login_required
def upload_gate_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        saved_path = default_storage.save('uploads/' + image_file.name, image_file)
        full_path = default_storage.path(saved_path)  # ✅ Get full path for cv2
        message = plate_detection(full_path)      # ✅ Pass correct path
        return render(request, 'gate_status.html', {'message': message})
    return render(request, 'upload_image.html')  # page with upload form


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # This creates the user
            return redirect('login')
            
    else:
        form = SignupForm()
        print(form.errors)
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('vehicle_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def gate_view(request):
    number_plate = detect_number_plate()
    try:
        vehicle = Vehicle.objects.get(number_plate=number_plate)
        message = f"✅ Access granted to {vehicle.owner_name}'s {vehicle.vehicle_type} ({vehicle.number_plate})"
    except Vehicle.DoesNotExist:
        message = f"❌ Vehicle with plate {number_plate} not registered!"
    
    return render(request, 'gate_status.html', {'message': message})

@login_required
def vehicle_register(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicle_register.html', {'form': form})

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

@login_required
def vehicle_delete(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    return redirect('vehicle_list')
