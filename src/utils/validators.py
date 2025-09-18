"""Input validation utilities for GitHub Analyzer Agent."""

import re
from typing import Optional, Tuple
from urllib.parse import urlparse
from pydantic import BaseModel, field_validator, Field
from .logger import get_logger

logger = get_logger(__name__)


class GitHubURLValidator(BaseModel):
    """Pydantic model for validating GitHub repository URLs."""
    
    url: str = Field(..., description="GitHub repository URL")
    owner: Optional[str] = Field(None, description="Repository owner")
    repo: Optional[str] = Field(None, description="Repository name")
    
    @field_validator('url')
    @classmethod
    def validate_github_url(cls, v: str) -> str:
        """Validate that the URL is a valid GitHub repository URL."""
        if not v:
            raise ValueError("URL cannot be empty")
        
        # Parse URL
        parsed = urlparse(v.strip())
        
        # Check if it's a GitHub URL
        if parsed.netloc.lower() not in ['github.com', 'www.github.com']:
            raise ValueError("URL must be from github.com")
        
        # Check if it's HTTPS
        if parsed.scheme != 'https':
            logger.warning("Non-HTTPS GitHub URL detected", url=v)
        
        # Extract and validate path
        path_parts = [part for part in parsed.path.split('/') if part]
        if len(path_parts) < 2:
            raise ValueError("URL must include both owner and repository name")
        
        # Validate owner and repo names (GitHub username/repo constraints)
        owner, repo = path_parts[0], path_parts[1]
        
        # Remove .git suffix if present
        if repo.endswith('.git'):
            repo = repo[:-4]
        
        if not _is_valid_github_name(owner):
            raise ValueError(f"Invalid GitHub username: {owner}")
        
        if not _is_valid_github_name(repo):
            raise ValueError(f"Invalid GitHub repository name: {repo}")
        
        return v
    
    def model_post_init(self, __context) -> None:
        """Extract owner and repo from validated URL."""
        parsed = urlparse(self.url)
        path_parts = [part for part in parsed.path.split('/') if part]
        
        self.owner = path_parts[0]
        self.repo = path_parts[1]
        
        # Remove .git suffix if present
        if self.repo.endswith('.git'):
            self.repo = self.repo[:-4]
            
        logger.info(
            "GitHub URL validated successfully",
            url=self.url,
            owner=self.owner,
            repo=self.repo
        )


def _is_valid_github_name(name: str) -> bool:
    """Validate GitHub username/repository name.
    
    GitHub names must:
    - Be 1-39 characters long
    - Start with alphanumeric character
    - Can contain hyphens but not consecutive hyphens
    - Cannot start or end with hyphen
    """
    if not name or len(name) > 39:
        return False
    
    # GitHub name pattern
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    
    if not re.match(pattern, name):
        return False
    
    # Check for consecutive hyphens
    if '--' in name:
        return False
    
    return True


def validate_github_url(url: str) -> Tuple[str, str, str]:
    """Validate GitHub URL and extract components.
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Tuple of (validated_url, owner, repo)
        
    Raises:
        ValueError: If URL is invalid
    """
    try:
        validator = GitHubURLValidator(url=url)
        return validator.url, validator.owner, validator.repo
    except Exception as e:
        logger.error("GitHub URL validation failed", url=url, error=str(e))
        raise ValueError(f"Invalid GitHub URL: {e}")


def validate_analysis_type(analysis_type: str) -> str:
    """Validate analysis type parameter.
    
    Args:
        analysis_type: Type of analysis to perform
        
    Returns:
        Validated analysis type
        
    Raises:
        ValueError: If analysis type is invalid
    """
    valid_types = {'security', 'summary', 'custom', 'code_review', 'dependencies'}
    
    if not analysis_type or analysis_type.lower() not in valid_types:
        raise ValueError(
            f"Invalid analysis type '{analysis_type}'. "
            f"Valid types: {', '.join(sorted(valid_types))}"
        )
    
    return analysis_type.lower()