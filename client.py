

import logging
from typing import Any, Literal

import httpx

from app.core.integrations.notion.decorators import retry
from app.core.integrations.notion.exceptions import (
    NotionAPIError,
    NotionAuthenticationError,
    NotionBadRequestError,
    NotionConflictError,
    NotionInternalServerError,
    NotionNotFoundError,
    NotionRateLimitError,
    NotionServiceUnavailableError,
)
from app.core.integrations.notion.schemas import (
    AppendBlockChildrenPayload,
    AppendBlockChildrenResponse,
    Comment,
    CreateCommentPayload,
    Database,
    FilesProperty,
    Page,
    PaginatedBlockResponse,
    PaginatedCommentResponse,
    PaginatedPageResponse,
    PaginatedUserResponse,
    QueryDatabasePayload,
    UpdatePagePayload,
    User,
)
from app.core.integrations.notion.utils import clean_id

# * Configure logging
logger = logging.getLogger(__name__)

# * Constants
NOTION_API_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"


class AsyncNotionClient:
    """An asynchronous client for the Notion API."""

    def __init__(self, token: str, client: httpx.AsyncClient):
        """
        Initializes the Notion client.

        Args:
            token: The Notion integration token.
            client: An httpx.AsyncClient instance.
        """
        self.token = token
        self.client = client
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION,
        }

    @retry()
    async def _request(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE"],
        endpoint: str,
        payload: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Makes an asynchronous request to the Notion API.

        Args:
            method: The HTTP method to use.
            endpoint: The API endpoint to call (e.g., "/databases/{db_id}").
            payload: The JSON payload for POST/PATCH requests.
            params: The URL query parameters.

        Returns:
            The JSON response from the API as a dictionary.

        Raises:
            NotionAPIError: For any API-related errors.
        """
        url = f"{BASE_URL}/{endpoint.lstrip('/')}"
        try:
            response = await self.client.request(
                method, url, headers=self.headers, json=payload, params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_details = e.response.json()
            logger.error(
                "Notion API request failed with status %d: %s",
                status_code,
                error_details,
            )
            error_map = {
                400: NotionBadRequestError,
                401: NotionAuthenticationError,
                404: NotionNotFoundError,
                409: NotionConflictError,
                429: NotionRateLimitError,
                500: NotionInternalServerError,
                503: NotionServiceUnavailableError,
            }
            exception_class = error_map.get(status_code, NotionAPIError)
            raise exception_class(
                f"Notion API Error ({status_code}): {error_details.get('message', 'Unknown error')}"
            ) from e
        except httpx.RequestError as e:
            logger.error("HTTP request to Notion API failed: %s", e)
            raise NotionAPIError(f"HTTP request failed: {e}") from e

    async def get_database(self, database_id: str) -> Database:
        """
        Retrieves a database object.

        Args:
            database_id: The ID of the database.

        Returns:
            A dictionary representing the Notion Database object.
        """
        db_id = clean_id(database_id)
        response = await self._request("GET", f"databases/{db_id}")
        return Database.model_validate(response)

    async def query_database(
        self, database_id: str, payload: QueryDatabasePayload | None = None
    ) -> PaginatedPageResponse:
        """
        Queries a database for pages.

        Args:
            database_id: The ID of the database to query.
            payload: The query payload (for filtering, sorting, etc.).

        Returns:
            A dictionary containing a list of page objects.
        """
        db_id = clean_id(database_id)
        dumped_payload = payload.model_dump(exclude_unset=True) if payload else None
        response = await self._request(
            "POST", f"databases/{db_id}/query", payload=dumped_payload
        )
        return PaginatedPageResponse.model_validate(response)

    async def create_page(self, payload: Page) -> Page:
        """
        Creates a new page in Notion.

        Args:
            payload: The payload containing parent, properties, etc.

        Returns:
            A dictionary representing the new Page object.
        """
        response = await self._request(
            "POST", "pages", payload=payload.model_dump(exclude_unset=True)
        )
        return Page.model_validate(response)

    async def get_page(self, page_id: str) -> Page:
        """
        Retrieves a page object.

        Args:
            page_id: The ID of the page.

        Returns:
            A dictionary representing the Page object.
        """
        p_id = clean_id(page_id)
        response = await self._request("GET", f"pages/{p_id}")
        return Page.model_validate(response)

    async def update_page(self, page_id: str, payload: UpdatePagePayload) -> Page:
        """
        Updates a page's properties.

        Args:
            page_id: The ID of the page to update.
            payload: The payload containing the properties to update.

        Returns:
            A dictionary representing the updated Page object.
        """
        p_id = clean_id(page_id)
        response = await self._request(
            "PATCH", f"pages/{p_id}", payload=payload.model_dump(exclude_unset=True)
        )
        return Page.model_validate(response)

    async def get_block_children(
        self, block_id: str, page_size: int | None = None
    ) -> PaginatedBlockResponse:
        """Retrieves a list of Block objects for a given block ID."""
        params = {}
        if page_size is not None:
            params["page_size"] = page_size

        response = await self._request(
            "GET", f"blocks/{block_id}/children", params=params
        )
        return PaginatedBlockResponse.model_validate(response)

    async def append_block_children(
        self, block_id: str, payload: AppendBlockChildrenPayload
    ) -> AppendBlockChildrenResponse:
        """Appends block children to a specific block."""
        response = await self._request(
            "PATCH",
            f"blocks/{block_id}/children",
            payload=payload.model_dump(exclude_unset=True),
        )
        return AppendBlockChildrenResponse.model_validate(response)

    async def list_comments(self, block_id: str) -> PaginatedCommentResponse:
        """Retrieves a list of comments for a given block ID."""
        response = await self._request("GET", f"comments?block_id={block_id}")
        return PaginatedCommentResponse.model_validate(response)

    async def create_comment(self, payload: CreateCommentPayload) -> Comment:
        """Creates a new comment."""
        response = await self._request(
            "POST", "comments", payload=payload.model_dump(exclude_unset=True)
        )
        return Comment.model_validate(response)

    async def list_users(self) -> PaginatedUserResponse:
        """Lists all users."""
        response = await self._request("GET", "users")
        return PaginatedUserResponse.model_validate(response)

    async def get_user(self, user_id: str) -> User:
        """Retrieves a user by their ID."""
        response = await self._request("GET", f"users/{user_id}")
        return User.model_validate(response)

    async def get_me(self) -> User:
        """Retrieves the bot user associated with the token."""
        response = await self._request("GET", "users/me")
        return User.model_validate(response)

    async def get_page_property(
        self, page_id: str, property_id: str
    ) -> FilesProperty:
        """
        Retrieves a single page property item.

        Args:
            page_id: The ID of the page.
            property_id: The ID of the property.

        Returns:
            A dictionary representing the property item.
        """
        p_id = clean_id(page_id)
        prop_id = clean_id(property_id)
        response = await self._request("GET", f"pages/{p_id}/properties/{prop_id}")
        # ! Note: This currently only validates FilesProperty.
        # TODO: Add a more robust validation for all property types.
        return FilesProperty.model_validate(response)
