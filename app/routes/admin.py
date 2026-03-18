from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Pet, User, AdoptionRequest, PetService
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_pets = Pet.query.count()
    total_users = User.query.filter_by(role='user').count()
    pending_requests = AdoptionRequest.query.filter_by(status='pending').count()
    approved_requests = AdoptionRequest.query.filter_by(status='approved').count()
    
    return render_template('admin/dashboard.html', 
                         total_pets=total_pets,
                         total_users=total_users,
                         pending_requests=pending_requests,
                         approved_requests=approved_requests)

@admin.route('/pets')
@login_required
@admin_required
def pets():
    pets = Pet.query.all()
    return render_template('admin/pets.html', pets=pets)

@admin.route('/pets/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_pet():
    if request.method == 'POST':
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        age = request.form.get('age')
        health_status = request.form.get('health_status')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        
        if not all([name, species]):
            flash('Name and species are required', 'error')
            return render_template('admin/add_pet.html')
        
        pet = Pet(
            name=name,
            species=species,
            breed=breed,
            age=int(age) if age else None,
            health_status=health_status,
            description=description,
            image_url=image_url
        )
        
        db.session.add(pet)
        db.session.commit()
        
        flash('Pet added successfully', 'success')
        return redirect(url_for('admin.pets'))
    
    return render_template('admin/add_pet.html')

@admin.route('/pets/edit/<int:pet_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    if request.method == 'POST':
        pet.name = request.form.get('name')
        pet.species = request.form.get('species')
        pet.breed = request.form.get('breed')
        pet.age = int(request.form.get('age')) if request.form.get('age') else None
        pet.health_status = request.form.get('health_status')
        pet.description = request.form.get('description')
        pet.image_url = request.form.get('image_url')
        pet.status = request.form.get('status')
        
        db.session.commit()
        flash('Pet updated successfully', 'success')
        return redirect(url_for('admin.pets'))
    
    return render_template('admin/edit_pet.html', pet=pet)

@admin.route('/pets/delete/<int:pet_id>', methods=['POST'])
@login_required
@admin_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash('Pet deleted successfully', 'success')
    return redirect(url_for('admin.pets'))

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(role='user').all()
    return render_template('admin/users.html', users=users)

@admin.route('/requests')
@login_required
@admin_required
def requests():
    requests = AdoptionRequest.query.order_by(AdoptionRequest.created_at.desc()).all()
    return render_template('admin/requests.html', requests=requests)

@admin.route('/requests/update/<int:request_id>', methods=['POST'])
@login_required
@admin_required
def update_request(request_id):
    adoption_request = AdoptionRequest.query.get_or_404(request_id)
    new_status = request.form.get('status')
    
    if new_status in ['approved', 'rejected']:
        adoption_request.status = new_status
        
        # If approved, update pet status to adopted
        if new_status == 'approved':
            adoption_request.pet.status = 'adopted'
        
        db.session.commit()
        flash(f'Request {new_status} successfully', 'success')
    else:
        flash('Invalid status', 'error')
    
    return redirect(url_for('admin.requests'))

@admin.route('/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    if request.method == 'POST':
        name = request.form.get('name')
        service_type = request.form.get('service_type')
        description = request.form.get('description')
        contact = request.form.get('contact')
        location = request.form.get('location')
        
        if not all([name, service_type]):
            flash('Name and service type are required', 'error')
            return render_template('admin/add_service.html')
        
        service = PetService(
            name=name,
            service_type=service_type,
            description=description,
            contact=contact,
            location=location
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash('Service added successfully', 'success')
        return redirect(url_for('admin.services'))
    
    return render_template('admin/add_service.html')

@admin.route('/services')
@login_required
@admin_required
def services():
    services = PetService.query.all()
    return render_template('admin/services.html', services=services)
