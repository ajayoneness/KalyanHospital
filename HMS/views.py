from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Doctor,patient_table



def signup(request):
    try:
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            uname = (request.POST['username']).lower()
            uname = uname.strip()
            email = (request.POST['email']).lower()
            email = email.strip()
            pass1 = request.POST['password']
            pass2 = request.POST['repassword']

            if pass1 == pass2:
                if User.objects.filter(username=uname).exists():
                    messages.info(request, 'Username Taken')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Taken')

                else:
                    user = User.objects.create_user(username=uname, password=pass1, email=email, first_name=fname,
                                                    last_name=lname)
                    user.save()
                    return redirect('/')
            else:
                messages.info(request, 'both password are not save')
    except:
        messages.info(request, "something Else")

    return render(request,"signup.html")


def login(request):

    if request.method == 'POST':
        uname = (request.POST['username']).lower()
        uname = uname.strip()
        password = request.POST['password']
        user = auth.authenticate(username=uname, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/home")
        else:
            messages.info(request, "invalid user")
            return redirect("/")

    if request.user.is_authenticated:
        return redirect("/home")
    else:
        return render(request,"login.html")



def logout(request):
    auth.logout(request)
    return redirect('/')


def home(request):
    return render(request,"base.html")



def opd(request):

    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        p_name = request.POST.get('p_name')
        p_age = request.POST.get('p_age')
        p_sex = request.POST.get('sex')
        mobile_number = request.POST.get('mobile_number')
        p_address = request.POST.get('p_address')


        patient_table(doctor=Doctor.objects.get(id=doctor),p_name=p_name,p_age=p_age,mobile_number=mobile_number,p_address=p_address, sex=p_sex).save()
        pid = patient_table.objects.all().order_by("-id")[0].id
        return redirect(f'opdbill/{pid}')


    doctor = Doctor.objects.all()
    return render(request,"opd.html",{'doctors':doctor})


def opdbill(request,idd):
    patient = patient_table.objects.get(id=idd)
    return render(request,'opd_bill.html',{'patient':patient})


def patients(request):
    return render(request, 'patients.html')

def doctors(request):
    return render(request, 'doctors.html')



