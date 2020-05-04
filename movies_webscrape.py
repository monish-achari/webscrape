import requests
from bs4 import BeautifulSoup

def movie_details(url):
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    class_var = 'mt20 mb20 hidden-xs hidden-sm torrent-qualities'
    mv_data = html_soup.find_all('div',class_=class_var)
    movie_genre =  html_soup.find_all('div',class_='hidden-xs')
    a_toren = mv_data[0].div.div.a
    a_toren['title'] = movie_genre[0].h1.text 
    a_toren['genre'] = movie_genre[0].h1.find_next().find_next('h2').text
    a_toren['year'] = movie_genre[0].h1.find_next('h2').text
    del a_toren['rel'] 
    del a_toren['class']
    return a_toren.attrs

def main_fun(DOMAIN,main_exclude_domain_url): 
    response = requests.get(main_exclude_domain_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    class_var = '__main mClearfix'
    mv_data = html_soup.find_all('div',class_=class_var)
    amv_data = mv_data[0].find_all('div',class_='card')
    all_movies= []
    for num,j in enumerate(amv_data):
        sub_data = amv_data[num].a.attrs
        sub_url = DOMAIN + sub_data.get('href')
        movie_as_key = sub_data.get('title').replace(' ','_')
        movie_lists = movie_details(sub_url) 
        all_movies.append({movie_as_key:movie_lists})
    return all_movies

DOMAIN = "https://yts.ms"
main_exclude_domain_url = DOMAIN + '/browse-movies'
main_fun(DOMAIN,main_exclude_domain_url)