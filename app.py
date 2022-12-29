from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import fredapi as fa
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import date, datetime
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# Flaskアプリ(app)とflask-bootstrapのインスタンスを紐付け
bootstrap = Bootstrap(app)

# ----------------------Home------------------------
@app.route('/')
def index():
    return render_template('index.html')

# --------------経済指標表示サービス-----------------
@app.route('/fredapi', methods=['GET'])
def fred_get():
    return render_template('fredapi.html')


@app.route('/fredapi', methods=['POST'])
def fred_post():
    fred = fa.Fred(api_key='6d0c0a6b221e21f5c00fcfd9cc04477f')
    name = request.form.get("name")

    if name == 'cpi':
        api = fred.get_series('CORESTICKM159SFRBATL')

    elif name == 'GDP':
        api = fred.get_series('GDP')

    elif name == 'interest_rate':
        api = fred.get_series('DEF')

    elif name == 'nikkei':
        api = fred.get_series('NIKKEI225')

    timelists = api.index.strftime('%Y-%m-%d').to_list()
    lists = api.to_list()
    return render_template('fredapi.html', timelists=timelists, lists=lists, message="データの数は"+str(len(lists))+'です。')

# -----------------株価表示サービス-----------------
@app.route('/stockpricechart', methods=['GET'])
def get():
    return render_template('stockpricechart.html', message="銘柄コードを入力してください。")


@app.route('/stockpricechart', methods=['POST'])
def post():
    code = request.form.get("name")  # formから銘柄コードを取得
    # yahoo finance api
    my_share = share.Share(code + ".T")
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                          3,
                                          share.FREQUENCY_TYPE_DAY,
                                          1)
    df = pd.DataFrame({'Date': [datetime.fromtimestamp(d / 1000) for d in symbol_data['timestamp']],
                       'Open': symbol_data['open'], 'High': symbol_data['high'], 'Low': symbol_data['low'],
                       'Close': symbol_data['close'], 'Volume': symbol_data['volume']}).set_index('Date')

    return render_template('stockpricechart.html', x=df.index.to_list(), y=df['Close'].to_list(), message="")

# -----------------業績表示サービス-----------------
@app.route('/pl', methods=['GET'])
def pl_get():
    return render_template('pl.html')


if __name__ == "__main__":
    app.run(debug=True)
