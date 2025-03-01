#include "quiz.hpp"
#include <string>

// Quiz state
int questionIndex = 0;

std::string parseAnswer(const std::string& request) {
    // Extract answer from POST request
    size_t pos = request.find("answer=");
    if (pos == std::string::npos) return "";
    return request.substr(pos + 7);
}

void processAnswer(const std::string& answer) {
    // Process the answer and update quiz state
    questionIndex++;
}

std::string getQuizPage() {
    // Return the HTML for the current quiz question
    return "<h1>Quiz Page</h1>"; // Basic implementation
}

quiz::quiz() {
    head = NULL;
}

quiz::~quiz() {
    Song *current = head;
    while (current != nullptr) {
        Song *next = current->next;
        delete current;
        current = next;
    }
    head = nullptr;
}

string quiz::sortMC(string answer) { 
    //return ""; // Temporary return 
    // Generate 4 random songs for multiple choice
    string mcOptions[4];
    // Randomly select initial position (0-3) for the correct answer
    int initialPosition = rand() % 4;
    mcOptions[initialPosition] = answer; // Place correct answer in random position
    
    // Generate 3 other random songs that are different from the answer
    for (int i = 1; i < 4; i++) {
        Song* current = head;
        string randomArtist;
        bool unique;
        
        do {
            // Reset to start of list and get random position
            current = head;
            int randomPos = rand() % 20; // Assuming we have at least 20 songs
            
            // Move to random position in linked list
            for (int j = 0; j < randomPos && current != nullptr; j++) {
                current = current->next;
            }
            
            if (current != nullptr) {
                randomArtist = current->artist;
            }
            
            // Check if this artist is unique from other options
            unique = true;
            for (int k = 0; k < i; k++) {
                if (mcOptions[k] == randomArtist) {
                    unique = false;
                    break;
                }
            }
        } while (!unique || randomArtist == answer);
        
        mcOptions[i] = randomArtist;
    }
    
    // Randomly select which position (1-4) will be the correct answer
    int correctPosition = rand() % 4;
    
    // Swap the correct answer into the randomly chosen position
    string temp = mcOptions[correctPosition];
    mcOptions[correctPosition] = answer;
    mcOptions[0] = temp;
    
    // Display the multiple choice options
    cout << "\nWho is the artist of this song?\n";
    char optionLetter = 'A';
    for (int i = 0; i < 4; i++) {
        cout << optionLetter++ << ") " << mcOptions[i] << endl;
    }
    
    return mcOptions[correctPosition];
}
//play sound clip of song, then ask who is the artist and display the answer choices    bool validInput = false;    while(!validInput){        sortMC(song->artist);    }    return false; // Added return statement}