from django.db.models import Min

from datetime import date, datetime, timedelta
import requests

from content.models import Post
from ranking.models import Stock


def yahoo_finance_url(symbol, start_date, end_date):
    yahoo_url = 'http://ichart.finance.yahoo.com/table.csv'
    start_month = start_date.month - 1
    start_day = start_date.day
    start_year = start_date.year

    end_month = end_date.month - 1
    end_day = end_date.day
    end_year = end_date.year

    yahoo_params = {
        's': symbol,
        'a': start_month,
        'b': start_day,
        'c': start_year,
        'd': end_month,
        'e': end_day,
        'f': end_year,
        'g': 'd'
    }

    return yahoo_url, yahoo_params


def get_historical_prices(symbol, start_date, end_date):
    yahoo_url, yahoo_params = yahoo_finance_url(symbol, start_date, end_date)
    response = requests.get(yahoo_url, params=yahoo_params)

    if response.status_code == requests.codes.ok:
        prices = response.iter_lines()
        try:
            prices.next()
            latest_price = float(prices.next().split(',')[6])
        except StopIteration:
            return None, None

        price_dict = {}
        for price in prices:
            price_split = price.split(',')
            price_dict[price_split[0]] = price_split[6]

        return latest_price, price_dict

    else:
        return None, None


def update_performance():
    stocks = Stock.objects.all()

    for stock in stocks:

        posts = Post.objects.filter(stock=stock)
        if len(posts) > 0:
            start_date = posts.aggregate(Min('created_on'))['created_on__min'] - timedelta(days=10)
            end_date = date.today()

            latest_price, historical_prices = get_historical_prices(stock.symbol,
                                                                    start_date,
                                                                    end_date)

            if not (latest_price and historical_prices):
                continue

            for post in posts:
                original_date = post.created_on
                for day in xrange(10):
                    post_date = (original_date - timedelta(day)).strftime('%Y-%m-%d')
                    if post_date in historical_prices:
                        original_price = float(historical_prices[post_date])
                        break
                if original_price:
                    performance = 100 * (latest_price - original_price) / original_price
                    post.performance = performance
                    post.performance_updated_on = datetime.now()
                    post.save()
                else:
                    print "Post {0} not updated on {1}".format(post.id, datetime.now())


def run(*args):
    update_performance()
