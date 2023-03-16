from flask import Flask, render_template,request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen


app=Flask(__name__)

def tech_news(genre):
    file="https://inshorts.com/en/read/"+genre        
    news_url=urlopen(file).read()   
    clean_html=bs(news_url,'html.parser')
    container=clean_html.find_all('div',{"class":"news-card z-depth-1"})  
    
    extracted_data={}
    try:
        count=0
        
        for i in container:
            img=i.find('div',{"class":"news-card-image"})['style'].replace("background-image: url(",'')
            img=img.replace("?')",'')
            img=img.replace("'",'')
            
            extracted_data.setdefault(count,{
                "heading": (i.find('div',{"class":"news-card-title news-right-box"}).span.text),
                "news": (i.find('div',{"class":"news-card-content news-right-box"}).div.text),
                "img": (img)
            })
            count=count+1
            
            
    except Exception:
        pass
    
    return extracted_data




@app.route('/')
def index():
    extracted_data=tech_news('')
    return render_template('index.html',data=extracted_data)

@app.route('/tech')
def tech():
    extracted_data=tech_news("technology")
    return render_template('index.html',data=extracted_data)

@app.route('/india')
def india():
    extracted_data=tech_news("india")
    return render_template('index.html',data=extracted_data)

@app.route('/business')
def business():
    extracted_data=tech_news("business")
    return render_template('index.html',data=extracted_data)

@app.route('/sports')
def sports():
    extracted_data=tech_news("sports")
    return render_template('index.html',data=extracted_data)

@app.route('/world')
def world():
    extracted_data=tech_news("world")
    return render_template('index.html',data=extracted_data)

@app.route('/politics')
def politics():
    extracted_data=tech_news("politics")
    return render_template('index.html',data=extracted_data)

@app.route('/startup')
def startup():
    extracted_data=tech_news("startup")
    return render_template('index.html',data=extracted_data)

@app.route('/entertainment')
def entertainment():
    extracted_data=tech_news("entertainment")
    return render_template('index.html',data=extracted_data)

@app.route('/hatke')
def hatke():
    extracted_data=tech_news("hatke")
    return render_template('index.html',data=extracted_data)

@app.route('/science')
def science():
    extracted_data=tech_news("science")
    return render_template('index.html',data=extracted_data)

@app.route('/automobile')
def automobile():
    extracted_data=tech_news("automobile")
    return render_template('index.html',data=extracted_data)


if __name__=="__main__":
    app.run()