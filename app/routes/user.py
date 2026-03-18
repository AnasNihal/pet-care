from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Pet, AdoptionRequest, PetService
from app import db

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/dashboard')
@login_required
def dashboard():
    pets = Pet.query.filter_by(status='available').all()
    return render_template('user/dashboard.html', pets=pets)

@user.route('/pet/<int:pet_id>')
@login_required
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('user/pet_detail.html', pet=pet)

@user.route('/adopt/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def adopt_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if pet is available
    if pet.status != 'available':
        flash('This pet is no longer available for adoption', 'error')
        return redirect(url_for('user.dashboard'))
    
    # Check if user has already applied for this pet
    existing_request = AdoptionRequest.query.filter_by(
        user_id=current_user.id, 
        pet_id=pet_id
    ).first()
    
    if existing_request:
        flash('You have already submitted an adoption request for this pet', 'error')
        return redirect(url_for('user.my_requests'))
    
    if request.method == 'POST':
        message = request.form.get('message')
        
        if not message:
            flash('Please provide a message explaining why you want to adopt this pet', 'error')
            return render_template('user/adopt_pet.html', pet=pet)
        
        # Create adoption request
        adoption_request = AdoptionRequest(
            user_id=current_user.id,
            pet_id=pet_id,
            message=message,
            status='pending'
        )
        
        db.session.add(adoption_request)
        db.session.commit()
        
        flash('Your adoption request has been submitted successfully!', 'success')
        return redirect(url_for('user.my_requests'))
    
    return render_template('user/adopt_pet.html', pet=pet)

@user.route('/my-requests')
@login_required
def my_requests():
    requests = AdoptionRequest.query.filter_by(user_id=current_user.id).order_by(
        AdoptionRequest.created_at.desc()
    ).all()
    return render_template('user/my_requests.html', requests=requests)

@user.route('/services')
@login_required
def services():
    services = PetService.query.all()
    return render_template('user/services.html', services=services)
