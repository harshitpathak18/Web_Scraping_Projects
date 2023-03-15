from flask import Flask,request,render_template
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

app=Flask(__name__)

global searched

@app.route("/", methods=['GET','POST'])
def index():
    if request.method=="POST":
        searched=request.form['search']
        
        link="https://www.flipkart.com/search?q="+searched.replace(" ",'-')+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY&as-backfill=on"
        products_=urlopen(link).read()
        products_html=bs(products_,'html.parser')  # beautify html
        product_container=products_html.find_all('div',{"class":"_1AtVbE col-12-12"})
        del product_container[0:3]  # useless 
        
        
        extracted_data={}
        try:
            count=0
            for i in product_container:
                extracted_data.setdefault(count,{
                    "link": ("https://www.flipkart.com"+i.div.div.div.a['href']),
                    "img": (i.div.div.div.a.div.div.div.div.img['src']),
                    "name": (i.div.div.div.a.find('div',{"class": "_3pLy-c row"}).div.div.text),
                    "rating": (i.div.div.div.a.find('div',{"class": "_3pLy-c row"}).div.find('div',{"class": "_3LWZlK"}).text),
                    "price" :(i.div.div.div.a.find('div',{"class": "col col-5-12 nlI3QM"}).div.div.div.text)
                })
                count=count+1
                
        except Exception as e:
            pass
        
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
    app.run()