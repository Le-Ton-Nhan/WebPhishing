"""Import models"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.utils.html import escape
from products.forms import URLForm
from .models import URL
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone
from sklearn import preprocessing
import os 
import numpy as np
import pickle
from Main_extract.feature_extractor import *
from django.urls import reverse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404

dir = os.getcwd()
result_folder_dir = dir + r'\Main_extract\results'
result_file = result_folder_dir + r'\results_data_final.csv'

predict_results = {"model_path": 0, "classifier": 0, "prediction": 0, "conf_score": 0, "error": 0,  "message": 'None'}
# Create your views here.
#view home
def home(request):
    features = []
    url = URL.objects.all().order_by('time')
    form = URLForm()
    if request.method == 'POST':
        form = URLForm(request.POST, user=request.user)
        if form.is_valid():
            #save url
            form.save()
            url_submit = URL.objects.filter(user=request.user).latest('time')
            all_url = URL.objects.filter(user=request.user).order_by("-time")
            submitedUrl = all_url[0].url
            #caculate conf_score & prediction
            generate_external_dataset(submitedUrl)
            # read result
            results = pd.read_csv(result_file, on_bad_lines='skip')
            data = results.drop(columns=["url", 'host', 'script_to_body_ratio', 'capitalizations', 'num_hidden_tags', 'num_iframes', 'num_embeds', 'num_objects', 'num_double_documents', 'num_eval_functions', 'num_suspicious_functions', 'num_subdomains', 'registration_date', 'expiration_date', 'last_updates_dates', 'age', 'intended_life_span', 'life_remaining', 'registrar', 'reg_country', 'open_ports', 'num_open_ports', 'is_live', 'isp', 'connection_speed', 'avg_update_days', 'total_updates', 'ttl', 'tld', 'host_is_ip', 'has_port_in_string', 'fragments', 'is_encoded',  'alexa_dis_similarity',  'has_client', 'has_login', 'has_admin', 'has_server', 'length_url', 'ip', 'nb_at', 'nb_qm',  'nb_or',  'nb_underscore', 'nb_tilde', 'nb_percent', 'nb_star', 'nb_colon', 'nb_comma', 'nb_semicolumn', 'nb_dollar', 'nb_space', 'nb_www', 'nb_com', 'nb_dslash', 'ratio_digits_url', 'ratio_digits_host', 'punycode', 'port', 'tld_in_path', 'tld_in_subdomain', 'abnormal_subdomain', 'prefix_suffix', 'shortening_service', 'path_extension', 'nb_redirection', 'nb_external_redirection', 'char_repeat', 'avg_word_host',  'phish_hints', 'domain_in_brand', 'brand_in_subdomain', 'brand_in_path', 'suspecious_tld', 'statistical_report', 'login_form', 'external_favicon', 'links_in_tags', 'submit_email', 'ratio_intMedia', 'sfh', 'iframe', 'popup_window', 'safe_anchor', 'onmouseover', 'right_clic', 'empty_title', 'domain_in_title', 'domain_with_copyright', 'whois_registered_domain', 'dns_record', 'tag'])
            data = _convert(data)
            data = data.fillna(0)
            fields = data.columns
            i = 0
            for f in fields:
                print(f)
                features.append(float(data[str(f)].values[i]))
            global predict_results 
            predict_results = predict(features)
            url_submit.prediction = predict_results["prediction"]
            url_submit.conf_score = predict_results["conf_score"]
            if predict_results["conf_score"] >= 50:
                url_submit.status = 'Phishing'
            else:
                url_submit.status = 'Normal'
            url_submit.save()
            return HttpResponseRedirect(request.path)
    return render(request, 'detect.html', { 'count': url.count(), 'url': url, 'form':form})

def MyUrl(request):
    url = URL.objects.filter(user=request.user).order_by('time')
    return render(request, 'MyUrl.html', { 'count': url.count(), 'url': url})

def url_details(request, pid):
    url = URL.objects.get(url_id = pid)
    return render(request, 'url_detail.html', {'url': url})

def _convert(data): 
    for col in data.columns:
        col_type = data[col].dtype
        if col_type == 'object' or col_type == 'bool' :
        
            label_encoder = preprocessing.LabelEncoder()
            # Encode labels in column 'species'.
            data[col]= label_encoder.fit_transform(data[col])
    return data

def predict(result):
    #Passing data to model & loading the model from disks
    print("OK HELLO")
    print("\n-------------------------------->\n\n")
    print("data for predict: ", result)
    model_path = 'ml_model/model_phishing.pkl'
    classifier = pickle.load(open(model_path, 'rb'))
    prediction = classifier.predict([result])[0]
    print("\nPREDICT: ", prediction)
    conf_score =  np.max(classifier.predict_proba([result]))*100
    error = '0'
    message = 'Successfull'
    return {"model_path": model_path, "classifier": classifier, "prediction": prediction, "conf_score": conf_score, "error": error,  "message": message}

# Trang thông báo lỗi
def error404(request, *args, **kwargs):
    return render(
        request, '404.html'
    )