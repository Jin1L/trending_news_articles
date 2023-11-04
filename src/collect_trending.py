import requests
import argparse
import bs4
from pathlib import Path
import json

def get_html_data(url):

    # Set User Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    # Extract html data given the url
    data = requests.get(url, headers=headers)

    return data.text

def collect_data():
    FULL_DATA = []

    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", required=True, help="output file that you want to save the information into")

    args = parser.parse_args()

    output_file = args.output

    # Extract the html data to scrape the homepage of Montreal Gazette
    main_html_data = get_html_data("https://montrealgazette.com/category/news/")

    soup = bs4.BeautifulSoup(main_html_data, "html.parser")

    # Find all trending articles
    top_trending = soup.find("div", class_="top-trending")
    article_links = top_trending.find_all("a", class_="article-card__link")
   
    data = {}
    
    for article in article_links:
        link = article.get('href')
        full_link = "https://montrealgazette.com" + link

        # Get the trending article html data
        article_html_data = get_html_data(full_link)

        soup = bs4.BeautifulSoup(article_html_data, "html.parser")

        article_detail = soup.find("div", class_="article-header__detail")

        # Get title of the article
        article_title = article_detail.find("h1", class_="article-title")

        # Get published date of the article
        article_published_date = article_detail.find("span", class_="published-date__since")

        # Get author of the article
        article_author_span = article_detail.find("span", class_="published-by__author")

        # If there is no author, set it to Unknown
        if article_author_span is not None:
            article_author = article_author_span.find("a")
            article_author = article_author.text
        else:
            article_author = "Unknown"

        # Get subtitle of the article
        article_subtitle = article_detail.find("p", class_="article-subtitle")
        
        data["title"] = article_title.text
        data["publication_date"] = article_published_date.text.replace("Published ", "")
        data["author"] = article_author
        data["blurb"] = article_subtitle.text

        FULL_DATA.append(data)

        data = {}

    json_data = json.dumps(FULL_DATA, indent=4)  # The 'indent' argument adds pretty-printing
    
    # Write the data into the output file given by the user
    output_location = 'outputs/' + output_file

    if not Path('outputs/').exists():
        Path('outputs/').mkdir()

    with open(output_location, "w") as json_file:
        json_file.write(json_data)
    




