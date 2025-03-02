from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import logging
import os

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Local song database with direct MP3 URLs
SONGS_DATABASE = [
    {
        "name": "Bohemian Rhapsody",
        "artist": "Queen",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/a1/cd/3f/a1cd3f7c-1e7e-9969-e89c-8d2dd9c8b692/mzaf_17827647781880122741.plus.aac.p.m4a"
    },
    {
        "name": "Billie Jean",
        "artist": "Michael Jackson",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview112/v4/19/66/ea/1966ea5f-c0c4-9d0d-7ba3-114ee7ed8ea8/mzaf_14078433767887591126.plus.aac.p.m4a"
    },
    {
        "name": "Sweet Child O' Mine",
        "artist": "Guns N' Roses",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview122/v4/f5/be/3f/f5be3f9f-9f9b-d1f0-12e9-8f7963a85c85/mzaf_17274733736747140400.plus.aac.p.m4a"
    },
    {
        "name": "Like a Rolling Stone",
        "artist": "Bob Dylan",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview122/v4/e1/50/0c/e1500c51-a1f1-c393-7ed0-981c7c4fea62/mzaf_14298489205862427612.plus.aac.p.m4a"
    },
    {
        "name": "Imagine",
        "artist": "John Lennon",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview125/v4/1e/df/99/1edf99f0-7a8f-af6e-f889-25fd84d72a1d/mzaf_17172980231767075265.plus.aac.p.m4a"
    }
]

# Additional artists for multiple choice options
ADDITIONAL_ARTISTS = [
    "Elvis Presley", "David Bowie", "Prince", "The Beatles", "Led Zeppelin",
    "Pink Floyd", "The Rolling Stones", "U2", "Nirvana", "Bruce Springsteen"
]

# Game state
current_song = None
current_choices = []
score = 0
total_questions = 0

def get_random_song():
    """Get a random song from our local database"""
    return random.choice(SONGS_DATABASE)

def get_artist_choices(correct_artist):
    """Get random artist choices including the correct one"""
    choices = {correct_artist}
    available_artists = ADDITIONAL_ARTISTS + [song['artist'] for song in SONGS_DATABASE]
    
    while len(choices) < 4:
        artist = random.choice(available_artists)
        if artist != correct_artist:
            choices.add(artist)
    
    return list(choices)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/')
def get_question():
    """Get a new question"""
    global current_song, current_choices
    
    try:
        current_song = get_random_song()
        current_choices = get_artist_choices(current_song['artist'])
        random.shuffle(current_choices)
        
        return jsonify({
            'song': {
                'name': current_song['name'],
                'preview_url': current_song['preview_url']
            },
            'choices': current_choices
        })
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        return jsonify({'error': 'Failed to generate question'}), 500

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    """Submit an answer and get the next question"""
    global current_song, current_choices, score, total_questions
    
    try:
        if not current_song:
            return jsonify({'error': 'No active question'}), 400
        
        data = request.get_json()
        if 'answer' not in data:
            return jsonify({'error': 'No answer provided'}), 400
        
        selected_index = int(data['answer'])
        if selected_index < 0 or selected_index >= len(current_choices):
            return jsonify({'error': 'Invalid answer index'}), 400
        
        selected_artist = current_choices[selected_index]
        is_correct = selected_artist == current_song['artist']
        
        total_questions += 1
        if is_correct:
            score += 1
        
        # Get next question
        next_song = get_random_song()
        next_choices = get_artist_choices(next_song['artist'])
        random.shuffle(next_choices)
        
        response = {
            'correct': is_correct,
            'correctAnswer': current_song['artist'],
            'score': score,
            'total': total_questions,
            'nextSong': {
                'title': next_song['name'],
                'previewUrl': next_song['preview_url'],
                'options': next_choices
            }
        }
        
        # Update current question
        current_song = next_song
        current_choices = next_choices
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing answer: {str(e)}")
        return jsonify({'error': 'Failed to process answer'}), 500

if __name__ == '__main__':
    # Clear port 5001 if it's in use
    os.system("lsof -ti:5001 | xargs kill -9 2>/dev/null")
    app.run(debug=True, host='0.0.0.0', port=5001) 