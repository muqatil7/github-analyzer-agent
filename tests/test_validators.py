"""Tests for validation utilities."""

import pytest
from src.utils.validators import (
    GitHubURLValidator,
    validate_github_url,
    validate_analysis_type,
    _is_valid_github_name
)


class TestGitHubNameValidation:
    """Test GitHub name validation."""
    
    def test_valid_names(self):
        """Test valid GitHub names."""
        valid_names = [
            "user",
            "user123",
            "user-name",
            "123user",
            "a",
            "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y"
        ]
        
        for name in valid_names:
            assert _is_valid_github_name(name), f"Name should be valid: {name}"
    
    def test_invalid_names(self):
        """Test invalid GitHub names."""
        invalid_names = [
            "",  # Empty
            "-user",  # Starts with hyphen
            "user-",  # Ends with hyphen
            "user--name",  # Consecutive hyphens
            "a" * 40,  # Too long
            "user@name",  # Invalid character
        ]
        
        for name in invalid_names:
            assert not _is_valid_github_name(name), f"Name should be invalid: {name}"


class TestGitHubURLValidation:
    """Test GitHub URL validation."""
    
    def test_valid_urls(self):
        """Test valid GitHub repository URLs."""
        valid_urls = [
            "https://github.com/user/repo",
            "https://github.com/user/repo.git",
            "https://github.com/user-name/repo-name",
            "https://www.github.com/123user/repo123",
            "https://github.com/user/repo/tree/main",
        ]
        
        for url in valid_urls:
            validator = GitHubURLValidator(url=url)
            assert validator.owner
            assert validator.repo
            assert validator.url == url
    
    def test_invalid_urls(self):
        """Test invalid GitHub repository URLs."""
        invalid_urls = [
            "",  # Empty
            "not-a-url",
            "https://gitlab.com/user/repo",  # Not GitHub
            "https://github.com/user",  # Missing repo
            "https://github.com/",  # Missing owner and repo
            "https://github.com/-user/repo",  # Invalid owner
            "https://github.com/user/repo--name",  # Invalid repo
        ]
        
        for url in invalid_urls:
            with pytest.raises(ValueError):
                GitHubURLValidator(url=url)
    
    def test_validate_github_url_function(self):
        """Test validate_github_url convenience function."""
        url = "https://github.com/user/repo"
        validated_url, owner, repo = validate_github_url(url)
        
        assert validated_url == url
        assert owner == "user"
        assert repo == "repo"


class TestAnalysisTypeValidation:
    """Test analysis type validation."""
    
    def test_valid_analysis_types(self):
        """Test valid analysis types."""
        valid_types = ["security", "summary", "custom", "code_review", "dependencies"]
        
        for analysis_type in valid_types:
            result = validate_analysis_type(analysis_type)
            assert result == analysis_type.lower()
            
            # Test case insensitive
            result = validate_analysis_type(analysis_type.upper())
            assert result == analysis_type.lower()
    
    def test_invalid_analysis_types(self):
        """Test invalid analysis types."""
        invalid_types = ["", "invalid", "test", None]
        
        for analysis_type in invalid_types:
            with pytest.raises(ValueError):
                validate_analysis_type(analysis_type)