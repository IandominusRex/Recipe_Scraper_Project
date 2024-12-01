def get_user_ingredients():
    print("Enter the ingredients you have! (seperated by commas)")
    user_ingredients_input = input(">").lower().split(",") #user prompt, formats and creates a list
    user_ingredients = [user_ingredient.strip() for user_ingredient in user_ingredients_input] #strip the whitespace for ingredients in the user input
    print("You have: " + ", ".join(user_ingredients))
    return user_ingredients #updates the cleaned ingredient list to the function

import requests #This library is used to send HTTP requests to websites. It retrieves the HTML content of a webpage.
from bs4 import BeautifulSoup #Used to parse and extract data from HTML or XML documents.
from requests.utils import quote #this encodes the query to the proper format

def scrape_allrecipes(user_ingredients):
    query = ", ".join(user_ingredients)
    encoded_query = quote(query)
    encoded_query = encoded_query.replace("%20","+")
    url = f"https://www.bbc.co.uk/food/search?q={encoded_query}"  # Dynamic URL
    print(f"Searching BBC with URL: {url}\n")
    
    response = requests.get(url)
    if response.status_code != 200: #Checks if the request was successful. A status code of 200 means success.
        print("Failed to retrieve data. Please check your internet connection or the website.")
        return

    soup = BeautifulSoup(response.text, "html.parser") #response.text Contains the raw HTML content of the webpage as a string.
    recipes = soup.find_all("a", class_="promo")[:5]  # Adjust based on inspection
    #print(soup.prettify())  # Print the HTML structure for inspection
    if not recipes:
        print("No recipes found. Try different ingredients!")
        return
    
    for recipe in recipes:
        # Extract title
        title_tag = recipe.find("h3", class_="promo__title")
        title = title_tag.text.strip() if title_tag else "No title available"

        # Extract link
        link_tag = recipe.get('href')
        link = f"https://www.bbc.co.uk{link_tag}" if link_tag else "No link available"

        print(f"Recipe: {title}\nLink: {link}\n")

user_ingredients = get_user_ingredients()
scrape_allrecipes(user_ingredients)