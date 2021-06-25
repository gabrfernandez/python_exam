from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job
import bcrypt

def show_login_reg_page(request):
    return render (request, "index.html")

def register_form(request):
    errors=User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, err in errors.items():
            messages.error(request, err)
        return redirect("/")
        
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    created_user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
    )

    request.session["user_id"]=created_user.id
    request.session["first_name"]=created_user.first_name # inserted

    return redirect("/dashboard")

def show_dashboard(request):

    if "user_id" not in request.session:
        messages.error(request, "Please login or register first.")
        return redirect("/")

    context={
        "user":User.objects.get(id=request.session["user_id"]),
        "jobs":Job.objects.all()
    }
    return render(request, "dashboard.html", context)


def login_form(request):

    potential_users=User.objects.filter(email=request.POST['email'])
    
    if len(potential_users)==0:
        messages.error(request, "Please check your email and password.")

        return redirect("/")

    user=potential_users[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password.")

        return redirect("/")

    request.session["user_id"]=user.id
    request.session["first_name"]=user.first_name #inserted
    return redirect ("/dashboard")


def logout(request):
    request.session.pop("user_id")
    request.session.pop("first_name")

    return redirect("/")

def create_job(request):

    context={
        "user":User.objects.get(id=request.session["user_id"]),
    }
    return render(request, "create-job.html" , context)

def create_job_form(request,):
    errors = Job.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect ("/createjob")
    
    Job.objects.create(
        title=request.POST['title'],
        description=request.POST['description'],
        location=request.POST['location'],
        category=request.POST['category'],
        user = User.objects.get(id=request.session['user_id'])
    )

    return redirect("/dashboard")

def job_profile(request, job_id):
    context={
        "job":Job.objects.get(id=job_id),
        "user":User.objects.get(id=request.session["user_id"]),
    }

    return render(request, "job-profile.html", context)

def edit_job_page(request, job_id):
    context={
        "job":Job.objects.get(id=job_id),
        "user":User.objects.get(id=request.session["user_id"]),
    }

    return render (request, "edit-job.html", context)

def update (request, job_id):
    errors=Job.objects.basic_validator(request.POST)

    if len(errors)>0:
        for error in errors.values():
            messages.error(request, error)
        return redirect(f"/jobs/edit/{job_id}")
        

    newjob=Job.objects.get(id=job_id)
    newjob.title=request.POST['title']
    newjob.description=request.POST['description']
    newjob.location=request.POST['location']

    newjob.save()

    return redirect("/dashboard")

def delete(request, job_id):
    job=Job.objects.get(id=job_id)
    job.delete()

    return redirect("/dashboard")







