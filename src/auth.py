"""
Authentication module for DNA Center API.

This module handles JWT-based authentication with Cisco DNA Center,
managing token acquisition and providing authenticated request headers.
"""
import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)


class DNACenterAuth:
    """
    Handles authentication with Cisco DNA Center.

    This class manages the authentication lifecycle including login,
    token storage, and header generation for authenticated API requests.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        verify_ssl: bool = False
    ) -> None:
        """
        Initialize DNA Center authentication handler.

        Parameters:
            base_url (str): Base URL of DNA Center
                (e.g., 'https://172.31.96.6')
            username (str): Username for authentication
            password (str): Password for authentication
            verify_ssl (bool): Whether to verify SSL certificates.
                Set to False for self-signed certificates. Default: False

        Returns:
            None
        """
        self.base_url: str = base_url.rstrip('/')
        self.username: str = username
        self.password: str = password
        self.verify_ssl: bool = verify_ssl
        self.token: Optional[str] = None
        self.session_id: Optional[str] = None

        # Disable SSL warnings when verification is disabled
        # This is necessary for environments with self-signed certificates
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()

    def login(self) -> bool:
        """
        Authenticate with DNA Center and obtain JWT token.

        Makes a POST request to the authentication endpoint using
        basic authentication. Stores the returned JWT token for
        subsequent API requests.

        Returns:
            bool: True if authentication successful, False otherwise

        Raises:
            None: Exceptions are caught and logged, returning False
        """
        auth_url = f"{self.base_url}/api/system/v1/auth/token"

        try:
            logger.info(f"Attempting authentication to {self.base_url}")
            response = requests.post(
                auth_url,
                auth=(self.username, self.password),
                headers={'Content-Type': 'application/json'},
                verify=self.verify_ssl,
                timeout=30
            )

            # Raise exception for 4xx/5xx status codes
            response.raise_for_status()

            # Extract JWT token from response
            self.token = response.json().get('Token')

            # Validate token was received
            if self.token:
                logger.info("Authentication successful")
                return True
            else:
                # Edge case: 200 response but no token in payload
                logger.error("No token received in response")
                return False

        except requests.exceptions.RequestException as e:
            # Handle all request-related errors (connection, timeout, HTTP)
            logger.error(f"Authentication failed: {e}")
            return False

    def get_headers(self) -> Dict[str, str]:
        """
        Get headers for authenticated API requests.

        Returns:
            Dict[str, str]: Dictionary of HTTP headers including
                authentication token

        Raises:
            ValueError: If called before successful authentication
        """
        # Edge case: Prevent API calls without authentication
        if not self.token:
            raise ValueError("Not authenticated. Call login() first.")

        return {
            'X-Auth-Token': self.token,
            'Content-Type': 'application/json'
        }
