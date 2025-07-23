"""Pydantic models for Notion API objects."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, HttpUrl


# Generic Notion Object Model
class NotionObject(BaseModel):
    object: str

# User Object
class User(NotionObject):
    id: str
    name: str | None = None
    avatar_url: HttpUrl | None = None
    type: str | None = None
    person: dict[str, Any] | None = None
    bot: dict[str, Any] | None = None

# File and Icon Objects
class FileObject(BaseModel):
    type: Literal["external", "file"]
    url: HttpUrl | None = None

class ExternalFile(FileObject):
    type: Literal["external"] = "external"
    external: dict[str, HttpUrl]

class InternalFile(FileObject):
    type: Literal["file"] = "file"
    file: dict[str, Any]

class Icon(BaseModel):
    type: Literal["emoji", "external"]
    emoji: str | None = None
    external: dict[str, HttpUrl] | None = None

# Parent Object
class Parent(BaseModel):
    type: Literal["database_id", "page_id", "workspace"]
    database_id: str | None = None
    page_id: str | None = None
    workspace: bool | None = None

# Rich Text and Annotations
class Annotations(BaseModel):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"

class RichText(BaseModel):
    plain_text: str
    href: HttpUrl | None = None
    annotations: Annotations
    type: Literal["text", "mention", "equation"]

class Text(RichText):
    type: Literal["text"] = "text"
    text: dict[str, Any]

# Properties
class Property(BaseModel):
    id: str
    type: str

class Title(Property):
    type: Literal["title"] = "title"
    title: list[Text]

class RichTextProperty(Property):
    type: Literal["rich_text"] = "rich_text"
    rich_text: list[Text]

class SelectOption(BaseModel):
    id: str
    name: str
    color: str

class Select(Property):
    type: Literal["select"] = "select"
    select: SelectOption | None

class MultiSelect(Property):
    type: Literal["multi_select"] = "multi_select"
    multi_select: list[SelectOption]

class Date(Property):
    type: Literal["date"] = "date"
    date: dict[str, Any] | None


class File(BaseModel):
    name: str
    type: Literal["external", "file"]
    external: dict[str, HttpUrl] | None = None
    file: dict[str, Any] | None = None


class FilesProperty(Property):
    type: Literal["files"] = "files"
    files: list[File]


# Page and Database Models
class Page(NotionObject):
    id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: User
    last_edited_by: User
    cover: ExternalFile | None = None
    icon: Icon | None = None
    parent: Parent
    archived: bool
    properties: dict[
        str, Title | RichTextProperty | Select | MultiSelect | Date | FilesProperty | Property
    ]
    url: HttpUrl

class Database(NotionObject):
    id: str
    created_time: datetime
    last_edited_time: datetime
    title: list[Text]
    description: list[Text]
    properties: dict[str, Property]
    parent: Parent
    url: HttpUrl
    archived: bool
    is_inline: bool



# Block and Block Children Models
class Block(NotionObject):
    """Represents a Block object in Notion."""

    id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: User
    last_edited_by: User
    has_children: bool
    archived: bool
    type: str
    # Each block type has a corresponding field with more data
    paragraph: dict[str, Any] | None = None
    heading_1: dict[str, Any] | None = None
    heading_2: dict[str, Any] | None = None
    heading_3: dict[str, Any] | None = None
    bulleted_list_item: dict[str, Any] | None = None
    numbered_list_item: dict[str, Any] | None = None
    to_do: dict[str, Any] | None = None
    toggle: dict[str, Any] | None = None
    child_page: dict[str, Any] | None = None
    child_database: dict[str, Any] | None = None
    embed: dict[str, Any] | None = None
    image: dict[str, Any] | None = None
    video: dict[str, Any] | None = None
    file: dict[str, Any] | None = None
    pdf: dict[str, Any] | None = None
    bookmark: dict[str, Any] | None = None
    code: dict[str, Any] | None = None


# API Payloads and Responses
class PaginatedBlockResponse(BaseModel):
    """Represents a paginated response for block children."""

    object: Literal["list"]
    results: list[Block]
    next_cursor: str | None
    has_more: bool


class AppendBlockChildrenPayload(BaseModel):
    """Represents the payload for appending block children."""

    children: list[dict[str, Any]]


class AppendBlockChildrenResponse(BaseModel):
    """Represents the response from appending block children."""

    object: Literal["list"]
    results: list[Block]
class QueryDatabasePayload(BaseModel):
    filter: dict[str, Any] | None = None
    sorts: list[dict[str, Any]] | None = None
    start_cursor: str | None = None
    page_size: int | None = None


class CreatePagePayload(BaseModel):
    parent: Parent
    properties: dict[str, Any]
    children: list[dict[str, Any]] | None = None
    icon: Icon | None = None
    cover: ExternalFile | None = None


class UpdatePagePayload(BaseModel):
    properties: dict[str, Any]
    archived: bool | None = None
    icon: Icon | None = None
    cover: ExternalFile | None = None


class PaginatedPageResponse(BaseModel):
    object: Literal["list"]
    results: list[Page]
    next_cursor: str | None
    has_more: bool


class PaginatedUserResponse(BaseModel):
    object: Literal["list"]
    results: list[User]
    next_cursor: str | None
    has_more: bool


# Comment Models
class Comment(NotionObject):
    id: str
    parent: Parent
    discussion_id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: User
    rich_text: list[RichText]


class PaginatedCommentResponse(BaseModel):
    object: Literal["list"]
    results: list[Comment]
    next_cursor: str | None
    has_more: bool


class CreateCommentPayload(BaseModel):
    parent: dict[str, str] | None = None
    discussion_id: str | None = None
    rich_text: list[dict[str, Any]]
