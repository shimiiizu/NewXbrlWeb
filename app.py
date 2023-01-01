from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import fredapi as fa
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import date, datetime
import pandas as pd
import sqlite3
import PLGetter as pl
import plotly.graph_objects as go






app = Flask(__name__)

# DBの指定
DB = 'D:/XBRLDB/XBRL_DB_v02.db'

# sqlの指定
sql = 'SELECT * FROM XbrlDB'

# ダウンロード済のXbrlファイルのリストを作成
conn = sqlite3.connect(DB)
cur = conn.cursor()
df = pd.read_sql(sql, conn)

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
    return render_template('fredapi.html', timelists=timelists, lists=lists, message="データの数は" + str(len(lists)) + 'です。')


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

    return render_template('stockpricechart.html', x=df.index.to_list(), y=df['Close'].to_list(), message="銘柄コード："+str(code))


# -----------------業績表示サービス-----------------
@app.route('/pl', methods=['GET'])
def pl_get():
    return render_template('pl.html',  message="銘柄コードを入力してください。")


@app.route('/pl', methods=['POST'])
def pl_post():
    # formから銘柄コードを取得
    code = request.form.get("name")
    print(code)
    print(pl.PLGetter(int(code)))
    print(df)
    # codeで抽出
    df_select = df[df['Code'] == int(code)].sort_values('Announcement_date')
    #print(df_select['Announcement_date'])

    print(df_select['Announcement_date'].values.tolist())
    print(pl.PLGetter(3679)[0].values.tolist())
    print(df_select['Sales'].values.tolist())
    print(pl.PLGetter(3679)[1].values.tolist())
    print(len(df_select['Sales'].values.tolist()))
    print(len(pl.PLGetter(3679)[1].values.tolist()))
    print(type(df_select['Announcement_date'].values.tolist()[0]))
    print(type(pl.PLGetter(3679)[0].values.tolist()[0]))
    print(type(pl.PLGetter(3679)[0].tolist()[0]))


    li = map(str, pl.PLGetter(3679)[0].values.tolist())
    yli = pl.PLGetter(int(code))[1].values.tolist()

    print(yli)

    #return render_template('pl.html', x=df_select['Announcement_date'].values.tolist()
     #                      , y=df_select['Sales'].values.tolist(), message="銘柄コード："+str(code))
    return render_template('pl.html', x=list(li)
                          , y=yli, message="銘柄コード："+str(code))


if __name__ == "__main__":
    app.run(debug=True)
