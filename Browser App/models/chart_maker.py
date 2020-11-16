import plotly.offline as pyo
import plotly.graph_objs as go


def scatter(df):
    """
    Must take in a df with property_type, year, price_paid
    """
    figs = []

    for prop_type in df['property_type'].unique():
        df_filt = df[df['property_type'] == prop_type]
        figs.append(
            go.Scatter(x=df_filt['year'],
                       y=df_filt['price_paid'],
                       mode='markers',
                       marker=dict(
                           size=35,
                           opacity=0.2,
                           line=dict(
                               width=1,
                               color='darkSlateGrey'
                           )
                       ),
                       name=prop_type,
                       connectgaps=True)
        )

    layout = go.Layout(width=600,
                       height=600,
                       title=dict(
                           text="Individual transactions, 1999 (merged with 1998) and 2020"),
                       xaxis=dict(
                           type='category',
                           title="Year (where 1999 includes 1998 data)"
                       ),
                       yaxis=dict(
                           title="Transaction Value"
                       )
                       )

    fig = go.Figure(data=figs, layout=layout)

    chart = pyo.plot(fig, output_type='div', include_plotlyjs=True)

    return chart


def box(df):
    """
    Must take in a df with property_type, year, price_paid
    """
    data = []

    for prop_type in df['property_type'].unique():
        df_filt = df[df['property_type'] == prop_type]
        data.append(
            go.Box(
                y=df_filt['price_paid'].values,
                x=df_filt['year'].values,
                name=prop_type,
                boxpoints='all',
                pointpos=-1,
                jitter=0.1
            )
        )

    layout = go.Layout(
        boxmode='group',
        height=600,
        width=1800,
        title=dict(
            text="Box Plot by Year and Property Type"
        ),
        xaxis=dict(
            title="Year and Property Type"
        ),
        yaxis=dict(
            title="Transaction Value"
        )
    )

    fig = go.Figure(data=data,
                    layout=layout)

    chart = pyo.plot(fig, output_type='div', include_plotlyjs=True)

    return chart
