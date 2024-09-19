#include "utils.h"
#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <codecvt>
#include <locale>
#include <unordered_set>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <algorithm>
#include <cmath>
#include <optional>
#include <variant>
#include <functional>
#include <stack>
#include <filesystem>
#include <regex>
#include <any>
#include <chrono>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <map>
#include <complex>
#include <random>

// Include headers for AgentBehavior and WebDevelopmentTools
#include "../agent_behavior.h"
#include "web_development_tools.h"

// Forward declarations
class ASTVisitor;

// TokenType enum definition
enum class TokenType {
    Unknown, Identifier, Number, String, Keyword, Operator, Punctuation,
    TeluguKeyword, TeluguIdentifier, TeluguStringLiteral, TeluguMathOperator,
    TeluguWebKeyword, TeluguDatabaseKeyword, TeluguAgentKeyword,
    TeluguControlFlowKeyword, TeluguFunctionKeyword,
    Comment, Whitespace, EndOfFile, ErrorToken,
    FunctionDeclaration, VariableDeclaration, IfStatement, WhileLoop,
    AgentDeclaration, BinaryExpression, ReturnStatement,
    Block, Program
};

class ASTNode {
public:
    virtual ~ASTNode() = default;
    virtual void accept(ASTVisitor& visitor) = 0;
    virtual TokenType getType() const = 0;
    virtual std::wstring getValue() const = 0;
    virtual std::unique_ptr<ASTNode> clone() const = 0;
    void addChild(std::unique_ptr<ASTNode> child) { m_children.push_back(std::move(child)); }
    const std::vector<std::unique_ptr<ASTNode>>& getChildren() const { return m_children; }
protected:
    std::vector<std::unique_ptr<ASTNode>> m_children;
};

class NumberNode : public ASTNode {
public:
    NumberNode(double value) : m_value(value) {}
    TokenType getType() const override { return TokenType::Number; }
    std::wstring getValue() const override { return std::to_wstring(m_value); }
    std::unique_ptr<ASTNode> clone() const override { return std::make_unique<NumberNode>(m_value); }
    void accept(ASTVisitor& visitor) override;
private:
    double m_value;
};

class StringNode : public ASTNode {
public:
    StringNode(const std::wstring& value) : m_value(value) {}
    TokenType getType() const override { return TokenType::String; }
    std::wstring getValue() const override { return m_value; }
    std::unique_ptr<ASTNode> clone() const override { return std::make_unique<StringNode>(m_value); }
    void accept(ASTVisitor& visitor) override;
private:
    std::wstring m_value;
};

class BlockNode : public ASTNode {
public:
    TokenType getType() const override { return TokenType::Block; }
    std::wstring getValue() const override { return L""; }
    std::unique_ptr<ASTNode> clone() const override { return std::make_unique<BlockNode>(*this); }
    void accept(ASTVisitor& visitor) override;
};

// Removed duplicate ASTNodeType enum and TokenType enum

class Token {
public:
    TokenType type;
    std::wstring value;
    std::wstring originalText;
    size_t line;
    size_t column;

    Token(TokenType t, const std::wstring& v, const std::wstring& o, size_t l = 0, size_t c = 0)
        : type(t), value(v), originalText(o), line(l), column(c) {}

    Token(TokenType t, const std::wstring& v, size_t l = 0, size_t c = 0)
        : Token(t, v, v, l, c) {}

    Token() : type(TokenType::Unknown), value(L""), originalText(L""), line(0), column(0) {}

    std::wstring toString() const;

    bool isTeluguSpecific() const {
        static const std::unordered_set<TokenType> teluguTypes = {
            TokenType::TeluguKeyword, TokenType::TeluguIdentifier,
            TokenType::TeluguStringLiteral, TokenType::TeluguMathOperator,
            TokenType::TeluguWebKeyword, TokenType::TeluguDatabaseKeyword,
            TokenType::TeluguAgentKeyword, TokenType::TeluguControlFlowKeyword,
            TokenType::TeluguFunctionKeyword
        };
        return teluguTypes.find(type) != teluguTypes.end();
    }

    TokenType getType() const { return type; }
    const std::wstring& getValue() const { return value; }
    const std::wstring& getOriginalText() const { return originalText; }
    size_t getLine() const { return line; }
    size_t getColumn() const { return column; }

    bool isMathRelated() const;
    bool isAgentRelated() const;
    bool isWebRelated() const;
    bool isDatabaseRelated() const;
    bool isControlFlow() const;
    bool isDataStructure() const;
    bool isFunctionRelated() const;
    bool isObjectOriented() const;
    bool isModuleRelated() const;
    bool isTypeRelated() const;
    bool isConcurrencyRelated() const;
    bool isMemoryManagementRelated() const;
    bool isLiteral() const;
    bool isAccessModifier() const;
};

class ProgramNode : public ASTNode {
public:
    ProgramNode() = default;
    ProgramNode(std::vector<std::unique_ptr<ASTNode>> statements)
        : statements(std::move(statements)) {}

    virtual void accept(ASTVisitor& visitor) override;
    virtual TokenType getType() const override { return TokenType::Program; }
    virtual std::wstring getValue() const override { return L""; }
    virtual std::unique_ptr<ASTNode> clone() const override {
        std::vector<std::unique_ptr<ASTNode>> clonedStatements;
        for (const auto& stmt : statements) {
            clonedStatements.push_back(stmt->clone());
        }
        return std::make_unique<ProgramNode>(std::move(clonedStatements));
    }

    std::vector<std::unique_ptr<ASTNode>> statements;
};

class FunctionDeclarationNode : public ASTNode {
public:
    virtual TokenType getType() const override { return TokenType::FunctionDeclaration; }
    virtual std::wstring getValue() const override { return m_name; }
    virtual void accept(ASTVisitor& visitor) override;
    virtual std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<FunctionDeclarationNode>(*this);
    }
    void setName(const std::wstring& name) { m_name = name; }
    const std::wstring& getName() const { return m_name; }
    const std::vector<std::wstring>& getParameterTypes() const { return m_parameterTypes; }
    const std::wstring& getReturnType() const { return m_returnType; }
private:
    std::wstring m_name;
    std::vector<std::wstring> m_parameterTypes;
    std::wstring m_returnType;
};

class ReturnStatementNode : public ASTNode {
public:
    ReturnStatementNode(std::unique_ptr<ASTNode> expression) : m_expression(std::move(expression)) {}
    virtual TokenType getType() const override { return TokenType::ReturnStatement; }
    virtual std::wstring getValue() const override { return L"return"; }
    virtual void accept(ASTVisitor& visitor) override;
    virtual std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<ReturnStatementNode>(m_expression ? m_expression->clone() : nullptr);
    }
private:
    std::unique_ptr<ASTNode> m_expression;
};

class VariableDeclarationNode : public ASTNode {
public:
    VariableDeclarationNode(const std::wstring& name, const std::wstring& dataType, std::unique_ptr<ASTNode> initializer = nullptr)
        : m_name(name), m_dataType(dataType), m_initializer(std::move(initializer)) {}
    virtual TokenType getType() const override { return TokenType::VariableDeclaration; }
    virtual std::wstring getValue() const override { return m_name; }
    virtual void accept(ASTVisitor& visitor) override;
    virtual std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<VariableDeclarationNode>(m_name, m_dataType, m_initializer ? m_initializer->clone() : nullptr);
    }
    const std::wstring& getName() const { return m_name; }
    const std::wstring& getDataType() const { return m_dataType; }
    bool hasInitializer() const { return m_initializer != nullptr; }
    const ASTNode* getInitializer() const { return m_initializer.get(); }
private:
    std::wstring m_name;
    std::wstring m_dataType;
    std::unique_ptr<ASTNode> m_initializer;
};

class IfStatementNode : public ASTNode {
public:
    IfStatementNode(std::unique_ptr<ASTNode> condition, std::unique_ptr<ASTNode> thenBranch, std::unique_ptr<ASTNode> elseBranch = nullptr)
        : m_condition(std::move(condition)), m_thenBranch(std::move(thenBranch)), m_elseBranch(std::move(elseBranch)) {}
    virtual TokenType getType() const override { return TokenType::IfStatement; }
    virtual std::wstring getValue() const override { return L""; }
    virtual void accept(ASTVisitor& visitor) override;
    virtual std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<IfStatementNode>(m_condition->clone(), m_thenBranch->clone(), m_elseBranch ? m_elseBranch->clone() : nullptr);
    }
    const ASTNode* getCondition() const { return m_condition.get(); }
    const ASTNode* getThenBranch() const { return m_thenBranch.get(); }
    bool hasElseBranch() const { return m_elseBranch != nullptr; }
    const ASTNode* getElseBranch() const { return m_elseBranch.get(); }
private:
    std::unique_ptr<ASTNode> m_condition;
    std::unique_ptr<ASTNode> m_thenBranch;
    std::unique_ptr<ASTNode> m_elseBranch;
};

class WhileLoopNode : public ASTNode {
public:
    WhileLoopNode(std::nullptr_t condition, std::nullptr_t body)
        : m_condition(nullptr), m_body(nullptr) {}
    virtual TokenType getType() const override { return TokenType::WhileLoop; }
    virtual std::wstring getValue() const override { return L""; }
    virtual void accept(ASTVisitor& visitor) override;
    virtual std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<WhileLoopNode>(nullptr, nullptr);
    }
    const ASTNode* getCondition() const { return m_condition.get(); }
    const ASTNode* getBody() const { return m_body.get(); }
private:
    std::unique_ptr<ASTNode> m_condition;
    std::unique_ptr<ASTNode> m_body;
};

class TeluguStringNode;

class IdentifierNode : public ASTNode {
public:
    IdentifierNode(const std::wstring& name) : name(name) {}

    virtual void accept(ASTVisitor& visitor) override;
    virtual TokenType getType() const override { return TokenType::Identifier; }
    virtual std::wstring getValue() const override { return name; }
    virtual std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<IdentifierNode>(name);
    }

    const std::wstring& getName() const { return name; }

    std::wstring name;
};

// Forward declarations for core components
class ASTNode;
class ASTVisitor;
class IRGenerator;
class CodeGenerator;
class Lexer;
class Parser;
class SemanticAnalyzer;

// Forward declarations for expression nodes
class TeluguKeywordNode;
class MatrixExpressionNode;
class VectorExpressionNode;
class TensorExpressionNode;

class SymbolTable {
public:
    enum class SymbolType { Variable, Function, Class, Agent };
    bool addSymbol(const std::wstring& name, const std::wstring& type, SymbolType symbolType);
    bool lookupSymbol(const std::wstring& name) const;
    void enterScope();
    void exitScope();
};

class AgentDeclarationNode : public ASTNode {
public:
    AgentDeclarationNode(const std::wstring& name)
        : m_name(name) {}

    AgentDeclarationNode(const std::wstring& name, std::vector<std::unique_ptr<ASTNode>> behaviors)
        : m_name(name), m_behaviors(std::move(behaviors)) {}

    AgentDeclarationNode(const std::wstring& name, std::unique_ptr<ASTNode> behavior)
        : m_name(name) {
        m_behaviors.push_back(std::move(behavior));
    }

    virtual void accept(ASTVisitor& visitor) override;
    virtual TokenType getType() const override { return TokenType::AgentDeclaration; }
    virtual std::wstring getValue() const override { return m_name; }
    virtual std::unique_ptr<ASTNode> clone() const override {
        std::vector<std::unique_ptr<ASTNode>> clonedBehaviors;
        for (const auto& behavior : m_behaviors) {
            clonedBehaviors.push_back(behavior->clone());
        }
        return std::make_unique<AgentDeclarationNode>(m_name, std::move(clonedBehaviors));
    }

    const std::wstring& getName() const { return m_name; }
    const std::vector<std::unique_ptr<ASTNode>>& getBehaviors() const { return m_behaviors; }

private:
    std::wstring m_name;
    std::vector<std::unique_ptr<ASTNode>> m_behaviors;
};

// Function declarations
void దోషం_నివేదించు(const std::wstring& message);
void reportError(const std::string& message);
std::unique_ptr<ASTNode> buildAST(const std::vector<Token>& tokens);

// Declaration of isTelugu function
bool isTelugu(wchar_t c);

// Forward declarations for specialized nodes
class WebOperationNode;
class DatabaseOperationNode;
class StatisticalFunctionNode;
class ComplexNumberNode;
class AgentBehaviorNode;
class AgentMessageNode;
class AgentStateNode;
class AgentEnvironmentNode;
class HttpRequestNode;
class HttpResponseNode;
class WebSocketOperationNode;
class RESTfulEndpointNode;
class GraphQLQueryNode;
class GraphQLMutationNode;

// Forward declarations for utility classes
class MatrixOperations;
class VectorOperations;
class TensorOperations;
class AgentBehavior;
class DatabaseManager;
class StatisticalFunctions;
class ComplexNumberOperations;

// Forward declarations for error handling
class CompilationError;
class RuntimeError;
class LexicalError;
class SyntaxError;
class SemanticError;

// ParsingError class definition
class ParsingError : public std::runtime_error {
public:
    ParsingError(size_t line, size_t column, const std::wstring& message)
        : std::runtime_error(to_utf8(L"Parsing error at line " + std::to_wstring(line) + L", column " + std::to_wstring(column) + L": " + message)),
          m_line(line), m_column(column), m_message(message) {}

    size_t getLine() const { return m_line; }
    size_t getColumn() const { return m_line; }
    const std::wstring& getMessage() const { return m_message; }

private:
    size_t m_line;
    size_t m_column;
    std::wstring m_message;
};

// Forward declarations for ASTNode derived classes
class FunctionDeclarationNode;
class VariableDeclarationNode;
class IfStatementNode;
class WhileLoopNode;
class IdentifierNode;
class BinaryExpressionNode;

// ASTVisitor class definition
class ASTVisitor {
public:
    virtual ~ASTVisitor() = default;
    virtual void visitFunctionDeclarationNode(FunctionDeclarationNode& node) = 0;
    virtual void visitVariableDeclarationNode(VariableDeclarationNode& node) = 0;
    virtual void visitIfStatementNode(IfStatementNode& node) = 0;
    virtual void visitWhileLoopNode(WhileLoopNode& node) = 0;
    virtual void visitIdentifierNode(IdentifierNode& node) = 0;
    virtual void visitBinaryExpressionNode(BinaryExpressionNode& node) = 0;
};

// ASTNode class definition
// ASTNodeType enum is defined elsewhere, so we remove the redundant definition here



// Derived ASTNode classes
// Derived ASTNode classes are already defined earlier in the file.
// Removing duplicate definitions for FunctionDeclarationNode, VariableDeclarationNode, IfStatementNode, and WhileLoopNode.

class BinaryExpressionNode : public ASTNode {
public:
    BinaryExpressionNode(const std::wstring& op, std::unique_ptr<ASTNode> left, std::unique_ptr<ASTNode> right)
        : m_left(std::move(left)), m_right(std::move(right)), m_operator(op), m_line(0), m_column(0), m_parent(nullptr) {}

    TokenType getType() const override { return TokenType::BinaryExpression; }
    std::wstring getValue() const override { return m_operator; }

    void addChild(std::unique_ptr<ASTNode> child) {
        m_children.push_back(std::move(child));
    }

    std::wstring toString() const {
        return L"BinaryExpression(" + m_left->getValue() + L" " + m_operator + L" " + m_right->getValue() + L")";
    }

    size_t getLine() const { return m_line; }
    size_t getColumn() const { return m_column; }

    void setSourceLocation(size_t line, size_t column) {
        m_line = line;
        m_column = column;
    }

    std::wstring getSourceLocation() const {
        return L"Line " + std::to_wstring(m_line) + L", Column " + std::to_wstring(m_column);
    }

    void validate() const {
        // Implement validation logic if needed
    }

    void setParent(ASTNode* parent) {
        m_parent = parent;
    }
    ASTNode* getParent() const { return m_parent; }

    const ASTNode* getLeft() const { return m_left.get(); }
    const ASTNode* getRight() const { return m_right.get(); }
    const std::wstring& getOperator() const { return m_operator; }

    void accept(ASTVisitor& visitor) override {
        visitor.visitBinaryExpressionNode(*this);
    }

    std::unique_ptr<ASTNode> clone() const override {
        auto cloned = std::make_unique<BinaryExpressionNode>(
            m_operator,
            m_left ? m_left->clone() : nullptr,
            m_right ? m_right->clone() : nullptr
        );
        cloned->setSourceLocation(m_line, m_column);
        return cloned;
    }

private:
    std::unique_ptr<ASTNode> m_left;
    std::unique_ptr<ASTNode> m_right;
    std::wstring m_operator;
    std::vector<std::unique_ptr<ASTNode>> m_children;
    size_t m_line;
    size_t m_column;
    ASTNode* m_parent;
};

class IdentifierNode;
class BinaryExpressionNode;

// Enum definitions
// TokenType enum is already defined at the beginning of the file
// Ensure all necessary token types are included in the original definition



    // Basic tokens
    EndOfFile, ErrorToken,

    // Telugu-specific types
    TeluguKeyword, TeluguIdentifier, TeluguStringLiteral,
    TeluguMathOperator, TeluguWebKeyword, TeluguDatabaseKeyword,
    TeluguAgentKeyword, TeluguControlFlowKeyword, TeluguFunctionKeyword,
    TeluguClassKeyword, TeluguModuleKeyword, TeluguConcurrencyKeyword,

    // Telugu-specific operators and literals
    TeluguComparisonOperator, TeluguLogicalOperator, TeluguAssignmentOperator,
    TeluguBooleanLiteral, TeluguNullLiteral,

    // Control flow
    IfKeyword, ElseKeyword, ForKeyword, WhileKeyword, DoWhileKeyword,
    SwitchKeyword, CaseKeyword, DefaultKeyword,
    BreakKeyword, ContinueKeyword, ReturnKeyword,

    // Error handling
    TryKeyword, CatchKeyword, FinallyKeyword, ThrowKeyword,

    // Functions and classes
    FunctionDeclaration, MethodDeclaration, ClassDeclaration,
    ConstructorDeclaration, DestructorDeclaration,

    // OOP concepts
    ThisKeyword, SuperKeyword, InterfaceKeyword,
    AbstractKeyword, OverrideKeyword,
    PublicKeyword, PrivateKeyword, ProtectedKeyword,

    // Data structures
    ListDeclaration, DictionaryDeclaration, SetDeclaration, TupleDeclaration,

    // Advanced math operations
    MathFunction, Matrix, Vector, Tensor, StatisticalFunction,
    ComplexNumber,

    // Agent-based behaviors
    AgentDeclaration, AgentBehavior, AgentState, AgentMessage, AgentEnvironment,
    AgentDecisionTree, AgentAction,

    // Web development capabilities
    HttpRequest, HttpResponse, WebSocketOperation,
    RESTfulEndpoint, GraphQLQuery, GraphQLMutation,
    DomManipulation, CSSRule, JavaScriptFunction,
    CSSProperty, HTTPMethod, HTMLTag,

    // Database operations
    DatabaseQuery, DatabaseConnection, DatabaseTransaction,
    DatabaseIndex, DatabaseView,
    SQLKeyword, TableName, ColumnName,

    // Concurrency and asynchronous operations
    AsyncKeyword, AwaitKeyword, ParallelKeyword, PromiseKeyword,

    // Memory management
    GarbageCollectionHint, ManualMemoryManagement,

    // Functional programming
    LambdaKeyword, HigherOrderFunctionKeyword, ClosureKeyword, CurryingKeyword,
    FunctionCall, LambdaExpression, ParameterDeclaration,

    // Type system
    TypeAnnotation, GenericType, UnionType, IntersectionType, TypeAlias,

    // Module system
    ImportKeyword, ExportKeyword, ModuleKeyword,
    ModuleDeclaration,

    // Metaprogramming
    ReflectionKeyword, CodeGenerationKeyword, MacroKeyword,

    // Internationalization
    LocalizationTag, TranslationUnit,

    // Additional OOP concepts
    InterfaceDeclaration, InheritanceDeclaration,

    // Telugu-specific data structure keywords
    TeluguListKeyword, TeluguDictionaryKeyword, TeluguSetKeyword, TeluguTupleKeyword,

    // Expressions
    BinaryExpression, UnaryExpression, TernaryExpression,
    CallExpression, MemberExpression, AssignmentExpression,

    // Telugu-specific constructs
    TeluguMathExpression, TeluguAgentDeclaration, TeluguWebComponent,
    TeluguDatabaseOperation, TeluguConcurrencyPrimitive,

    // Advanced math operations
    MatrixExpression, VectorExpression, TensorExpression,
    StatisticalExpression, ComplexNumberExpression,

    // Web development features
    CSSPropertyDeclaration, HTMLTagDeclaration, JavaScriptFunctionDeclaration,

    // Database operations
    SQLStatement, TableDeclaration, ColumnDeclaration,

    // Concurrency
    AsyncFunction, AwaitExpression, ParallelExecution, PromiseExpression,

    // Error handling
    TryCatchBlock, ThrowStatement, FinallyBlock,

    // Object-oriented features
    PropertyDeclaration, AbstractClassDeclaration,

    // Functional programming features
    HigherOrderFunction, Closure, CurryingExpression,
    FunctionCallExpression,

    // Type system
    GenericTypeDeclaration,

    // Meta-programming
    ReflectionExpression, CodeGenerationExpression, MacroDefinition,

    // Additional Telugu-specific features
    TeluguListDeclaration, TeluguDictionaryDeclaration, TeluguSetDeclaration, TeluguTupleDeclaration,

    // Access modifiers
    PublicAccessModifier, PrivateAccessModifier, ProtectedAccessModifier,

    // Additional keywords
    ConstKeyword, StaticKeyword,

    // Telugu-specific control flow
    TeluguIfStatement, TeluguWhileLoop, TeluguForLoop,

    // Telugu-specific error handling
    TeluguTryCatchBlock, TeluguThrowStatement,

    // Telugu-specific OOP features
    TeluguClassDeclaration, TeluguMethodDeclaration, TeluguInterfaceDeclaration,

    // Telugu-specific functional programming
    TeluguLambdaExpression, TeluguHigherOrderFunction,

    // Telugu-specific module system
    TeluguImportDeclaration, TeluguExportDeclaration,

    // Telugu-specific type system
    TeluguTypeAnnotation, TeluguGenericTypeDeclaration,

    // Telugu-specific meta-programming
    TeluguReflectionExpression, TeluguCodeGenerationExpression,

    // Telugu-specific memory management
    TeluguGarbageCollectionHint, TeluguManualMemoryManagement,

    // Additional required tokens
    Block, Program
};

// Forward declarations
class Token;
class SymbolTable;
class ASTNode;
class FunctionDeclarationNode;
class VariableDeclarationNode;
class IfStatementNode;
class WhileLoopNode;
class IdentifierNode;
class BinaryExpressionNode;
class Token;
class SymbolTable;
class ASTNode;
class FunctionDeclarationNode;
class VariableDeclarationNode;
class IfStatementNode;
class WhileLoopNode;
class IdentifierNode;
class BinaryExpressionNode;

// AgentBehavior is already defined in agent_behavior.h, so we remove the redefinition here



// Remove WebDevelopmentTools redefinition

// Note: These classes are implemented here for now, but can be moved to separate files later
// to keep the main compiler file clean and modular

// Unicode conversion utilities
#include <codecvt>
#include <locale>

std::wstring_convert<std::codecvt_utf8<wchar_t>, wchar_t> utf8_conv;

std::wstring వాక్యానికి_మార్చు(const std::string& వాక్యం) {
    try {
        return utf8_conv.from_bytes(వాక్యం);
    } catch (const std::exception& e) {
        దోషం_నివేదించు(L"వాక్యానికి మార్చడంలో దోషం: " + వాక్యానికి_మార్చు(e.what()));
        return L"";
    }
}

std::string యూటీఎఫ్8కి_మార్చు(const std::wstring& వాక్యం) {
    try {
        return utf8_conv.to_bytes(వాక్యం);
    } catch (const std::exception& e) {
        దోషం_నివేదించు(L"యూటీఎఫ్8కి మార్చడంలో దోషం: " + వాక్యానికి_మార్చు(e.what()));
        return "";
    }
}

// Error handling
void దోషం_నివేదించు(const std::wstring& సందేశం) {
    std::wcerr << L"దోషం: " << సందేశం << std::endl;
}

// Front-end parsing
std::unique_ptr<ASTNode> parse(const std::wstring& sourceCode) {
    std::vector<Token> tokens;
    size_t pos = 0;
    size_t line = 1;
    size_t column = 1;

    auto isTelugu = [](wchar_t c) {
        return (c >= 0x0C00 && c <= 0x0C7F);
    };

    auto isTeluguKeyword = [](const std::wstring& word) {
        static const std::unordered_set<std::wstring> keywords = {
            L"ప్రమేయం", L"చర", L"తిరిగిఇవ్వు", L"ఒకవేళ", L"లేకపోతే", L"కొరకు", L"అయ్యేవరకు",
            L"స్థిరం", L"తరగతి", L"దిగుమతి", L"ఏజెంట్", L"నిజం", L"తప్పు", L"శూన్యం", L"మరియు", L"లేదా",
            L"మాట్రిక్స్", L"వెక్టర్", L"టెన్సర్", L"సాంఖ్యిక", L"సంకీర్ణం", L"వెబ్", L"డేటాబేస్",
            L"అసమకాలిక", L"సమాంతర", L"ప్రామిస్", L"లాంబ్డా", L"జెనెరిక్", L"యూనియన్", L"ఇంటర్సెక్షన్"
        };
        return keywords.find(word) != keywords.end();
    };

    auto addToken = [&](TokenType type, const std::wstring& value) {
        tokens.emplace_back(type, value, value, line, column);
        column += value.length();
    };

    try {
        while (pos < sourceCode.length()) {
            if (std::isspace(sourceCode[pos])) {
                if (sourceCode[pos] == L'\n') {
                    line++;
                    column = 1;
                } else {
                    column++;
                }
                pos++;
            } else if (sourceCode[pos] == L'/' && pos + 1 < sourceCode.length()) {
                if (sourceCode[pos + 1] == L'/') {
                    // Single-line comment
                    pos = sourceCode.find(L'\n', pos);
                    if (pos == std::wstring::npos) break;
                    line++;
                    column = 1;
                } else if (sourceCode[pos + 1] == L'*') {
                    // Multi-line comment
                    size_t start_line = line;
                    size_t start_column = column;
                    pos += 2;
                    column += 2;
                    while (pos < sourceCode.length() && (sourceCode[pos] != L'*' || sourceCode[pos + 1] != L'/')) {
                        if (sourceCode[pos] == L'\n') {
                            line++;
                            column = 1;
                        } else {
                            column++;
                        }
                        pos++;
                    }
                    if (pos >= sourceCode.length()) {
                        throw ParsingError(start_line, start_column, L"Unterminated multi-line comment");
                    }
                    pos += 2;
                    column += 2;
                }
            } else if (isTelugu(sourceCode[pos]) || std::isalpha(sourceCode[pos])) {
                // Identifier or keyword
                size_t start = pos;
                while (pos < sourceCode.length() && (isTelugu(sourceCode[pos]) || std::isalnum(sourceCode[pos]) || sourceCode[pos] == L'_')) {
                    pos++;
                }
                std::wstring word = sourceCode.substr(start, pos - start);
                if (isTeluguKeyword(word)) {
                    addToken(TokenType::TeluguKeyword, word);
                } else if (isTelugu(word[0])) {
                    addToken(TokenType::TeluguIdentifier, word);
                } else {
                    addToken(TokenType::Identifier, word);
                }
            } else if (std::isdigit(sourceCode[pos])) {
                // Number literal
                size_t start = pos;
                bool hasDecimalPoint = false;
                while (pos < sourceCode.length() && (std::isdigit(sourceCode[pos]) || sourceCode[pos] == L'.')) {
                    if (sourceCode[pos] == L'.') {
                        if (hasDecimalPoint) {
                            throw ParsingError(line, column, L"Invalid number literal: multiple decimal points");
                        }
                        hasDecimalPoint = true;
                    }
                    pos++;
                }
                addToken(TokenType::Number, sourceCode.substr(start, pos - start));
            } else if (sourceCode[pos] == L'"') {
                // String literal
                size_t start = pos;
                pos++;
                column++;
                while (pos < sourceCode.length() && sourceCode[pos] != L'"') {
                    if (sourceCode[pos] == L'\\' && pos + 1 < sourceCode.length()) {
                        pos += 2;
                        column += 2;
                    } else {
                        if (sourceCode[pos] == L'\n') {
                            throw ParsingError(line, column, L"Unterminated string literal");
                        }
                        pos++;
                        column++;
                    }
                }
                if (pos >= sourceCode.length()) {
                    throw ParsingError(line, column, L"Unterminated string literal");
                }
                pos++;
                std::wstring stringLiteral = sourceCode.substr(start, pos - start);
                addToken(isTelugu(stringLiteral[1]) ? TokenType::TeluguStringLiteral : TokenType::String, stringLiteral);
            } else {
                // Operators and punctuation
                static const std::vector<std::pair<std::wstring, TokenType>> operators = {
                    {L"==", TokenType::Operator}, {L"!=", TokenType::Operator},
                    {L"<=", TokenType::Operator}, {L">=", TokenType::Operator},
                    {L"&&", TokenType::Operator}, {L"||", TokenType::Operator},
                    {L"+=", TokenType::Operator}, {L"-=", TokenType::Operator},
                    {L"*=", TokenType::Operator}, {L"/=", TokenType::Operator},
                    {L"%=", TokenType::Operator}, {L"++", TokenType::Operator},
                    {L"--", TokenType::Operator},
                    // Telugu-specific operators
                    {L"సమానం", TokenType::Operator},
                    {L"మరియు", TokenType::Operator},
                    {L"లేదా", TokenType::Operator},
                    {L"కాదు", TokenType::Operator},
                    {L"+", TokenType::TeluguMathOperator},
                    {L"-", TokenType::TeluguMathOperator},
                    {L"*", TokenType::TeluguMathOperator},
                    {L"/", TokenType::TeluguMathOperator},
                    {L"%", TokenType::TeluguMathOperator},
                    {L"^", TokenType::TeluguMathOperator}
                };
                bool found = false;
                for (const auto& [op, type] : operators) {
                    if (sourceCode.substr(pos, op.length()) == op) {
                        addToken(type, op);
                        pos += op.length();
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    // Check for matrix operations
                    if (sourceCode.substr(pos, 9) == L"మాట్రిక్స్") {
                        addToken(TokenType::TeluguMathOperator, L"మాట్రిక్స్");
                        pos += 9;
                    }
                    // Check for agent-based behaviors
                    else if (sourceCode.substr(pos, 6) == L"ఏజెంట్") {
                        addToken(TokenType::TeluguAgentKeyword, L"ఏజెంట్");
                        pos += 6;
                    }
                    // Check for web development capabilities
                    else if (sourceCode.substr(pos, 3) == L"వెబ్") {
                        addToken(TokenType::TeluguWebKeyword, L"వెబ్");
                        pos += 3;
                    }
                    else {
                        addToken(TokenType::Punctuation, sourceCode.substr(pos, 1));
                        pos++;
                    }
                }
            }
        }
    } catch (const ParsingError& e) {
        reportError(e.what());
        return nullptr;
    }

    return buildAST(tokens);
}

std::unique_ptr<ASTNode> buildAST(const std::vector<Token>& tokens) {
    std::vector<std::unique_ptr<ASTNode>> stack;
    auto root = std::make_unique<ProgramNode>();
    stack.push_back(std::move(root));

    for (size_t i = 0; i < tokens.size(); ++i) {
        const auto& token = tokens[i];
        switch (token.type) {
            case TokenType::TeluguKeyword:
            case TokenType::Keyword:
                if (token.value == L"ప్రమేయం" || token.value == L"function") {
                    auto funcDecl = std::make_unique<FunctionDeclarationNode>();
                    funcDecl->setName(tokens[++i].value);
                    stack.back()->addChild(std::move(funcDecl));
                    stack.push_back(std::move(funcDecl));
                } else if (token.value == L"చర" || token.value == L"var") {
                    auto varDecl = std::make_unique<VariableDeclarationNode>(tokens[++i].value, L"");
                    stack.back()->addChild(std::move(varDecl));
                } else if (token.value == L"ఒకవేళ" || token.value == L"if") {
                    auto ifStmt = std::make_unique<IfStatementNode>(nullptr, nullptr);
                    stack.back()->addChild(std::move(ifStmt));
                    stack.push_back(std::move(ifStmt));
                } else if (token.value == L"అయ్యేవరకు" || token.value == L"while") {
                    auto whileLoop = std::make_unique<WhileLoopNode>(nullptr, nullptr);
                    stack.back()->addChild(std::move(whileLoop));
                    stack.push_back(std::move(whileLoop));
                } else if (token.value == L"తిరిగిఇవ్వు" || token.value == L"return") {
                    auto returnStmt = std::make_unique<ReturnStatementNode>(nullptr);
                    stack.back()->addChild(std::move(returnStmt));
                }
                break;
            case TokenType::TeluguIdentifier:
            case TokenType::Identifier:
                stack.back()->addChild(std::make_unique<IdentifierNode>(token.value));
                break;
            case TokenType::Number:
                stack.back()->addChild(std::make_unique<NumberNode>(std::stod(token.value)));
                break;
            case TokenType::TeluguStringLiteral:
            case TokenType::String:
                stack.back()->addChild(std::make_unique<StringNode>(token.value));
                break;
            case TokenType::TeluguMathOperator:
            case TokenType::Operator:
                if (token.value == L"+" || token.value == L"-" || token.value == L"*" || token.value == L"/") {
                    auto& children = stack.back()->getChildren();
                    if (children.size() >= 2) {
                        auto binaryExpr = std::make_unique<BinaryExpressionNode>(token.value, std::move(children[children.size() - 1]), std::move(children[children.size() - 2]));
                        children.pop_back();
                        children.pop_back();
                        stack.back()->addChild(std::move(binaryExpr));
                    } else {
                        throw ParsingError(token.line, token.column, L"Invalid binary expression");
                    }
                }
                break;
            case TokenType::Punctuation:
                if (token.value == L"{") {
                    auto block = std::make_unique<BlockNode>();
                    stack.back()->addChild(std::move(block));
                    stack.push_back(std::move(block));
                } else if (token.value == L"}") {
                    if (stack.size() > 1) {
                        stack.pop_back();
                    } else {
                        throw ParsingError(token.line, token.column, L"Unmatched closing brace");
                    }
                }
                break;
            case TokenType::TeluguAgentKeyword:
                if (token.value == L"ఏజెంట్" || token.value == L"agent") {
                    auto agentDecl = std::make_unique<AgentDeclarationNode>(tokens[++i].value);
                    stack.back()->addChild(std::move(agentDecl));
                    stack.push_back(std::move(agentDecl));
                }
                break;
            case TokenType::TeluguWebKeyword:
                // Handle web-related keywords
                break;
            case TokenType::TeluguDatabaseKeyword:
                // Handle database-related keywords
                break;
            default:
                throw ParsingError(token.line, token.column, L"Unexpected token type: " + std::to_wstring(static_cast<int>(token.type)));
        }
    }

    if (stack.size() != 1) {
        throw ParsingError(0, 0, L"Unbalanced AST construction");
    }

    return std::move(stack.front());
}

// Semantic analysis
bool performSemanticAnalysis(const ASTNode* ast, SymbolTable& symbolTable) {
    if (!ast) return false;

    switch (ast->getType()) {
        case TokenType::FunctionDeclaration:
            if (ast->getChildren().size() < 2) return false;
            {
                auto funcNode = dynamic_cast<const FunctionDeclarationNode*>(ast);
                std::wstring funcName = funcNode->getName();
                std::vector<std::wstring> params = funcNode->getParameterTypes();
                std::wstring returnType = funcNode->getReturnType();

                if (!symbolTable.addSymbol(funcName, returnType, SymbolTable::SymbolType::Function)) {
                    reportError(std::string("Function redefinition: ") + std::string(funcName.begin(), funcName.end()));
                    return false;
                }
                symbolTable.enterScope();
                if (!performSemanticAnalysis(funcNode->getChildren().back().get(), symbolTable)) {
                    return false;
                }
                symbolTable.exitScope();
            }
            break;

        case TokenType::VariableDeclaration:
            {
                auto varNode = dynamic_cast<const VariableDeclarationNode*>(ast);
                std::wstring varName = varNode->getName();
                std::wstring varType = varNode->getDataType();
                if (!symbolTable.addSymbol(varName, varType, SymbolTable::SymbolType::Variable)) {
                    reportError(std::string("Variable redefinition: ") + std::string(varName.begin(), varName.end()));
                    return false;
                }
                // Check initialization expression if present
                if (varNode->getInitializer()) {
                    if (!performSemanticAnalysis(varNode->getInitializer(), symbolTable)) {
                        return false;
                    }
                    // TODO: Type check initializer against declared type
                }
            }
            break;

        case TokenType::Identifier:
            {
                auto identNode = dynamic_cast<const IdentifierNode*>(ast);
                if (!symbolTable.lookupSymbol(identNode->getName())) {
                    reportError(std::string("Undefined symbol: ") + std::string(identNode->getName().begin(), identNode->getName().end()));
                    return false;
                }
            }
            break;

        case TokenType::IfStatement:
            {
                auto ifNode = dynamic_cast<const IfStatementNode*>(ast);
                if (!performSemanticAnalysis(ifNode->getCondition(), symbolTable)) return false;
                if (!performSemanticAnalysis(ifNode->getThenBranch(), symbolTable)) return false;
                if (ifNode->getElseBranch()) {
                    if (!performSemanticAnalysis(ifNode->getElseBranch(), symbolTable)) return false;
                }
            }
            break;

        case TokenType::WhileLoop:
            {
                auto whileNode = dynamic_cast<const WhileLoopNode*>(ast);
                if (!performSemanticAnalysis(whileNode->getCondition(), symbolTable)) return false;
                if (!performSemanticAnalysis(whileNode->getBody(), symbolTable)) return false;
            }
            break;

        case TokenType::BinaryExpression:
            {
                auto binExpr = dynamic_cast<const BinaryExpressionNode*>(ast);
                if (!performSemanticAnalysis(binExpr->getLeft(), symbolTable)) return false;
                if (!performSemanticAnalysis(binExpr->getRight(), symbolTable)) return false;
                // TODO: Implement type checking for binary expressions
            }
            break;

        // Remove cases for MatrixExpression, VectorExpression, TensorExpression, AgentBehavior, AgentMessage, HttpRequest, WebSocketOperation

        default:
            // For node types not explicitly handled, traverse children
            for (const auto& child : ast->getChildren()) {
                if (!performSemanticAnalysis(child.get(), symbolTable)) {
                    return false;
                }
            }
            break;
    }

    return true;
}

// Intermediate representation
std::unique_ptr<IRGenerator> generateIR(const ASTNode* ast) {
    auto irGenerator = std::make_unique<IRGenerator>();

    std::function<void(const ASTNode*)> generateIRRecursive = [&](const ASTNode* node) {
        if (!node) return;

        switch (node->getType()) {
            case TokenType::Program:
            case TokenType::Block:
                for (const auto& child : node->getChildren()) {
                    generateIRRecursive(child.get());
                }
                break;
            case TokenType::FunctionDeclaration:
                if (auto funcDeclNode = dynamic_cast<const FunctionDeclarationNode*>(node)) {
                    irGenerator->addInstruction(std::make_unique<FunctionDeclarationInstruction>(*funcDeclNode));
                    generateIRRecursive(funcDeclNode->getBody());
                }
                break;
            case TokenType::VariableDeclaration:
                if (auto varDeclNode = dynamic_cast<const VariableDeclarationNode*>(node)) {
                    irGenerator->addInstruction(std::make_unique<DeclarationInstruction>(*varDeclNode));
                }
                break;
            case TokenType::IfStatement:
            case TokenType::WhileLoop:
            case TokenType::ForLoop:
                irGenerator->addInstruction(std::make_unique<ControlFlowInstruction>(*node));
                break;
            case TokenType::ReturnStatement:
                irGenerator->addInstruction(std::make_unique<ReturnInstruction>(*node));
                break;
            case TokenType::BinaryExpression:
                irGenerator->addInstruction(std::make_unique<ArithmeticInstruction>(*node));
                break;
            case TokenType::MatrixExpression:
                irGenerator->addInstruction(std::make_unique<MatrixInstruction>(*node, MatrixOperations()));
                break;
            case TokenType::AgentDeclaration:
                irGenerator->addInstruction(std::make_unique<AgentInstruction>(*node, AgentBehavior()));
                break;
            case TokenType::HttpRequest:
            case TokenType::WebSocketOperation:
                irGenerator->addInstruction(std::make_unique<WebInstruction>(*node, WebDevelopmentTools()));
                break;
            default:
                // For unhandled node types, we'll skip IR generation for now
                break;
        }
    };

    generateIRRecursive(ast);
    return irGenerator;
}

// Back-end code generation
std::wstring generateCode(const IRGenerator* ir) {
    // TODO: Implement code generation
    // This should produce code that supports advanced math operations,
    // agent-based behaviors, and web development capabilities
    return L"";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::wcout << L"వినియోగం: " << వాక్యానికి_మార్చు(argv[0]) << L" <మూలఫైల్>" << std::endl;
        return 1;
    }

    // Read source code from file
    std::wifstream sourceFile(argv[1], std::ios::binary);
    if (!sourceFile.is_open()) {
        దోషం_నివేదించు(L"మూలఫైల్ తెరవడంలో విఫలమైంది");
        return 1;
    }
    sourceFile.imbue(std::locale(sourceFile.getloc(), new std::codecvt_utf8<wchar_t>));
    std::wstringstream buffer;
    buffer << sourceFile.rdbuf();
    std::wstring sourceCode = buffer.str();

    // Front-end parsing
    auto ast = parse(sourceCode);
    if (!ast) {
        దోషం_నివేదించు(L"పార్సింగ్ విఫలమైంది");
        return 1;
    }

    // Semantic analysis
    SymbolTable symbolTable;
    if (!performSemanticAnalysis(ast.get(), symbolTable)) {
        దోషం_నివేదించు(L"అర్థ విశ్లేషణ విఫలమైంది");
        return 1;
    }

    // Generate intermediate representation
    auto ir = generateIR(ast.get());
    if (!ir) {
        దోషం_నివేదించు(L"IR ఉత్పత్తి విఫలమైంది");
        return 1;
    }

    // Back-end code generation
    std::wstring generatedCode = generateCode(ir.get());
    if (generatedCode.empty()) {
        దోషం_నివేదించు(L"కోడ్ ఉత్పత్తి విఫలమైంది");
        return 1;
    }

    // TODO: Output or further process the generated code

    std::wcout << L"కంపైలేషన్ విజయవంతమైంది" << std::endl;
    return 0;
}

// Forward declarations
class ASTNode;
class SymbolTable;

// ASTNode class implementation
enum class ASTNodeType {
    // Basic constructs
    Program, Block, Identifier, Number, String, Boolean, Null,

    // Declarations and definitions
    FunctionDeclaration, VariableDeclaration, ConstantDeclaration,
    ClassDeclaration, AgentDeclaration, InterfaceDeclaration,

    // Statements
    ExpressionStatement, IfStatement, WhileLoop, ForLoop, DoWhileLoop,
    SwitchStatement, ReturnStatement, BreakStatement, ContinueStatement,

    // Expressions
    BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, AssignmentExpression, TernaryExpression,

    // Advanced math operations
    MatrixExpression, VectorExpression, TensorExpression,
    StatisticalExpression, ComplexNumberExpression,

    // Agent-based behaviors
    AgentBehavior, AgentMessage, AgentState, AgentEnvironment, AgentDecisionTree,

    // Web development capabilities
    HttpRequest, HttpResponse, WebSocketOperation,
    DomManipulation, RESTfulEndpoint, GraphQLQuery, GraphQLMutation,

    // Database operations
    DatabaseQuery, DatabaseConnection, DatabaseTransaction, DatabaseIndex, DatabaseView,

    // Error handling
    TryCatchBlock, ThrowStatement, FinallyBlock,

    // Concurrency
    AsyncFunction, AwaitExpression, PromiseExpression, ParallelExecution,

    // TeluguFusion specific
    TeluguStringLiteral, TeluguIdentifier, TeluguKeyword, TeluguOperator,

    // Modules and imports
    ImportDeclaration, ExportDeclaration, ModuleDeclaration,

    // Object-oriented features
    MethodDeclaration, PropertyDeclaration, ConstructorDeclaration,
    DestructorDeclaration, InheritanceDeclaration,

    // Functional programming features
    LambdaExpression, HigherOrderFunction, Closure, CurryingExpression,

    // Type system
    TypeAnnotation, GenericTypeDeclaration, UnionType, IntersectionType, TypeAlias,

    // Comments
    SingleLineComment, MultiLineComment, DocumentationComment,

    // Meta-programming
    ReflectionExpression, CodeGenerationExpression, MacroDefinition,

    // Memory management
    GarbageCollectionHint, ManualMemoryManagement,

    // Internationalization
    LocalizationTag, TranslationUnit
};

class ASTNode {
public:
    virtual ~ASTNode() = default;

    virtual ASTNodeType getType() const = 0;
    virtual std::wstring getValue() const = 0;
    virtual const std::vector<std::unique_ptr<ASTNode>>& getChildren() const = 0;
    virtual std::wstring getOriginalTeluguText() const = 0;
    virtual std::wstring getDataType() const = 0;
    virtual size_t getLine() const = 0;
    virtual size_t getColumn() const = 0;

    virtual void addChild(std::unique_ptr<ASTNode> child) = 0;
    virtual std::wstring toString() const = 0;
    virtual bool isTeluguSpecific() const = 0;
    virtual bool supportsMathOperations() const = 0;
    virtual bool supportsWebDevelopment() const = 0;
    virtual bool supportsAgentBehaviors() const = 0;
    virtual bool supportsDatabaseOperations() const = 0;
    virtual bool supportsAsyncOperations() const = 0;
    virtual void setDataType(const std::wstring& dt) = 0;
    virtual bool isLValue() const = 0;
    virtual bool isConstant() const = 0;
    virtual void accept(class ASTVisitor& visitor) = 0;
    virtual std::unique_ptr<ASTNode> clone() const = 0;
    virtual std::wstring getSourceLocation() const = 0;
    virtual void setSourceLocation(size_t l, size_t c) = 0;
};

class BaseASTNode : public ASTNode {
protected:
    ASTNodeType type;
    std::wstring value;
    std::vector<std::unique_ptr<ASTNode>> children;
    std::wstring originalTeluguText;
    std::wstring dataType;
    size_t line;
    size_t column;

public:
    BaseASTNode(ASTNodeType t, const std::wstring& v = L"", const std::wstring& originalText = L"", const std::wstring& dt = L"", size_t l = 0, size_t c = 0)
        : type(t), value(v), originalTeluguText(originalText), dataType(dt), line(l), column(c) {}

    BaseASTNode(const BaseASTNode& other)
        : type(other.type), value(other.value), originalTeluguText(other.originalTeluguText),
          dataType(other.dataType), line(other.line), column(other.column) {
        for (const auto& child : other.children) {
            children.push_back(child ? child->clone() : nullptr);
        }
    }

    ASTNodeType getType() const override { return type; }
    std::wstring getValue() const override { return value; }
    const std::vector<std::unique_ptr<ASTNode>>& getChildren() const override { return children; }
    std::wstring getOriginalTeluguText() const override { return originalTeluguText; }
    std::wstring getDataType() const override { return dataType; }
    size_t getLine() const override { return line; }
    size_t getColumn() const override { return column; }

    void addChild(std::unique_ptr<ASTNode> child) override {
        children.push_back(std::move(child));
    }

    std::wstring toString() const override {
        return L"ASTNode(" + std::to_wstring(static_cast<int>(type)) + L", " + value + L", " + dataType + L", " + std::to_wstring(line) + L":" + std::to_wstring(column) + L")";
    }

    bool isTeluguSpecific() const override {
        return !originalTeluguText.empty();
    }

    bool supportsMathOperations() const override {
        return type == ASTNodeType::MatrixExpression || type == ASTNodeType::VectorExpression ||
               type == ASTNodeType::TensorExpression || type == ASTNodeType::StatisticalExpression ||
               type == ASTNodeType::ComplexNumberExpression;
    }

    bool supportsWebDevelopment() const override {
        return type == ASTNodeType::HttpRequest || type == ASTNodeType::HttpResponse ||
               type == ASTNodeType::WebSocketOperation || type == ASTNodeType::DomManipulation ||
               type == ASTNodeType::RESTfulEndpoint || type == ASTNodeType::GraphQLQuery ||
               type == ASTNodeType::GraphQLMutation;
    }

    bool supportsAgentBehaviors() const override {
        return type == ASTNodeType::AgentBehavior || type == ASTNodeType::AgentMessage ||
               type == ASTNodeType::AgentState || type == ASTNodeType::AgentEnvironment ||
               type == ASTNodeType::AgentDecisionTree;
    }

    bool supportsDatabaseOperations() const override {
        return type == ASTNodeType::DatabaseQuery || type == ASTNodeType::DatabaseConnection ||
               type == ASTNodeType::DatabaseTransaction || type == ASTNodeType::DatabaseIndex ||
               type == ASTNodeType::DatabaseView;
    }

    bool supportsAsyncOperations() const override {
        return type == ASTNodeType::AsyncFunction || type == ASTNodeType::AwaitExpression ||
               type == ASTNodeType::PromiseExpression || type == ASTNodeType::ParallelExecution;
    }

    void setDataType(const std::wstring& dt) override {
        dataType = dt;
    }

    bool isLValue() const override {
        return type == ASTNodeType::Identifier || type == ASTNodeType::MemberExpression;
    }

    bool isConstant() const override {
        return type == ASTNodeType::Number || type == ASTNodeType::String || type == ASTNodeType::Boolean;
    }

    std::wstring getSourceLocation() const override {
        return L"Line " + std::to_wstring(line) + L", Column " + std::to_wstring(column);
    }

    void setSourceLocation(size_t l, size_t c) override {
        line = l;
        column = c;
    }

    virtual void accept(ASTVisitor& visitor) override = 0;
    virtual std::unique_ptr<ASTNode> clone() const override = 0;
};

class ASTVisitor {
public:
    virtual ~ASTVisitor() = default;
    virtual void visitProgramNode(class ProgramNode& node) = 0;
    virtual void visitFunctionDeclarationNode(class FunctionDeclarationNode& node) = 0;
    FunctionDeclarationNode() : m_line(0), m_column(0), m_parent(nullptr) {}
    virtual void visitVariableDeclarationNode(class VariableDeclarationNode& node) = 0;
    virtual void visitIfStatementNode(class IfStatementNode& node) = 0;
    virtual void visitWhileLoopNode(class WhileLoopNode& node) = 0;
    virtual void visitForLoopNode(class ForLoopNode& node) = 0;
    virtual void visitReturnStatementNode(class ReturnStatementNode& node) = 0;
    virtual void visitBinaryExpressionNode(class BinaryExpressionNode& node) = 0;
    virtual void visitUnaryExpressionNode(class UnaryExpressionNode& node) = 0;
    virtual void visitIdentifierNode(class IdentifierNode& node) = 0;
    virtual void visitNumberNode(class NumberNode& node) = 0;
    virtual void visitStringNode(class StringNode& node) = 0;
    virtual void visitTeluguSpecificNode(class TeluguSpecificNode& node) = 0;
    virtual void visitMatrixExpressionNode(class MatrixExpressionNode& node) = 0;
    virtual void visitAgentBehaviorNode(class AgentBehaviorNode& node) = 0;
    virtual void visitWebOperationNode(class WebOperationNode& node) = 0;
};

class TeluguSpecificNode : public BaseASTNode {
private:
    ASTNode* m_parent;

public:
    TeluguSpecificNode(ASTNodeType t, const std::wstring& v, const std::wstring& originalText)
        : BaseASTNode(t, v, originalText), m_parent(nullptr) {}

    void accept(ASTVisitor& visitor) override {
        visitor.visitTeluguSpecificNode(*this);
    }

    std::unique_ptr<ASTNode> clone() const override {
        return std::make_unique<TeluguSpecificNode>(*this);
    }

    void validate() const override {
        if (getValue().empty()) {
            throw std::runtime_error("TeluguSpecificNode: Value cannot be empty");
        }
        // Add more validation logic if needed
    }

    void setParent(ASTNode* parent) override {
        m_parent = parent;
    }

    ASTNode* getParent() const override {
        return m_parent;
    }
};

// Add more specific node types as needed, e.g., MatrixNode, AgentNode, WebDevelopmentNode, etc.

// SymbolTable class implementation
class SymbolTable {
public:
    enum class SymbolType {
        Variable,
        Function,
        Class,
        Agent,
        TeluguSpecific,
        Module,
        Interface,
        Enum
    };

    struct Symbol {
        std::wstring name;
        std::wstring type;
        SymbolType symbolType;
        bool isConstant;
        std::vector<std::wstring> parameters;  // For functions
        std::wstring returnType;  // For functions
        std::wstring originalTeluguText;  // For Telugu-specific symbols
        size_t scopeLevel;  // To track the scope level of the symbol
    };

private:
    std::vector<std::unordered_map<std::wstring, Symbol>> scopes;
    size_t currentScopeLevel;

public:
    SymbolTable() : currentScopeLevel(0) {
        // Initialize with global scope
        scopes.push_back({});
    }

    void enterScope() {
        scopes.push_back({});
        currentScopeLevel++;
    }

    void exitScope() {
        if (scopes.size() > 1) {
            scopes.pop_back();
            currentScopeLevel--;
        }
    }

    bool addSymbol(const std::wstring& name, const std::wstring& type, SymbolType symbolType, bool isConstant = false, const std::wstring& originalTeluguText = L"") {
        if (scopes.back().find(name) != scopes.back().end()) {
            return false; // Symbol already exists in current scope
        }
        scopes.back()[name] = Symbol{name, type, symbolType, isConstant, {}, L"", originalTeluguText, currentScopeLevel};
        return true;
    }

    bool addFunctionSymbol(const std::wstring& name, const std::wstring& returnType, const std::vector<std::wstring>& parameters, const std::wstring& originalTeluguText = L"") {
        if (scopes.back().find(name) != scopes.back().end()) {
            return false; // Symbol already exists in current scope
        }
        scopes.back()[name] = Symbol{name, L"function", SymbolType::Function, false, parameters, returnType, originalTeluguText, currentScopeLevel};
        return true;
    }

    Symbol* lookupSymbol(const std::wstring& name) {
        for (auto it = scopes.rbegin(); it != scopes.rend(); ++it) {
            auto found = it->find(name);
            if (found != it->end()) {
                return &(found->second);
            }
        }
        return nullptr; // Symbol not found
    }

    bool isSymbolInCurrentScope(const std::wstring& name) const {
        return scopes.back().find(name) != scopes.back().end();
    }

    bool isTeluguSpecificSymbol(const std::wstring& name) const {
        for (auto it = scopes.rbegin(); it != scopes.rend(); ++it) {
            auto found = it->find(name);
            if (found != it->end()) {
                return found->second.symbolType == SymbolType::TeluguSpecific;
            }
        }
        return false;
    }

    std::vector<Symbol> getAllSymbolsInScope(size_t scopeLevel) const {
        std::vector<Symbol> symbols;
        if (scopeLevel < scopes.size()) {
            for (const auto& pair : scopes[scopeLevel]) {
                symbols.push_back(pair.second);
            }
        }
        return symbols;
    }

    bool updateSymbol(const std::wstring& name, const Symbol& newSymbol) {
        for (auto& scope : scopes) {
            auto it = scope.find(name);
            if (it != scope.end()) {
                it->second = newSymbol;
                return true;
            }
        }
        return false; // Symbol not found
    }

    size_t getCurrentScopeLevel() const {
        return currentScopeLevel;
    }

    void clear() {
        scopes.clear();
        scopes.push_back({});
        currentScopeLevel = 0;
    }
};

// IRInstruction class definition
class IRInstruction {
public:
    enum class Type {
        Arithmetic,
        ControlFlow,
        FunctionCall,
        Assignment,
        Declaration,
        Return,
        AgentBehavior,
        WebOperation,
        MathOperation,
        MatrixOperation,
        VectorOperation,
        StatisticalOperation,
        AgentCommunication,
        HttpRequest,
        HttpResponse,
        WebSocketOperation,
        DomManipulation,
        DatabaseQuery,
        DatabaseConnection
    };

    IRInstruction(Type type) : type(type) {}
    virtual ~IRInstruction() = default;

    Type getType() const { return type; }

    virtual std::wstring toString() const = 0;

protected:
    Type type;
};

// Specific instruction classes
class ArithmeticInstruction : public IRInstruction {
public:
    ArithmeticInstruction(const ASTNode* node) : IRInstruction(Type::Arithmetic) {
        // TODO: Initialize with node data
    }
    std::wstring toString() const override { return L"ArithmeticInstruction"; }
};

class FunctionDeclarationInstruction : public IRInstruction {
public:
    FunctionDeclarationInstruction(const FunctionDeclarationNode* node) : IRInstruction(Type::FunctionCall) {
        // TODO: Initialize with node data
    }
    std::wstring toString() const override { return L"FunctionDeclarationInstruction"; }
};

class DeclarationInstruction : public IRInstruction {
public:
    DeclarationInstruction(const VariableDeclarationNode* node) : IRInstruction(Type::Declaration) {
        // TODO: Initialize with node data
    }
    std::wstring toString() const override { return L"DeclarationInstruction"; }
};

class DeclarationInstruction : public IRInstruction {
public:
    DeclarationInstruction(const ASTNode* node) : IRInstruction(Type::Declaration) {
        // TODO: Initialize with node data
    }
    std::wstring toString() const override { return L"DeclarationInstruction"; }
};

class ControlFlowInstruction : public IRInstruction {
public:
    ControlFlowInstruction(const ASTNode* node) : IRInstruction(Type::ControlFlow) {
        // TODO: Initialize with node data
    }
    std::wstring toString() const override { return L"ControlFlowInstruction"; }
};

class ReturnInstruction : public IRInstruction {
public:
    ReturnInstruction(const ASTNode* node) : IRInstruction(Type::Return) {
        // TODO: Initialize with node data
    }
    std::wstring toString() const override { return L"ReturnInstruction"; }
};

// New instruction classes
class MatrixInstruction : public IRInstruction {
public:
    MatrixInstruction(const ASTNode* node, const MatrixOperations& matrixOps)
        : IRInstruction(Type::MatrixOperation), node(node), matrixOps(matrixOps) {}
    std::wstring toString() const override { return L"MatrixInstruction"; }
private:
    const ASTNode* node;
    const MatrixOperations& matrixOps;
};

class AgentInstruction : public IRInstruction {
public:
    AgentInstruction(const ASTNode* node, const AgentBehavior& agentBehavior)
        : IRInstruction(Type::AgentBehavior), node(node), agentBehavior(agentBehavior) {}
    std::wstring toString() const override { return L"AgentInstruction"; }
private:
    const ASTNode* node;
    const AgentBehavior& agentBehavior;
};

class WebInstruction : public IRInstruction {
public:
    WebInstruction(const ASTNode* node, const WebDevelopmentTools& webTools)
        : IRInstruction(Type::WebOperation), node(node), webTools(webTools) {}
    std::wstring toString() const override { return L"WebInstruction"; }
private:
    const ASTNode* node;
    const WebDevelopmentTools& webTools;
};

class TeluguStringInstruction : public IRInstruction {
public:
    TeluguStringInstruction(const ASTNode* node)
        : IRInstruction(Type::Declaration), node(node) {}
    std::wstring toString() const override { return L"TeluguStringInstruction"; }
private:
    const ASTNode* node;
};

// IRGenerator class implementation
class IRGenerator {
private:
    std::vector<std::unique_ptr<IRInstruction>> instructions;
    MatrixOperations matrixOps;
    AgentBehavior agentBehavior;
    WebDevelopmentTools webTools;

public:
    IRGenerator() = default;
    ~IRGenerator() = default;

    void generateIR(const ASTNode* ast) {
        generateIRRecursive(ast);
    }

    const std::vector<std::unique_ptr<IRInstruction>>& getInstructions() const {
        return instructions;
    }

    void addInstruction(std::unique_ptr<IRInstruction> instruction) {
        instructions.push_back(std::move(instruction));
    }

private:
    void generateIRRecursive(const ASTNode* node) {
        if (!node) return;

        switch (node->getType()) {
            case TokenType::BinaryExpression:
                addInstruction(std::make_unique<ArithmeticInstruction>(static_cast<const BinaryExpressionNode*>(node)));
                break;
            case TokenType::FunctionDeclaration:
                addInstruction(std::make_unique<FunctionDeclarationInstruction>(static_cast<const FunctionDeclarationNode*>(node)));
                break;
            case TokenType::VariableDeclaration:
                addInstruction(std::make_unique<DeclarationInstruction>(static_cast<const VariableDeclarationNode*>(node)));
                break;
            case TokenType::IfStatement:
            case TokenType::WhileLoop:
            case TokenType::ForLoop:
                addInstruction(std::make_unique<ControlFlowInstruction>(node));
                break;
            case TokenType::ReturnStatement:
                addInstruction(std::make_unique<ReturnInstruction>(static_cast<const ReturnStatementNode*>(node)));
                break;
            case TokenType::MatrixExpression:
                addInstruction(std::make_unique<MatrixInstruction>(static_cast<const MatrixExpressionNode*>(node), matrixOps));
                break;
            case TokenType::AgentDeclaration:
                addInstruction(std::make_unique<AgentInstruction>(static_cast<const AgentDeclarationNode*>(node), agentBehavior));
                break;
            case TokenType::HttpRequest:
            case TokenType::WebSocketOperation:
                addInstruction(std::make_unique<WebInstruction>(node, webTools));
                break;
            case TokenType::TeluguStringLiteral:
                addInstruction(std::make_unique<TeluguStringInstruction>(static_cast<const StringNode*>(node)));
                break;
            default:
                throw std::runtime_error("Unrecognized ASTNode type in IRGenerator");
        }

        for (const auto& child : node->getChildren()) {
            generateIRRecursive(child.get());
        }
    }
};

// CodeGenerator class implementation
class CodeGenerator {
private:
    std::string generatedCode;

public:
    CodeGenerator() = default;
    ~CodeGenerator() = default;

    void generateCode(const std::vector<std::unique_ptr<IRInstruction>>& instructions) {
        // TODO: Implement code generation logic
        // This method should process IR instructions and generate final code
    }

    const std::string& getGeneratedCode() const {
        return generatedCode;
    }
};

// Forward declarations
class ASTNode;
class SymbolTable;

// ASTNodeType enum definition

enum class ASTNodeType {
    Program, Block, Identifier, Number, String, Boolean, Null,

    // Declarations and definitions
    FunctionDeclaration, VariableDeclaration, ConstantDeclaration,
    ClassDeclaration, AgentDeclaration, InterfaceDeclaration,

    // Statements
    ExpressionStatement, IfStatement, WhileLoop, ForLoop, DoWhileLoop,
    SwitchStatement, ReturnStatement, BreakStatement, ContinueStatement,

    // Expressions
    BinaryExpression, UnaryExpression, CallExpression,
    MemberExpression, AssignmentExpression, TernaryExpression,

    // Advanced math operations
    MatrixExpression, VectorExpression, TensorExpression,
    StatisticalExpression, ComplexNumberExpression,

    // Agent-based behaviors
    AgentBehavior, AgentMessage, AgentState, AgentEnvironment, AgentDecisionTree,

    // Web development capabilities
    HttpRequest, HttpResponse, WebSocketOperation,
    DomManipulation, RESTfulEndpoint, GraphQLQuery, GraphQLMutation,

    // Database operations
    DatabaseQuery, DatabaseConnection, DatabaseTransaction, DatabaseIndex, DatabaseView,

    // Error handling
    TryCatchBlock, ThrowStatement, FinallyBlock,

    // Concurrency
    AsyncFunction, AwaitExpression, PromiseExpression, ParallelExecution,

    // TeluguFusion specific
    TeluguStringLiteral, TeluguIdentifier, TeluguKeyword, TeluguOperator,

    // Modules and imports
    ImportDeclaration, ExportDeclaration, ModuleDeclaration,

    // Object-oriented features
    MethodDeclaration, PropertyDeclaration, ConstructorDeclaration,
    DestructorDeclaration, InheritanceDeclaration,

    // Functional programming features
    LambdaExpression, HigherOrderFunction, Closure, CurryingExpression,

    // Type system
    TypeAnnotation, GenericTypeDeclaration, UnionType, IntersectionType, TypeAlias,

    // Comments
    SingleLineComment, MultiLineComment, DocumentationComment,

    // Meta-programming
    ReflectionExpression, CodeGenerationExpression, MacroDefinition,

    // Memory management
    GarbageCollectionHint, ManualMemoryManagement,

    // Internationalization
    LocalizationTag, TranslationUnit
};

class IRGenerator {
public:
    void addInstruction(std::unique_ptr<IRInstruction> instruction);
    // Add other necessary methods
};

class FunctionDeclarationInstruction : public IRInstruction {
public:
    FunctionDeclarationInstruction(const ASTNode* node) : IRInstruction(node) {}
    // Add necessary methods
};

class DeclarationInstruction : public IRInstruction {
public:
    DeclarationInstruction(const ASTNode* node) : IRInstruction(node) {}
    // Add necessary methods
};

class DeclarationInstruction : public IRInstruction {
public:
    DeclarationInstruction(const ASTNode* node) : IRInstruction(node) {}
    // Add necessary methods
};

// Token and TokenType definitions
enum class TokenType {
    // Basic types
    Keyword,
    Identifier,
    Number,
    String,
    Operator,
    Punctuation,
    Comment,
    Whitespace,
    EndOfFile,
    ErrorToken,

    // Telugu-specific types
    TeluguKeyword,
    TeluguIdentifier,
    TeluguStringLiteral,
    TeluguMathOperator,
    TeluguWebKeyword,
    TeluguDatabaseKeyword,
    TeluguAgentKeyword,
    TeluguControlFlowKeyword,
    TeluguFunctionKeyword,
    TeluguClassKeyword,
    TeluguModuleKeyword,
    TeluguConcurrencyKeyword,

    // Control flow
    IfKeyword,
    ElseKeyword,
    WhileKeyword,
    ForKeyword,
    ReturnKeyword,
    TryKeyword,
    CatchKeyword,
    FinallyKeyword,
    BreakKeyword,
    ContinueKeyword,
    SwitchKeyword,
    CaseKeyword,
    DefaultKeyword,

    // Data structures and types
    ListDeclaration,
    DictionaryDeclaration,
    SetDeclaration,
    TupleDeclaration,
    TypeAnnotation,
    GenericType,
    UnionType,
    IntersectionType,

    // Function-related
    FunctionDeclaration,
    FunctionCall,
    LambdaExpression,
    ParameterDeclaration,

    // Object-oriented
    ClassDeclaration,
    MethodDeclaration,
    InterfaceDeclaration,
    InheritanceDeclaration,
    ConstructorDeclaration,
    DestructorDeclaration,

    // Module-related
    ImportKeyword,
    ExportKeyword,
    ModuleDeclaration,

    // Advanced math operations
    MathFunction,
    Matrix,
    Vector,
    Tensor,
    StatisticalFunction,
    ComplexNumber,

    // Agent-based behaviors
    AgentDeclaration,
    AgentAction,
    AgentState,
    AgentMessage,
    AgentEnvironment,
    AgentDecisionTree,

    // Web development capabilities
    HTMLTag,
    CSSProperty,
    JavaScriptFunction,
    HTTPMethod,
    WebSocketOperation,
    RESTfulEndpoint,
    GraphQLQuery,
    GraphQLMutation,

    // Database operations
    TableName,
    ColumnName,
    DatabaseQuery,
    DatabaseConnection,
    DatabaseTransaction,
    SQLKeyword,

    // Concurrency
    AsyncKeyword,
    AwaitKeyword,
    ParallelKeyword,

    // Memory management
    GarbageCollectionHint,
    ManualMemoryManagement,

    // Additional types
    TeluguBooleanLiteral,
    TeluguNullLiteral,
    ThisKeyword,
    SuperKeyword,
    ConstKeyword,
    StaticKeyword,
    PublicKeyword,
    PrivateKeyword,
    ProtectedKeyword,

    // Telugu-specific literals and operators
    TeluguComparisonOperator,
    TeluguLogicalOperator,
    TeluguAssignmentOperator,

    // Telugu-specific data structure keywords
    TeluguListKeyword,
    TeluguDictionaryKeyword,
    TeluguSetKeyword,
    TeluguTupleKeyword
};



    Token(Type t, const std::wstring& v, const std::wstring& originalText, size_t l = 0, size_t c = 0)
        : m_type(t), m_value(v), m_originalText(originalText), m_line(l), m_column(c) {}

    ~Token() = default;

    std::wstring toString() const {
        return L"Token(" + tokenTypeToString(m_type) + L", " + m_value + L", " + m_originalText + L", " +
               std::to_wstring(m_line) + L", " + std::to_wstring(m_column) + L")";
    }

    static std::wstring tokenTypeToString(TokenType t) {
        static const std::unordered_map<TokenType, std::wstring> tokenTypeMap = {
            {TokenType::Keyword, std::wstring(L"Keyword")},
            {TokenType::Identifier, std::wstring(L"Identifier")},
            {TokenType::Number, std::wstring(L"Number")},
            {TokenType::String, std::wstring(L"String")},
            {TokenType::Operator, std::wstring(L"Operator")},
            {TokenType::Punctuation, std::wstring(L"Punctuation")},
            {TokenType::TeluguKeyword, std::wstring(L"TeluguKeyword")},
            {TokenType::TeluguIdentifier, std::wstring(L"TeluguIdentifier")},
            {TokenType::TeluguStringLiteral, std::wstring(L"TeluguStringLiteral")},
            {TokenType::MathFunction, std::wstring(L"MathFunction")},
            {TokenType::Matrix, std::wstring(L"Matrix")},
            {TokenType::Vector, std::wstring(L"Vector")},
            {TokenType::Tensor, std::wstring(L"Tensor")},
            {TokenType::StatisticalFunction, std::wstring(L"StatisticalFunction")},
            {TokenType::AgentDeclaration, std::wstring(L"AgentDeclaration")},
            {TokenType::AgentAction, std::wstring(L"AgentAction")},
            {TokenType::AgentState, std::wstring(L"AgentState")},
            {TokenType::AgentMessage, std::wstring(L"AgentMessage")},
            {TokenType::AgentEnvironment, std::wstring(L"AgentEnvironment")},
            {TokenType::HTMLTag, std::wstring(L"HTMLTag")},
            {TokenType::CSSProperty, std::wstring(L"CSSProperty")},
            {TokenType::JavaScriptFunction, std::wstring(L"JavaScriptFunction")},
            {TokenType::HTTPMethod, std::wstring(L"HTTPMethod")},
            {TokenType::WebSocketOperation, std::wstring(L"WebSocketOperation")},
            {TokenType::RESTfulEndpoint, std::wstring(L"RESTfulEndpoint")},
            {TokenType::SQLKeyword, std::wstring(L"SQLKeyword")},
            {TokenType::TableName, std::wstring(L"TableName")},
            {TokenType::ColumnName, std::wstring(L"ColumnName")},
            {TokenType::DatabaseQuery, std::wstring(L"DatabaseQuery")},
            {TokenType::DatabaseConnection, std::wstring(L"DatabaseConnection")},
            {TokenType::Comment, std::wstring(L"Comment")},
            {TokenType::Whitespace, std::wstring(L"Whitespace")},
            {TokenType::EndOfFile, std::wstring(L"EndOfFile")},
            {TokenType::ErrorToken, std::wstring(L"ErrorToken")},
            {TokenType::TeluguMathOperator, std::wstring(L"TeluguMathOperator")},
            {TokenType::TeluguWebKeyword, std::wstring(L"TeluguWebKeyword")},
            {TokenType::TeluguDatabaseKeyword, std::wstring(L"TeluguDatabaseKeyword")},
            {TokenType::TeluguAgentKeyword, std::wstring(L"TeluguAgentKeyword")},
            {TokenType::IfKeyword, std::wstring(L"IfKeyword")},
            {TokenType::ElseKeyword, std::wstring(L"ElseKeyword")},
            {TokenType::WhileKeyword, std::wstring(L"WhileKeyword")},
            {TokenType::ForKeyword, std::wstring(L"ForKeyword")},
            {TokenType::ReturnKeyword, std::wstring(L"ReturnKeyword")},
            {TokenType::TryKeyword, std::wstring(L"TryKeyword")},
            {TokenType::CatchKeyword, std::wstring(L"CatchKeyword")},
            {TokenType::FinallyKeyword, std::wstring(L"FinallyKeyword")},
            {TokenType::BreakKeyword, std::wstring(L"BreakKeyword")},
            {TokenType::ContinueKeyword, std::wstring(L"ContinueKeyword")},
            {TokenType::SwitchKeyword, std::wstring(L"SwitchKeyword")},
            {TokenType::CaseKeyword, std::wstring(L"CaseKeyword")},
            {TokenType::DefaultKeyword, std::wstring(L"DefaultKeyword")},
            {TokenType::ListDeclaration, std::wstring(L"ListDeclaration")},
            {TokenType::DictionaryDeclaration, std::wstring(L"DictionaryDeclaration")},
            {TokenType::SetDeclaration, std::wstring(L"SetDeclaration")},
            {TokenType::TupleDeclaration, std::wstring(L"TupleDeclaration")},
            {TokenType::TypeAnnotation, std::wstring(L"TypeAnnotation")},
            {TokenType::GenericType, std::wstring(L"GenericType")},
            {TokenType::UnionType, std::wstring(L"UnionType")},
            {TokenType::IntersectionType, std::wstring(L"IntersectionType")},
            {TokenType::FunctionDeclaration, std::wstring(L"FunctionDeclaration")},
            {TokenType::FunctionCall, std::wstring(L"FunctionCall")},
            {TokenType::LambdaExpression, std::wstring(L"LambdaExpression")},
            {TokenType::ParameterDeclaration, std::wstring(L"ParameterDeclaration")},
            {TokenType::ClassDeclaration, std::wstring(L"ClassDeclaration")},
            {TokenType::MethodDeclaration, std::wstring(L"MethodDeclaration")},
            {TokenType::InterfaceDeclaration, std::wstring(L"InterfaceDeclaration")},
            {TokenType::InheritanceDeclaration, std::wstring(L"InheritanceDeclaration")},
            {TokenType::ConstructorDeclaration, std::wstring(L"ConstructorDeclaration")},
            {TokenType::DestructorDeclaration, std::wstring(L"DestructorDeclaration")},
            {TokenType::ImportKeyword, std::wstring(L"ImportKeyword")},
            {TokenType::ExportKeyword, std::wstring(L"ExportKeyword")},
            {TokenType::ModuleDeclaration, std::wstring(L"ModuleDeclaration")},
            {TokenType::ComplexNumber, std::wstring(L"ComplexNumber")},
            {TokenType::AgentDecisionTree, std::wstring(L"AgentDecisionTree")},
            {TokenType::GraphQLQuery, std::wstring(L"GraphQLQuery")},
            {TokenType::GraphQLMutation, std::wstring(L"GraphQLMutation")},
            {TokenType::DatabaseTransaction, std::wstring(L"DatabaseTransaction")},
            {TokenType::AsyncKeyword, std::wstring(L"AsyncKeyword")},
            {TokenType::AwaitKeyword, std::wstring(L"AwaitKeyword")},
            {TokenType::ParallelKeyword, std::wstring(L"ParallelKeyword")},
            {TokenType::GarbageCollectionHint, std::wstring(L"GarbageCollectionHint")},
            {TokenType::ManualMemoryManagement, std::wstring(L"ManualMemoryManagement")},
            {TokenType::TeluguBooleanLiteral, std::wstring(L"TeluguBooleanLiteral")},
            {TokenType::TeluguNullLiteral, std::wstring(L"TeluguNullLiteral")},
            {TokenType::ThisKeyword, std::wstring(L"ThisKeyword")},
            {TokenType::SuperKeyword, std::wstring(L"SuperKeyword")},
            {TokenType::ConstKeyword, std::wstring(L"ConstKeyword")},
            {TokenType::StaticKeyword, std::wstring(L"StaticKeyword")},
            {TokenType::PublicKeyword, std::wstring(L"PublicKeyword")},
            {TokenType::PrivateKeyword, std::wstring(L"PrivateKeyword")},
            {TokenType::ProtectedKeyword, std::wstring(L"ProtectedKeyword")}
        };
        auto it = tokenTypeMap.find(t);
        return it != tokenTypeMap.end() ? it->second : std::wstring(L"Unknown");
    }

    bool isTeluguSpecific();
    bool isMathRelated();
    bool isAgentRelated();
    bool isWebRelated();
    bool isDatabaseRelated();
    bool isControlFlow();
    bool isDataStructure();
    bool isFunctionRelated();
    bool isObjectOriented();
    bool isModuleRelated();
    bool isTypeRelated();
    bool isConcurrencyRelated();
    bool isMemoryManagementRelated();
    bool isLiteral();
    bool isAccessModifier();
};

// ParsingError definition
