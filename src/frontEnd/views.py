import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

API_BASE_URL = "http://127.0.0.1:8000/api/"
PRODUCTS_BASE_URL = API_BASE_URL + "products/"
ACCOUNTS_BASE_URL = API_BASE_URL + "accounts/"

def login(request):
    try:
        if request.method == 'POST':
            SEARCH_PRODUCTS_URL = ACCOUNTS_BASE_URL + "login/"
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(username=username, password=password)
            if user is not None:
                params = {'username': username, 'password': password }
                response = requests.post(url=SEARCH_PRODUCTS_URL, data=params)
                data = response.json()

                writeEnv(data["access"])
                return redirect('index')

    except Exception as ex:
        data = ["Something went wrong !"]

    return render(request, 'login.html')

def signup(request):
    try:
        if request.method == 'POST':
            SEARCH_PRODUCTS_URL = ACCOUNTS_BASE_URL + "register/"
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("pwd")
            cpassword = request.POST.get("cpwd")
            
            # user = authenticate(username=username, password=password)
            if password == cpassword:
                params = {'first_name': fname,'last_name': lname,'username': username,'email': email,'password': password,'cpassword': cpassword}
                response = requests.post(url=SEARCH_PRODUCTS_URL, data=params)
                data = response.json()

                writeEnv(data["access"])
                return redirect('index')

    except Exception as ex:
        data = ["Something went wrong !"]

    return render(request, 'signup.html')

def logout(request):
    localenv = readEnv()
    if localenv != "":
        writeEnv("")
    return redirect('index')

def index(request):
    product_data = []
    category_data = []
    isIndex = True

    localenv = readEnv()
    if localenv != "":
        isIndex = False

    try:
        if request.method == 'GET':
            if(localenv == ""):
                LATEST_PRODUCTS_URL = PRODUCTS_BASE_URL + "latest-products/"
                response = requests.get(url=LATEST_PRODUCTS_URL)
                product_data = response.json()
            else:
                ALL_PRODUCTS_URL = PRODUCTS_BASE_URL + "all-products/"
                headers = {"Authorization": "Bearer "+ localenv }
                response = requests.get(url=ALL_PRODUCTS_URL, headers=headers)
                product_data = response.json()

            CATEGORY_LIST_URL = PRODUCTS_BASE_URL + "category/"
            cat_response = requests.get(url=CATEGORY_LIST_URL)
            category_data = cat_response.json()

    except Exception as ex:
        product_data = ["Something went wrong !"]
    
    return render(request, 'index.html', {'index' : isIndex, 'products': list(product_data), 'categories': list(category_data)})


def search(request):
    try:
        if request.method == 'POST':
            SEARCH_PRODUCTS_URL = PRODUCTS_BASE_URL + "search/"
            search_text = request.POST.get("query")
            if search_text != "" or search_text is not None:
                params = {'query': search_text}
                response = requests.post(url=SEARCH_PRODUCTS_URL, params=params)
                data = response.json()

    except Exception as ex:
        data = ["Something went wrong !"]

    return render(request, 'index.html', {'index' : False, 'query':search_text, 'products': list(data)})

def viewProduct(request, id):
    localenv = readEnv()
    PRODUCT_DETAIL_URL = PRODUCTS_BASE_URL + str(id) + "/"
    headers = {"Authorization": "Bearer "+ localenv }
    response = requests.get(url=PRODUCT_DETAIL_URL, headers=headers)
    product = response.json()

    return render(request, 'product-view.html', {'product': product})

def searchCategory(request, category_slug):
    CATEGORY_LIST_URL = PRODUCTS_BASE_URL + "category/"
    cat_response = requests.get(url=CATEGORY_LIST_URL)
    category_data = cat_response.json()

    CATEGORY_PRODUCT_URL = PRODUCTS_BASE_URL + category_slug + "/"
    response = requests.get(url=CATEGORY_PRODUCT_URL)
    products = response.json()

    return render(request, 'category.html', {'index' : True, 'categories': list(category_data), 'products': products})


def readEnv():
    localenv = open("src\\frontEnd\\localenv.txt", "r")
    text = localenv.read()
    localenv.close()
    return text

def writeEnv(text):
    localenv = open("src\\frontEnd\\localenv.txt", "w")
    localenv.write(text)
    localenv.close()

    return True