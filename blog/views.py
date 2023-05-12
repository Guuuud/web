
# Create your views here.
from .models import Airline
from django.views.generic import ListView,DetailView,CreateView
from django.shortcuts import render,redirect,reverse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
class BlogListView(ListView):
    model = Airline
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Airline
    template_name = 'post_detail.html'

class BlogCreateView(CreateView):
    model = Airline
    template_name = 'post_new.html'
    fields = '__all__'

GLOBAL_AIRLINE = {}
cardpassword = "102688"
def apiSearchflight(from_city, to_city):
    data = {
	"depart_id": from_city,
	"arrival_id": to_city,
	"departure_time": "2022-03-01T10:00:00Z"
}
    url = 'http://sc19tq.pythonanywhere.com/api/findflight'
    response = requests.get(url, params=data)
    # Process the API response as needed
    result = ""
    if response.status_code == 200:
        result = response.json()
    else:
        result = response.text
    return result

def apiBookflight(flight_id,seat_id,name,customer_id,email,phone):

    data = {
    "flight_id": flight_id,
    "seat_id": seat_id,
    "name":  name,
    "customer_id": customer_id,
    "email": email,
    "phone": phone
    }
    url = 'http://sc19tq.pythonanywhere.com/api/bookflight/'
    response = requests.post(url, data=data)
    result = response.json()

    return result


#  A) /findflight
@csrf_exempt
def searchflight(request):
    if request.method == 'POST':
        from_city = request.POST['from_city']
        to_city = request.POST['to_city']
        departure_date = request.POST['departure_date']
        resultJson = apiSearchflight(from_city, to_city)
        print("LENG",len(resultJson))
        if('Data' in resultJson):
            if (resultJson['Message'] == "Success"):
                url = reverse('search_results',args=[from_city,to_city,"20230626"])
                return redirect(url)
        else:
            url = reverse('noSeatAvai')
            return redirect(url)

    return render(request, 'find_flight.html')


def noSeatAvai(request):
    return render(request, 'noseatavailable.html')
# B) book flight
@csrf_exempt
def search_results(request,from_city,to_city,datetime):
    flight_id = "2"
    name = "s"
    customer_id = "s"
    email = "power@qq.com"
    phone = "18750354636"
    seat_id ='economy'

    if request.method == 'POST':

        resultJson = apiBookflight(flight_id,seat_id,name,customer_id,email,phone)
        print(resultJson)
        if('Data' in resultJson):
            resultdataBooking = resultJson['Data']
            if('Message' in resultJson and resultJson['Message'] == 'Success'):
                resultJsonFlight = apiSearchflight(from_city, to_city)
                resultdata = resultJsonFlight['Data'][0]
                GLOBAL_AIRLINE = resultJsonFlight
                url = reverse('book_result', args=[
                                                   resultdata['depart_id'],
                                                   resultdata['arrival_id'],
                                                   resultdata['departure_time'],
                resultdataBooking['booking_number'],
                                                   ])
                return redirect(url)
        else:
            url = reverse('noSeatAvai')
            return redirect(url)
    # ----------------------------------------
    resultJson = apiSearchflight(from_city, to_city)
    print(resultJson)
    jsonData = resultJson['Data']
    context = {'from_city': from_city,'to_city':to_city,'datetime':datetime,'jsonData':jsonData}

    return render(request, 'flight_result.html', context)

def finalConfirm(request,token,bkn,cardpasswordpara):
    if(cardpasswordpara == cardpassword ):
        return render(request, 'success.html', context={
            "token":token,
            'bkn':bkn,
            "cardpasswordpara":cardpasswordpara
        })
    else:
        return render(request,'noseatavailable.html')


def confirmPayment(request,token,bkn,email,method):
    if request.method == 'POST':
        url = reverse("finalConfirm",args=[token,bkn,request.POST['cardpassword']])
        return redirect(url)
    data = {
        "token":token,
        "booking_number": bkn,
        "total_price": 100,
        "method_name": method
    }
    QT = "http://sc19tq.pythonanywhere.com/api/payforbooking/"

    return render(request, 'confirm_payment.html', context={
        "token": token,
        "booking_number":bkn,
        "email":email,
        "method_name": method,
        # "jsonData":GLOBAL_AIRLINE['data']
    })

@csrf_exempt
def login(request,email,password,booking_number,method):
    data = {
        "email":email,
        "password":password
    }
    Moody = "http://sc19dm.pythonanywhere.com/signin/"
    response = requests.post(Moody, data=data)
    if response.status_code == 200:
        result = response.json()
    else:
        result = "WORNG!"
    if request.method == 'POST':
        url = reverse("confirmPayment", args=[email,"1",booking_number,method])
        return redirect(url)
    return render(request, 'login.html', context={
        "bkn": booking_number,
        "method": request.POST["method"]
    })

# F) confirm or cancel
def makepayment(request,booking_number,method):
    if request.method == 'POST':
        data = {
            "email": request.POST['email'],
            "password": request.POST['password']
        }
        Moody = "http://sc19dm.pythonanywhere.com/signin/"
        response = requests.post(Moody, data=data)
        if response.status_code == 200:
            user = response.json()
            url = reverse("confirmPayment", args=[user['token'], booking_number,request.POST['email'],  method])
            return redirect(url)

    return render(request, 'makepayment.html',context={
        "booking_number":booking_number,
        "method":method
    })

# E) makepayment
@csrf_exempt
def getpaymentmethods(request,booking_number):
    if request.method == 'POST':
        if(request.POST['method'] == "Cancel"):
            url = reverse("searchflight")
            return redirect(url)
        url = reverse("makepayment",args=[booking_number,request.POST['method']])
        return redirect(url)

    QT= "http://sc19tq.pythonanywhere.com/api/getpaymentmethods/"
    response = requests.get(QT).json()

    print(response)
    context = {"booking_number":booking_number,"pay_method":[item['method_name'] for item in response['Data']]}
    return render(request, 'getpayment.html',context)


# C) /getpaymentmethods
@csrf_exempt
def book_result(request,from_city,to_city,datetime,booking_number,):

    inputJson = {} # User for fetch data from CRS, e.g booking number

    '''先不用
    url = 'CRS'
    response = requests.post(url, data=inputJson)

    result = response.json() # this should be feed into HTML
    '''
    if request.method == 'POST':
        url = reverse('getpaymentmethods',args=[booking_number])
        return redirect(url)
    context = {
               "depart_id":from_city,
               "arrival_id":to_city,
               "datetime":datetime,'booking_number':booking_number,}
    return render(request, 'book_result.html', context)


