from .helpers import get_season, get_season_multiplier, get_competing_releases

def calculate_results(release_date, genre, budget, marketing_budget, competitor_data, market_data):
    month = release_date.split()[0] if release_date else None
    selected_month_data = next((m for m in market_data if m['month'] == month), None)
    
    if not selected_month_data:
        return default_results()
    
    # Get competing releases for the selected month
    competing_releases = get_competing_releases(competitor_data, month, genre)
    
    # Base potential calculation (in Crores ₹)
    base_potential = calculate_base_potential(budget, genre)
    
    # Normalize multipliers
    audience_multiplier = selected_month_data['audienceReceptivity'] / 10000
    marketing_multiplier = calculate_marketing_multiplier(marketing_budget, budget, selected_month_data)
    competition_impact = calculate_competition_impact(competing_releases, genre)
    season_multiplier = get_season_multiplier(month, genre)
    festival_bonus = calculate_festival_bonus(month)
    
    # Calculate final box office with balanced multipliers
    final_box_office = (
        base_potential * 
        (1 + audience_multiplier) *  # Convert to multiplier form
        marketing_multiplier * 
        competition_impact * 
        season_multiplier * 
        festival_bonus
    )
    
    # Financial calculations
    total_cost = budget + marketing_budget
    profit = final_box_office - total_cost
    roi = (profit / total_cost * 100) if total_cost > 0 else 0
    
    # Calculate Nash Equilibrium
    is_optimal = (
        selected_month_data['audienceReceptivity'] >= 60 and
        selected_month_data['competitionLevel'] <= 70 and
        competition_impact >= 0.7
    )
    
    return {
        'boxOffice': round(final_box_office, 2),
        'profit': round(profit, 2),
        'roi': round(roi, 1),
        'competingReleases': competing_releases,
        'marketConditions': {
            'audienceReceptivity': selected_month_data['audienceReceptivity'],
            'competitionLevel': selected_month_data['competitionLevel'],
            'marketingEffectiveness': selected_month_data['marketingEffectiveness']
        },
        'multipliers': {
            'audience': round(1 + audience_multiplier, 2),
            'marketing': round(marketing_multiplier, 2),
            'competition': round(competition_impact, 2),
            'seasonal': round(season_multiplier, 2),
            'festival': round(festival_bonus, 2)
        },
        'nashEquilibrium': {
            'isOptimal': is_optimal,
            'explanation': get_strategy_explanation(month, competing_releases, selected_month_data, genre),
            'recommendation': get_strategy_recommendation(month, competing_releases, selected_month_data, genre)
        }
    }

def is_optimal_release_date(month, competing_releases, month_data, genre):
    direct_competition = sum(1 for r in competing_releases if r['genre'] == genre)
    return (
        month_data['audienceReceptivity'] >= 70 and
        direct_competition <= 1 and
        month_data['marketingEffectiveness'] >= 60
    )

def get_strategy_explanation(month, competing_releases, month_data, genre):
    if is_optimal_release_date(month, competing_releases, month_data, genre):
        return "This release date represents a Nash Equilibrium as it maximizes potential returns while minimizing direct competition."
    else:
        return "This release date may not be optimal due to high competition or suboptimal market conditions."

def get_strategy_recommendation(month, competing_releases, month_data, genre):
    if is_optimal_release_date(month, competing_releases, month_data, genre):
        return "Maintain current release strategy"
    else:
        if month_data['audienceReceptivity'] < 70:
            return "Consider months with higher audience receptivity"
        elif len(competing_releases) > 1:
            return "Consider a month with less competition"
        else:
            return "Consider months with better marketing effectiveness"

def default_results():
    return {
        'boxOffice': 0,
        'profit': 0,
        'roi': 0,
        'competingReleases': [],
        'marketConditions': None,
        'multipliers': None
    }

def calculate_base_potential(budget, genre):
    genre_multipliers = {
        'action': 3.2,
        'comedy': 2.8,
        'crime_thriller': 2.6,
        'documentary': 1.5,
        'drama': 2.4,
        'fantasy': 3.1,
        'horror': 3.5,
        'musical': 2.7,
        'romance': 2.6,
        'scifi': 3.0,
        'sport': 2.3
    }
    return budget * genre_multipliers.get(genre, 2.8)

def calculate_marketing_multiplier(marketing_budget, budget, month_data):
    base_effectiveness = month_data['marketingEffectiveness'] / 10000  # Scale down
    budget_ratio = min(1.5, marketing_budget / budget)  # Cap the ratio
    return 1 + (budget_ratio * base_effectiveness)

def calculate_competition_impact(competing_releases, genre):
    direct_competition = sum(1 for r in competing_releases if r['genre'] == genre)
    indirect_competition = len(competing_releases) - direct_competition
    
    impact = 1 - (direct_competition * 0.15 + indirect_competition * 0.05)  # Reduced impact
    return max(0.6, min(1.0, impact))  # Ensure minimum impact isn't too severe

def calculate_base_potential(budget, genre):
    genre_multipliers = {
        'action': 2.2,  # Reduced from 2.8
        'comedy': 2.0,  # Reduced from 2.5
        'drama': 1.8,   # Reduced from 2.2
        'horror': 2.3,  # Reduced from 3.0
        'scifi': 2.1,   # Reduced from 2.7
        'family': 2.0   # Reduced from 2.6
    }
    return budget * genre_multipliers.get(genre, 2.0)

def calculate_festival_bonus(month):
    festival_months = {
        'October': 1.2,    # Reduced from 1.3 (Dussehra)
        'November': 1.25,  # Reduced from 1.4 (Diwali)
        'December': 1.2,   # Reduced from 1.3 (Christmas)
        'January': 1.15,   # Reduced from 1.2 (Pongal/Sankranti)
        'August': 1.1      # Reduced from 1.2 (Independence Day)
    }
    return festival_months.get(month, 1.0)

def calculate_performance_rating(results):
    roi = results['roi']
    if roi >= 100:
        return {'label': 'Blockbuster Success', 'class': 'success'}
    elif roi >= 50:
        return {'label': 'Hit', 'class': 'primary'}
    elif roi >= 0:
        return {'label': 'Break Even', 'class': 'info'}
    else:
        return {'label': 'Loss', 'class': 'danger'}