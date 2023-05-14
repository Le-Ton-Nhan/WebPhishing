#Import necessary libraries
import pickle
from django.shortcuts import render
import numpy as np
from phishing.models import URL, User
from phishing.form import URLForm
from icecream import ic
from django.http import HttpResponseRedirect, HttpResponse


# Tạo trang chủ 
def home_view(request):
    return render(
        request,
        'base.html',
    )

def predict_phishing_link(request):
    # page_entropy = 5.048844
    # num_script_tags = 59
    # html_length = 175618	
    # page_tokens = 5542
    # num_sentences = 982
    # num_punctuations = 10792	
    # distinct_tokens = 2140
    # avg_tokens_per_sentence = 6.608961 
    # num_html_tags = 990
    # hyperlinks = 211
    # num_whitespaces = 32233
    # num_included_elemets = 24
    # num_suspicious_elements = 25
    # avg_script_length = 265
    # avg_script_entropy = 3.908571
    # host_country = 4.000000
    # scheme = 0.000000
    # url_length = 83
    # path_length = 64
    # host_length = 12
    # num_digits = 0.000000
    # parameters = 0.000000
    # string_entropy = 4.197927
    # subdirectories = 6.000000
    # periods = 2.000000
    # num_encoded_chars = 0.000000
    # length_hostname = 12
    # nb_dots = 2.000000
    # nb_hyphens = 2.000000
    # nb_and = 0.000000
    # nb_eq = 0.000000
    # nb_slash = 7.000000
    # http_in_path = 0.000000
    # https_token = 1.000000
    # nb_subdomains = 2.000000
    # length_words_raw = 7.000000
    # shortest_words_raw = 5.000000
    # shortest_word_host = 5.000000
    # shortest_word_path = 7.000000
    # longest_words_raw = 14
    # longest_word_host = 5.000000
    # longest_word_path = 14
    # avg_words_raw = 8.857142
    # avg_word_path = 9.500000
    # ratio_extMedia = 25
    # domain_registration_length = 0.000000
    # page_rank = 5.000000
    page_entropy = 5.291521
    num_script_tags = 2
    html_length = 443409
    page_tokens = 9746
    num_sentences = 24468
    num_punctuations = 72498	
    distinct_tokens = 3934
    avg_tokens_per_sentence = 1.395332
    num_html_tags = 1179
    hyperlinks = 74
    num_whitespaces = 46047
    num_included_elemets = 1.000000
    num_suspicious_elements = 734
    avg_script_length = 2817
    avg_script_entropy = 2.455201
    host_country = 13
    scheme = 1.000000
    url_length = 28
    path_length = 1.000000
    host_length = 19
    num_digits = 0.000000
    parameters = 0.000000
    string_entropy = 3.842370
    subdirectories = 2.000000
    periods = 2.000000
    num_encoded_chars = 0.000000
    length_hostname = 1.900000
    nb_dots = 2.000000
    nb_hyphens = 0.000000
    nb_and = 0.000000
    nb_eq = 0.000000
    nb_slash = 3.000000
    http_in_path = 0.000000
    https_token = 0.000000
    nb_subdomains = 2.000000
    length_words_raw = 2.000000
    shortest_words_raw = 7.000000
    shortest_word_host = 7.000000
    shortest_word_path = 0.500000
    longest_words_raw = 8.000000
    longest_word_host = 8.000000
    longest_word_path = 0.000000
    avg_words_raw = 7.500000
    avg_word_path = 0.000000
    ratio_extMedia = 0.000000
    domain_registration_length = 0.000000
    page_rank = 2.000000
    fields = [page_entropy,num_script_tags,html_length,page_tokens,num_sentences,num_punctuations,distinct_tokens,avg_tokens_per_sentence,num_html_tags,hyperlinks,num_whitespaces,num_included_elemets,num_suspicious_elements,avg_script_length,avg_script_entropy,host_country,scheme,url_length,path_length,host_length,num_digits,parameters,string_entropy,subdirectories,periods,num_encoded_chars,length_hostname,nb_dots,nb_hyphens,nb_and,nb_eq,nb_slash,http_in_path,https_token,nb_subdomains,length_words_raw,shortest_words_raw,shortest_word_host,shortest_word_path,longest_words_raw,longest_word_host,longest_word_path,avg_words_raw,avg_word_path,ratio_extMedia,domain_registration_length,page_rank ]
    if not None in fields:
        page_entropy = float(page_entropy)
        num_script_tags = float(num_script_tags)
        html_length = float(html_length)
        page_tokens = float(page_tokens)
        num_sentences = float(num_sentences)
        num_punctuations = float(num_punctuations)	
        distinct_tokens = float(distinct_tokens)
        avg_tokens_per_sentence = float(avg_tokens_per_sentence)
        num_html_tags = float(num_html_tags)
        hyperlinks = float(hyperlinks)
        num_whitespaces = float(num_whitespaces)
        num_included_elemets = float(num_included_elemets)
        num_suspicious_elements = float(num_suspicious_elements)
        avg_script_length = float(avg_script_length)
        avg_script_entropy = float(avg_script_entropy)
        host_country = float(host_country)
        scheme = float(scheme)
        url_length = float(url_length)
        path_length = float(path_length)
        host_length = float(host_length)
        num_digits = float(num_digits)
        parameters = float(parameters)
        string_entropy = float(string_entropy)
        subdirectories = float(subdirectories)
        periods = float(periods)
        num_encoded_chars = float(num_encoded_chars)
        length_hostname = float(length_hostname)
        nb_dots = float(nb_dots)
        nb_hyphens = float(nb_hyphens)
        nb_and = float(nb_and)
        nb_eq = float(nb_eq)
        nb_slash = float(nb_slash)
        http_in_path = float(http_in_path)
        https_token = float(https_token)
        nb_subdomains = float(nb_subdomains)
        length_words_raw = float(length_words_raw)
        shortest_words_raw = float(shortest_words_raw)
        shortest_word_host = float(shortest_word_host)
        shortest_word_path = float(shortest_word_path)
        longest_words_raw = float(longest_words_raw)
        longest_word_host = float(longest_word_host)
        longest_word_path = float(longest_word_path)
        avg_words_raw = float(avg_words_raw)
        avg_word_path = float(avg_word_path)
        ratio_extMedia = float(ratio_extMedia)
        domain_registration_length = float(domain_registration_length)
        page_rank = float(page_rank)
        result = [page_entropy,num_script_tags,html_length,page_tokens,num_sentences,num_punctuations,distinct_tokens,avg_tokens_per_sentence,num_html_tags,hyperlinks,num_whitespaces,num_included_elemets,num_suspicious_elements,avg_script_length,avg_script_entropy,host_country,scheme,url_length,path_length,host_length,num_digits,parameters,string_entropy,subdirectories,periods,num_encoded_chars,length_hostname,nb_dots,nb_hyphens,nb_and,nb_eq,nb_slash,http_in_path,https_token,nb_subdomains,length_words_raw,shortest_words_raw,shortest_word_host,shortest_word_path,longest_words_raw,longest_word_host,longest_word_path,avg_words_raw,avg_word_path,ratio_extMedia,domain_registration_length,page_rank ]
        #Passing data to model & loading the model from disks
        model_path = 'ml_model/model_phishing.pkl'
        classifier = pickle.load(open(model_path, 'rb'))
        prediction = classifier.predict([result])[0]
        conf_score =  np.max(classifier.predict_proba([result]))*100
        error = '0'
        message = 'Successfull'
    else:
        error = '1'
        message = 'Invalid Parameters' 
    url = URL.objects.filter().order_by("-Time")
    form = URLForm()
    if request.method == 'POST':
        form = URLForm(request.POST)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)            
    return render(
        request,
        'base.html',
        {
            'prediction' : prediction,
            'conf_score' : conf_score,
            'error' : error,
            'message' : message,
            'form' : form,
            'url' : url,
        }
    )