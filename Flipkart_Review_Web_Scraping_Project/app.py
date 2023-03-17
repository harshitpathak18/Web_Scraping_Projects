from flask import Flask,request,render_template
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

def flipkart(search):
    search=search.replace(" ","+")
    link=f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    
    
    try:
        try:
            req=urlopen(link)
            clean_html=bs(req.read(),'html.parser')
            a=clean_html.find_all('div',{"class":"_4ddWXP"})
            product_price=a[0].find('div',{"class":"_25b18c"}).div.text
            product_name=a[0].find('a',{"class":"s1Q9rs"}).text
            product_link="https://www.flipkart.com"+a[0].find('a',{"class":"s1Q9rs"})['href']
            product_image=a[0].find('img',{"class":"_396cs4"})['src']
            product_rating=a[0].find('div',{"class":"gUuXy- _2D5lwg"}).span.div.text
            product_total_rating=a[0].find('div',{"class":"gUuXy- _2D5lwg"}).find('span',{"class":"_2_R_DZ"}).text
            product_total_rating=product_total_rating.replace('(','')
            product_total_rating=product_total_rating.replace(')','')
            
            
            
            extracted_data={}
            try:
                count=0
                for i in a:
                    product_total_rating=i.find('div',{"class":"gUuXy- _2D5lwg"}).find('span',{"class":"_2_R_DZ"}).text
                    product_total_rating=product_total_rating.replace('(','')
                    product_total_rating=product_total_rating.replace(')','')
                    
                    extracted_data.setdefault(count,{
                        "link": "https://www.flipkart.com"+i.find('a',{"class":"s1Q9rs"})['href'],
                        "img": i.find('img',{"class":"_396cs4"})['src'],
                        "name": (i.find('a',{"class":"s1Q9rs"}).text),
                        "rating": (i.find('div',{"class":"gUuXy- _2D5lwg"}).span.div.text),
                        "price" :(i.find('div',{"class":"_25b18c"}).div.text),
                        "total_ratings": product_total_rating
                    })
                    count=count+1

            except Exception:
                pass
            
            
            
            

        except Exception:
            a=clean_html.find_all('div',{"class":"_2kHMtA"})
            product_price=a[1].find('div',{"class":"_30jeq3 _1_WHN1"}).text
            product_name=a[1].find('div',{"class":"_4rR01T"}).text
            product_link="https://www.flipkart.com"+a[0].a['href']
            product_image=a[1].find('img',{"class":"_396cs4"})['src']
            product_rating=a[1].find('div',{"class":"_3LWZlK"}).text
            product_total_rating=a[1].find('span',{"class":"_2_R_DZ"}).span.span.text
            product_total_rating=product_total_rating.replace(' Ratings\xa0','')
            
            
            extracted_data={}
            try:
                count=0
                for i in a:
                    product_total_rating=a[1].find('span',{"class":"_2_R_DZ"}).span.span.text
                    product_total_rating=product_total_rating.replace(' Ratings\xa0','')
                    
                    extracted_data.setdefault(count,{
                        "link": "https://www.flipkart.com"+i.a['href'],
                        "img": i.find('img',{"class":"_396cs4"})['src'],
                        "name": (i.find('div',{"class":"_4rR01T"}).text),
                        "rating": (i.find('div',{"class":"_3LWZlK"}).text),
                        "price" :(i.find('div',{"class":"_30jeq3 _1_WHN1"}).text),
                        "total_ratings": product_total_rating
                    })
                    count=count+1

            except Exception:
                pass
            
        return extracted_data
    
    except Exception:
        pass


app=Flask(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    if request.method=="POST":
        searched=request.form['search']
        extracted_data=flipkart(searched)
        
        return render_template('index.html',data=extracted_data)
        
    return render_template('index.html')


@app.route("/reviews",methods=['GET','POST'])
def reviews():    
    link=request.form['link']
    link=link.replace('/p/','/product-reviews/')
    product=urlopen(link).read()
    product_html=bs(product,'html.parser')  # beautify html
    product_container=product_html.find_all('div',{"class":"_27M-vq"})
    
    del product_container[0]  # useless

    extracted_data={}
    
    name=product_html.find('div',{"class":"_1YokD2 _3Mn1Gg col-9-12"}).div.div.div.div.text.replace("Reviews","")
    
    try:
        count=1
        for i in product_container:
            extracted_data.setdefault(count,{
                "rating": (i.div.div.div.div.text),
                "header": (i.div.div.div.p.text),
                "comment": (i.div.div.find("div",{"class":""}).text.replace("READ MORE","")),
                "user_name": (i.find('div',{"class":"row _3n8db9"}).p.text)
            })
            
            count=count+1
    except Exception as e:
        print(" ")
        
        
    return render_template('review.html', data=extracted_data, data1={"name":name})


if __name__=="__main__":
    app.run(debug=True)