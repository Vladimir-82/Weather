import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm



def index(request):
    appid = '31bd6b6a3c005a57dc32dbd102f5b6b1'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    cities = City.objects.all()
    if (request.method == 'POST'):
        if request.POST.get('_method') == 'delete':
            city_name = request.POST.get('city_name', False)
            if city_name:
                cities.filter(name=city_name).delete()
        else:
            form = CityForm(request.POST)
            form.save()

    form = CityForm()

    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res == {'cod': '404', 'message': 'city not found'}:
            print('Такого города не существует')
            cities.filter(name=city).delete()
            continue

        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
            'humidity': res['main']['humidity']
        }
        all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)


def info(request):
    return render(request, 'weather/info.html', None)


def doc(request):
    return render(request, 'weather/doc.html', None)