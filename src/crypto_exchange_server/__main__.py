from flask import Flask, render_template, request, jsonify
import ccxt
import datetime

app = Flask(__name__)


@app.template_filter('ctime')
def timectime(s):
    return datetime.datetime.fromtimestamp(s / 1000)


def create_exchange(exchange_name):
    exchange = getattr(ccxt, exchange_name)({
        # 'apiKey': '<YOUR API KEY HERE>',
        # 'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()
    return exchange


def get_market(exchange_name, market_id):
    exchange = create_exchange(exchange_name)
    market = exchange.markets_by_id[market_id]
    return exchange, market


def get_ohlc(exchange_name, market_id, time_frame, count):
    exchange = create_exchange(exchange_name)
    market = exchange.markets_by_id[market_id]
    candles = exchange.fetchOHLCV(market['symbol'], time_frame, limit=int(count))
    return exchange, market, candles


@app.route('/')
def index():
    return render_template('index.html', exchanges=ccxt.exchanges)


@app.route('/exchanges/<exchange_name>')
def exchange(exchange_name):
    exchange = create_exchange(exchange_name)
    return render_template('exchange.html', exchange=exchange)


@app.route('/exchanges/<exchange_name>/markets/<market_id>')
def market(exchange_name, market_id):
    exchange, market = get_market(exchange_name, market_id)
    return render_template(
        'market.html',
        market=market,
        timeframes=exchange.timeframes)


@app.route('/exchanges/<exchange_name>/markets/<market_id>/<time_frame>/<count>')
def candles(exchange_name, market_id, time_frame, count):
    exchange, market, candles = get_ohlc(
        exchange_name,
        market_id,
        time_frame,
        count)

    # bad req if timeframe not in timeframes
    # exchange not matched or market not matched

    if(request.accept_mimetypes.accept_html):
        return render_template(
            'ohlcv.html',
            exchange=exchange,
            market=market,
            candles=candles)

    if(request.accept_mimetypes.accept_json):  # ['application/json']
        return jsonify({
            'exchange': exchange_name,
            'instrument': market_id,
            'candle_width': time_frame,
            'candle_data': candles
        }), '200 OK'


if(__name__ == '__main__'):
    app.run(debug=False, host='0.0.0.0', port=8080)
