from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import logging
import os
import json

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Local song database
SONGS_DATABASE = [
    {
        "name": "Shape of You",
        "artist": "Ed Sheeran",
        "preview_url": "https://p.scdn.co/mp3-preview/84462d8e1e4d0f9e5ccd06f0da390f65843774a2"
    },
    {
        "name": "Blinding Lights",
        "artist": "The Weeknd",
        "preview_url": "https://p.scdn.co/mp3-preview/3ff1f9a43139f8c7606bfad8e8009e3dd8d02d8e"
    },
    {
        "name": "Bad Guy",
        "artist": "Billie Eilish",
        "preview_url": "https://p.scdn.co/mp3-preview/2f37da3eb08858d6d47d5a391d8c66e8e1083e57"
    },
    {
        "name": "Uptown Funk",
        "artist": "Mark Ronson ft. Bruno Mars",
        "preview_url": "https://p.scdn.co/mp3-preview/066d0f12b48af5c3c49b826c6f3f4744f7cc9e5c"
    },
    {
        "name": "Someone Like You",
        "artist": "Adele",
        "preview_url": "https://p.scdn.co/mp3-preview/49df5f5e0ba4c4f147bfb5152dc6a1056f7b3fa8"
    },
    {
        "name": "Shake It Off",
        "artist": "Taylor Swift",
        "preview_url": "https://p.scdn.co/mp3-preview/9ff05067562d0771eacc64fc88aa77a5e2c5f745"
    }
]

# List of additional artists for choices
ADDITIONAL_ARTISTS = [
    "Drake", "Lady Gaga", "Justin Bieber", "Ariana Grande", "Post Malone",
    "Dua Lipa", "Kendrick Lamar", "Rihanna", "Eminem", "Katy Perry"
]

# Global variables
current_song = None
current_choices = []
score = 0
total_questions = 0

def get_random_song():
    """Get a random song from our local database"""
    try:
        return random.choice(SONGS_DATABASE)
    except Exception as e:
        logger.error(f"Error getting random song: {str(e)}")
        return None

def get_artist_choices(correct_artist):
    """Get random artist choices including the correct one"""
    try:
        # Start with the correct artist
        choices = {correct_artist}
        
        # Add random artists from our database and additional artists list
        all_artists = ([song['artist'] for song in SONGS_DATABASE] + 
                      ADDITIONAL_ARTISTS)
        
        while len(choices) < 4:
            artist = random.choice(all_artists)
            if artist != correct_artist:
                choices.add(artist)
        
        # Convert to list and shuffle
        choices = list(choices)
        random.shuffle(choices)
        return choices
    except Exception as e:
        logger.error(f"Error getting artist choices: {str(e)}")
        return [correct_artist]

@app.route('/')
def index():
    global current_song, current_choices, score, total_questions
    
    try:
        current_song = get_random_song()
        if not current_song:
            error_msg = "Unable to fetch a song. Please try refreshing the page."
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
        
        # Get multiple choice options
        current_choices = get_artist_choices(current_song['artist'])
        
        return jsonify({
            'song': {
                'name': current_song['name'],
                'preview_url': current_song['preview_url']
            },
            'choices': current_choices
        })
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    global current_song, current_choices, score, total_questions
    
    try:
        if not current_song:
            return jsonify({
                'success': False,
                'error': 'No current song'
            })
        
        data = request.get_json()
        selected_artist = current_choices[int(data['answer'])]
        correct_artist = current_song['artist']
        
        total_questions += 1
        is_correct = selected_artist == correct_artist
        if is_correct:
            score += 1
        
        # Get next song
        next_song = get_random_song()
        next_choices = get_artist_choices(next_song['artist'])
        
        response = {
            'success': True,
            'correct': is_correct,
            'correctAnswer': correct_artist,
            'score': score,
            'total': total_questions,
            'nextSong': {
                'title': next_song['name'],
                'previewUrl': next_song['preview_url'],
                'options': next_choices
            }
        }
        
        # Update current song and choices for next question
        current_song = next_song
        current_choices = next_choices
        
        logger.info(f"Successfully processed answer. Correct: {is_correct}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in submit_answer route: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 