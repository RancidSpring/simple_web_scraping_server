import scrapy
from bs4 import BeautifulSoup
import pandas as pd
from scrapy_selenium import SeleniumRequest
import psycopg2
import psycopg2.extras as extras

NUMBER_OF_SREALITY_PAGES = 25
WAIT_TIME = 10

connection = psycopg2.connect(database="db", user="postgres", password="postgres", host='postgres', port='5432')


def truncate_table(table: str):
    """
    Truncates the table at the beginning to get rid of the old data that might be stored in the database
    :param table: name of the table
    :return:
    """
    truncate_sql = f"TRUNCATE {table};\n"
    cursor = connection.cursor()
    try:
        cursor.execute(truncate_sql)
        connection.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        return 1


truncate_table('sreality')


def write_to_db(data: pd.DataFrame, table: str):
    """
    Function for writing data into the database, taking a dataframe and a name of the table to put data to
    :param data: dataframe with data
    :param table: string representing a name of the table in the database
    :return:
    """
    tuples = [tuple(x) for x in data.to_numpy()]
    cols = ','.join(list(data.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = connection.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        connection.commit()
        print("The dataframe is successfully inserted")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        return 1


class FlatsSpider(scrapy.Spider):
    """
    Special spider created for the purpose of scraping data about apartments currently being sold.
    Uses Selenium-Scrapy library to combine both of frameworks and scrape data from a dynamically rendered website.
    """
    name = "flats"
    pages_num = NUMBER_OF_SREALITY_PAGES

    def start_requests(self):
        """
        Yields SeleniumRequests to be later parsed on a callback for each page containing data on apartments
        :return:
        """
        urls = [f'https://www.sreality.cz/hledani/prodej/byty?strana={x}' for x in range(1, self.pages_num+1)]
        for page_idx, url in enumerate(urls):
            print(f"Yielding page number {page_idx}")
            yield SeleniumRequest(
                url=url,
                wait_time=WAIT_TIME,
                screenshot=True,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response: SeleniumRequest):
        """
        Uses BeautifulSoup library to parse the content of yielded page. Gets the attributes to be stored in the db,
        such as titles, addresses, prices and images. After each page is scraped and parsed, the content is being
        inserted into the database
        :param response: SeleniumRequest yielded previously by the start_requests function
        :return:
        """
        print("Parsing a page...")
        content = response.body
        soup = BeautifulSoup(content, 'html.parser')
        titles, images, addresses, prices = [], [], [], []
        for item in soup.findAll("div", attrs={"class", "property ng-scope"}):
            titles.append(item.find("span", attrs={"class", "name ng-binding"}).text)
            addresses.append(item.find("span", attrs={"class", "locality ng-binding"}).text)
            prices.append(item.find("span", attrs={"class", "norm-price ng-binding"}).text)
            images.append(item.find("img")["src"])

        data = pd.DataFrame({"title": titles, "image": images, "address": addresses, "prices": prices})
        write_to_db(data=data, table='sreality')


