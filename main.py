import argparse
from wlw.scraper import WLWScraper

def main():
    parser = argparse.ArgumentParser(description="Gelbe Seiten Scraper CLI")
    parser.add_argument('-u', '--url', required=True, help='URL of the website to scrape')
    args = parser.parse_args()
    scraper = WLWScraper(url=args.url)
    scraper.scrape()

if __name__ == "__main__":
    main()