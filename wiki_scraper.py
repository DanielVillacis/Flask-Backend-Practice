import requests
from bs4 import BeautifulSoup
import json

url = "https://type.fit/api/quotes"


def create_api_url(url):
    response = requests.get(url)
    return response.json()


def create_quotes_dict(api_data):
    quotes = {}
    for data in api_data:
        if data["author"]:
            if not data["author"] in quotes:
                quotes[data["author"]] = []
            quotes[data["author"]].append(data["text"])
    return quotes


def get_image(author):
    url = f"https://en.wikipedia.org/wiki/{author}"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    try: 
        td = soup.find("td", class_ = "infobox-image")
        image = td.find("img")
        return "https:" + image['src']
    except Exception as e:
        print(e)
        return None


def get_image_dict(authors):
    image_dict = {}
    num_authors = len(authors)
    for author_num, author in enumerate(authors, start=1):
        image_dict[author] = get_image(author)
        print(f"processing {author_num}/{num_authors} author")
    return image_dict


def create_json_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    api_data = create_api_url(url)
    quotes = create_quotes_dict(api_data)
    authors = list(quotes.keys())
    image_dict = get_image_dict(authors)
    create_json_file("quotes.json", quotes)
    create_json_file("images.json", image_dict)


