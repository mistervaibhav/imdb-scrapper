import requests
import json
from bs4 import BeautifulSoup

from constants import ROOT_URL


PAGE_URL = ROOT_URL + "/chart/top"


def main():
    """
    * Scrape top 250 movies from imdb
    """

    try:
        source = requests.get(PAGE_URL)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, "html.parser")

        table = soup.find("tbody", attrs={"class": "lister-list"})
        table_rows = table.find_all("tr")

        data = list()

        for row in table_rows:
            data.append(
                {
                    "poster": row.find("td", attrs={"class": "posterColumn"}).a.img[
                        "src"
                    ],
                    "title": row.find("td", attrs={"class": "titleColumn"}).a.text,
                    "year": row.find("td", attrs={"class": "titleColumn"}).span.text,
                    "rating": row.find(
                        "td", attrs={"class": "ratingColumn imdbRating"}
                    ).strong.text,
                }
            )

        with open("top_250_movies/data.json", "w") as f:
            f.write(json.dumps(data))
            f.close()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
