#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>
#include "quiz.hpp"

#pragma comment(lib, "ws2_32.lib")  // Link Winsock library

#define PORT 8080
#define BUFFER_SIZE 8192

std::string readFile(const std::string &filename) {
    std::ifstream file(filename);
    if (!file.is_open()) return "<h1>File Not Found</h1>";
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

void handleClient(SOCKET clientSocket) {
    char buffer[BUFFER_SIZE] = {0};
    recv(clientSocket, buffer, BUFFER_SIZE, 0);
    std::string request(buffer);

    std::string response;
    if (request.find("GET / ") != std::string::npos) {
        std::string html = getQuizPage();
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + std::to_string(html.size()) + "\r\n\r\n" + html;
    } else if (request.find("GET /style.css") != std::string::npos) {
        std::string css = readFile("style.css");
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: " + std::to_string(css.size()) + "\r\n\r\n" + css;
    } else if (request.find("POST /submit-answer") != std::string::npos) {
        std::string answer = parseAnswer(request);
        processAnswer(answer);
        std::string html = getQuizPage();
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + std::to_string(html.size()) + "\r\n\r\n" + html;
    } else {
        response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n";
    }

    send(clientSocket, response.c_str(), response.size(), 0);
    closesocket(clientSocket);
}

int main() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed!" << std::endl;
        return 1;
    }

    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "Socket creation failed!" << std::endl;
        WSACleanup();
        return 1;
    }

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Bind failed!" << std::endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    if (listen(serverSocket, 5) == SOCKET_ERROR) {
        std::cerr << "Listen failed!" << std::endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    std::cout << "Server running on http://localhost:" << PORT << std::endl;
    while (true) {
        SOCKET clientSocket = accept(serverSocket, nullptr, nullptr);
        if (clientSocket != INVALID_SOCKET) {
            handleClient(clientSocket);
        }
    }

    closesocket(serverSocket);
    WSACleanup();
    return 0;
}
