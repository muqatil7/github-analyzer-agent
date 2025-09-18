"""MCP (Model Context Protocol) integration module."""

from .client import GitHubMCPClient
from .config import MCPConfig

__all__ = ["GitHubMCPClient", "MCPConfig"]