"""Import models"""
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.utils.html import escape
from products.forms import URLForm
from .models import *
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone
import os 
from Main_extract.feature_extractor import *
from django.urls import reverse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from PIL import Image as im
import plotly.express as px
import pandas as pd
import plotly.io as pio
import time
from pathlib import Path
from ml_model_src.prediction import *
from decimal import Decimal, ROUND_HALF_UP

dir = os.getcwd()
# result_file = result_folder_dir + r'\results_data_final.csv'


predict_results = {"model_path": 0, "classifier": 0, "prediction": 0, "conf_score": 0, "error": 0,  "message": 'None'}
drop_list = [ 
                # Investigation findings
                'host', "get_os","get_asn",  "longitude", "latitude" , 'num_open_ports' , "hostnames", 'open_ports',"subdomains", 'isp', 'connection_speed',  'is_live', 
                # Lifecycle Information
                'registration_date', 'expiration_date', 'last_updates_dates', 'intended_life_span', 'life_remaining', 'ttl', 
                # HTTP Response
                "url",  'tld',   'suspecious_tld', 'abnormal_subdomain', 'is_encoded',  'status_code', 'header',
                # Website Access
                'has_login', 'has_admin', 'login_form', 'submit_email', 'has_port_in_string',  'ip',


                'domain_in_brand', 'brand_in_subdomain', 'brand_in_path',
                'ratio_digits_url',  'punycode', 'port','prefix_suffix', 'shortening_service', 'path_extension', 'char_repeat', 
                'avg_word_host',  'statistical_report', 'external_favicon', 'links_in_tags', 'ratio_intMedia', 'sfh', 'iframe', 
                'popup_window', 'safe_anchor', 'domain_in_title',  'whois_registered_domain',  'fragments', 'phish_hints', 
                'num_hidden_tags', 'alexa_dis_similarity', 'tag','nameServerwhois']

# Create your views here.
def location_view(data, folder_result_name):
    color_scale = [(0, 'orange'), (1,'red')]
    fig = px.scatter_mapbox(data, 
                            lat="latitude", 
                            lon="longitude", 
                            hover_name="host", 
                            hover_data=["host"],
                            color="host",
                            size="num_open_ports",
                            color_continuous_scale=color_scale,
                            zoom=8, 
                            height=1080,
                            width=1920)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
   
    path = 'media/loc/' + 'loc_{}.png'.format(Path(folder_result_name).name)
    pio.write_image(fig, file=path)
    return path


def save_staticResults(request,features, submitedUrl):

    url_submit_by_user = submitedUrl.url
    res = static_prediction(features)

    static_result.objects.get_or_create(user = request.user, url = submitedUrl)
    staticResult = static_result.objects.get(url = submitedUrl)

    staticResult.prediction = res["prediction"]
    staticResult.conf_score = res["conf_score"]
    staticResult.url = url_submit_by_user

    if res["prediction"] == 1:
        staticResult.status = 'Phishing'
    else:
        staticResult.status = 'Normal'
    staticResult.save()
    return 0 if staticResult.status == 'Normal' else 1

def save_dynamicResult(request, folder_screenshot, submitedUrl):
    # dynamic prediction process
    url_submit_by_user = submitedUrl.url
    res = dynamic_predictions(folder_screenshot)

    dynamic_result.objects.get_or_create(user = request.user, url = submitedUrl)
    dynamicResult = dynamic_result.objects.get(url = submitedUrl)
    b_name = res['brand_name'] if res['brand_name']!= None else "No brand name"
    dynamicResult.brand_name = b_name
    dynamicResult.conf_score = res['conf_score'] if res['conf_score'] != None else "0"
    dynamicResult.prediction = res["prediction"]

    dynamicResult.url= url_submit_by_user
    if res["prediction"] == 1:
        dynamicResult.status = 'Phishing'
    else:
        dynamicResult.status = 'Normal'
    dynamicResult.save()
    r = 0 if  dynamicResult.status == 'Normal' else 1
    return { "vt_score" : res["virustotal"], "img_path" : res['image_result'], 'brand_name': b_name,  "pre": r }





def MyUrl(request):
    all_url = final_result.objects.filter(user=request.user).order_by('-time')
    return render(request, 'MyUrl.html', { 'count': all_url.count(), 'url': all_url})

# Trang thông báo lỗi
def error404(request, *args, **kwargs):
    return render(
        request, '404.html'
    )


def url_details(request, pid):
    url = final_result.objects.get(url_id = pid)
    return render(request, 'url_detail.html', {'Result': url})

def img_details(request, pid):
    obj = final_result.objects.get(url_id = pid) 
    return render(request, 'img_details.html', {'obj': obj})

def loc_details(request, pid):
    obj = final_result.objects.get(url_id = pid) 
    return render(request, 'loc_details.html', {'obj': obj})

def home(request):
    global process
    global _url
    process = ""
    _url = ""
    features = []
    all_URLs = final_result.objects.all().order_by('-time')[:10]
    form = URLForm()

    if request.method == 'POST':
        form = URLForm(request.POST, user=request.user)
        if form.is_valid():
            #save url to final_result form
            form.save()

            # get url 
            submitedUrl = final_result.objects.filter(user=request.user).latest('time')
            _url = submitedUrl.url
            _id = submitedUrl.url_id
            start_time = time.time()

            #caculate conf_score & prediction
            folder_result_name, result_file = generate_external_dataset(submitedUrl.url)
            
            if folder_result_name == False:
                process = False
                final_result.objects.filter(url_id = _id).delete()
                all_URLs = final_result.objects.all().order_by('-time')[:10]
                return render(request, 'detect.html', { 'count': all_URLs.count(), 'url': all_URLs, 'form':form, 'process': process})
            
            
            # read result
            results = pd.read_csv(result_file, on_bad_lines='skip')
            path = location_view(results, folder_result_name)


            submitedUrl.loc_path = path
            submitedUrl.host = results["host"].values[0]
            submitedUrl.is_live = results["is_live"].values[0]
            submitedUrl.host_country = results["host_country"].values[0]
            submitedUrl.get_os = results["get_os"].values[0]
            submitedUrl.get_asn = results["get_asn"].values[0]
            submitedUrl.num_open_ports = results["num_open_ports"].values[0]
            submitedUrl.subdomains = results["subdomains"].values[0]
            submitedUrl.hostnames = results['hostnames'].values[0]
            submitedUrl.open_ports= results["open_ports"].values[0]
            submitedUrl.connection_speed = results["connection_speed"].values[0]
            submitedUrl.isp= results["isp"].values[0]
            submitedUrl.nameServerwhois = results["nameServerwhois"].values[0]
            
            
            submitedUrl.registration_date = results["registration_date"].values[0]
            submitedUrl.expiration_date= results["expiration_date"].values[0]
            submitedUrl.last_updates_dates = results['last_updates_dates'].values[0]
            submitedUrl.intended_life_span = results['intended_life_span'].values[0]
            submitedUrl.life_remaining = results['life_remaining'].values[0]
            submitedUrl.ttl = results['ttl'].values[0]

            # "url",  'tld',   'suspecious_tld', 'abnormal_subdomain', 'is_encoded',  'status_code', 'header',
            submitedUrl.url = results['url'].values[0]
            submitedUrl.scheme = results["scheme"].values[0]
            submitedUrl.status_code = results['status_code'].values[0]
            submitedUrl.headers = results['header'].values[0]
            submitedUrl.tld = results['tld'].values[0]
            submitedUrl.suspecious_tld = results['suspecious_tld'].values[0]
            submitedUrl.abnormal_subdomain = results['abnormal_subdomain'].values[0]
            submitedUrl.is_encoded = results['is_encoded'].values[0]


            #
            submitedUrl.has_login = results['has_login'].values[0]
            submitedUrl.has_admin = results['has_admin'].values[0]
            submitedUrl.login_form = results['login_form'].values[0]
            submitedUrl.submit_email = results['submit_email'].values[0]
            submitedUrl.has_port_in_string = results['has_port_in_string'].values[0]
            submitedUrl.ip = results['ip'].values[0]



            data = results.drop(columns=drop_list)
            data = convertData(data)
            data = data.fillna(0)
            fields = data.columns

            i = 0
            for f in fields:
                features.append(float(data[str(f)].values[i]))
            
            s = save_staticResults(request, features, submitedUrl)
            d = save_dynamicResult(request, folder_result_name, submitedUrl)

            with open(d['img_path'], 'rb') as f:
                data = f.read()

            print("s = ", s)
            print("d['pre']= ", d['pre'])
            score = float(s)*0.3 + float(d['pre'])* 0.7
            ## final results evaluation 7:3 
            final_score = 0

            if score >=0.5:
                final_score = 1
            elif score >0 and score <0.5:
                final_score = 0.5
            else:
                final_score = 0
            
            submitedUrl.prediction_final = final_score
            if final_score == 1:
                submitedUrl.status = "phishing"
            elif final_score == 0.5:
                submitedUrl.status = "warning"
            else: 
                submitedUrl.status = "normal"
                
            print("score: ", score)
            print("final score: ", final_score)
            submitedUrl.vt_score = d['vt_score']
            submitedUrl.img_path.save("predict.png", ContentFile(data) )
            submitedUrl.brand_name = d['brand_name'] 
            submitedUrl.save()
            process = True

            print("TIME ----->: ", round(time.time() - start_time, 4))
        return render(request, 'url_detail.html', {'Result': submitedUrl })
    # final_result.objects.filter(url_id = _id).delete()
    # all_URLs = final_result.objects.all().order_by('-time')[:10]
    return render(request, 'detect.html', { 'count': all_URLs.count(), 'url': all_URLs, 'form':form, 'process': process})



