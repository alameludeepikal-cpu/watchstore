from flask import Flask, render_template, session, redirect, url_for, request
import json, csv, os

app=Flask(__name__)
app.secret_key="watchstore_secret"

def load_watches():
    with open("data/watches.json") as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/watches")
def watches():
    products=load_watches()
    return render_template("watches.html", watches=products)

@app.route("/watch/<int:id>")
def watch_detail(id):

    filename= open("data\watches.json","r")
    products = json.load(filename)
    product = None

    for eachproduct in products:
        if eachproduct["id"] == id:
            product = eachproduct
            break   # stop once found

    return render_template("watch_detail.html", watch=product)

@app.route("/cart/<int:id>")
def add_and_show_cart(id):
    # 1 Get the cart (basket). If empty, start a new one
    cart = session.get("cart")
    if "cart" not in session :
        cart =[]
    
    # 2️Add the new product id
    cart.append(id)
    # 3️ Save the cart back into session
    session["cart"] = cart
    # 4️ Load all products
    products = load_watches()
    # 5️ Create a list of products that are in the cart
    cart_items = []
    for cid in cart:          # go through each id stored in cart
        for p in products:    # search in product list
            if p["id"] == cid:
                cart_items.append(p)

    # 6️ Show cart page
    return render_template("cart.html", cart=cart_items)


@app.route("/checkout", methods=["GET","POST"])
def checkout():
    
    #this loads the file data
    filename=open("data\watches.json","r")
    products=json.load(filename)
    #get the data from session storage
    cart_ids=session.get("cart", [])
    #compares with the json and gets the items that are added to the 
    #cart
    cart_items=[]       #stores all the cart items
    for i in cart_ids:
        for p in products:
            if p["id"] == i:
             cart_items.append(p)
             break
    
    total =0
    for item in cart_items:
        total += item["price"]
    return render_template("checkout.html", cart=cart_items, total=total)

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

if __name__=="__main__":
    app.run(debug=True)
