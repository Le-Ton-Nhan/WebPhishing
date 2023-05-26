"""Import models"""
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
from sklearn import preprocessing
import os 
import numpy as np
import pickle
from Main_extract.feature_extractor import *
from django.urls import reverse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from Phishpedia.phishpedia.phishpedia_main import *
from Phishpedia.phishpedia.phishpedia_config import load_config
from PIL import Image as im


dir = os.getcwd()
result_folder_dir = dir + r'\Main_extract\results'
result_file = result_folder_dir + r'\results_data_final.csv'


predict_results = {"model_path": 0, "classifier": 0, "prediction": 0, "conf_score": 0, "error": 0,  "message": 'None'}
drop_list = ["url", 'host', 'script_to_body_ratio', 'capitalizations', 'num_hidden_tags', 'num_iframes', 'num_embeds', 'num_objects', 'num_double_documents', 'num_eval_functions', 'num_suspicious_functions', 'num_subdomains', 'registration_date', 'expiration_date', 'last_updates_dates', 'age', 'intended_life_span', 'life_remaining', 'registrar', 'reg_country', 'open_ports', 'num_open_ports', 'is_live', 'isp', 'connection_speed', 'avg_update_days', 'total_updates', 'ttl', 'tld', 'host_is_ip', 'has_port_in_string', 'fragments', 'is_encoded',  'alexa_dis_similarity',  'has_client', 'has_login', 'has_admin', 'has_server', 'length_url', 'ip', 'nb_at', 'nb_qm',  'nb_or',  'nb_underscore', 'nb_tilde', 'nb_percent', 'nb_star', 'nb_colon', 'nb_comma', 'nb_semicolumn', 'nb_dollar', 'nb_space', 'nb_www', 'nb_com', 'nb_dslash', 'ratio_digits_url', 'ratio_digits_host', 'punycode', 'port', 'tld_in_path', 'tld_in_subdomain', 'abnormal_subdomain', 'prefix_suffix', 'shortening_service', 'path_extension', 'nb_redirection', 'nb_external_redirection', 'char_repeat', 'avg_word_host',  'phish_hints', 'domain_in_brand', 'brand_in_subdomain', 'brand_in_path', 'suspecious_tld', 'statistical_report', 'login_form', 'external_favicon', 'links_in_tags', 'submit_email', 'ratio_intMedia', 'sfh', 'iframe', 'popup_window', 'safe_anchor', 'onmouseover', 'right_clic', 'empty_title', 'domain_in_title', 'domain_with_copyright', 'whois_registered_domain', 'dns_record', 'tag']

# Create your views here.

def MyUrl(request):
    url = static_result.objects.filter(user=request.user).order_by('time')
    return render(request, 'MyUrl.html', { 'count': url.count(), 'url': url})

def url_details(request, pid):
    url = final_result.objects.get(url_id = pid)
    return render(request, 'url_detail.html', {'url': url})

def _convert(data): 
    for col in data.columns:
        col_type = data[col].dtype
        if col_type == 'object' or col_type == 'bool' :
        
            label_encoder = preprocessing.LabelEncoder()
            # Encode labels in column 'species'.
            data[col]= label_encoder.fit_transform(data[col])
    return data

def static_prediction(result):
    #Passing data to model & loading the model from disks
    model_path = 'ml_model/model_phishing.pkl'
    classifier = pickle.load(open(model_path, 'rb'))
    prediction = classifier.predict([result])[0]
    conf_score =  np.max(classifier.predict_proba([result]))*100
    error = '0'
    message = 'Successfull'
    return {"model_path": model_path, "classifier": classifier, "prediction": prediction, "conf_score": conf_score, "error": error,  "message": message}


def dynamic_predictions(folder_result_name):
    # url_path = folder_result_name+"/info.txt"
    # screenshot_path = folder_result_name + "/shot.png"

    cfg_path = None # None means use default config.yaml
    reload_targetlist = False
    ELE_MODEL, SIAMESE_THRE, SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH = load_config(cfg_path, reload_targetlist)
    # phish_category, pred_target, plotvis, siamese_conf, pred_boxes = test(url_path, screenshot_path,
    #                                                                   ELE_MODEL, SIAMESE_THRE, SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH)
    phish_category, phish_target, siamese_conf, vt_result, img_path = runit( folder_result_name, result_folder_dir + "/test.txt", ELE_MODEL, SIAMESE_THRE, SIAMESE_MODEL, LOGO_FEATS, LOGO_FILES, DOMAIN_MAP_PATH )
    return {"prediction": phish_category, "brand_name": phish_target, "conf_score": siamese_conf, "virustotal": vt_result,"image_result": img_path}
# Trang thông báo lỗi
def error404(request, *args, **kwargs):
    return render(
        request, '404.html'
    )

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

def save_dynamicResult(request, folder_screenshot, submitedUrl):
    # dynamic prediction process
    url_submit_by_user = submitedUrl.url
    res = dynamic_predictions(folder_screenshot)

    dynamic_result.objects.get_or_create(user = request.user, url = submitedUrl)
    dynamicResult = dynamic_result.objects.get(url = submitedUrl)

    dynamicResult.brand_name = res['brand_name'] if res['brand_name']!= None else "No brand name"
    dynamicResult.conf_score = res['conf_score'] if res['conf_score'] != None else "0"
    dynamicResult.img_path = res['image_result']
    dynamicResult.prediction = res["prediction"]

    dynamicResult.url= url_submit_by_user
    if res["prediction"] == 1:
        dynamicResult.status = 'Phishing'
    else:
        dynamicResult.status = 'Normal'
    dynamicResult.save()
    return res["virustotal"]

def home(request):
    global process
    process = ""
    features = []
    all_URLs = final_result.objects.all().order_by('time')
    form = URLForm()

    if request.method == 'POST':
        form = URLForm(request.POST, user=request.user)
        if form.is_valid():
            #save url to final_result form
            form.save()

            # get url 
            submitedUrl = final_result.objects.filter(user=request.user).latest('time')
            
            #caculate conf_score & prediction
            folder_result_name = generate_external_dataset(submitedUrl.url)
            
            if folder_result_name == False:
                process = False
                return render(request, 'detect.html', { 'count': all_URLs.count(), 'url': all_URLs, 'form':form, 'process': process})

            # read result
            results = pd.read_csv(result_file, on_bad_lines='skip')
            data = results.drop(columns=drop_list)
            data = _convert(data)
            data = data.fillna(0)
            fields = data.columns
            i = 0
            for f in fields:
                features.append(float(data[str(f)].values[i]))

            global predict_results 
            
            save_staticResults(request, features, submitedUrl)
            vt_score = save_dynamicResult(request, folder_result_name, submitedUrl)

            ## final results


            process = True
            # return HttpResponseRedirect(request.path)
        

    return render(request, 'detect.html', { 'count': all_URLs.count(), 'url': all_URLs, 'form':form, 'process': process})
