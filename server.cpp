#include "crow.h"
#include <vector>
#include <cstdlib>
#include <ctime>

struct Question {
    std::string songName;
    std::string correctArtist;
    std::vector<std::string> options;
};

// Sample questions (replace with actual song snippets)
std::vector<Question> quiz = {
    {"Song A", "The Weeknd", {"The Weeknd", "Drake", "Kanye West", "Travis Scott"}},
    {"Song B", "Beyoncé", {"Beyoncé", "Alicia Keys", "Mariah Carey", "Rihanna"}},
    {"Song C", "Kendrick Lamar", {"Kendrick Lamar", "J. Cole", "Lil Wayne", "Nas"}}
};

int questionIndex = 0;
bool lastAnswerWrong = false;

crow::response generateQuizPage() {
    if (questionIndex >= quiz.size()) {
        questionIndex = 0; // Reset quiz
    }

    Question& q = quiz[questionIndex];

    std::string bodyClass = lastAnswerWrong ? "flash-red" : "";

    std::string html = R"(
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Music Quiz</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body class=")" + bodyClass + R"(">
            <div class="quiz-container">
                <h1>Music Quiz</h1>
                <div class="playing-message">Now Playing: )" + q.songName + R"(...</div>
                <form action="/submit-answer" method="post">
                    <p>Who is the artist of this song?</p>
                    <div class="btn-container">
    )";

    for (const auto& answer : q.options) {
        html += "<input type='radio' name='answer' value='" + answer + "' required> " + answer + "<br>";
    }

    html += R"(
                    </div>
                    <input type="hidden" name="correct" value=")" + q.correctArtist + R"(">
                    <button type="submit">Submit Answer</button>
                </form>
            </div>
        </body>
        </html>
    )";

    return crow::response{html};
}

int main() {
    crow::SimpleApp app;

    // Serve the quiz page
    CROW_ROUTE(app, "/")([]() {
        return generateQuizPage();
    });

    // Handle answer submission
    CROW_ROUTE(app, "/submit-answer").methods("POST"_method)([](const crow::request& req) {
        auto params = crow::query_string(req.body);
        std::string selectedAnswer = params.get("answer");
        std::string correctAnswer = params.get("correct");

        lastAnswerWrong = (selectedAnswer != correctAnswer); // Flash red if wrong
        if (!lastAnswerWrong) {
            questionIndex++; // Move to next question only if correct
        }

        return generateQuizPage();
    });

    app.port(5000).multithreaded().run();
}
