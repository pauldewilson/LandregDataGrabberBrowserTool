import pandas as pd
from models.forms import PostCodeForm
from models.chart_maker import scatter, box
from flask import Flask, render_template, url_for, redirect, session, Markup, flash

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
    post_sector = session['search_postcode'].strip()
    session['search_postcode'] = ''

    # filter and create dataframes
    df_filt = df[df['post_sect'] == post_sector]
    df_filt['year'].replace(1998, 1999, inplace=True)
    
    columns = 'price_paid year postcode post_sect property_type'.split()
    df_postcode = df_filt[columns]
    df_stats = df_postcode.groupby(['post_sect', 'year', 'property_type']).agg(['mean', 'median'])['price_paid']
    df_stats['mean'] = df_stats['mean'].astype(int)
    df_quantile = df_filt.groupby(['post_sect', 'year', 'property_type']).quantile([0.25, 0.50, 0.75]).iloc[:, 0:1]

    df_filt_mu = Markup(df_filt.to_html(table_id='table_stats', index=False, na_rep='NULL'))
    df_stats_mu = Markup(df_stats.to_html(table_id='table_results', sparsify=False))
    df_quantile_mu = Markup(df_quantile.to_html(table_id='table_quantile', sparsify=False))

    chart_scatter = Markup(scatter(df_filt))
    chart_box = Markup(box(df_filt))

    if len(df_filt) > 0:
        return render_template('results.html',
                               df_filt_mu=df_filt_mu,
                               df_stats_mu=df_stats_mu,
                               df_quantile_mu=df_quantile_mu,
                               chart_scatter=chart_scatter,
                               chart_box=chart_box)
    else:
        if len(post_sector) > 6:
            flash(f'No transactions found, did you accidentally search the whole postcode?')
        else:
            flash('No transactions found')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
