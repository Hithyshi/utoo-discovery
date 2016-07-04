from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.
import re
import csv
import requests
from math import sin, cos, sqrt, atan2, radians



def home(request):
    return render_to_response("homepage.html",context_instance=RequestContext(request))


def searchresult(request):
#    mydata=request.POST['speciality']
    mylat=request.POST['latlong']
    print (mylat)
#    print mydata + " " + mylat
#    print "YEEEEEEEESSSSSS"
    res_list=[]
    R = 6373.0
    lats = re.findall(r'Latitude: (..\...)*', mylat)
    longs = re.findall(r'.*Longitude: (..\...)*', mylat)
    print (float(lats[0]))
    print (float(longs[0]))
    lat1 = radians(float(lats[0]))
    lon1 = radians(float(longs[0]))
    CSV_URL = 'https://data.gov.in/node/356921/datastore/export/csv'
    search_speciality = request.POST['speciality']
    print (search_speciality)
    speciality_str=search_speciality[0].upper()+search_speciality[1:].lower()
    result_list=list()
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            for item in row:
                if speciality_str in item:
                    if row[21]!='NA' and (row[21][2]=='.' or row[21][3]=='.'):
                        lat2 = radians(float(row[21]))
                        lon2 = radians(float(row[22]))
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distance = R * c
                        result_list.append((row[1],row[2],row[10],row[19],row[5],distance))
                    break
    for res in sorted(result_list, key=lambda x: x[5]):
        res_list.append(res)
    return render_to_response("resultpage.html",{"res_list":res_list},context_instance=RequestContext(request))


