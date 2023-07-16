from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Doctor,patient_table,LAB,Patient_LAB
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




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
            return redirect("/opd")
        else:
            messages.info(request, "invalid user")
            return redirect("/")

    if request.user.is_authenticated:
        return redirect("/opd")
    else:
        return render(request,"login.html")



def logout(request):
    auth.logout(request)
    return redirect('/')


# def home(request):
#     return render(request,"base.html")



def opd(request):

    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        oe = request.POST.get('oe')
        p_name = request.POST.get('p_name').lower()
        p_age = request.POST.get('p_age')
        p_sex = request.POST.get('sex')
        mobile_number = request.POST.get('mobile_number')
        p_address = request.POST.get('p_address').lower()


        patient_table(doctor=Doctor.objects.get(id=doctor),oe=oe,p_name=p_name,p_age=p_age,mobile_number=mobile_number,p_address=p_address, sex=p_sex).save()
        pid = patient_table.objects.all().order_by("-id")[0].id
        return redirect(f'opdbill/{pid}')


    doctor = Doctor.objects.all()
    return render(request,"opd.html",{'doctors':doctor})


def opdbill(request,idd):
    patient = patient_table.objects.get(id=idd)
    return render(request,'opd_bill.html',{'patient':patient})


def patients(request):

    if request.method == "POST":
        search = request.POST['search']
        try:
            ss = int(search)
            if len(str(ss)) < 10:
                print(ss)
                p=patient_table.objects.filter(id=int(ss))
                print(p)
            else:
                p=patient_table.objects.filter(mobile_number__icontains=ss)
        except:
            p=patient_table.objects.filter(p_name__icontains=search)
        return render(request, 'patients.html', {'patients': p})


    patient = patient_table.objects.all().order_by("-id")
    return render(request, 'patients.html',{'patients':patient})


def doctors(request):
    if request.method == "POST":
        search = request.POST['search']
        try:
            ss = int(search)
            if len(str(ss)) < 10:
                d=Doctor.objects.filter(id=int(ss))
            else:
                d=Doctor.objects.filter(contact_number__icontains=ss)
        except:
            d = Doctor.objects.filter(first_name__icontains = search)

        return render(request, 'doctors.html', {'doctors': d})
    doctor = Doctor.objects.all().order_by("-id")
    return render(request, 'doctors.html',{'doctors':doctor})


def lab(request):
    if request.POST:
        search = request.POST['search']
        try:
            pp = patient_table.objects.get(id=int(search))
            return render(request, 'labs.html',{'patient':pp})
        except:
            message = "patient is not found!!! "
            return render(request, 'labs.html', {'message': message})

    message = "Welcome to Lab 😍"
    return render(request,'labs.html',{'message': message})


# API PART

@csrf_exempt
def lab_search_api(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        labs = LAB.objects.filter(lab_name__icontains=search_query).values('id','lab_name', 'lab_price')
        results = list(labs)
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


@csrf_exempt
def patient_lab_api(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id', None)
        labs = request.POST.get('labs', None)

        if patient_id is None or labs is None:
            return JsonResponse({'error': 'Missing patient_id or labs'}, status=400)

        try:
            patient_lab = Patient_LAB(patient_id=patient_id, labs=labs)
            patient_lab.save()
            return JsonResponse({'success': 'Patient_LAB record created'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def testBill(request):
    import json
    p_lab = Patient_LAB.objects.all().order_by("-id")[0]
    jsondata = p_lab.labs
    data = json.loads(jsondata)
    array = []
    t_price = 0
    for i in data['labs']:
        array.append(LAB.objects.get(id=i))
        t_price = t_price + int(LAB.objects.get(id=i).lab_price)

    return render(request,"testbill.html",{'pl':p_lab,'labs':array,'tprice':t_price})


def labresult(request):
    return render(request,'labresult.html')