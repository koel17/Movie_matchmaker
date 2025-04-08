from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Movie data (from original code, updated for consistency)
mood_to_genre = {
    "happy": ["comedy", "musical", "animated"],
    "sad": ["drama", "romance"],
    "angry": ["action", "thriller", "horror"],
    "anxious": ["comedy", "documentary"],
    "bored": ["action", "sci-fi", "thriller"],
    "soothing": ["documentary", "animated"],
    "romantic": ["romance", "musical"],
    "thoughtful": ["drama", "documentary"],
    "excited": ["action", "sci-fi"],
    "scared": ["horror", "thriller"],
    "curious": ["documentary", "sci-fi"]
}

genre_to_movies = {
    "comedy": [
        {"title": "The Hangover", "rating": "7.7/10", "description": "A bachelor party gone hilariously wrong in Las Vegas"},
        {"title": "Bridesmaids", "rating": "6.8/10", "description": "Competition between the maid of honor and a bridesmaid"},
        {"title": "Superbad", "rating": "7.6/10", "description": "Two high school friends try to lose their virginity before graduation"},
        {"title": "The Grand Budapest Hotel", "rating": "8.1/10", "description": "Adventures of a legendary concierge and his trusted lobby boy"},
        {"title": "Game Night", "rating": "6.9/10", "description": "A group's game night becomes a real-life mystery"}
    ],
    "romance": [
        {"title": "Eternal Sunshine of the Spotless Mind", "rating": "8.3/10", "description": "A couple erases each other from their memories"},
        {"title": "500 Days of Summer", "rating": "7.7/10", "description": "A non-linear telling of a romance that spans 500 days"},
        {"title": "Pride and Prejudice", "rating": "7.8/10", "description": "The story of Elizabeth Bennet and Mr. Darcy"},
        {"title": "About Time", "rating": "7.8/10", "description": "A man uses time travel to find love"},
        {"title": "Carol", "rating": "7.2/10", "description": "A forbidden affair between two women in 1950s New York"}
    ],
    "musical": [
        {"title": "The Greatest Showman", "rating": "7.6/10", "description": "The story of P.T. Barnum and his circus"},
        {"title": "Les Misérables", "rating": "7.6/10", "description": "Musical adaptation of Victor Hugo's classic novel"},
        {"title": "Hamilton", "rating": "8.4/10", "description": "The story of American founding father Alexander Hamilton"},
        {"title": "Into the Woods", "rating": "5.9/10", "description": "A modern twist on several beloved fairy tales"},
        {"title": "Chicago", "rating": "7.2/10", "description": "Murder, greed, and showbiz in 1920s Chicago"}
    ],
    "drama": [
        {"title": "The Shawshank Redemption", "rating": "9.3/10", "description": "A banker's journey through decades in prison"},
        {"title": "Schindler's List", "rating": "9.0/10", "description": "A businessman saves Jews during the Holocaust"},
        {"title": "A Beautiful Mind", "rating": "8.2/10", "description": "The story of mathematician John Nash"},
        {"title": "Manchester by the Sea", "rating": "7.8/10", "description": "A man becomes guardian of his teenage nephew"},
        {"title": "Moonlight", "rating": "7.4/10", "description": "A young man's journey of self-discovery"}
    ],
    "action": [
        {"title": "The Dark Knight", "rating": "9.0/10", "description": "Batman faces his greatest nemesis, the Joker"},
        {"title": "Mission: Impossible - Fallout", "rating": "7.7/10", "description": "Ethan Hunt's most dangerous mission yet"},
        {"title": "Top Gun: Maverick", "rating": "8.3/10", "description": "Top aviator trains elite graduates for a special mission"},
        {"title": "The Bourne Ultimatum", "rating": "8.0/10", "description": "Jason Bourne's search for his true identity"},
        {"title": "Edge of Tomorrow", "rating": "7.9/10", "description": "A soldier caught in a time loop during an alien invasion"}
    ],
    "thriller": [
        {"title": "Parasite", "rating": "8.5/10", "description": "A poor family schemes to become employed by a wealthy family"},
        {"title": "Shutter Island", "rating": "8.2/10", "description": "A U.S. Marshal investigates a psychiatric facility"},
        {"title": "Nightcrawler", "rating": "7.8/10", "description": "A man discovers the world of L.A. crime journalism"},
        {"title": "Get Out", "rating": "7.7/10", "description": "A young man uncovers a disturbing secret about his girlfriend's family"},
        {"title": "Ex Machina", "rating": "7.7/10", "description": "A programmer participates in an AI experiment"}
    ],
    "sci-fi": [
        {"title": "Arrival", "rating": "7.9/10", "description": "A linguist tries to communicate with alien visitors"},
        {"title": "The Martian", "rating": "8.0/10", "description": "An astronaut struggles to survive on Mars"},
        {"title": "Dune", "rating": "8.0/10", "description": "A noble family becomes involved in a war for a dangerous planet"},
        {"title": "District 9", "rating": "7.9/10", "description": "Aliens become refugees in South Africa"},
        {"title": "Annihilation", "rating": "6.8/10", "description": "A biologist enters a mysterious quarantined zone"}
    ],
    "horror": [
        {"title": "Hereditary", "rating": "7.3/10", "description": "A family unravels cryptic and terrifying secrets"},
        {"title": "A Quiet Place", "rating": "7.5/10", "description": "A family must live in silence to avoid mysterious creatures"},
        {"title": "The Babadook", "rating": "6.8/10", "description": "A single mother battles with her son's fear of a monster"},
        {"title": "It Follows", "rating": "6.8/10", "description": "A teenager is pursued by a supernatural entity"},
        {"title": "Train to Busan", "rating": "7.6/10", "description": "Passengers struggle to survive a zombie outbreak on a train"}
    ],
    "documentary": [
        {"title": "Free Solo", "rating": "8.1/10", "description": "A climber attempts to scale El Capitan without ropes"},
        {"title": "My Octopus Teacher", "rating": "8.1/10", "description": "A filmmaker forges a relationship with an octopus"},
        {"title": "The Last Dance", "rating": "9.1/10", "description": "The story of Michael Jordan and the Chicago Bulls"},
        {"title": "Won't You Be My Neighbor?", "rating": "8.3/10", "description": "The life of Fred Rogers"},
        {"title": "Blackfish", "rating": "8.1/10", "description": "The controversy of killer whales in captivity"}
    ],
    "animated": [
        {"title": "Spider-Man: Into the Spider-Verse", "rating": "8.4/10", "description": "Multiple Spider-People team up to save reality"},
        {"title": "Your Name", "rating": "8.4/10", "description": "Two teenagers mysteriously swap bodies"},
        {"title": "Inside Out", "rating": "8.2/10", "description": "The emotions inside a young girl's head come to life"},
        {"title": "How to Train Your Dragon", "rating": "8.1/10", "description": "A Viking befriends a dragon"},
        {"title": "Zootopia", "rating": "8.0/10", "description": "A rabbit police officer solves a conspiracy"}
    ]
}

watch_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    data = request.get_json()
    mood = data.get('mood', '').lower()
    intensity = int(data.get('intensity', 3))
    num_suggestions = int(data.get('num_suggestions', 1))

    if mood in mood_to_genre:
        possible_genres = mood_to_genre[mood]
        selected_genre = random.choice(possible_genres)
        suggestions = random.sample(genre_to_movies[selected_genre], min(num_suggestions, len(genre_to_movies[selected_genre])))

        for movie in suggestions:
            watch_history.append(movie['title'])
            if len(watch_history) > 3:
                watch_history.pop(0)

        return jsonify({
            'success': True,
            'genre': selected_genre,
            'suggestions': suggestions,
            'watch_history': watch_history
        })

    return jsonify({
        'success': False,
        'message': "Sorry, I don't have recommendations for that mood yet!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)