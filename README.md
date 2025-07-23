# Notion as a Headless CMS: A Production-Ready Python SDK

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/techwithty)
[![Release](https://img.shields.io/github/v/release/techwithty/notion-sdk-python?color=brightgreen)](https://github.com/techwithty)

**Unlock the power of Notion as a fast, flexible, and collaborative headless CMS for your applications. This Python SDK provides a robust, asynchronous, and type-safe interface to the official Notion API, making it easier than ever to use Notion as a database backend, similar to Strapi or Contentful.**

This library is designed for production use with [FastAPI](https://fastapi.tiangolo.com/), offering a seamless integration experience with dependency injection, Pydantic V2 data validation, and a clean, modern API.

---

## ✨ Key Features

- **Notion as a Database**: Specifically designed to treat your Notion databases as a fully-featured, user-friendly CMS.
- **Fully Asynchronous**: Built with `httpx` for high-performance, non-blocking I/O suitable for modern web frameworks.
- **Pydantic V2 Models**: Comprehensive, type-hinted models for all Notion objects, ensuring data integrity and providing excellent editor support.
- **Complete API Coverage**: Interacts with all major Notion API endpoints: Databases, Pages, Blocks, Users, and Search.
- **Secure Webhook Handling**: Includes utilities for verifying webhook signatures to securely process real-time updates from Notion.
- **Production-Ready**: Comes with robust error handling, rate limit considerations, and a clean, modular structure.
- **FastAPI Integration**: Simple to integrate with FastAPI's dependency injection system.

## 🚀 The "Notion as a CMS" Philosophy

Why use Notion as a backend? It's the perfect blend of a powerful, structured database and a user-friendly, collaborative editor. Unlike traditional headless CMS platforms, Notion allows non-technical team members to manage content with zero learning curve.

- **Intuitive Content Management**: Your team can create, edit, and manage content using Notion's beautiful and intuitive interface.
- **Flexible Data Structures**: Design complex data models using Notion's database properties (Text, Numbers, Selects, Relations, etc.).
- **Real-Time Collaboration**: Multiple editors can work on content simultaneously.
- **Programmatic Access**: This SDK provides the bridge to fetch and manipulate that content in any application.

Think of it as **Strapi with the world's best editor**. You define the schema in Notion, and your team manages the content, while your application consumes it via a clean, modern API.

## ⚙️ Installation

You can add this library to your project using pip:

```bash
# Install from PyPI (once published)
pip install notion-fastapi-sdk

# Or, install directly from GitHub
pip install git+https://github.com/techwithty/notion-sdk-python.git
```

## ⚡ Quick Start

Here's a simple example of how to initialize the client and query a database.

```python
import asyncio
from notion_client import AsyncNotionClient

# Best practice: store your token in an environment variable
NOTION_TOKEN = "secret_..."
DATABASE_ID = "your_database_id_here"

async def main():
    # 1. Initialize the asynchronous client
    async with AsyncNotionClient(auth=NOTION_TOKEN) as client:

        # 2. Query your database
        response = await client.databases.query(database_id=DATABASE_ID)

        # 3. Process the results
        for page in response.get('results', []):
            try:
                title = page['properties']['Name']['title'][0]['plain_text']
                print(f"- Fetched Page: {title}")
            except (KeyError, IndexError):
                print("- Fetched a page with no title.")

if __name__ == "__main__":
    asyncio.run(main())

```

## 🤝 Contributing

Contributions are welcome! Whether it's a bug report, a new feature, or documentation improvements, please feel free to open an issue or submit a pull request.

1.  **Fork the repository.**
2.  **Create a new branch** (`git checkout -b feature/your-feature-name`).
3.  **Make your changes** and add tests.
4.  **Ensure all tests pass.**
5.  **Submit a pull request** with a clear description of your changes.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
