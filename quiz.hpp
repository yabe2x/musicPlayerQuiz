#pragma once

#include <iostream>
#include <iomanip>
#include <fstream>
#include <ostream>
#include <sstream>
#include <string>

using namespace std;
struct Song{
    string question;
    string artist;
    Song *next;
};




class quiz
{
private:
    string answer;
    string artist;
    Song *head;
    int highScores[10];
    int highScoresIndex = 0;
    Song *choices[4];

    
public:
    quiz();
    ~quiz();
    bool displayAnswers(Song *song); //after song is played, gives user multiple choice options to choose from and makes sure user input is valid. Returns true if user answer is correct, returns false otherwise
    string sortMC(); //sorts answers out, randomly having answer as A, B, C, or D
    void readInSongs(fstream file); //reads in file of songs and creates a linked list out of all the songs
    Song returnSong(); // randomly selects a song from the linked list of songs for the user to guess the artist based off the sound clip

    
};

quiz::quiz(/* args */)
{
}

quiz::~quiz()
{
}

std::string getQuizPage();
std::string parseAnswer(const std::string& request);
void processAnswer(const std::string& answer);

