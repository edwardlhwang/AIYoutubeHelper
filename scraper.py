import requests
from bs4 import BeautifulSoup

# Send a GET request to the news article page
url = "https://apnews.com/article/russia-ukraine-war-military-deaths-facd75c2311ed7be660342698cf6a409"  # Replace with the URL of the news article page
response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')


headline_element = soup.find('h1', class_='Page-headline') 
body_element = soup.find('div', class_='RichTextStoryBody RichTextBody') 


headline = headline_element.get_text().strip() if headline_element else None
body = body_element.get_text().strip() if body_element else None

if headline:
    print("Headline:", headline)
else:
    print("Headline not found.")

if body:
    print("Body:", body)
else:
    print("Body not found.")
