import os
import time
import csv
from urllib import parse
import user_agent
import random
from wlw.wrapper import fetch_url


class WLWScraper:
    def __init__(self, url=None):
        self.base_url = "https://www.wlw.de/de/suche"
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': user_agent.generate_user_agent(),
        }
        self.url = url
        self.cwd = os.getcwd()
        _dir = os.path.join(self.cwd, "output")
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        self.csv_file = open(f"{_dir}/wlw.csv", "w", newline="")
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["Name", "URL", "Street", "City", "Zip Code", "Country", "Supplier Types", "Phone Number", "Homepage", "Slug", "Description", "Employee Count", "Product Count", "Distribution Area", "Founding Year", "Average Response Time"])
        self.total_pages = 0
        self.total_products = 0
        print("""
                 WLW CLI SCRAPER
---------------------------------------------------
Author : invinciblepy
GitHub : https://github.com/invinciblepy
Site   : https://hashamx.com
---------------------------------------------------""")

    def create_params(self, url):
        params = {}
        if "/products" in url:
            print("[x] Product Pages Not Supported")
            exit()
        else:
            parsed_url = parse.urlparse(url)
            query_params = parsed_url.query.replace("q=", "")
            tld = parsed_url.netloc.split(".")[-1]
            params["query"] = query_params
            params["lang"] = tld
            params["country"] = tld.upper()
            params["site"] = "wlw"
            params["top_level_domain"] = tld.upper()
            params["city_extraction_radius"] = "50km"
            params["sort"] = "responsiveness"
            params["userLatitude"] = random.uniform(48.0, 54.0)
            params["userLongitude"] = random.uniform(6.0, 15.0)
        return params

    def scrape(self, page=1):
        if "/products" in self.url:
            print("[x] Product Pages Not Supported")
            return
        params = self.create_params(self.url)
        params["page"] = page
        response = fetch_url("https://www.wlw.de/search-frontend/alibaba-api/online.company.search", params=params, headers=self.headers)
        if page==1:
            self.total_pages = response.get("data", {}).get("paging",{}).get("total_pages")
            self.total_products = response.get("data", {}).get("paging",{}).get("total")
            print(f"[i] Total Pages: {self.total_pages} | Total Products: {self.total_products}")
        companies = response.get("data", {}).get("companies", [])
        for company in companies:
            self.csv_writer.writerow([
                company.get("name"),
                company.get("companyUrl"),
                company.get("street"),
                company.get("city"),
                company.get("zip_code"),
                company.get("country_code"),
                ", ".join(company.get("supplier_types", [])),
                company.get("phone_number"),
                company.get("homepage"),
                company.get("slug"),
                company.get("highlightings", {}).get("secondary_description", ""),
                company.get("employee_count"),
                company.get("product_count"),
                company.get("distribution_area"),
                company.get("founding_year"),
                company.get("average_response_time"),
            ])
            time.sleep(0.5)
            print(f"[+] Scraped {company.get('name')}")
        if page < self.total_pages:
            print(f"[i] Scraping Page {page+1} of {self.total_pages}")
            time.sleep(random.randint(2, 4))
            self.scrape(page=page+1)
