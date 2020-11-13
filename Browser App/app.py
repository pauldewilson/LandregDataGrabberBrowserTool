import pandas as pd
from models.forms import PostCodeForm
from flask import Flask, render_template, url_for, redirect, session, Markup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'x'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostCodeForm()
    if form.validate_on_submit():
        session['search_postcode'] = form.postcode.data
        return redirect(url_for('results'))
    else:
        pass
    return render_template('index.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    # read in data and grab search element from session
    df = pd.read_csv('../data/landreg_data.csv')
    post_sector = session['search_postcode']
    session['search_postcode'] = ''

    # filter and create dataframes
    df_filt = df[df['post_sect'] == post_sector]

    columns = 'price_paid year postcode post_sect property_type'.split()
    df_postcode = df_filt[columns]
    df_stats = df_postcode.groupby(['post_sect', 'year', 'property_type']).agg(['mean', 'median'])['price_paid']
    df_stats['mean'] = df_stats['mean'].astype(int)

    df_filt.set_index('transaction_id', drop=True, inplace=True)
    # cutting out thie Unnamed: 0 column
    df_filt = df_filt.iloc[:, 1::]

    df_stats = Markup(df_stats.to_html())
    df_filt = Markup(df_filt.to_html())

    return render_template('results.html', df=df_filt, df_stats=df_stats)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
