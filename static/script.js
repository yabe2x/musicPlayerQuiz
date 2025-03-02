// Global variables to track quiz state
let audioTimeout;
let hasSubmitted = false;
let isAudioPlaying = false;

// DOM Elements
let audioElement;
let submitButton;
let radioInputs;
let scoreElement;
let quizForm;
let loadingIndicator;

// Initialize the quiz when the page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeQuiz();
    setupEventListeners();
});

function initializeQuiz() {
    // Get DOM elements
    audioElement = document.getElementById('audio-preview');
    quizForm = document.getElementById('quiz-form');
    submitButton = document.querySelector('button[type="submit"]');
    radioInputs = document.querySelectorAll('input[type="radio"]');
    scoreElement = document.getElementById('score');
    
    // Create loading indicator
    loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading';
    loadingIndicator.style.display = 'none';
    document.querySelector('.quiz-container').appendChild(loadingIndicator);

    // Start playing preview if available
    if (audioElement) {
        playPreview();
    }
}

function setupEventListeners() {
    // Form submission
    if (quizForm) {
        quizForm.addEventListener('submit', submitAnswer);
    }

    // Audio controls
    if (audioElement) {
        audioElement.addEventListener('play', () => {
            isAudioPlaying = true;
            updatePlaybackUI(true);
        });

        audioElement.addEventListener('pause', () => {
            isAudioPlaying = false;
            updatePlaybackUI(false);
        });

        audioElement.addEventListener('ended', () => {
            isAudioPlaying = false;
            updatePlaybackUI(false);
        });
    }

    // Radio button interactions
    radioInputs.forEach(input => {
        input.addEventListener('change', () => {
            submitButton.disabled = false;
        });
    });
}

function playPreview() {
    if (!audioElement || isAudioPlaying) return;

    audioElement.play().catch(error => {
        console.log("Auto-play prevented:", error);
        showNotification("Click to play the song preview", "info");
    });

    // Stop after 10 seconds
    audioTimeout = setTimeout(() => {
        audioElement.pause();
        audioElement.currentTime = 0;
        showNotification("Preview ended. Make your guess!", "info");
    }, 10000);
}

function updatePlaybackUI(isPlaying) {
    const playingMessage = document.querySelector('.playing-message');
    if (playingMessage) {
        playingMessage.style.display = isPlaying ? 'block' : 'none';
    }
}

async function submitAnswer(event) {
    event.preventDefault();
    
    if (hasSubmitted) return;
    hasSubmitted = true;

    // Show loading indicator
    showLoading(true);
    
    // Disable form elements
    disableFormElements(true);
    
    const formData = new FormData(event.target);
    const selectedAnswer = formData.get('answer');
    
    try {
        const response = await fetch('/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answer: selectedAnswer
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Stop audio if playing
            stopAudio();
            
            // Show feedback
            showFeedback(data.correct, data.correct_answer);
            
            // Update score if provided
            if (data.score !== undefined && data.total !== undefined) {
                updateScore(data.score, data.total);
            }
            
            // Prepare for next question
            setTimeout(() => {
                window.location.href = '/quiz';
            }, 2000);
        } else {
            showNotification(data.error || "Error processing answer. Please try again.", "error");
            hasSubmitted = false;
            disableFormElements(false);
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification("Network error. Please try again.", "error");
        hasSubmitted = false;
        disableFormElements(false);
    } finally {
        showLoading(false);
    }
}

function showFeedback(isCorrect, correctAnswer) {
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
    feedbackDiv.innerHTML = isCorrect ? 
        '✅ Correct!' : 
        `❌ Incorrect! The correct answer was: ${correctAnswer}`;
    
    document.querySelector('.quiz-container').appendChild(feedbackDiv);
}

function updateScore(score, total) {
    if (scoreElement) {
        const percentage = ((score * 100) / total).toFixed(1);
        scoreElement.textContent = `Score: ${score}/${total} (${percentage}%)`;
        
        // Animate score change
        scoreElement.classList.add('score-update');
        setTimeout(() => scoreElement.classList.remove('score-update'), 1000);
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

function showLoading(show) {
    if (loadingIndicator) {
        loadingIndicator.style.display = show ? 'block' : 'none';
    }
}

function disableFormElements(disable) {
    submitButton.disabled = disable;
    radioInputs.forEach(input => input.disabled = disable);
}

function stopAudio() {
    if (audioElement) {
        audioElement.pause();
        audioElement.currentTime = 0;
        clearTimeout(audioTimeout);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    if (hasSubmitted) return;
    
    const key = event.key.toLowerCase();
    if (['a', 'b', 'c', 'd'].includes(key)) {
        const radioInput = document.querySelector(`input[value="${key}"]`);
        if (radioInput) {
            radioInput.checked = true;
            submitButton.disabled = false;
        }
    } else if (event.key === 'Enter' && !submitButton.disabled) {
        quizForm.requestSubmit();
    } else if (event.code === 'Space' && audioElement) {
        event.preventDefault();
        if (isAudioPlaying) {
            audioElement.pause();
        } else {
            audioElement.play();
        }
    }
});
