import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Button, 
  RadioGroup, 
  FormControlLabel, 
  Radio, 
  Paper,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import axios from 'axios';

const Quiz = () => {
  const [currentSong, setCurrentSong] = useState(null);
  const [choices, setChoices] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [feedback, setFeedback] = useState({ show: false, message: '', type: 'success' });

  useEffect(() => {
    fetchNewQuestion();
  }, []);

  const fetchNewQuestion = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5001/');
      const data = response.data;
      setCurrentSong(data.song);
      setChoices(data.choices);
      setSelectedAnswer('');
      setError(null);
    } catch (err) {
      setError('Failed to fetch question. Please try again.');
      console.error('Error fetching question:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5001/submit-answer', {
        answer: choices.indexOf(selectedAnswer)
      });
      
      const data = response.data;
      
      if (data.correct) {
        setFeedback({
          show: true,
          message: `Correct! The artist is ${data.correctAnswer}`,
          type: 'success'
        });
      } else {
        setFeedback({
          show: true,
          message: `Incorrect. The artist is ${data.correctAnswer}`,
          type: 'error'
        });
      }
      
      setScore({ correct: data.score, total: data.total });
      
      // Load next question after delay
      setTimeout(() => {
        if (data.nextSong) {
          setCurrentSong({
            name: data.nextSong.title,
            preview_url: data.nextSong.previewUrl
          });
          setChoices(data.nextSong.options);
          setSelectedAnswer('');
        }
        setFeedback({ show: false, message: '', type: 'success' });
      }, 2000);
    } catch (err) {
      setError('Failed to submit answer. Please try again.');
      console.error('Error submitting answer:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !currentSong) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchNewQuestion}>
            Retry
          </Button>
        }>
          {error}
        </Alert>
      </Box>
    );
  }

  return (
    <Container maxWidth="sm">
      <Box py={4}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Music Quiz
        </Typography>
        
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Score: {score.correct}/{score.total}
            {score.total > 0 && ` (${((score.correct / score.total) * 100).toFixed(1)}%)`}
          </Typography>
        </Paper>

        {currentSong && (
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Song: "{currentSong.name}"
            </Typography>
            
            <Box my={3}>
              <audio controls style={{ width: '100%' }}>
                <source src={currentSong.preview_url} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            </Box>

            <Typography variant="h6" gutterBottom>
              Who is the artist?
            </Typography>

            <RadioGroup
              value={selectedAnswer}
              onChange={(e) => setSelectedAnswer(e.target.value)}
            >
              {choices.map((choice, index) => (
                <FormControlLabel
                  key={index}
                  value={choice}
                  control={<Radio />}
                  label={choice}
                  disabled={loading}
                />
              ))}
            </RadioGroup>

            <Box mt={3}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={handleSubmit}
                disabled={!selectedAnswer || loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Submit Answer'}
              </Button>
            </Box>
          </Paper>
        )}
      </Box>

      <Snackbar
        open={feedback.show}
        autoHideDuration={2000}
        onClose={() => setFeedback({ ...feedback, show: false })}
      >
        <Alert severity={feedback.type} sx={{ width: '100%' }}>
          {feedback.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Quiz; 