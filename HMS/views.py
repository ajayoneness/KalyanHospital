from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Doctor,patient_table,LAB,Patient_LAB,OtherCharges,Patient_OtherCharges,LabCategory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from decimal import Decimal





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
            admincode = request.POST['admin-code']
            if admincode == "2263262":
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
            else:
                messages.info(request, 'Contact to Developer')
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

    if request.user.is_authenticated:
        doctor = Doctor.objects.all()
        return render(request,"opd.html",{'doctors':doctor})
    else:
        return render(request,"login.html")



def opdbill(request,idd):
    if request.user.is_authenticated:
        patient = patient_table.objects.get(id=idd)
        return render(request,'opd_bill.html',{'patient':patient})
    else:
        return render(request,"login.html")



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

    if request.user.is_authenticated:
        patient = patient_table.objects.all().order_by("-id")
        return render(request, 'patients.html',{'patients':patient})
    else:
        return render(request,"login.html")




# def patientDetails(request,pid):
#     patient = patient_table.object.filter(id=pid)
#     return render(request,'patientDetails.html',patient)



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

    if request.user.is_authenticated:
        doctor = Doctor.objects.all().order_by("-id")
        return render(request, 'doctors.html',{'doctors':doctor})
    else:
        return render(request,"login.html")



def lab(request):
    if request.POST:
        search = request.POST['search']
        try:
            pp = patient_table.objects.get(id=int(search))
            return render(request, 'labs.html',{'patient':pp})
        except:
            message = "patient is not found!!! "
            return render(request, 'labs.html', {'message': message})

    if request.user.is_authenticated:
        message = "Welcome to Lab 😍"
        return render(request,'labs.html',{'message': message})
    else:
        return render(request,"login.html")






# API PART


#Other Charge Part Started
@csrf_exempt
def other_charges_api(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        oc = OtherCharges.objects.filter(oc_name__icontains=search_query).values('id','oc_name', 'oc_price')
        results = list(oc)
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)




@csrf_exempt
def create_patient_othercharges(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient_id = data.get('patientid')
        othercharge_id = data.get('otherchargeId')
        quantity = data.get('quantity', 1)  # Default quantity to 1 if not provided in the request data

        try:
            patient = patient_table.objects.get(pk=patient_id)
            othercharge = OtherCharges.objects.get(pk=othercharge_id)
        except (patient_table.DoesNotExist, OtherCharges.DoesNotExist):
            return JsonResponse({'error': 'Invalid patientid or otherchargeId.'}, status=400)

        try:
            patient_other_charges = Patient_OtherCharges.objects.get(patient=patient, othercharge=othercharge)
            # If the entry for the same patient and othercharge already exists, update the quantity
            patient_other_charges.quantity = quantity
            patient_other_charges.save()
        except Patient_OtherCharges.DoesNotExist:
            # If the entry does not exist, create a new one with the provided quantity
            Patient_OtherCharges.objects.create(patient=patient, othercharge=othercharge, quantity=quantity)

        return JsonResponse({'message': 'Patient_OtherCharges created/updated successfully.'}, status=201)

    return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)



@csrf_exempt
def patient_lab_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract data from the JSON object
        patient_id = data.get('patient')
        labCat_id = data.get('labCat')
        quantity = data.get('quantity',1)



        try:
            patient = patient_table.objects.get(pk=patient_id)
            labCat = LabCategory.objects.get(pk=labCat_id)
        except (patient_table.DoesNotExist, LabCategory.DoesNotExist):
            return JsonResponse({'error': 'Invalid patient or lab category ID.'}, status=400)


        # Calculate the total price
        if quantity is not None:
            total_price = Decimal(labCat.lab_price) * quantity
        else:
            total_price = Decimal(labCat.lab_price)

        # Create the Patient_LAB instance
        patient_lab = Patient_LAB(patient=patient, labCat=labCat, quantity=quantity, total_price=total_price)
        patient_lab.save()

        return JsonResponse({'message': 'Patient_LAB created successfully.'}, status=201)

    return JsonResponse({'error': 'This endpoint only accepts POST requests.'}, status=405)




def otherchargesbill(request,idd):
    p_data = patient_table.objects.get(id=int(idd))
    current_date = timezone.now().date()
    p_other_charges = Patient_OtherCharges.objects.filter(patient=p_data)

    tc = 0
    for i in p_other_charges:
        tc += int(i.total_price)

    context = {
        "othercharge":p_other_charges,
        'total_charge':float(tc)
    }

    return render(request,'chargesbill.html',context)




# Lab Part Started
@csrf_exempt
def lab_search_api(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        labs = LabCategory.objects.filter(sub_category__icontains=search_query).values('id', 'sub_category', 'lab_price')
        results = list(labs)
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)







def testBill(request,idd):
    p_data = patient_table.objects.get(id=int(idd))
    current_date = timezone.now().date()
    p_lab_data = Patient_LAB.objects.filter(patient=p_data)

    tc = 0
    for i in p_lab_data:
        tc += int(i.total_price)

    context = {
        "labcharge":p_lab_data,
        'total_charge':float(tc)
    }
    return render(request,'testbillNew.html',context)


# @csrf_exempt
# def patient_lab_api(request):
#     if request.method == 'POST':
#         patient_id = request.POST.get('patient_id', None)
#         labs = request.POST.get('labs', None)
#
#         if patient_id is None or labs is None:
#             return JsonResponse({'error': 'Missing patient_id or labs'}, status=400)
#
#         try:
#             patient_lab = Patient_LAB(patient_id=patient_id, labs=labs)
#             patient_lab.save()
#             return JsonResponse({'success': 'Patient_LAB record created'}, status=201)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)






# def testBill(request):
#     p_lab = Patient_LAB.objects.all().order_by("-id")[0]
#     jsondata = p_lab.labs
#     data = json.loads(jsondata)
#     array = []
#     t_price = 0
#     for i in data['labs']:
#         array.append(LAB.objects.get(id=i))
#         t_price = t_price + int(LAB.objects.get(id=i).lab_price)
#
#     if request.user.is_authenticated:
#         return render(request,"testbill.html",{'pl':p_lab,'labs':array,'tprice':t_price})
#     else:
#         return render(request,"login.html")




def labresult(request):
    if request.POST:
        lab_id = request.POST['search']
        print(lab_id)

        try:
            pl = Patient_LAB.objects.get(id=int(lab_id))
            jsondata = pl.labs
            data = json.loads(jsondata)
            array = []
            t_price = 0
            for i in data['labs']:
                array.append(LAB.objects.get(id=i))

            al = len(array)
            return render(request, 'labresult.html',{'plab':pl,'ptests':array,'alen':al})

        except:
            message = "patient is not found!!! "
            return render(request, 'labresult.html', {'message': message})

    if request.user.is_authenticated:
        return render(request,'labresult.html')
    else:
        return render(request,"login.html")




@csrf_exempt
def update_patient_lab(request, pk):
    try:
        patient_lab = Patient_LAB.objects.get(id=pk)
    except Patient_LAB.DoesNotExist:
        return JsonResponse({'error': 'Invalid Patient LAB ID'}, status=400)

    if request.method == 'POST':
        labs_data = request.POST.get('labs')

        try:
            labs_data = json.loads(labs_data)
            labs = patient_lab.labs or {}
            labs = json.loads(labs) if labs else {}  # Parse existing labs data if it exists
            labs.update(labs_data)
            patient_lab.labs = json.dumps(labs)  # Convert labs back to JSON string
            patient_lab.save()
            return JsonResponse({'success': 'Patient LAB updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def testreportbill(request,pk):
    pl = Patient_LAB.objects.get(id=int(pk))
    request.session['labid'] = int(pk)
    jsondata = pl.labs
    data = json.loads(jsondata)
    array = []
    for i in data['labs']:
        array.append(LAB.objects.get(id=i))
    labval=[]
    for j in data['labvalue']:
        labval.append(j)

    print(array,labval)
    tlen = len(array)

    dlen = range(0,tlen)

    if request.user.is_authenticated:
        return render(request,'testreport.html',{"tests":array,"pl":pl,"labval":labval,'tlen':tlen,'loop_times':dlen})
    else:
        return render(request,"login.html")



def otrhecharges(request):
    if request.POST:
        search = request.POST['search']
        try:
            pp = patient_table.objects.get(id=int(search))
            context = {
                'patient': pp
            }
            return render(request, 'othercharges.html',context)

        except:
            message = "patient is not found!!! "
            return render(request, 'othercharges.html', {'message': message})


    if request.user.is_authenticated:
        message = ""
        return render(request, 'othercharges.html', {'message': message})

    else:
        return render(request, "login.html")








