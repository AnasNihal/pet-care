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
    
    if request.method == 'POST':
        # Check if user already has a pending request for this pet
        existing_request = AdoptionRequest.query.filter_by(
            user_id=current_user.id, 
            pet_id=pet.id, 
            status='pending'
        ).first()
        
        if existing_request:
            flash('You already have a pending adoption request for this pet.', 'error')
            return redirect(url_for('user.pet_detail', pet_id=pet.id))
        
        # Create new adoption request
        adoption_request = AdoptionRequest(
            user_id=current_user.id,
            pet_id=pet.id,
            message=request.form.get('message', ''),
            status='pending'
        )
        
        db.session.add(adoption_request)
        db.session.commit()
        
        flash('Your adoption request has been submitted successfully!', 'success')
        return redirect(url_for('user.my_requests'))
    
    return render_template('user/adopt_pet.html', pet=pet)

@user.route('/requests')
@login_required
def my_requests():
    requests = AdoptionRequest.query.filter_by(user_id=current_user.id).order_by(AdoptionRequest.created_at.desc()).all()
    return render_template('user/my_requests.html', requests=requests)

@user.route('/services')
@login_required
def services():
    services = PetService.query.all()
    return render_template('user/services.html', services=services)

@user.route('/profile')
@login_required
def profile():
    requests = AdoptionRequest.query.filter_by(user_id=current_user.id).order_by(AdoptionRequest.created_at.desc()).all()
    return render_template('user/profile.html', requests=requests)

@user.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Update name and email
        current_user.name = request.form.get('name', current_user.name)
        current_user.email = request.form.get('email', current_user.email)
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
