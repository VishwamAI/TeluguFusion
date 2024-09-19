#ifndef AGENT_BEHAVIOR_H
#define AGENT_BEHAVIOR_H

#include <string>
#include <vector>
#include <unordered_map>
#include <functional>
#include <memory>

class AgentBehavior {
public:
    AgentBehavior() = default;
    virtual ~AgentBehavior() = default;

    virtual void act() = 0;
    virtual void perceive(const std::unordered_map<std::wstring, std::any>& environment) = 0;
    virtual void learn(const std::unordered_map<std::wstring, std::any>& feedback) = 0;
    virtual std::wstring getState() const = 0;
    virtual void setState(const std::wstring& state) = 0;

    virtual void sendMessage(const std::wstring& recipient, const std::wstring& message) = 0;
    virtual std::vector<std::wstring> receiveMessages() = 0;

    virtual void addBehavior(const std::wstring& name, std::function<void()> behavior) = 0;
    virtual void removeBehavior(const std::wstring& name) = 0;
    virtual void executeBehavior(const std::wstring& name) = 0;

    virtual std::unique_ptr<AgentBehavior> clone() const = 0;
};

class SimpleAgentBehavior : public AgentBehavior {
private:
    std::wstring m_state;
    std::unordered_map<std::wstring, std::function<void()>> m_behaviors;
    std::vector<std::wstring> m_messageQueue;

public:
    void act() override {
        // Default implementation
    }

    void perceive(const std::unordered_map<std::wstring, std::any>& environment) override {
        // Default implementation
    }

    void learn(const std::unordered_map<std::wstring, std::any>& feedback) override {
        // Default implementation
    }

    std::wstring getState() const override {
        return m_state;
    }

    void setState(const std::wstring& state) override {
        m_state = state;
    }

    void sendMessage(const std::wstring& recipient, const std::wstring& message) override {
        // In a real implementation, this would send a message to another agent
        m_messageQueue.push_back(message);
    }

    std::vector<std::wstring> receiveMessages() override {
        auto messages = m_messageQueue;
        m_messageQueue.clear();
        return messages;
    }

    void addBehavior(const std::wstring& name, std::function<void()> behavior) override {
        m_behaviors[name] = std::move(behavior);
    }

    void removeBehavior(const std::wstring& name) override {
        m_behaviors.erase(name);
    }

    void executeBehavior(const std::wstring& name) override {
        if (m_behaviors.find(name) != m_behaviors.end()) {
            m_behaviors[name]();
        }
    }

    std::unique_ptr<AgentBehavior> clone() const override {
        return std::make_unique<SimpleAgentBehavior>(*this);
    }
};

#endif // AGENT_BEHAVIOR_H
