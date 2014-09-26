from ranking.models import Stock
from csv import reader


def load_stocks(exchange, file_name):
    with open(file_name) as f:
        rdr = reader(f, delimiter='\t')
        next(rdr, None)

        for row in rdr:
            _, created = Stock.objects.get_or_create(
                exchange=exchange,
                symbol=row[0],
                name=row[1]
            )
            if not created:
                print "ERROR: Stock {0}:{1} - {2} not created".format(exchange, row[0], row[1])


def run(*args):
    if len(args) != 2:
        print "Usage: manage.py runscript load_stocks --script-args <exchange> <file>"
        return
    exchange = args[0]
    file_name = args[1]
    load_stocks(exchange, file_name)
