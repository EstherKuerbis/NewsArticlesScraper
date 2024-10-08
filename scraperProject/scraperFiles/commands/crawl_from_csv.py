from ..portalcsv import PortalCSV
from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.utils.project import get_project_settings
import csv


def get_csv_values(csv_file):
    portale = []
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            portal = PortalCSV(row['start_url'], row['allowed_domains'], row['homepage'],
                               row['article'], row['crawler'])
            portale.append(portal)
    return portale


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '<csv_file>'

    def short_desc(self):
        return 'Run spiders with URLs from csv file'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)

    def run(self, args, opts):
        if len(args) != 0:
            raise UsageError("Too many arguments")

        settings = get_project_settings()
        csv_file = settings.get('CSV_INPUT_FILE')
        process = CrawlerProcess(get_project_settings())

        portale = get_csv_values(csv_file)
        for portal in portale:
            if portal.crawler == 'scrapy':
                process.crawl('gonnaCrawlThemAll', portal_csv=portal)
            else:
                process.crawl('seleniumCrawlThemAll', portal_csv=portal)
        process.start()
