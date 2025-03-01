#pragma once

#include <iostream>
#include <iomanip>
#include <fstream>
#include <ostream>
#include <sstream>
#include <string>

using namespace std;




class quiz
{
private:
    string answer;
    string artist;

    
public:
    quiz(/* args */);
    ~quiz();
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

