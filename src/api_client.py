"""
API Client for DNA Center AI-RRM data collection.

This module provides a client interface for interacting with Cisco DNA
Center APIs, specifically for AI-RRM (AI Radio Resource Management)
data collection using both REST and GraphQL endpoints.
"""
import logging
from typing import Any, Dict, List, Optional

import requests

from auth import DNACenterAuth

logger = logging.getLogger(__name__)


class DNACenterClient:
    """
    Client for interacting with DNA Center APIs.

    This class provides methods to query AI-RRM data including building
    configurations, coverage metrics, performance statistics, and
    AI-generated insights via GraphQL queries.
    """

    def __init__(self, auth: DNACenterAuth) -> None:
        """
        Initialize DNA Center API client.

        Parameters:
            auth (DNACenterAuth): Authenticated DNA Center session

        Returns:
            None
        """
        self.auth: DNACenterAuth = auth
        self.base_url: str = auth.base_url
        self.verify_ssl: bool = auth.verify_ssl

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> requests.Response:
        """
        Make authenticated request to DNA Center API.

        This is a private helper method that handles authentication
        headers, SSL verification, and error handling for all API calls.

        Parameters:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path (e.g., '/api/v1/health')
            **kwargs (Any): Additional arguments passed to requests library

        Returns:
            requests.Response: HTTP response object

        Raises:
            requests.exceptions.RequestException: For HTTP errors,
                connection issues, or timeouts
        """
        url = f"{self.base_url}{endpoint}"
        headers = self.auth.get_headers()

        # Merge additional headers if provided
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                verify=self.verify_ssl,
                timeout=60,
                **kwargs
            )
            # Raise exception for 4xx/5xx status codes
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            # Log error with full context for troubleshooting
            logger.error(
                f"API request failed: {method} {endpoint} - {e}"
            )
            raise

    def get_airrm_buildings(self) -> List[Dict[str, Any]]:
        """
        Get list of buildings with AI-RRM enabled (building-level only).

        Queries the DNA Center API to retrieve all buildings that have
        AI-RRM profiles configured. The API returns floor-level sites,
        so this method groups them by building name to return one entry
        per building, matching AI-RRM's building-level operation model.

        Returns:
            List[Dict[str, Any]]: List of building dictionaries, each
                containing building metadata (UUID, name, hierarchy)
                and AI-RRM profile information. Deduplicated to show
                one entry per building.

        Raises:
            requests.exceptions.RequestException: If API call fails

        Example:
            >>> client.get_airrm_buildings()
            [{'instanceUUID': 'abc-123', 'name': 'Building 1', ...}]
        """
        logger.info("Fetching AI-RRM enabled buildings")
        endpoint = "/api/v1/dna/sunray/airfprofilesitesinfo"

        response = self._make_request('GET', endpoint)
        data = response.json()

        # Use dict to deduplicate floor-level entries by building name
        building_map: Dict[str, Dict[str, Any]] = {}
        floor_count = 0
        
        # Parse response and extract buildings from each profile
        if 'response' in data:
            for profile in data['response']:
                profile_name = profile.get('aiRfProfileName', 'Unknown')
                for site in profile.get('associatedBuildings', []):
                    floor_count += 1
                    building_name = site.get('name', '')
                    
                    # Group by building name - keep first occurrence
                    # AI-RRM operates at building level, not floor level
                    if building_name and building_name not in building_map:
                        site['aiRfProfileName'] = profile_name
                        building_map[building_name] = site
                        logger.debug(
                            f"Added building: {building_name} "
                            f"(UUID: {site.get('instanceUUID')})"
                        )

        buildings = list(building_map.values())

        logger.info(
            f"Found {len(buildings)} buildings with AI-RRM enabled "
            f"(deduplicated from {floor_count} floor-level sites)"
        )
        return buildings

    def graphql_query(
        self,
        operation_name: str,
        query: str,
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute GraphQL query against DNA Center.

        Parameters:
            operation_name (str): Name of the GraphQL operation
            query (str): GraphQL query string
            variables (Dict[str, Any]): Query variables dictionary

        Returns:
            Dict[str, Any]: Query response data

        Raises:
            requests.exceptions.RequestException: If API call fails
        """
        endpoint = (
            "/api/kairos/v1/proxy/api/v2/core-services/"
            "customer-id/sunray/graphql"
        )

        payload = {
            "operationName": operation_name,
            "variables": variables,
            "query": query
        }

        logger.debug(f"Executing GraphQL query: {operation_name}")
        response = self._make_request('POST', endpoint, json=payload)
        return response.json()

    def get_coverage_summary(
        self,
        building_id: str,
        frequency_band: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get RF coverage summary for a building and frequency band.

        Retrieves coverage metrics including AP count, client count,
        and SNR data for a specific building and frequency.

        Parameters:
            building_id (str): Building UUID
            frequency_band (int): Frequency band (2=2.4GHz, 5=5GHz,
                6=6GHz)

        Returns:
            Optional[Dict[str, Any]]: Coverage summary data with keys:
                - totalApCount: Number of access points
                - totalClients: Number of connected clients
                - connectivitySnr: SNR metrics
                Returns None if no data available

        Raises:
            requests.exceptions.RequestException: If API call fails
        """
        query = """query getRfCoverageSummaryLatest01(
            $buildingId: String,
            $frequencyBand: Int
        ) {
            getRfCoverageSummaryLatest01(
                buildingId: $buildingId,
                frequencyBand: $frequencyBand
            ) {
                nodes {
                    buildingId
                    frequencyBand
                    siteId
                    timestampMs
                    timestamp
                    connectivitySnr
                    connectivitySnrDensity
                    apDensity
                    totalApCount
                    totalClients
                }
            }
        }"""

        variables = {
            "buildingId": building_id,
            "frequencyBand": frequency_band
        }

        result = self.graphql_query(
            "getRfCoverageSummaryLatest01",
            query,
            variables
        )

        # Extract first node from result (edge case: empty response)
        nodes = result.get('data', {}).get(
            'getRfCoverageSummaryLatest01', {}
        ).get('nodes', [])
        return nodes[0] if nodes else None

    def get_performance_summary(
        self,
        building_id: str,
        frequency_band: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get RF performance summary for a building and frequency band.

        Retrieves RRM performance metrics including health score,
        optimization changes, and CCI (co-channel interference) data.

        Parameters:
            building_id (str): Building UUID
            frequency_band (int): Frequency band (2=2.4GHz, 5=5GHz,
                6=6GHz)

        Returns:
            Optional[Dict[str, Any]]: Performance summary with keys:
                - rrmHealthScore: Health score (0-100)
                - totalRrmChangesV2: Number of RRM optimizations
                - apPercentageWithHighCci: % APs with high interference
                Returns None if no data available

        Raises:
            requests.exceptions.RequestException: If API call fails
        """
        query = """query getRfPerformanceSummaryLatest01(
            $buildingId: String,
            $frequencyBand: Int
        ) {
            getRfPerformanceSummaryLatest01(
                buildingId: $buildingId,
                frequencyBand: $frequencyBand
            ) {
                nodes {
                    buildingId
                    frequencyBand
                    siteId
                    timestampMs
                    timestamp
                    totalRrmChangesV2
                    rrmHealthScore
                    apPercentageWithHighCci
                }
            }
        }"""

        variables = {
            "buildingId": building_id,
            "frequencyBand": frequency_band
        }

        result = self.graphql_query(
            "getRfPerformanceSummaryLatest01",
            query,
            variables
        )

        # Edge case: Handle missing or empty response
        nodes = result.get('data', {}).get(
            'getRfPerformanceSummaryLatest01', {}
        ).get('nodes', [])
        return nodes[0] if nodes else None

    def get_insights(
        self,
        building_id: str,
        frequency_band: int
    ) -> List[Dict[str, Any]]:
        """
        Get current AI-generated insights for a building/frequency.

        Retrieves AI-RRM insights which are recommendations and
        observations about the RF environment.

        Parameters:
            building_id (str): Building UUID
            frequency_band (int): Frequency band (2=2.4GHz, 5=5GHz,
                6=6GHz)

        Returns:
            List[Dict[str, Any]]: List of insight dictionaries with:
                - insightType: Type/category of insight
                - insightValue: Numeric value associated with insight
                - description: Human-readable description
                - reason: Explanation of why insight was generated
                Returns empty list if no insights available

        Raises:
            requests.exceptions.RequestException: If API call fails
        """
        query = """query getCurrentInsights01(
            $buildingId: String,
            $frequencyBand: Int
        ) {
            getCurrentInsights01(
                buildingId: $buildingId,
                frequencyBand: $frequencyBand
            ) {
                nodes {
                    buildingId
                    frequencyBand
                    siteId
                    timestampMs
                    timestamp
                    insightType
                    insightValue
                    description
                    reason
                }
            }
        }"""

        variables = {
            "buildingId": building_id,
            "frequencyBand": frequency_band
        }

        result = self.graphql_query(
            "getCurrentInsights01",
            query,
            variables
        )

        # Edge case: Return empty list instead of None for consistency
        nodes = result.get('data', {}).get(
            'getCurrentInsights01', {}
        ).get('nodes', [])
        return nodes if nodes else []
