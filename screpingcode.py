import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
URL = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
# import ipdb; ipdb.set_trace()
#TASK-1
def scrap_to_tist():
    
    sample = requests.get(URL)
    soup = BeautifulSoup(sample.text,"html.parser") 
    
    tbody=soup.find('tbody',class_="lister-list")
    trs = tbody.findAll('tr')
    whole_data = []
    j=0
    for i in  trs :
        new={}
        position =j=j+1
        
        name = i.find('td',class_="titleColumn").a.get_text()
        # print name
        year = i.find('td',class_="titleColumn").span.get_text()
        # print year
        reng = i.find('td',class_="ratingColumn").get_text()
        # print reng
        link = i.find("a",href=True)
        movie_link = "https://www.imdb.com/"+link["href"]
        # print movie_link
        new['position']=position
        new['name']=name
        new['year']=int(year[1:5])
        new['reting']=float(reng)
        new['url']=movie_link
        
        whole_data.append(new)
        with open("250_movies_data.json","w") as fs:
                json.dump(whole_data,fs,indent = 1 )

    return whole_data

scrept = scrap_to_tist()
#pprint (scrept)

#TASK-2
def group_by_year(movi):
        years=[]
        for i in movi:
                year=i["year"]
                if year not in years:
                        years.append(year)
               
        movie_dict={i:[]for i in years}
        for i in movi:
                year=i["year"]
                for x in movie_dict:
                        if str(x)==str(year):
                                movie_dict[x].append(i)

        with open("yearwise_data.json","w") as fs:
                json.dump(movie_dict,fs,indent = 1 )

        return movie_dict
year_by_data = group_by_year(scrept) 
#print year_by_data
#TASK-3

def group_by_decade(movies):
        moviedec={}
        list1=[]
        for index in movies:
                mod=index%10
                # print mode
                decade=index-mod
                # print decade
                if decade not in list1:
                        list1.append(decade)
        list1.sort()

        for i in list1:
                moviedec[i]=[]
        for i in moviedec:
                drc10=i+9
                for x in movies:
                        if x <= drc10 and x >= i:
                                for v in movies[x]:
                                        moviedec[i].append(v)
                with open("decades.json","w") as fs:
                        json.dump(moviedec,fs,indent = 1 )

        return (moviedec)                              
#print group_by_decade(year_by_data)

#TASK-4

def scrape_top_list(movie_url):
        new={}
        sample = requests.get(movie_url)
        soup = BeautifulSoup(sample.text,"html.parser") 
        
        movie_name=soup.find('h1',class_="").get_text().split("(")
        # return movie_name[0]
        
        movie_Directors=soup.find('div',class_="credit_summary_item")
        director_list = movie_Directors.findAll("a")
        director_name=[]
        for i in director_list:
                director_name.append(i.get_text())
        # return director_name
        

        movie_poster_link = soup.find("div",class_="poster").a["href"]
        movie_poster = "https://www.imdb.com"+movie_poster_link
        # return movie_poster
        
        movies_bio=soup.find("div",class_="summary_text").get_text().strip()
        # return movies_bio
        movie_genres1=soup.find("div",class_="subtext")
        gener = movie_genres1.findAll("a")
        gener.pop()
        movie_gener=[]
        for i in gener:
                movie_gener.append(i.get_text())
        # return movie_gener
        extra_details = soup.find("div", attrs={"class":"article","id":"titleDetails"})
        list_of_div = extra_details.find_all("div")
        for div in list_of_div:
                tag_h4 = div.find_all("h4")
                for text in tag_h4:
                        if "Language:" in text:
                            tag_anchor = div.find_all("a")
                            movie_language = [language.get_text() for language in tag_anchor]
                        elif "Country:" in text:
                            tag_anchor = div.find_all("a")
                            movie_country = "".join([country.get_text() for country in tag_anchor])
			# elif "Runtime" in text:
			#     tag_anchor = div.find("time")
			#     movie_runtime = tag_anchor.get_text() 
        # return movie_language
        # return movie_country 
        # return movie_runtime
	
        movie_time=soup.find("div",class_="subtext")
        run_time=movie_time.find("time").get_text().strip()
        run_time_hours=int(run_time[0])*60
        run_minuts=0
        if 'min' in run_time:
                run_minuts=int(run_time[3:].strip("min"))
                movie_runtime=run_time_hours+ run_minuts
        else:
                movie_runtime=run_time_hours         
        # return movie_runtime

        new["name"]= movie_name[0]
        new["director"]=director_name
        new["country"]=movie_country
        new["language"]=movie_language
        new["poster_image_url"]=movie_poster
        new["bio"]=(movies_bio)
        new["runtime"]=movie_runtime
        new["genre"]=movie_gener
        
        
        with open("one_url_ditels.json","w") as fs:
                json.dump(new,fs,indent = 1 )
        #return new
url1 = scrept[0]["url"] 
one_movie_data = scrape_top_list(url1)
# print (one_movie_data)

#TASK-5
storage = []
def scrape_top_list(movie_url):
        new={}
        sample = requests.get(movie_url)
        soup = BeautifulSoup(sample.text,"html.parser") 
        
        movie_name=soup.find('h1',class_="").get_text().split("(")
        # return movie_name[0]
        
        movie_Directors=soup.find('div',class_="credit_summary_item")
        director_list = movie_Directors.findAll("a")
        director_name=[]
        for i in director_list:
                director_name.append(i.get_text())
        # return director_name
        # return movie_Directors[0]

        movie_poster_link = soup.find("div",class_="poster").a["href"]
        movie_poster = "https://www.imdb.com"+movie_poster_link
        # return movie_poster
        
        movies_bio=soup.find("div",class_="summary_text").get_text().strip()
        # return movies_bio
        movie_genres1=soup.find("div",class_="subtext")
        gener = movie_genres1.findAll("a")
        gener.pop()
        movie_gener=[]
        for i in gener:
                movie_gener.append(i.get_text())
        # return movie_gener
        extra_details = soup.find("div", attrs={"class":"article","id":"titleDetails"})
        list_of_div = extra_details.find_all("div")
        for div in list_of_div:
                tag_h4 = div.find_all("h4")
                for text in tag_h4:
                        if "Language:" in text:
                            tag_anchor = div.find_all("a")
                            movie_language = [language.get_text() for language in tag_anchor]
                        elif "Country:" in text:
                            tag_anchor = div.find_all("a")
                            movie_country = "".join([country.get_text() for country in tag_anchor])
        # return movie_language
        # return movie_country 

        movie_time=soup.find("div",class_="subtext")
        run_time=movie_time.find("time").get_text().strip()
        run_time_hours=int(run_time[0])*60
        run_minuts=0
        if 'min' in run_time:
                run_minuts=int(run_time[3:].strip("min"))
                movie_runtime=run_time_hours+ run_minuts
        else:
                movie_runtime=run_time_hours         
        # # return movie_runtime
        
        new["name"]= movie_name[0]
        new["director"]=director_name
        new["country"]=movie_country
        new["language"]=movie_language
        new["poster_image_url"]=movie_poster
        new["bio"]=(movies_bio)
        new["runtime"]=movie_runtime
        new["genre"]=movie_gener
        
        storage.append(new)
        
        with open("m_10urls_ditels.json","w") as fs:
                json.dump(storage,fs,indent = 1 )
        
for i in range(10):
        url1 = scrept[i]["url"] 
        data = scrape_top_list(url1)
# print (storage)
# 

#task-6
def analyse_movies_language(movies_language_list):
        movie_language_details={}
        
        for movie_name in movies_language_list:
                
                if movie_name not in movie_language_details:

                        movie_language_details[movie_name] = 1
                else: 
                        movie_language_details[movie_name] += 1


        with open("language_data.json","w") as fs:
                json.dump(movie_language_details,fs,indent = 1 )
        return movie_language_details
movie_languages = []
for storage_language in storage:
        languages = storage_language["language"]
        movie_languages.extend(languages)
# print movie_languages
movies_language_count = analyse_movies_language(movie_languages)
# print movies_language_count

# # TASK-7

def analyse_movies_directors(movies_directors_list):
        movie_directors_details={}
        
        for directors_name in movies_directors_list:
                
                if directors_name not in movies_directors_list :

                        movie_directors_details[directors_name] = 1
                else: 
                        movie_directors_details[directors_name] += 1


        with open("directors_m.json","w") as fs:
                json.dump(movie_directors_details,fs,indent = 1 )
        return movie_directors_details
movie_directors = []
for storage_directors in storage:
        directors = storage_directors["director"]
        movie_directors.extend(directors)
print movie_directors
movies_directors_count = analyse_movies_directors(movie_directors)

# print movies_directors_count