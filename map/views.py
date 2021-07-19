from django.shortcuts import render, redirect
from django.http import HttpResponse
import geocoder
import folium
from .models import Search
from .forms import SearchForm
# Create your views here.


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SearchForm()
    address = Search.objects.all().last()
    # It is a tool to search data by name and address
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('Address invalid')
    # Create a map object
    m = folium.Map(location=[19, -12], zoom_start=2)

    folium.Marker([lat, lng], tooltip="click for more",
                  popup=country).add_to(m)
    m = m._repr_html_()  # Html representation of folium map objects
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)
