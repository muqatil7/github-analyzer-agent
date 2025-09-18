"""GitHub Analyzer Agent - AI Agent for analyzing GitHub repositories."""

__version__ = "1.0.0"
__author__ = "Yahya Sayed"
__email__ = "your.email@example.com"
__description__ = "AI Agent built with LangGraph + LangChain + LangSmith for analyzing GitHub repositories"

# Import main classes for easy access
try:
    from .main import GitHubAnalyzerAgent
    from .agent.github_agent import GitHubAgent
    from .mcp.client import GitHubMCPClient
    from .services.context_manager import ContextManager
    from .services.langsmith_tracer import LangSmithTracer
    from .services.openai_service import OpenAIService
    
    __all__ = [
        "GitHubAnalyzerAgent",
        "GitHubAgent", 
        "GitHubMCPClient",
        "ContextManager",
        "LangSmithTracer",
        "OpenAIService"
    ]
except ImportError:
    # Handle import errors gracefully during development
    pass