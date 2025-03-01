#include "quiz.hpp"

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

    
public:
    quiz();
    ~quiz();
    bool displayAnswers(Song *song); //after song is played, gives user multiple choice options to choose from and makes sure user input is valid. Returns true if user answer is correct, returns false otherwise
    string sortMC(string answer); //sorts answers out, randomly having answer as A, B, C, or D
    void readInSongs(fstream file); //reads in file of songs and creates a linked list out of all the songs
    Song returnSong(); // randomly selects a song from the linked list of songs for the user to guess the artist based off the sound clip
    
    
};






quiz::quiz()
{
    head = NULL;
}

quiz::~quiz()
{
    Song *temp;
    while(temp != NULL){
        temp = head->next;
        delete head;
    }
}

string sortMC(string answer){

}

bool quiz::displayAnswers(Song *song){
    //play sound clip of song, then ask who is the artist and display the answer choices
    bool validInput = false;
    while(!validInput){

    
        sortMC(song->artist);
    }
}
