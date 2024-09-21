#ifndef WEB_DEVELOPMENT_TOOLS_H
#define WEB_DEVELOPMENT_TOOLS_H

#include <string>
#include <vector>
#include <map>
#include <functional>

class WebDevelopmentTools {
public:
    WebDevelopmentTools() : serverPort(8080) {}
    ~WebDevelopmentTools();

    // Basic web server functionality
    void createServer(int port);
    void handleRequest(const std::string& path, std::function<void(const std::string&, std::string&)> handler);
    void sendResponse(const std::string& response);

    // RESTful API support
    void addRESTEndpoint(const std::string& path, const std::string& method, std::function<void(const std::map<std::string, std::string>&, std::string&)> handler);

    // WebSocket support
    void createWebSocket(const std::string& path);
    void sendWebSocketMessage(const std::string& message);
    void onWebSocketMessage(std::function<void(const std::string&)> handler);

    // HTML DOM manipulation
    std::string createElement(const std::string& tag, const std::map<std::string, std::string>& attributes);
    void appendChild(const std::string& parentId, const std::string& childElement);
    void removeElement(const std::string& elementId);

    // AJAX requests
    void sendAJAXRequest(const std::string& url, const std::string& method, const std::string& data, std::function<void(const std::string&)> callback);

private:
    // Private implementation details
    int serverPort;
    std::map<std::string, std::function<void(const std::string&, std::string&)>> requestHandlers;
    std::map<std::string, std::function<void(const std::map<std::string, std::string>&, std::string&)>> restEndpoints;
    std::function<void(const std::string&)> webSocketHandler;
};

#endif // WEB_DEVELOPMENT_TOOLS_H
