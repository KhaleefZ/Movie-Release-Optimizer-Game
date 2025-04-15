import random

def get_season(month):
    season_map = {
        "January": "regular", "February": "regular", "March": "regular",
        "April": "summer", "May": "summer", "June": "summer",
        "July": "regular", "August": "regular", "September": "regular",
        "October": "diwali", "November": "diwali", "December": "christmas"
    }
    return season_map.get(month, "regular")

def get_season_multiplier(month, genre):
    seasons = {
        'summer': ['April', 'May', 'June'],
        'diwali': ['October', 'November'],
        'christmas': ['December'],
        'regular': ['January', 'February', 'March', 'July', 'August', 'September']
    }
    
    genre_multipliers = {
        'action': {
            'summer': 1.6, 'diwali': 1.8, 'christmas': 1.5, 'regular': 1.0
        },
        'comedy': {
            'summer': 1.4, 'diwali': 1.6, 'christmas': 1.5, 'regular': 1.1
        },
        'drama': {
            'summer': 1.1, 'diwali': 1.4, 'christmas': 1.3, 'regular': 1.0
        },
        'horror': {
            'summer': 1.2, 'diwali': 1.0, 'christmas': 0.9, 'regular': 1.1
        },
        'scifi': {
            'summer': 1.5, 'diwali': 1.4, 'christmas': 1.4, 'regular': 1.0
        },
        'family': {
            'summer': 1.5, 'diwali': 1.7, 'christmas': 1.8, 'regular': 1.2
        }
    }
    
    current_season = 'regular'
    for season, months in seasons.items():
        if month in months:
            current_season = season
            break
    
    genre_season_multipliers = genre_multipliers.get(genre, genre_multipliers['action'])
    return genre_season_multipliers.get(current_season, 1.0)

def find_most_common(arr):
    counts = {}
    max_count = 0
    most_common = None
    
    for item in arr:
        if item not in counts:
            counts[item] = 0
        counts[item] += 1
        
        if counts[item] > max_count:
            max_count = counts[item]
            most_common = item
    
    return most_common

def capitalize_first_letter(string):
    return string[0].upper() + string[1:]

def get_competing_releases(competitor_data, month, genre):
    competing_releases = []
    for competitor in competitor_data:
        for release in competitor['releases']:
            if release['month'] == month:
                release_info = release.copy()
                release_info['studioName'] = competitor['name']
                release_info['studioStrength'] = competitor['strength']
                release_info['competitionLevel'] = (
                    'High' if release['genre'] == genre else 'Moderate'
                )
                competing_releases.append(release_info)
    return competing_releases

def get_random_genre(exclude_genre):
    genres = ["action", "comedy", "crime_thriller", "documentary", "drama", 
              "fantasy", "horror", "musical", "romance", "scifi", "sport"]
    available_genres = [g for g in genres if g != exclude_genre]
    return random.choice(available_genres)

def get_season_multiplier(month, genre):
    seasons = {
        'summer': ['April', 'May', 'June'],
        'diwali': ['October', 'November'],
        'christmas': ['December'],
        'regular': ['January', 'February', 'March', 'July', 'August', 'September']
    }
    
    genre_multipliers = {
        'action': {'summer': 1.6, 'diwali': 1.8, 'christmas': 1.5, 'regular': 1.0},
        'comedy': {'summer': 1.4, 'diwali': 1.6, 'christmas': 1.5, 'regular': 1.1},
        'crime_thriller': {'summer': 1.2, 'diwali': 1.3, 'christmas': 1.2, 'regular': 1.0},
        'documentary': {'summer': 1.0, 'diwali': 1.1, 'christmas': 1.1, 'regular': 1.0},
        'drama': {'summer': 1.1, 'diwali': 1.4, 'christmas': 1.3, 'regular': 1.0},
        'fantasy': {'summer': 1.5, 'diwali': 1.5, 'christmas': 1.6, 'regular': 1.1},
        'horror': {'summer': 1.2, 'diwali': 1.0, 'christmas': 0.9, 'regular': 1.1},
        'musical': {'summer': 1.3, 'diwali': 1.5, 'christmas': 1.6, 'regular': 1.1},
        'romance': {'summer': 1.3, 'diwali': 1.4, 'christmas': 1.5, 'regular': 1.1},
        'scifi': {'summer': 1.5, 'diwali': 1.4, 'christmas': 1.4, 'regular': 1.0},
        'sport': {'summer': 1.4, 'diwali': 1.2, 'christmas': 1.1, 'regular': 1.0}
    }
    current_season = 'regular'
    for season, months in seasons.items():
        if month in months:
            current_season = season
            break
    
    genre_season_multipliers = genre_multipliers.get(genre, genre_multipliers['action'])
    return genre_season_multipliers.get(current_season, 1.0)

def generate_movie_title(genre):
    title_components = {
        'action': {
            'prefixes': ["The", "Ultimate", "Extreme", "Deadly", "Rogue"],
            'nouns': ["Mission", "Warrior", "Agent", "Vengeance", "Protocol"]
        },
        'comedy': {
            'prefixes': ["Crazy", "Hilarious", "Awkward", "Wild", "Unexpected"],
            'nouns': ["Vacation", "Wedding", "Family", "Neighbors", "Journey"]
        },
        'crime_thriller': {
            'prefixes': ["Dark", "Silent", "Deadly", "Hidden", "Last"],
            'nouns': ["Evidence", "Detective", "Mystery", "Crime", "Case"]
        },
        'documentary': {
            'prefixes': ["Inside", "Beyond", "Untold", "Secret", "Lost"],
            'nouns': ["Story", "Truth", "World", "Journey", "Legacy"]
        },
        'drama': {
            'prefixes': ["Lost", "Broken", "Silent", "Eternal", "Forgotten"],
            'nouns': ["Promise", "Memory", "Echo", "Legacy", "Shadow"]
        },
        'fantasy': {
            'prefixes': ["Mystic", "Enchanted", "Magical", "Ancient", "Legendary"],
            'nouns': ["Kingdom", "Crystal", "Legend", "Realm", "Quest"]
        },
        'horror': {
            'prefixes': ["Dark", "Haunted", "Cursed", "Sinister", "Nightmare"],
            'nouns': ["House", "Forest", "Ritual", "Presence", "Whisper"]
        },
        'musical': {
            'prefixes': ["Singing", "Dancing", "Rhythmic", "Melodic", "Musical"],
            'nouns': ["Heart", "Dreams", "Stage", "Symphony", "Beat"]
        },
        'romance': {
            'prefixes': ["Love's", "Sweet", "Forever", "Perfect", "Endless"],
            'nouns': ["Romance", "Heart", "Love", "Kiss", "Destiny"]
        },
        'scifi': {
            'prefixes': ["Quantum", "Galactic", "Cyber", "Neural", "Temporal"],
            'nouns': ["Horizon", "Protocol", "Dimension", "Singularity", "Convergence"]
        },
        'sport': {
            'prefixes': ["Champion", "Winning", "Ultimate", "Golden", "Legendary"],
            'nouns': ["Goal", "Victory", "Spirit", "Game", "Champion"]
        }
    }
    
    components = title_components.get(genre, title_components['action'])
    prefix = random.choice(components['prefixes'])
    noun = random.choice(components['nouns'])
    
    return f"{prefix} {noun}"