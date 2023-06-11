import requests

def get_product_list():
    """This function retrieves a list of products from a dummy API and returns it, or an empty list if the API call fails."""
    openAI_key="7yY9eBigr44EAA1RZ9JaT3BlbkFJzxUsDCR4ELWyoBSe7tfb"
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        product_list = response.json()
        return product_list.get("product", [])
    else:
        print("Error: Failed to retrieve product list")
        return []


# Get product list
products = get_product_list()
for product in products:
    print(product)
