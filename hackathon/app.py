import requests

def get_product_list():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        product_list = response.json()
        return product_list.get("products", [])
    else:
        print("Error: Failed to retrieve product list")
        return []


# Get product list
products = get_product_list()
for product in products:
    print(product)
