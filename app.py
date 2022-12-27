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




"""
# 何に使っているか不明
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

"""
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fredapi')
def fredapi():
    fred = fa.Fred(api_key='6d0c0a6b221e21f5c00fcfd9cc04477f')
    cpi = fred.get_series('CORESTICKM159SFRBATL')
    cpi_timelists = cpi.index.strftime('%Y-%m-%d').to_list()
    cpilists = cpi.to_list()
    if request.method == 'POST':
        screen_name = request.form['screen_name']
    return render_template('fredapi.html', cpi_timelists=cpi_timelists, cpilists=cpilists)


@app.route('/stockpricechart')
def stockpricechart():
    # Yahoo API
    code = "1301"  # (株)極洋の東証コード
    my_share = share.Share(code + ".T")  # データ取得用のクラス
    symbol_data = None  # 株価のデータ
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                          3,
                                          share.FREQUENCY_TYPE_DAY,
                                          1)
    df = pd.DataFrame({'Date': [datetime.fromtimestamp(d / 1000) for d in symbol_data['timestamp']], \
                       'Open': symbol_data['open'], 'High': symbol_data['high'], 'Low': symbol_data['low'], \
                       'Close': symbol_data['close'], 'Volume': symbol_data['volume']}).set_index('Date')

    return render_template('stockpricechart.html', x=df.index.to_list(), y=df['Close'].to_list())


@app.route('/graph')
def graph():
    return render_template('graph.html')


@app.route('/graph3')
def graph3():
    return render_template('graph3.html')


@app.route('/graph4')
def graph4():
    title = 'Bar'
    labels = ['2022-10-3', '2022-10-4', '2022-10-5', '2022-10-11', '2022-10-21', '2022-10-31']
    values = [10, 9, 8, 7, 6, 8]
    return render_template('graph4.html', values=values, labels=labels, title=title)


@app.route('/graph5')
def graph5():
    title = 'Scatter'
    xlists = [1, 2, 3]
    ylists = [10, 20, 30]
    lists = [{'x': 1, 'y': 10}, {'x': 2, 'y': 20}, {'x': 3, 'y': 30}]

    return render_template('graph5.html', xlists=xlists, ylists=ylists, title=title, lists=lists)


@app.route('/graph6')
def graph6():
    return render_template('graph6.html')


@app.route('/graph7')
def graph7():
    timelists = cpi.index.to_list()
    cpilists = cpi.to_list()
    xlists = [1, 2, 3]
    ylists = [10, 20, 30]
    return render_template('graph7.html', xlists=xlists, ylists=ylists, timelists=timelists, cpilists=cpilists)


@app.route('/graph8')
def graph8():
    timelists = cpi.index.strftime('%Y-%m-%d').to_list()
    cpilists = cpi.to_list()
    xlists = [1, 2, 3]
    ylists = [10, 20, 30]
    return render_template('graph8.html', xlists=xlists, ylists=ylists, timelists=timelists, cpilists=cpilists)





@app.route('/graph10')
def graph10():
    cpi_timelists = cpi.index.strftime('%Y-%m-%d').to_list()
    cpilists = cpi.to_list()
    return render_template('graph10.html', cpi_timelists=cpi_timelists, cpilists=cpilists)


@app.route('/nikka')
def nikka():
    return render_template('nikka.html')


if __name__ == "__main__":
    app.run(debug=True)
