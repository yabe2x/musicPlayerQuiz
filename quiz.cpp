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


