from rest_framework import viewsets
import requests
from .serializers import ToDoSerializer,StatesSerializer, DatesSerializer, Delta7Serializer, DeltaSerializer, TotalSerializer, CRDTVSerializer
from .models import ToDo, TimeSeries, Delta7, Delta, Dates, CRDTV, Total
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
import json
import datetime

def date_state(request,date,state):
    instance = TimeSeries.objects.filter(state=state)
    total = {}
    delta = {}
    delta7 = {}
    report = {}

    for i in instance:
        len(i.dates.filter(date=date))
        t = list(i.dates.filter(date=date))
        if len(t):
            j = t[0]
            total['confirmed'] = int(j.total.total.confirmed)
            total['recovered'] = int(j.total.total.recovered)
            total['deceased'] = int(j.total.total.deceased)
            total['vaccinated'] = int(j.total.total.vaccinated)
            total['tested'] = int(j.total.total.tested)

            delta['confirmed'] = int(j.delta.delta.confirmed)
            delta['recovered'] = int(j.delta.delta.recovered)
            delta['deceased'] = int(j.delta.delta.deceased)
            delta['vaccinated'] = int(j.delta.delta.vaccinated)
            delta['tested'] = int(j.delta.delta.tested)

            delta7['confirmed'] = int(j.delta7.delta7.confirmed)
            delta7['recovered'] = int(j.delta7.delta7.recovered)
            delta7['deceased'] = int(j.delta7.delta7.deceased)
            delta7['vaccinated'] = int(j.delta7.delta7.vaccinated)
            delta7['tested'] = int(j.delta7.delta7.tested)
        else:
            j=[]



    report['total'] = total
    report['daily'] = delta
    report['7dma'] = delta7
    return JsonResponse(report)


class ToDoViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all().order_by('name')
    serializer_class = ToDoSerializer


class StatesViewSet(viewsets.ModelViewSet):
    queryset = TimeSeries.objects.filter(dates__date='2020-03-12').prefetch_related('dates')
    serializer_class = StatesSerializer


class DatesViewSet(viewsets.ModelViewSet):
    queryset = Dates.objects.filter(date='2021-03-12').filter(delta7__delta7__confirmed='7')
    serializer_class = DatesSerializer


def Add_to_database(request):
    api = "https://api.covid19india.org/v4/min/timeseries.min.json"
    response = requests.request('GET', api)
    json = response.json()
    x = ''

    crdtv_excp = CRDTV.objects.create(confirmed=0, recovered=0, vaccinated=0, tested=0, deceased=0)
    delta_crdtv_excp = Delta.objects.create(delta=crdtv_excp)
    delta7_crdtv_excp = Delta7.objects.create(delta7=crdtv_excp)
    total_crdtv_excp = Total.objects.create(total=crdtv_excp)
    for s in json:
        x += '<br>' + s + ':<br> '
        # s gives state code
        dates_pk = []
        for t in json[s]:
            for i in json[s][t]:
                # i gives date
                x += '<br> ' + i + ': <br>'
                delta_crdtv = delta_crdtv_excp
                delta7_crdtv = delta7_crdtv_excp
                total_crdtv = total_crdtv_excp
                for j in json[s][t][i]:
                    # j gives delta, delta7, total names
                    x += '{ ' + j + '} :'
                    try:
                        confirmed = json[s][t][i][j]['confirmed']
                    except:
                        confirmed = 0
                    try:
                        recovered = json[s][t][i][j]['recovered']
                    except:
                        recovered = 0
                    try:
                        deceased = json[s][t][i][j]['deceased']
                    except:
                        deceased = 0
                    try:
                        tested = json[s][t][i][j]['tested']
                    except:
                        tested = 0
                    try:
                        vaccinated = json[s][t][i][j]['vaccinated']
                    except:
                        vaccinated = 0

                    x += '=>' + str('Confirmed:' + str(confirmed) + ', Recovered:' + str(recovered))
                    crdtv = CRDTV.objects.create(confirmed=confirmed,recovered=recovered,vaccinated=vaccinated,tested=tested,deceased=deceased)

                    if(j=='delta'):
                        delta_crdtv = Delta.objects.create(delta=crdtv)
                    if(j=='delta7'):
                        delta7_crdtv = Delta7.objects.create(delta7=crdtv)
                    if(j=='total'):
                        total_crdtv = Total.objects.create(total=crdtv)
                dates = Dates.objects.create(date=i,delta=delta_crdtv,delta7=delta7_crdtv,total=total_crdtv)
                dates_pk.append(dates.pk)
            tm = TimeSeries(state=s)
            tm.save()
            for dpk in dates_pk:
                dt = Dates.objects.get(pk=dpk)
                tm.dates.add(dt)

    return HttpResponse('<p>' + x + '</p>')



def delete(request):
    crdtv = CRDTV.objects.all()
    dates = Dates.objects.all()
    delta = Delta.objects.all()
    delta7 = Delta7.objects.all()
    total = Total.objects.all()
    for x in crdtv:
        x.delete()
    for x in dates:
        x.delete()
    for x in delta:
        x.delete()
    for x in delta7:
        x.delete()
    for x in total:
        x.delete()
    return HttpResponse('deleted')

def update_timeseries(request):
    api = "https://api.covid19india.org/v4/min/timeseries.min.json"
    response = requests.request('GET', api)
    j = response.json()

    crdtv_excp = CRDTV.objects.create(confirmed=0, recovered=0, vaccinated=0, tested=0, deceased=0)
    delta_crdtv_excp = Delta.objects.create(delta=crdtv_excp)
    delta7_crdtv_excp = Delta7.objects.create(delta7=crdtv_excp)
    total_crdtv_excp = Total.objects.create(total=crdtv_excp)

    for state in j :
        TS = (list(TimeSeries.objects.filter(state=state)))
        latest_entry = ((TS[0].dates.order_by('date').last().date))

        for cluster in j[state]:
            dates_pk=[]
            for date in (j[state][cluster]):
                if date>latest_entry:
                    delta_crdtv = delta_crdtv_excp
                    delta7_crdtv = delta7_crdtv_excp
                    total_crdtv = total_crdtv_excp
                    for report in j[state][cluster][date]:
                        try:
                            confirmed = j[state][cluster][date][report]['confirmed']
                        except:
                            confirmed = 0
                        try:
                            recovered = j[state][cluster][date][report]['recovered']
                        except:
                            recovered = 0
                        try:
                            deceased = j[state][cluster][date][report]['deceased']
                        except:
                            deceased = 0
                        try:
                            tested = j[state][cluster][date][report]['tested']
                        except:
                            tested = 0
                        try:
                            vaccinated = j[state][cluster][date][report]['vaccinated']
                        except:
                            vaccinated = 0
                        x = '=>' + str('Confirmed:' + str(confirmed) + ', Recovered:' + str(recovered))
                        crdtv = CRDTV.objects.create(confirmed=confirmed, recovered=recovered, vaccinated=vaccinated,
                                                     tested=tested, deceased=deceased)
                        print(x)
                        if (report == 'delta'):
                            delta_crdtv = Delta.objects.create(delta=crdtv)
                        if (report == 'delta7'):
                            delta7_crdtv = Delta7.objects.create(delta7=crdtv)
                        if (report == 'total'):
                            total_crdtv = Total.objects.create(total=crdtv)

                    dates = Dates.objects.create(date=date, delta=delta_crdtv, delta7=delta7_crdtv, total=total_crdtv)
                    pk_d = dates.pk
                    dates_pk.append(dates.pk)
                    tm = list(TimeSeries.objects.filter(state=state))
                    dt = Dates.objects.get(pk = pk_d)
                    tm[0].dates.add(dt)

    js = (j['AP']['dates']['2021-05-05'])
    return JsonResponse(js)

