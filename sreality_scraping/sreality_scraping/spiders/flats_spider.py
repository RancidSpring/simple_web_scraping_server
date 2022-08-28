import scrapy
from bs4 import BeautifulSoup
import pandas as pd
from scrapy_selenium import SeleniumRequest
import psycopg2
import psycopg2.extras as extras

connection = psycopg2.connect(
    database="db", user="postgres", password="postgres", host='localhost', port='5432'
)


def truncate_table(table):
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


def write_to_db(data, table):
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
    name = "flats"
    # truncate_table('sreality')
    pages_num = 3

    def start_requests(self):
        urls = [f'https://www.sreality.cz/hledani/prodej/byty?strana={x}' for x in range(1, self.pages_num+1)]
        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
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
        # connection.close()


