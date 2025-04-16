from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import CSRFProtect
import os
from models.forms import MovieSetupForm
from utils.market_analysis import generate_market_data, analyze_seasonal_trends, analyze_competitor_strategies, generate_competitor_data
from utils.calculations import calculate_results, calculate_performance_rating
from utils.charts import generate_bar_chart, generate_line_chart, generate_pie_chart

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_movie_release_game')
csrf = CSRFProtect(app)  # Make sure this line is present

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MovieSetupForm()
    
    if form.validate_on_submit():
        # Store form data in session
        session['movie_title'] = form.movie_title.data
        session['genre'] = form.genre.data
        session['budget'] = form.budget.data
        session['marketing_budget'] = form.marketing_budget.data
        session['target_audience'] = form.target_audience.data
        
        # Generate market and competitor data
        market_data = generate_market_data(form.genre.data)
        competitor_data = generate_competitor_data(form.genre.data)
        
        # Store data in session
        session['market_data'] = market_data
        session['competitor_data'] = competitor_data
        session['game_phase'] = 'analysis'
        
        return redirect(url_for('market'))
    
    # Clear session if starting a new game
    if request.args.get('new_game'):
        session.clear()
    
    return render_template('index.html', form=form, active_tab='dashboard')

@app.route('/market')
def market():
    if 'market_data' not in session:
        return redirect(url_for('index'))
    
    market_data = session['market_data']
    genre = session['genre']
    
    # Generate charts
    audience_chart = generate_bar_chart(
        [m['month'] for m in market_data],
        [m['audienceReceptivity'] for m in market_data],
        'Audience Receptivity by Month',
        'Month',
        'Audience Receptivity (%)',
        '#4BC0C0'
    )
    
    competition_chart = generate_bar_chart(
        [m['month'] for m in market_data],
        [m['competitionLevel'] for m in market_data],
        'Competition Level by Month',
        'Month',
        'Competition Level (%)',
        '#FF6384'
    )
    
    marketing_chart = generate_bar_chart(
        [m['month'] for m in market_data],
        [m['marketingEffectiveness'] for m in market_data],
        'Marketing Effectiveness by Month',
        'Month',
        'Marketing Effectiveness (%)',
        '#9966FF'
    )
    
    profit_chart = generate_line_chart(
        [m['month'] for m in market_data],
        [m['profitPotential'] for m in market_data],
        'Profit Potential by Month',
        'Month',
        'Profit Potential (%)',
        '#36A2EB'
    )
    
    seasonal_analysis = analyze_seasonal_trends(market_data, genre)
    
    return render_template(
        'market.html',
        active_tab='market',
        genre=genre,
        audience_chart=audience_chart,
        competition_chart=competition_chart,
        marketing_chart=marketing_chart,
        profit_chart=profit_chart,
        seasonal_analysis=seasonal_analysis
    )

@app.route('/competitors')
def competitors():
    if 'competitor_data' not in session:
        return redirect(url_for('index'))
    
    competitor_data = session['competitor_data']
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    
    # Count releases by month
    release_counts = {month: 0 for month in months}
    for competitor in competitor_data:
        for release in competitor['releases']:
            release_counts[release['month']] += 1
    
    month_distribution_chart = generate_pie_chart(
        list(release_counts.keys()),
        list(release_counts.values()),
        'Release Distribution by Month'
    )
    
    # Count releases by genre
    genre_counts = {}
    for competitor in competitor_data:
        for release in competitor['releases']:
            genre = release['genre']
            if genre not in genre_counts:
                genre_counts[genre] = 0
            genre_counts[genre] += 1
    
    genre_distribution_chart = generate_pie_chart(
        [g.title() for g in genre_counts.keys()],
        list(genre_counts.values()),
        'Release Distribution by Genre'
    )
    
    game_theory_analysis = analyze_competitor_strategies(competitor_data)
    
    return render_template(
        'competitors.html',
        active_tab='competitors',
        competitor_data=competitor_data,
        month_distribution_chart=month_distribution_chart,
        genre_distribution_chart=genre_distribution_chart,
        game_theory_analysis=game_theory_analysis
    )

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'market_data' not in session or 'competitor_data' not in session:
        return redirect(url_for('index'))

    form = MovieSetupForm()
    
    market_data = session['market_data']
    competitor_data = session['competitor_data']
    
    # Create date info mapping
    date_info = {}
    for data in market_data:
        month = data['month']
        date_info[month] = {
            'marketData': data,
            'competitorReleases': []
        }

    for competitor in competitor_data:
        for release in competitor['releases']:
            month = release['month']
            if month in date_info:
                release_with_studio = release.copy()
                release_with_studio['studioName'] = competitor['name']
                date_info[month]['competitorReleases'].append(release_with_studio)

    selected_month = request.args.get('month')
    selected_date = None

    # ✅ Handle reset
    if request.method == 'POST' and 'reset_date' in request.form:
        session.pop('release_date', None)
        session.pop('results', None)
        session['game_phase'] = 'setup'  # Optional: reset game phase
        return redirect(url_for('calendar'))  # Redirect to clean up form resubmission

    if request.method == 'POST':
        selected_month = request.form.get('selected_month')
        selected_date = request.form.get('release_date')
        if selected_month and selected_date:
            session['release_date'] = f"{selected_month} {selected_date}"
        
        if 'finalize' in request.form:
            if 'release_date' not in session:
                return render_template(
                    'calendar.html',
                    active_tab='calendar',
                    date_info=date_info,
                    error="Please select a release date before finalizing your decision.",
                    form=form
                )
            
            results = calculate_results(
                session.get('release_date'),
                session.get('genre'),
                session.get('budget'),
                session.get('marketing_budget'),
                competitor_data,
                market_data
            )
            
            session['results'] = results
            session['game_phase'] = 'results'
            
            return redirect(url_for('results'))

    if 'release_date' in session:
        month_date = session['release_date'].split()
        if len(month_date) == 2:
            selected_month = month_date[0]
            selected_date = int(month_date[1])

    selected_month_info = date_info.get(selected_month, None) if selected_month else None

    return render_template(
        'calendar.html',
        active_tab='calendar',
        date_info=date_info,
        selected_month=selected_month,
        selected_date=selected_date,
        selected_month_info=selected_month_info,
        form=form
    )

@app.route('/results')
def results():
    if 'results' not in session:
        return redirect(url_for('index'))
    
    results = session['results']
    movie_details = {
        'movieTitle': session['movie_title'],
        'genre': session['genre'],
        'budget': session['budget'],
        'marketingBudget': session['marketing_budget'],
        'targetAudience': session['target_audience'],
        'releaseDate': session['release_date']
    }
    
    financial_chart = generate_bar_chart(
        ['Budget', 'Marketing', 'Box Office', 'Profit'],
        [
            movie_details['budget'],
            movie_details['marketingBudget'],
            results['boxOffice'],
            results['profit']
        ],
        'Financial Breakdown (in Crores ₹)',
        '',
        'Amount (Crores ₹)',
        ['#FF6384', '#FFA540', '#4BC0C0', '#36A2EB' if results['profit'] > 0 else '#FF6384']
    )
    
    performance_rating = calculate_performance_rating(results)
    
    return render_template(
        'results.html',
        active_tab='results',
        results=results,
        movie_details=movie_details,
        financial_chart=financial_chart,
        performance_rating=performance_rating
    )

@app.route('/reset_game')
def reset_game():
    session.clear() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)