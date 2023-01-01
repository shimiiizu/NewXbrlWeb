import plotly.graph_objects as go
import PLGetter as pl


def PLGetterGraph():

    print(pl.PLGetter(3679)[0])

    d0 = go.Scatter(
        x=pl.PLGetter(3679)[0],
        y=pl.PLGetter(3679)[1],
        mode='markers',
        text=pl.PLGetter(3679)[3],
        name='売上'
    )

    d1 = go.Scatter(
        x=pl.PLGetter(3679)[0],
        y=pl.PLGetter(3679)[2],
        mode='markers',
        text=pl.PLGetter(3679)[3],
        name='営業利益'
    )

    plot = [d0, d1]
    fig = go.Figure(data=plot)
    fig.show()


if __name__ == "__main__":
    PLGetterGraph()