#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:23:31 2020

@author: hannousse
"""
import time
import os
import uuid
from . import content_features as ctnfe 
# import content_features as ctnfe
from . import url_features as urlfe
from . import external_features as trdfe

from . import ContentFeatures_new as ctnfe_new
from . import HostFeatures as htfe
from . import LexicalFeatures as lxfe

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



# import ml_models as models
import pandas as pd 
import urllib.parse
import tldextract
import requests
import json
import csv
import os
import re


# from pandas2arff import pandas2arff
from urllib.parse import urlparse
from bs4 import BeautifulSoup

key = 'gks80wkockcokoo444sok4480wgk0g480ko84kwg '

import signal


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--window-size=1920,1040")

driver = webdriver.Chrome(options=chrome_options)

dir = os.getcwd()
base_dir = dir + r'\Main_extract'
cache_file_dir = base_dir + r'\data\cache.csv'
results_file_dir = base_dir + r'\results\results_data_final.csv'
# data_file_dir = base_dir + r'\data\data_final.csv'


def take_screenshot(url):
    print("\n**************************URL: " + url)
    folder_result_name = ""
    #get hostname
    hostname, domain, path = get_domain(url)
    
    try:
        folder_result_name = base_dir + r'\\results\\'
        folder_result_name += hostname
        os.mkdir(folder_result_name)
    except FileExistsError:
        folder_result_name = base_dir + r'\\results\\' + hostname +str(uuid.uuid4().hex)
        print("This domain extraction has already existed")
        os.mkdir(folder_result_name)
    
    # Sleep for a few seconds
    state, iurl, page = is_URL_accessible(url) 
    if state == True:
        rawText = getRawHTML(content= page.content)
        with open(folder_result_name + "/html.txt", "w", encoding='utf-8') as f:
            print("HTML source is saved to: " + folder_result_name)
            f.write(str(rawText))

        driver.get(url)
        time.sleep(3)
        driver.save_screenshot(folder_result_name + "/shot.png")

        with open(folder_result_name + "/info.txt", "w") as f:
            f.write(url)
        
    else:
        removeFolder(folder_result_name)
        with open("results/erro.txt", "a+") as f:
            f.write(url + "\n")
        return False
    
    return True

    

class TimedOutExc(Exception):
    pass

def deadline(timeout, *args):
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()

        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            return f(*args)
            signal.alarm(0)

        new_f.__name__ = f.__name__
        return new_f
    return decorate

# @deadline(5)
def is_URL_accessible(url):
    iurl = url
    parsed = urlparse(url)
    url = parsed.scheme+'://'+parsed.netloc
    page = None
    # print("Url = ", url)
    try:
        page = requests.get(url, timeout=1000)   
        print("Page: ", page.status_code)
    except:
        parsed = urlparse(url)
        url = parsed.scheme+'://'+parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            try:
                page = requests.get(url, timeout=1000)
                print("Page: ", page.status_code)
            except:
                page = None
                pass
        # if not parsed.netloc.startswith('www'):
        #     url = parsed.scheme+'://www.'+parsed.netloc
        #     #iurl = iurl.replace('https://', 'https://www.')
        #     try:
        #         page = requests.get(url)
        #     except:        
        #         # url = 'http://'+parsed.netloc
        #         # iurl = iurl.replace('https://', 'http://')
        #         # try:
        #         #     page = requests.get(url) 
        #         # except:
        #         #     if not parsed.netloc.startswith('www'):
        #         #         url = parsed.scheme+'://www.'+parsed.netloc
        #         #         iurl = iurl.replace('http://', 'http://www.')
        #         #         try:
        #         #             page = requests.get(url)
        #         #         except:
        #         #             pass
        #         pass 
    # if page and page.content not in ["b''", "b' '"]:
    if page == None:
        print("Cannot get content from this URL.")
        return False, url, page
    return True, url, page
    # else:
    #     return False, None, None

def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path


def getPageContent(url):
    parsed = urlparse(url)
    url = parsed.scheme+'://'+parsed.netloc
    try:
        page = requests.get(url)
    except:
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            page = requests.get(url)
    if page.status_code != 200:
        return None, None
    else:    
        return url, page.content
 

    
#################################################################################################################################
#              Data Extraction Process
#################################################################################################################################

def getRawHTML(content):
    soup = BeautifulSoup(content, 'html.parser', from_encoding='iso-8859-1')
    return soup

def extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text):
    #print("OK")
    Null_format = ["", "#", "#nothing", "#doesnotexist", "#null", "#void", "#whatever",
               "#content", "javascript::void(0)", "javascript::void(0);", "javascript::;", "javascript"]

    soup = BeautifulSoup(content, 'html.parser', from_encoding='iso-8859-1')
    # collect all external and internal hrefs from url
    for href in soup.find_all('a', href=True):
        dots = [x.start(0) for x in re.finditer('\.', href['href'])]
        if hostname in href['href'] or domain in href['href'] or len(dots) == 1 or not href['href'].startswith('http'):
            if "#" in href['href'] or "javascript" in href['href'].lower() or "mailto" in href['href'].lower():
                 Anchor['unsafe'].append(href['href']) 
            if not href['href'].startswith('http'):
                if not href['href'].startswith('/'):
                    Href['internals'].append(hostname+'/'+href['href']) 
                elif href['href'] in Null_format:
                    Href['null'].append(href['href'])  
                else:
                    Href['internals'].append(hostname+href['href'])   
        else:
            Href['externals'].append(href['href'])
            Anchor['safe'].append(href['href'])

    # # collect all media src tags
    for img in soup.find_all('img', src=True):
        dots = [x.start(0) for x in re.finditer('\.', img['src'])]
        if hostname in img['src'] or domain in img['src'] or len(dots) == 1 or not img['src'].startswith('http'):
            if not img['src'].startswith('http'):
                if not img['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+img['src']) 
                elif img['src'] in Null_format:
                    Media['null'].append(img['src'])  
                else:
                    Media['internals'].append(hostname+img['src'])   
        else:
            Media['externals'].append(img['src'])
           
    
    for audio in soup.find_all('audio', src=True):
        dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
        if hostname in audio['src'] or domain in audio['src'] or len(dots) == 1 or not audio['src'].startswith('http'):
             if not audio['src'].startswith('http'):
                if not audio['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+audio['src']) 
                elif audio['src'] in Null_format:
                    Media['null'].append(audio['src'])  
                else:
                    Media['internals'].append(hostname+audio['src'])   
        else:
            Media['externals'].append(audio['src'])
            
    for embed in soup.find_all('embed', src=True):
        dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
        if hostname in embed['src'] or domain in embed['src'] or len(dots) == 1 or not embed['src'].startswith('http'):
             if not embed['src'].startswith('http'):
                if not embed['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+embed['src']) 
                elif embed['src'] in Null_format:
                    Media['null'].append(embed['src'])  
                else:
                    Media['internals'].append(hostname+embed['src'])   
        else:
            Media['externals'].append(embed['src'])
           
    for i_frame in soup.find_all('iframe', src=True):
        dots = [x.start(0) for x in re.finditer('\.', i_frame['src'])]
        if hostname in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1 or not i_frame['src'].startswith('http'):
            if not i_frame['src'].startswith('http'):
                if not i_frame['src'].startswith('/'):
                    Media['internals'].append(hostname+'/'+i_frame['src']) 
                elif i_frame['src'] in Null_format:
                    Media['null'].append(i_frame['src'])  
                else:
                    Media['internals'].append(hostname+i_frame['src'])   
        else: 
            Media['externals'].append(i_frame['src'])
           

    # # collect all link tags
    for link in soup.findAll('link'):
        url_link = link.get('href', None)
        dots = [x.start(0) for x in re.finditer('\.', url_link)]
        if hostname in url_link or domain in url_link or len(dots) == 1 or not url_link.startswith('http'):
            if not url_link.startswith('http'):
                if not url_link.startswith('/'):
                    Link['internals'].append(hostname+'/'+url_link) 
                elif url_link in Null_format:
                    Link['null'].append(url_link)  
                else:
                    Link['internals'].append(hostname+url_link)   
        else:
            Link['externals'].append(url_link)

    for script in soup.find_all('script', src=True):
        dots = [x.start(0) for x in re.finditer('\.', script['src'])]
        if hostname in script['src'] or domain in script['src'] or len(dots) == 1 or not script['src'].startswith('http'):
            if not script['src'].startswith('http'):
                if not script['src'].startswith('/'):
                    Link['internals'].append(hostname+'/'+script['src']) 
                elif script['src'] in Null_format:
                    Link['null'].append(script['src'])  
                else:
                    Link['internals'].append(hostname+script['src'])   
        else:
            Link['externals'].append(link['href'])
           
            
    # collect all css
    for link in soup.find_all('link', rel='stylesheet'):
        dots = [x.start(0) for x in re.finditer('\.', link['href'])]
        if hostname in link['href'] or domain in link['href'] or len(dots) == 1 or not link['href'].startswith('http'):
            if not link['href'].startswith('http'):
                if not link['href'].startswith('/'):
                    CSS['internals'].append(hostname+'/'+link['href']) 
                elif link['href'] in Null_format:
                    CSS['null'].append(link['href'])  
                else:
                    CSS['internals'].append(hostname+link['href'])   
        else:
            CSS['externals'].append(link['href'])
    
    for style in soup.find_all('style', type='text/css'):
        try: 
            start = str(style[0]).index('@import url(')
            end = str(style[0]).index(')')
            css = str(style[0])[start+12:end]
            dots = [x.start(0) for x in re.finditer('\.', css)]
            if hostname in css or domain in css or len(dots) == 1 or not css.startswith('http'):
                if not css.startswith('http'):
                    if not css.startswith('/'):
                        CSS['internals'].append(hostname+'/'+css) 
                    elif css in Null_format:
                        CSS['null'].append(css)  
                    else:
                        CSS['internals'].append(hostname+css)   
            else: 
                CSS['externals'].append(css)
        except:
            continue
            
    # collect all form actions
    for form in soup.findAll('form', action=True):
        dots = [x.start(0) for x in re.finditer('\.', form['action'])]
        if hostname in form['action'] or domain in form['action'] or len(dots) == 1 or not form['action'].startswith('http'):
            if not form['action'].startswith('http'):
                if not form['action'].startswith('/'):
                    Form['internals'].append(hostname+'/'+form['action']) 
                elif form['action'] in Null_format or form['action'] == 'about:blank':
                    Form['null'].append(form['action'])  
                else:
                    Form['internals'].append(hostname+form['action'])   
        else:
            Form['externals'].append(form['action'])
            

    # collect all link tags
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
            if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link['href'].startswith('http'):
                if not head.link['href'].startswith('http'):
                    if not head.link['href'].startswith('/'):
                        Favicon['internals'].append(hostname+'/'+head.link['href']) 
                    elif head.link['href'] in Null_format:
                        Favicon['null'].append(head.link['href'])  
                    else:
                        Favicon['internals'].append(hostname+head.link['href'])   
            else:
                Favicon['externals'].append(head.link['href'])
                
        for head.link in soup.findAll('link', {'href': True, 'rel':True}):
            isicon = False
            if isinstance(head.link['rel'], list):
                for e_rel in head.link['rel']:
                    if (e_rel.endswith('icon')):
                        isicon = True
            else:
                if (head.link['rel'].endswith('icon')):
                    isicon = True
       
            if isicon:
                 dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                 if hostname in head.link['href'] or len(dots) == 1 or domain in head.link['href'] or not head.link['href'].startswith('http'):
                     if not head.link['href'].startswith('http'):
                        if not head.link['href'].startswith('/'):
                            Favicon['internals'].append(hostname+'/'+head.link['href']) 
                        elif head.link['href'] in Null_format:
                            Favicon['null'].append(head.link['href'])  
                        else:
                            Favicon['internals'].append(hostname+head.link['href'])   
                 else:
                     Favicon['externals'].append(head.link['href'])
                     
                    
    # collect i_frame
    for i_frame in soup.find_all('iframe', width=True, height=True, frameborder=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameborder'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, border=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['border'] == "0":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
    for i_frame in soup.find_all('iframe', width=True, height=True, style=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['style'] == "border:none;":
            IFrame['invisible'].append(i_frame)
        else:
            IFrame['visible'].append(i_frame)
          
    # get page title
    try:
        Title = soup.title.string
    except:
        pass
    
    # get content text
    Text = soup.get_text()

    
    
    return Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text, soup


#################################################################################################################################
#              Calculate features from extracted data
#################################################################################################################################


def extract_features(url,status):
    
    
    def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())   
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None,raw_words))
        return raw_words, list(filter(None,w_host)), list(filter(None,w_path))

    
    Href = {'internals':[], 'externals':[], 'null':[]}
    Link = {'internals':[], 'externals':[], 'null':[]}
    Anchor = {'safe':[], 'unsafe':[], 'null':[]}
    Media = {'internals':[], 'externals':[], 'null':[]}
    Form = {'internals':[], 'externals':[], 'null':[]}
    CSS = {'internals':[], 'externals':[], 'null':[]}
    Favicon = {'internals':[], 'externals':[], 'null':[]}
    IFrame = {'visible':[], 'invisible':[], 'null':[]}
    Title =''
    Text= ''

    try: 
        state, iurl, page = is_URL_accessible(url) 
    except Exception as e:
        print("url status error: " + str(e))
    if state:
        content = page.content
        hostname, domain, path = get_domain(url)
        extracted_domain = tldextract.extract(url)
        domain = extracted_domain.domain+'.'+extracted_domain.suffix
        subdomain = extracted_domain.subdomain
        tmp = url[url.find(extracted_domain.suffix):len(url)]
        pth = tmp.partition("/")
        path = pth[1] + pth[2]
        words_raw, words_raw_host, words_raw_path= words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
        tld = extracted_domain.suffix
        parsed = urlparse(url)
        scheme = parsed.scheme
        
        try:
            Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text , rawText= extract_data_from_URL(hostname, content, domain, Href, Link, Anchor, Media, Form, CSS, Favicon, IFrame, Title, Text)
        except Exception as e:
            print('e = ', e)
        
        row = [
               # url-based features
               urlfe.url_length(url),
               urlfe.url_length(hostname),
               urlfe.having_ip_address(url),
               urlfe.count_dots(url),
               urlfe.count_hyphens(url),
               urlfe.count_at(url),
               urlfe.count_exclamation(url),
               urlfe.count_and(url),
               urlfe.count_or(url),
               urlfe.count_equal(url),
               urlfe.count_underscore(url),
               urlfe.count_tilde(url),
               urlfe.count_percentage(url),
               urlfe.count_slash(url),
               urlfe.count_star(url),
               urlfe.count_colon(url),
               urlfe.count_comma(url),
               urlfe.count_semicolumn(url),
               urlfe.count_dollar(url),
               urlfe.count_space(url),
               
               urlfe.check_www(words_raw),
               urlfe.check_com(words_raw),
               urlfe.count_double_slash(url),
               urlfe.count_http_token(path),
               urlfe.https_token(scheme),
               
               urlfe.ratio_digits(url),
               urlfe.ratio_digits(hostname),
               urlfe.punycode(url),
               urlfe.port(url),
               urlfe.tld_in_path(tld, path),
               urlfe.tld_in_subdomain(tld, subdomain),
               urlfe.abnormal_subdomain(url),
               urlfe.count_subdomain(url),
               urlfe.prefix_suffix(url),
            #    urlfe.random_domain(domain),
               urlfe.shortening_service(url),
               
               
               urlfe.path_extension(path),
               urlfe.count_redirection(page),
               urlfe.count_external_redirection(page, domain),
               urlfe.length_word_raw(words_raw),
               urlfe.char_repeat(words_raw),
               urlfe.shortest_word_length(words_raw),
               urlfe.shortest_word_length(words_raw_host),
               urlfe.shortest_word_length(words_raw_path),
               urlfe.longest_word_length(words_raw),
               urlfe.longest_word_length(words_raw_host),
               urlfe.longest_word_length(words_raw_path),
               urlfe.average_word_length(words_raw),
               urlfe.average_word_length(words_raw_host),
               urlfe.average_word_length(words_raw_path),
               
               urlfe.phish_hints(url),  
               urlfe.domain_in_brand(extracted_domain.domain),
               urlfe.brand_in_path(extracted_domain.domain,subdomain),
               urlfe.brand_in_path(extracted_domain.domain,path),
               urlfe.suspecious_tld(tld),
               urlfe.statistical_report(url, domain),
               # # # content-based features
               # ctnfe.nb_hyperlinks(content),
            #    ctnfe.internal_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
            #    ctnfe.external_hyperlinks(Href, Link, Media, Form, CSS, Favicon),
            #    ctnfe.null_hyperlinks(hostname, Href, Link, Media, Form, CSS, Favicon),
            #   ctnfe.external_css(CSS),
            #      ctnfe.internal_redirection(Href, Link, Media, Form, CSS, Favicon),
            #      ctnfe.external_redirection(Href, Link, Media, Form, CSS, Favicon),
            #      ctnfe.internal_errors(Href, Link, Media, Form, CSS, Favicon),
            #      ctnfe.external_errors(Href, Link, Media, Form, CSS, Favicon),
                ctnfe.login_form(Form),
                ctnfe.external_favicon(Favicon),
                ctnfe.links_in_tags(Link),
                ctnfe.submitting_to_email(Form),
                ctnfe.internal_media(Media),
                ctnfe.external_media(Media),
            #    #  # additional content-based features
                ctnfe.sfh(hostname,Form),
                ctnfe.iframe(IFrame),
                ctnfe.popup_window(Text),
                ctnfe.safe_anchor(Anchor),
                ctnfe.onmouseover(Text),
                ctnfe.right_clic(Text),
                ctnfe.empty_title(Title),
                ctnfe.domain_in_title(extracted_domain.domain, Title),
                ctnfe.domain_with_copyright(extracted_domain.domain, Text),
                 
            #     # # # thirs-party-based features
                trdfe.whois_registered_domain(domain), 
                trdfe.domain_registration_length(domain),
                # trdfe.domain_age(domain),
                # trdfe.web_traffic(url),
                trdfe.dns_record(domain),
                # trdfe.google_index(url),
                trdfe.page_rank(key,domain),
               status]
        # print("Row: ", row)
        return row
        # return None
    return None










#################################################################################################################################
#             Intialization
#################################################################################################################################



ctn_headers = [
                #    'nb_hyperlinks', 
                #    'ratio_intHyperlinks',
                #    'ratio_extHyperlinks', 
                #    'ratio_nullHyperlinks',
                #    'nb_extCSS',
                #    'ratio_intRedirection',
                #    'ratio_extRedirection',
                #    'ratio_intErrors',
                #    'ratio_extErrors',
                   'login_form', 
                   'external_favicon',
                   'links_in_tags',
                   'submit_email', 
                   'ratio_intMedia',
                   'ratio_extMedia',
                   'sfh',
                   'iframe',
                   'popup_window',
                   'safe_anchor', 
                   'onmouseover',
                   'right_clic',
                   'empty_title', 
                   'domain_in_title',
                   'domain_with_copyright',
                                       
                ]

ctn_hyperlinks_headers = [
                   'nb_hyperlinks', 
                   'ratio_intHyperlinks',
                   'ratio_extHyperlinks', 
                   'ratio_nullHyperlinks',
                   'nb_extCSS',
                   'ratio_intRedirection',
                   'ratio_extRedirection',
                   'ratio_intErrors',
                   'ratio_extErrors',
                   'external_favicon',
                   'links_in_tags',
                   'ratio_intMedia',
                   'ratio_extMedia'
                ]

ctn_abnormalness_headers = [
                   'login_form', 
                   'submit_email', 
                   'sfh',
                   'iframe',
                   'popup_window',
                   'safe_anchor', 
                   'onmouseover',
                   'right_clic',
                   'empty_title', 
                   'domain_in_title',
                   'domain_with_copyright'
                                       
                ]


    
url_headers = [    'length_url',                                  
                   'length_hostname',
                   'ip',
                   'nb_dots',
                   'nb_hyphens',
                   'nb_at',
                   'nb_qm',
                   'nb_and',
                   'nb_or',
                   'nb_eq',                  
                   'nb_underscore',
                   'nb_tilde',
                   'nb_percent',
                   'nb_slash',
                   'nb_star',
                   'nb_colon',
                   'nb_comma',
                   'nb_semicolumn',
                   'nb_dollar',
                   'nb_space',
                   'nb_www',
                   'nb_com',
                   'nb_dslash',
                   'http_in_path',
                   'https_token',
                   'ratio_digits_url',
                   'ratio_digits_host',
                   'punycode',
                   'port',
                   'tld_in_path',
                   'tld_in_subdomain',
                   'abnormal_subdomain',
                   'nb_subdomains',
                   'prefix_suffix',
                   # 'random_domain',
                   'shortening_service',
                   'path_extension',
                   
                   'nb_redirection',
                   'nb_external_redirection',
                   'length_words_raw',
                   'char_repeat',
                   'shortest_words_raw',
                   'shortest_word_host',
                   'shortest_word_path',
                   'longest_words_raw',
                   'longest_word_host',
                   'longest_word_path',
                   'avg_words_raw',
                   'avg_word_host',
                   'avg_word_path',
                   'phish_hints',
                   'domain_in_brand',
                   'brand_in_subdomain',
                   'brand_in_path',
                   'suspecious_tld',
                   'statistical_report'

                ]

url_struct_headers = [    
                   'ip',
                   'https_token',
                   'punycode',
                   'port',
                   'tld_in_path',
                   'tld_in_subdomain',
                   'abnormal_subdomain',
                   'prefix_suffix',
                   'random_domain',
                   'shortening_service',
                   'path_extension',
                   
                   'domain_in_brand',
                   'brand_in_subdomain',
                   'brand_in_path',
                   'suspecious_tld',
                   'statistical_report'
                ]



url_stat_headers = [    
                    'length_url',                                  
                   'length_hostname',
                   'nb_dots',
                   'nb_hyphens',
                   'nb_at',
                   'nb_qm',
                   'nb_and',
                   'nb_or',
                   'nb_eq',                  
                   'nb_underscore',
                   'nb_tilde',
                   'nb_percent',
                   'nb_slash',
                   'nb_star',
                   'nb_colon',
                   'nb_comma',
                   'nb_semicolumn',
                   'nb_dollar',
                   'nb_space',
                   'nb_www',
                   'nb_com',
                   'nb_dslash',
                   'http_in_path',
                   'ratio_digits_url',
                   'ratio_digits_host',
                   'nb_subdomains',
                   
                   
                   'nb_redirection',
                   'nb_external_redirection',
                   'length_words_raw',
                   'char_repeat',
                   'shortest_words_raw',
                   'shortest_word_host',
                   'shortest_word_path',
                   'longest_words_raw',
                   'longest_word_host',
                   'longest_word_path',
                   'avg_words_raw',
                   'avg_word_host',
                   'avg_word_path',
                   'phish_hints',
                ]


tpt_headers = [
                   # 'phish_hints', 
                   'whois_registered_domain',
                   'domain_registration_length',
                   # 'domain_age', 
                   # 'web_traffic',
                   'dns_record',
                   # 'google_index',
                   'page_rank'
                   # 'domain_in_brand',
                   # 'brand_in_path',
                   # 'suspecious_tld',
                   # 'statistical_report'
                ]
ctn_new_headers = [
                    'host', 
                    'page_entropy', 
                    'num_script_tags', 
                    'script_to_body_ratio', 
                    'html_length', 
                    'page_tokens', 
                    'num_sentences', 
                    'num_punctuations', 
                    'distinct_tokens', 
                    'capitalizations', 
                    'avg_tokens_per_sentence', 
                    'num_html_tags', 
                    'num_hidden_tags',
                    'num_iframes', 
                    'num_embeds', 
                    'num_objects', 
                    'hyperlinks', 
                    'num_whitespaces', 
                    'num_included_elemets',
                    'num_double_documents', 
                    'num_suspicious_elements', 
                    'num_eval_functions', 
                    'avg_script_length', 
                    'avg_script_entropy', 
                    'num_suspicious_functions'
]

hsfe_headers = [
                    "num_subdomains", 
                    "registration_date",
                    "expiration_date",
                    "last_updates_dates",
                    "age",
                    "intended_life_span",
                    "life_remaining",
                    "registrar",
                    "reg_country",
                    "host_country",
                    "open_ports",
                    "num_open_ports",
                    "is_live",
                    "isp",
                    "connection_speed",
                    #"first_seen",
                    #"last_seen",
                    #"days_since_last_seen",
                    #"days_since_first_seen",
                    "avg_update_days",
                    "total_updates",
                    "ttl"
]

lxfe_headers = [
                'tld',
                'scheme',
                'url_length',
                'path_length',
                'host_length',
                'host_is_ip',
                'has_port_in_string',
                'num_digits',
                'parameters',
                'fragments',
                'is_encoded',
                'string_entropy',
                'alexa_dis_similarity',
                'subdirectories',
                'periods',
                'has_client',
                'has_login',
                'has_admin',
                'has_server',
                'num_encoded_chars'
]


l_models = ['Random Forest', 
                'SVM', #'XGBoost', 
                'Logistic Regression', 
                'Decision Tree', 
                'KNeighbors', 
                'SGD',
                'Gaussian Naive Bayes', 
                'MLP'
            ]

headers = ctn_new_headers + hsfe_headers + lxfe_headers + url_headers + ctn_headers + tpt_headers 

#################################################################################################################################
#              Generate datasets
#################################################################################################################################
import shutil
def removeFolder(folderName):
    try:
        shutil.rmtree(folderName)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

def main_forScreenshot():
    try:
        os.mkdir("results")
    except FileExistsError:
        print("WAR: Directory already exists")
    # read cache
    db = pd.read_csv('data/cache.csv', on_bad_lines='skip')
    cache = list(db['url'])
    cache = list(set(cache))

    dataset = pd.read_csv('data/data_final.csv')
    lst = list(dataset['url'])
    lst = list(set(lst))
    


    i = 0 
    nb = 0
    
    nb = len(cache)
    i = nb
    
    for row in lst:
        #url = 'https://'+row['domain']
        url = row
        print("\nTake screenshot for ", url)
        
        if url not in cache:
            if take_screenshot(url):
                state = 'OK'
                nb +=1 
            else:
                state = 'Er'

            with open('data/cache.csv', 'a', newline="") as cachefile :
                print("Saved to cache file ", url)
                writer = csv.writer(cachefile)
                writer.writerow([url])
                cachefile.close()
        else:
           state = 'Cached' 
           i -=1
        i+=1
        print('[',state,']',nb,'succeded from:', i)
        print("----------------------------------------------------------------\n")



def generate_external_dataset(lst_url = "", header = headers):
    
    
    


    try:
        os.mkdir(base_dir + r"\results")
    except FileExistsError:
        print("WAR: Directory already exists")
    lst_url = lst_url.strip()
    lst_url = lst_url.split("\r\n")

    print("LIST URL:\n", lst_url)


    if not os.path.isfile(cache_file_dir) :
        with open(cache_file_dir, 'w', newline="") as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['url'])
            csvfile.close()
    else:
        os.remove(cache_file_dir)
        with open(cache_file_dir, 'w', newline="") as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['url'])
            csvfile.close()

    # read cache
    db = pd.read_csv(cache_file_dir, on_bad_lines='skip')
    cache = list(db['url'])
    cache = list(set(cache))

    
    lst = lst_url

    i = 0 
    nb = 0
    
    if not os.path.isfile(results_file_dir) :
        with open(results_file_dir, 'w', newline="") as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['url']+header+['tag'])
            csvfile.close()
    else:
        os.remove(results_file_dir)
        with open(results_file_dir, 'w', newline="") as csvfile :
            writer = csv.writer(csvfile)
            writer.writerow(['url']+header+['tag'])
            csvfile.close()
        nb = len(cache)
        i = nb
        

    for row in lst:
        #url = 'https://'+row['domain']
        url = row
        print("\nExtract feature for ", url)
        status = "phishing"
        #status = "normal"
        if url not in cache:
            take_screenshot(url)
            try:
                res = extract_features(url, status)
                ft = ctnfe_new.ContentFeatures(url).run()
                hfe = htfe.HostFeatures(url).run()
                lfe = lxfe.LexicalURLFeature(url).run()
            except Exception as e: 
                print("Res Error: ", e)
                res = None
                ft = None
                hfe = None
                lfe = None

                
                pass
            # print("RRES: ", res)
            if res and ft and hfe and lfe:
                url = url.split(" ")

                ft = list(ft.values())
                ft = url + ft

                hfe = list(hfe.values())

                lfe = list(lfe.values())

                with open(results_file_dir, 'a', newline="") as csvfile :
                    writer = csv.writer(csvfile)
                    writer.writerow(ft + hfe + lfe + res)
                    csvfile.close()
                
                
                state = 'OK'
                
                nb +=1 
            else:
                state = 'Er'

            with open(cache_file_dir, 'a', newline="") as cachefile :
                writer = csv.writer(cachefile)
                writer.writerow(url)
                cachefile.close()
        else:
           state = 'Cached' 
        i+=1
        print('[',state,']',nb,'succeded from:', i)
        print("----------------------------------------------------------------\n")

    


# if __name__ == '__main__':
    # generate_external_dataset(headers)
    # main_forScreenshot()
    # content features 63 
