import numpy as np
from googlesearch import search as search1
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QMessageBox
from os import popen
import requests
from bs4 import BeautifulSoup

# def extract_links_from_google(soup):
#     links = []
#     for link in soup.find_all('a'):
#         href = link.get('href')
#         if href.startswith('/url?q='):
#             url = href.split('/url?q=')[1].split('&')[0]
#             links.append(url)
#     return links

def extract_links_from_bing(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def extract_links_from_yahoo(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def extract_links_from_duckduckgo(soup):
    links = []
    for link in soup.find_all('a', {'class': 'result__a'}):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def extract_links_from_ask(soup):
    links = []
    for link in soup.find_all('a', {'class': 'PartialSearchResults-item-title-link result-link'}):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def extract_links_from_yandex(soup):
    links = []
    for link in soup.find_all('a', {'class': 'link link_theme_normal organic__url link_cropped_no i-bem'}):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def extract_links_from_aol(soup):
    links = []
    for link in soup.find_all('a', {'class': 'ac-algo fz-l ac-21th lh-24'}):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    return links

def search_links_from_alltheinternet(search_url, query, num_results):
    links = []
    count = 1
    while count <= num_results or len(links) <= num_results:
        
        response = requests.get(search_url+f"#gsc.tab=0&gsc.q={query}&gsc.page={count}")
        #print(response.text)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    links.append(href)
        count += 1
    return links

def grab():
    dork = w.dork.text()
    thread = w.thread.text()
    
    if (not( w.b1.isChecked() or
             w.b2.isChecked() or 
             w.b3.isChecked() or
             w.b4.isChecked() or
             w.b5.isChecked() or
             w.b6.isChecked() or
             w.b7.isChecked() or
             w.b8.isChecked() or
             w.boost.isChecked())):
        QMessageBox.critical(w, 'Warning', 'choose an options')

    if w.b1.isChecked() and w.b8.isChecked() == False:
        result = list(search1(dork, num_results=int(thread)))

    if w.b2.isChecked() and w.b8.isChecked() == False:
        result = search(dork, 'Bing') 

    if w.b3.isChecked() and w.b8.isChecked() == False:
        result = search(dork, 'Yahoo') 

    if w.b4.isChecked() and w.b8.isChecked() == False:
        result = search(dork, 'DuckDuckGo') 

    if w.b7.isChecked() and w.b8.isChecked() == False:
        result = search(dork, 'Ask') 
 
    if w.b6.isChecked() and w.b8.isChecked() == False:
        result = search(dork, 'Yandex') 
        
    if w.b5.isChecked() and w.b8.isChecked() == False:
        result = search(dork, 'AOL') 

    if w.b8.isChecked() and w.boost.isChecked() == False:
        result = search(dork, 'All')  
    
    with open("hits.txt", "w") as f:
        f.writelines(result)
    
    i = 0
    ok = False
    while ok == False:
        try:
            w.table.insertRow(i)
            w.table.setItem(i, 0, QTableWidgetItem(result[i]))
            i = i + 1
        except:
            ok = True

def search(query, engines=None, thread=10):
    search_engines = {
        "Google": "https://www.google.com/search?q=",
        "Bing": "https://www.bing.com/search?q=",
        "Yahoo": "https://search.yahoo.com/search?p=",
        "DuckDuckGo": "https://duckduckgo.com/html/?q=",
        "Ask": "https://www.ask.com/web?q=",
        "Yandex": "https://yandex.com/search/?text=",
        "AOL": "https://search.aol.com/aol/search?q=",
        "alltheinternet": "https://www.alltheinternet.com/?q=",
    }

    lst = []
    if engines == 'All':
        for i in search_engines.keys():
            links = []
            search_url = search_engines[i] + query
            response = requests.get(search_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if i == 'Google':
                    try:
                        links = list(search1(query, num_results=int(thread)))
                    except:
                        pass
                    
                elif i == "Bing":
                    links = extract_links_from_bing(soup)
                elif i == "Yahoo":
                    links = extract_links_from_yahoo(soup)
                elif i == "DuckDuckGo":
                    links = extract_links_from_duckduckgo(soup)
                elif i == "Ask":
                    links = extract_links_from_ask(soup)
                elif i == "Yandex":
                    links = extract_links_from_yandex(soup)
                elif i == "AOL":
                    links = extract_links_from_aol(soup)
                elif i == "alltheinternet":
                    links = search_links_from_alltheinternet(search_url, query, thread)
                lst.extend(links)
                #print(links)
        return lst
    
    search_url = search_engines[engines] + query
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if engines == "Bing":
            links = extract_links_from_bing(soup)
        elif engines == "Yahoo":
            links = extract_links_from_yahoo(soup)
        elif engines == "DuckDuckGo":
            links = extract_links_from_duckduckgo(soup)
        elif engines == "Ask":
            links = extract_links_from_ask(soup)
        elif engines == "Yandex":
            links = extract_links_from_yandex(soup)
        elif engines == "AOL":
            links = extract_links_from_aol(soup)
        elif engines == "Gigablast":
            links = search_links_from_alltheinternet(search_url, query, thread)
        # Add more conditions for other search engines if needed

    else:
        print(f"Failed to fetch results from {engines}")
    return links


def clear():
    # w.dork.setText("")
    # w.thread.setText("")
    # w.b1.setChecked(False)
    # w.b2.setChecked(False)
    # w.b3.setChecked(False)
    # w.b4.setChecked(False)
    # w.b5.setChecked(False)
    # w.b6.setChecked(False)
    # w.b7.setChecked(False)
    # w.b8.setChecked(False)
    # w.gra.setChecked(False)
    # w.sys.setChecked(False)
    w.table.clear()
    QMessageBox.information(w, 'info', 'cleaning success~!')


def shutdown():
    if w.sys.isChecked():
        popen("shutdown /s /f")
    elif w.gra.isChecked():
        w.close()

app = QApplication([])
w = loadUi("app.ui")
w.show()

w.thread.setText('10')
w.hit.clicked.connect(grab)
w.clear.clicked.connect(clear)
w.shut.clicked.connect(shutdown)

app.exec_()