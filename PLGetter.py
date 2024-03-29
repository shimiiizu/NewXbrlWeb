import sqlite3
import pandas as pd


def PLGetter(code):

    # DBの指定
    DB = 'D:/XBRLDB/XBRL_DB_v02.db'
    sql = 'SELECT * FROM XbrlDB'
    conn = sqlite3.connect(DB)
    df = pd.read_sql(sql, conn)

    # codeを抽出、日付でソート、インデックスの振り直し
    df_select = df[df['Code'] == code].sort_values('Announcement_date', ascending=False).reset_index()

    maxi = max(df_select.index.tolist())  # インデックスのMax値
    cof = 1 / 100000000  # 通貨単位を億円にするための係数

    for i in range(0, maxi):
        if df_select.loc[i, 'Quarter'] == 'Q1':
            df_select.loc[i, 'Sales_quarter'] = df_select.loc[i, 'Sales'] * cof
            df_select.loc[i, 'OperatingIncome_quarter'] = df_select.loc[i, 'OperatingIncome'] * cof
            df_select.loc[i, 'Announcement_date_quarter'] = df_select.loc[i, 'Announcement_date']

        elif df_select.loc[i, 'Quarter'] == 'Q2' and df_select.loc[i + 1, 'Quarter'] == 'Q1':
            df_select.loc[i, 'Sales_quarter'] = df_select.loc[i, 'Sales'] * cof - df_select.loc[i + 1, 'Sales'] * cof
            df_select.loc[i, 'OperatingIncome_quarter'] = df_select.loc[i, 'OperatingIncome'] * cof - df_select.loc[
                i + 1, 'OperatingIncome'] * cof
            df_select.loc[i, 'Announcement_date_quarter'] = df_select.loc[i, 'Announcement_date']

        elif df_select.loc[i, 'Quarter'] == 'Q3' and df_select.loc[i + 1, 'Quarter'] == 'Q2':
            df_select.loc[i, 'Sales_quarter'] = df_select.loc[i, 'Sales'] * cof - df_select.loc[i + 1, 'Sales'] * cof
            df_select.loc[i, 'OperatingIncome_quarter'] = df_select.loc[i, 'OperatingIncome'] * cof - df_select.loc[
                i + 1, 'OperatingIncome'] * cof
            df_select.loc[i, 'Announcement_date_quarter'] = df_select.loc[i, 'Announcement_date']

        elif df_select.loc[i, 'Quarter'] == 'FY' and df_select.loc[i + 1, 'Quarter'] == 'Q3':
            df_select.loc[i, 'Sales_quarter'] = df_select.loc[i, 'Sales'] * cof - df_select.loc[i + 1, 'Sales'] * cof
            df_select.loc[i, 'OperatingIncome_quarter'] = df_select.loc[i, 'OperatingIncome'] * cof - df_select.loc[
                i + 1, 'OperatingIncome'] * cof
            df_select.loc[i, 'Announcement_date_quarter'] = df_select.loc[i, 'Announcement_date']

<<<<<<< HEAD
    xlist = pd.to_datetime(df_select['Announcement_date_quarter'])
    y1list = df_select['Sales_quarter']
    y2list = df_select['OperatingIncome_quarter']
    label = df_select['Quarter']

    return xlist, y1list, y2list, label
=======
    # 欠損値処理
    df = df_select.dropna(subset=["Announcement_date_quarter", "Sales_quarter"])

    xlist = df['Announcement_date_quarter']
    y1list = df['Sales_quarter']
    y2list = df['OperatingIncome_quarter']
    label = df['Quarter']
    cname = df['CompanyName']

    return xlist, y1list, y2list, label, cname
>>>>>>> origin/main


if __name__ == "__main__":
    print(PLGetter(3679)[0])
<<<<<<< HEAD
    print(PLGetter(3679)[1])
    print(PLGetter(3679)[2])
=======
    # print(PLGetter(3679)[1])
    # print(PLGetter(3679)[2])
>>>>>>> origin/main

    """
    d0 = go.Scatter(
        x=xlist,
        y=ylist,
        mode='markers',
        text=label,
        name='売上'
    )
    
    d1 = go.Scatter(
        x=xlist,
        y=y2list,
        mode='markers',
        text=label,
        name='営業利益'
    )
    
    
    plot = [d0, d1]
    fig = go.Figure(data=plot)
    fig.show()
    
    plt.scatter(xlist, ylist)
    plt.show()
    """
