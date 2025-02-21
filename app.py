from flask import Flask, request, jsonify
from datetime import date
import uuid
import logging

#Initializing flask framework
app = Flask(__name__)

#Initializing logger, creating a .txt file for logs, setting level as INFO
#and setting format as date, levelname, and logmessage
logging.basicConfig(filename="api_log.txt", level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(message)s')

#Function for getting the current date (Year,Month,Day)
def get_date():
    return date.today()

#Function for getting an unique id for every request made
def transaction_id():
    return uuid.uuid4()
    

#Initial function to test a simple GET request
@app.route("/", methods=['GET'])
def inicio():
    response = {"endpoint": f"{request.path}",
                "message": "API working corrrectly",
                 "method" : f"{request.method}",
                 "date": f"{get_date()}",
                 "http-status": 200,
                 "reques-id": f"{transaction_id()}"
                }
    
    logging.info(response)
    return jsonify(response)

#Function for listing business general information
@app.route("/business/info", methods=['GET'])
def business_info():
    response = {"endpoint": f"{request.path}",
                "message": "Tech Products",
                "method" : f"{request.method}",
                "date": f"{get_date()}",
                "http-status": 200,
                "request-id": f"{transaction_id()}"
                }
    
    logging.info(response)
    return jsonify(response)

products = [
    {"id": 1, "ProductName": "Computers"},
    {"id": 2, "ProductName": "Laptops"},
    {"id": 3, "ProductName": "Cellphones"},
    {"id": 4, "ProductName": "Chargers"},
    {"id": 5, "ProductName": "Cases"},
    {"id": 6, "ProductName": "Keyboards"},
    {"id": 7, "ProductName": "Mouse"},
    {"id": 8, "ProductName": "Headphones"},
    {"id": 9, "ProductName": "Smart Watches"},
    {"id": 10, "ProductName": "Controllers"},
]

#Function for listing existing products
@app.route("/business/products", methods=['GET', 'POST'])
def business_products():
    #Handling request, if GET: only return product info
    if request.method == 'GET':
        response = {"endpoint":f"{request.path}",
                    "products": products,
                    "method" : f"{request.method}",
                    "date": f"{get_date()}",
                    "http-status": 200,
                    "request-id": f"{transaction_id()}"
                    }
        
        logging.info(response)
        return jsonify(response)

    #If request type is POST then verify if product already exists, if not
    #add product to the existing list of products
    elif request.method == 'POST':
        #Reading the entered product
        data = request.get_json()
        product_name = data.get("ProductName", None)

        if not product_name:
            response = {"endpoint": f"{request.path}",
                        "message": "Product name is required. Enter: \"ProdutName\": \"Value\"",
                        "method": f"{request.method}",
                        "date": f"{get_date()}",
                        "http-status": 400,
                        "request-id": f"{transaction_id()}",}
            
            logging.info(response)
            return jsonify(response)
        

        #Verifying if the product already exists in the original list
        #If so, do not append it twice
        for product in products:
            if product["ProductName"].lower() == product_name.lower():
                response = {"endpoint": f"{request.path}",
                            "message": "Product already exists",
                            "method": f"{request.method}",
                            "date": f"{get_date()}",
                            "http-status": 400,
                            "request-id": f"{transaction_id()}",
                            }
                
                logging.info(response)
                return jsonify(response)
        
        #Calculating the ID for the new product
        if products:
            new_id = products[-1]["id"] + 1
        
        else:
            new_id = 1

        #Creating new product
        new_product = {"id": new_id, "ProductName": product_name}

        #Adding new product to the existing products list
        products.append(new_product)

        response = {"endpoint": f"{request.path}",
                    "message": "Product added successfully",
                    "new_product": new_product,
                    "method": f"{request.method}",
                    "date": f"{get_date()}",
                    "http-status": 201,
                    "request-id": f"{transaction_id()}"
                    }
        
        logging.info(response)
        return jsonify(response)

    #If the request wasnt GET or POST return an error message
    """elif request.method not in ["GET", "POST"]:
        return jsonify({"message": "request type not permitted for this endpoint"})"""

#Function for listing business contact info
@app.route("/business/contact", methods=['GET'])
def contact():
    response = {"endpoint": f"{request.path}",
                "message": [{"TelephoneNumber": 123456789}, {"email": "test@gmail.com"}],
                "method": f"{request.method}",
                "date": f"{get_date()}",
                "http-status": 201,
                "request-id": f"{transaction_id()}"
                }
    
    logging.info(response)
    return jsonify(response)

#Keeping the API running until manually stop
if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)