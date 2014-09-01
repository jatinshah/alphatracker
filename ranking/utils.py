from ranking.models import Stock
from csv import reader


def load_stock_data(file_name):
    with open(file_name) as f:
        rdr = reader(f, delimiter='\t')
        next(rdr, None)

        for row in rdr:
            _, created = Stock.objects.get_or_create(
                exchange=row[0],
                symbol=row[1],
                name=row[2]
            )
            if not created:
                print "ERROR: Stock {0}:{1} - {2} not created".format(row[0], row[1], row[2])


def load_eod_data():
    pass


