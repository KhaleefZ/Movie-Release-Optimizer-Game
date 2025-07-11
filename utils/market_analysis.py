import random
from .helpers import get_random_genre, generate_movie_title, find_most_common, get_season_multiplier, get_season  # Added get_season

# Define months at module level so it's accessible to all functions
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def generate_market_data(genre):
    # Reduced seasonal multipliers with more realistic ranges
    genre_seasonality = {
        'action': {'summer': 1.15, 'diwali': 1.2, 'christmas': 1.15, 'regular': 1.0},
        'comedy': {'summer': 1.1, 'diwali': 1.15, 'christmas': 1.15, 'regular': 1.05},
        'crime_thriller': {'summer': 1.05, 'diwali': 1.1, 'christmas': 1.1, 'regular': 1.0},
        'documentary': {'summer': 1.0, 'diwali': 1.05, 'christmas': 1.05, 'regular': 1.0},
        'drama': {'summer': 1.05, 'diwali': 1.1, 'christmas': 1.1, 'regular': 1.0},
        'fantasy': {'summer': 1.15, 'diwali': 1.15, 'christmas': 1.2, 'regular': 1.05},
        'horror': {'summer': 1.05, 'diwali': 0.95, 'christmas': 0.9, 'regular': 1.1},
        'musical': {'summer': 1.1, 'diwali': 1.15, 'christmas': 1.2, 'regular': 1.05},
        'romance': {'summer': 1.1, 'diwali': 1.15, 'christmas': 1.15, 'regular': 1.05},
        'scifi': {'summer': 1.15, 'diwali': 1.1, 'christmas': 1.1, 'regular': 1.0},
        'sport': {'summer': 1.15, 'diwali': 1.05, 'christmas': 1.05, 'regular': 1.0}
    }
    
    # Monthly base values for audience and competition
    monthly_base_values = {
        "January": {'audience': 45, 'competition': 50},    # Post-holiday season
        "February": {'audience': 40, 'competition': 45},   # Regular month
        "March": {'audience': 45, 'competition': 50},      # Exam season
        "April": {'audience': 60, 'competition': 65},      # Summer vacation starts
        "May": {'audience': 65, 'competition': 70},        # Peak summer
        "June": {'audience': 70, 'competition': 75},       # Summer vacation
        "July": {'audience': 50, 'competition': 55},       # Regular month
        "August": {'audience': 55, 'competition': 60},     # Independence Day
        "September": {'audience': 45, 'competition': 50},  # Regular month
        "October": {'audience': 65, 'competition': 70},    # Dussehra season
        "November": {'audience': 70, 'competition': 75},   # Diwali season
        "December": {'audience': 65, 'competition': 70}    # Christmas season
    }
    
    current_genre_seasonality = genre_seasonality.get(genre, genre_seasonality['action'])
    result = []
    
    for month in MONTHS:
        base_values = monthly_base_values[month]
        season = get_season(month)  # Changed from season_map[month] to get_season(month)
        season_multiplier = current_genre_seasonality.get(season, 1.0)
        
        # Calculate audience receptivity (30-75% range)
        base_audience = base_values['audience']
        audience_variation = random.uniform(-5, 5)
        final_audience = min(75, max(30, base_audience + audience_variation))
        
        # Calculate competition level (30-80% range)
        base_competition = base_values['competition']
        competition_variation = random.uniform(-5, 5)
        final_competition = min(80, max(30, base_competition + competition_variation))
        
        # Calculate marketing effectiveness based on season and festival
        marketing_effectiveness = calculate_marketing_effectiveness(month, season)
        
        # Calculate profit potential based on all factors
        profit_potential = calculate_profit_potential(
            final_audience,
            final_competition,
            marketing_effectiveness,
            season_multiplier
        )
        
        result.append({
            'month': month,
            'season': season,
            'audienceReceptivity': round(final_audience, 1),
            'competitionLevel': round(final_competition, 1),
            'marketingEffectiveness': round(marketing_effectiveness, 1),
            'profitPotential': round(profit_potential, 1)
        })
    
    return result

def calculate_marketing_effectiveness(month, season):
    # Base marketing effectiveness by season
    season_marketing = {
        'summer': 65,
        'diwali': 70,
        'christmas': 70,
        'regular': 55
    }
    
    # Festival bonus for specific months
    festival_bonus = {
        'October': 10,    # Dussehra
        'November': 15,   # Diwali
        'December': 10,   # Christmas
        'January': 5,     # New Year
        'August': 5       # Independence Day
    }
    
    base_effectiveness = season_marketing.get(season, 55)
    bonus = festival_bonus.get(month, 0)
    variation = random.uniform(-5, 5)
    
    return min(75, max(30, base_effectiveness + bonus + variation))

def calculate_profit_potential(audience, competition, marketing, season_multiplier):
    # Calculate profit potential (20-80 range)
    base_potential = (audience / competition) * 50
    marketing_impact = (marketing / 100) * 20
    seasonal_impact = (season_multiplier - 1) * 15
    
    final_potential = base_potential + marketing_impact + seasonal_impact
    return min(80, max(20, final_potential))

def generate_competitor_data(genre):
    competitors = [
        {'name': 'Blockbuster Studios', 'strength': 85, 'strategy': 'Aggressive'},
        {'name': 'Indie Films Inc.', 'strength': 60, 'strategy': 'Niche'},
        {'name': 'Global Entertainment', 'strength': 75, 'strategy': 'Balanced'},
        {'name': 'Artistic Productions', 'strength': 65, 'strategy': 'Quality-focused'}
    ]
    
    result = []
    for competitor in competitors:
        number_of_releases = 1 + random.randint(0, 1)
        releases = []
        
        for _ in range(number_of_releases):
            release_month = random.choice(MONTHS)  # Use MONTHS constant
            movie_genre = genre if random.random() > 0.6 else get_random_genre(genre)
            movie_budget = 20 + random.randint(0, 50)  # Reduced budget range
            
            releases.append({
                'title': generate_movie_title(movie_genre),
                'month': release_month,
                'genre': movie_genre,
                'budget': movie_budget,
                'marketingBudget': int(movie_budget * 0.3)  # Reduced marketing ratio
            })
        
        competitor_copy = competitor.copy()
        competitor_copy['releases'] = releases
        result.append(competitor_copy)
    
    return result

def analyze_seasonal_trends(market_data, genre):
    seasonal_data = {
        'summer': {'months': [], 'avgAudience': 0, 'avgCompetition': 0, 'avgProfit': 0},
        'diwali': {'months': [], 'avgAudience': 0, 'avgCompetition': 0, 'avgProfit': 0},
        'christmas': {'months': [], 'avgAudience': 0, 'avgCompetition': 0, 'avgProfit': 0},
        'regular': {'months': [], 'avgAudience': 0, 'avgCompetition': 0, 'avgProfit': 0}
    }
    
    # Genre-specific game theory insights
    genre_insights = {
        'action': {
            'summer': "Action movies perform exceptionally well in summer due to school holidays and increased youth audience.",
            'diwali': "Diwali season historically favors action blockbusters with family appeal.",
            'christmas': "End-year holidays provide good opportunity for action-adventure releases.",
            'regular': "Regular seasons require strong marketing to maintain audience interest."
        },
        'comedy': {
            'summer': "Light-hearted comedies are perfect for summer vacation mood.",
            'diwali': "Festival season amplifies comedy appeal across all demographics.",
            'christmas': "Holiday season particularly favors family-friendly comedies.",
            'regular': "Comedy performs consistently well throughout regular seasons."
        },
        'drama': {
            'summer': "Drama films face tough competition from blockbusters in summer.",
            'diwali': "Festival season offers good platform for meaningful dramas.",
            'christmas': "Year-end awards season boosts serious drama prospects.",
            'regular': "Regular seasons are ideal for dramatic releases with less competition."
        },
        'horror': {
            'summer': "Horror films can counter-program against summer blockbusters.",
            'diwali': "Festival season typically challenging for horror releases.",
            'christmas': "Holiday season generally unfavorable for horror genre.",
            'regular': "Regular seasons provide stable audience for horror releases."
        },
        'romance': {
            'summer': "Summer romance films appeal to younger audiences.",
            'diwali': "Festival season enhances family-oriented romance appeal.",
            'christmas': "Holiday season particularly strong for romantic releases.",
            'regular': "Valentine's season in regular months offers opportunities."
        },
        'scifi': {
            'summer': "Sci-fi blockbusters dominate summer box office.",
            'diwali': "Festival season good for sci-fi with cultural elements.",
            'christmas': "Holiday season favors spectacular sci-fi releases.",
            'regular': "Regular seasons need strong marketing for sci-fi success."
        }
    }

    for data in market_data:
        season = data['season']
        seasonal_data[season]['months'].append(data['month'])
        seasonal_data[season]['avgAudience'] += data['audienceReceptivity']
        seasonal_data[season]['avgCompetition'] += data['competitionLevel']
        seasonal_data[season]['avgProfit'] += data['profitPotential']
    
    for season in seasonal_data:
        month_count = len(seasonal_data[season]['months'])
        if month_count > 0:
            seasonal_data[season]['avgAudience'] /= month_count
            seasonal_data[season]['avgCompetition'] /= month_count
            seasonal_data[season]['avgProfit'] /= month_count
    
    sorted_seasons = []
    for season in seasonal_data:
        sorted_seasons.append({
            'season': season,
            'months': seasonal_data[season]['months'],
            'avgProfit': seasonal_data[season]['avgProfit'],
            'avgAudience': seasonal_data[season]['avgAudience'],
            'avgCompetition': seasonal_data[season]['avgCompetition'],
            'insight': genre_insights.get(genre, {}).get(season, "General market conditions apply.")
        })
    
    sorted_seasons.sort(key=lambda x: x['avgProfit'], reverse=True)
    
    best_seasons = sorted_seasons[:2]
    worst_seasons = sorted_seasons[-2:]
    
    return {
        'bestSeasons': best_seasons,
        'worstSeasons': worst_seasons,
        'gameTheoryInsight': genre_insights.get(genre, {}).get(sorted_seasons[0]['season'], 
            "Consider market dynamics and competition levels when planning your release."),
        'seasonalStrategies': {
            season['season']: {
                'months': season['months'],
                'insight': season['insight'],
                'metrics': {
                    'avgProfit': round(season['avgProfit'], 2),
                    'avgAudience': round(season['avgAudience'], 2),
                    'avgCompetition': round(season['avgCompetition'], 2)
                }
            } for season in sorted_seasons
        }
    }

def analyze_competitor_strategies(competitor_data):
    # Use MONTHS constant instead of redefining
    month_counts = {month: 0 for month in MONTHS}
    
    for competitor in competitor_data:
        for release in competitor['releases']:
            month_counts[release['month']] += 1
    
    sorted_months = sorted(month_counts.items(), key=lambda x: x[1])
    
    lowest_competition_months = [month for month, count in sorted_months[:3]]
    highest_competition_months = [month for month, count in sorted_months[-3:]][::-1]
    
    competitor_strategies = [competitor['strategy'] for competitor in competitor_data]
    dominant_strategy = find_most_common(competitor_strategies)
    
    strategy_descriptions = {
        "Aggressive": "high-budget blockbusters with wide releases",
        "Niche": "targeting specific audience segments with specialized content",
        "Balanced": "maintaining a mix of commercial appeal and artistic merit",
        "Quality-focused": "prioritizing critical acclaim over commercial success"
    }
    
    return {
        'dominantStrategies': f"The dominant strategy among competitors appears to be \"{dominant_strategy}\". This suggests that most studios are focusing on {strategy_descriptions.get(dominant_strategy, '')}.",
        'counterProgramming': f"The months with lowest competition are {', '.join(lowest_competition_months)}. These represent potential opportunities for counter-programming, where your film can capture audience attention with less competitive pressure. Conversely, {', '.join(highest_competition_months)} show the highest concentration of competing releases.",
        'nashEquilibrium': "According to Nash Equilibrium principles, the optimal strategy would be to avoid direct competition with similar films while still releasing in months with good audience receptivity. This suggests exploring release windows where your film offers something distinctly different from competitors, creating a situation where neither you nor competitors would benefit from changing release strategies."
    }  # Added closing bracket here