
# REST API Parameter Extraction Guide

This rule helps identify and extract ALL necessary parameters from API documentation to build a dlt REST API source. **Crucially, configuration parameters like pagination and incremental loading can vary significantly between different API endpoints. Do not assume a single global strategy applies to all resources.**

## 1. Base Configuration Parameters (Client Level)

These settings usually apply globally but *can* sometimes be overridden at the resource level.

### Client Settings
Look for these in the API documentation (often in "Overview", "Getting Started", "Authentication"):
- **Base URL**:
  - Aliases: "API endpoint", "root URL", "service URL"
  - Example Format: `https://api.example.com/v1/`
  - Find the main entry point for the API version you need.

- **Authentication**:
  - Keywords: "Authentication", "Authorization", "API Keys", "Security"
  - Common Types & dlt Mappings:
    - API Key: Look for "API Key", "Access Token", "Secret Token", "Subscription Key". Map API key value to `api_key`, name to `name`, location (`query` or `header`) to `location`.
    - Bearer Token: Look for "Bearer Token", "JWT". Map token value to `token`.
    - OAuth2: Look for "OAuth", "Client ID", "Client Secret", "Scopes", "Token URL". Map to `client_id`, `client_secret`, `scopes`, `token_url`.
    - Basic Auth: Look for "Basic Authentication". Map to `username` and `password`.
  - Note where credentials go (header, query parameter, request body).
  - **Secret Handling:**
    - **Pattern 1: Using `@dlt.source` or `@dlt.resource` Decorators (Recommended when applicable):**
      Define your source/resource function with arguments having defaults like `api_key: str = dlt.secrets.value` or `client_secret: str = dlt.secrets["specific_key"]`. `dlt` injects the resolved secret when calling the decorated function. You can then use the argument variable directly.
      ```python
      @dlt.source
      def my_api_source(api_key: str = dlt.secrets.value):
          config = {...
              "auth": {"type": "api_key", "api_key": api_key, ...}
              ...
          }
          yield rest_api_source(config)
      ```
    - **Pattern 2: Calling `rest_api_source` Directly (Requires Explicit Resolution):**
      If calling `rest_api_source` *without* a `@dlt.source/resource` decorator on the calling function, you **must resolve the secret explicitly *before* creating the configuration dictionary**. Using `dlt.secrets.value` directly in the dictionary or as a default function argument *will not work* in this context.

- **Global Headers** (Optional):
  - Keywords: "Headers", "Request Headers", "Required Headers"
  - Common Headers: `Accept: application/json`, `Content-Type: application/json`, `User-Agent`.
  - Look for any custom headers required for *all* requests (e.g., `X-Api-Version`). Resource-specific headers go in the resource config.

## 2. Resource / Endpoint Parameters

**Crucially, examine the documentation for EACH resource/endpoint individually.**

### Endpoint Configuration
For each endpoint/resource (e.g., `/users`, `/orders/{order_id}`), find:
- **Path**: Format: `/resource`, `/v1/resource`. Note any path parameters like `{id}`.
- **Method**: Usually explicit: `GET`, `POST`, `PUT`, `DELETE`. Default is `GET`.
- **Resource-Specific Query Parameters**: e.g. `status=active`, `sort=created_at`, `fields=id,name,email`
- **Request Body** (for `POST`, `PUT`, `PATCH`): Define the expected structure (usually JSON).

### Data Selection (Response Parsing)
- **Identify the JSON path** to the list/array of actual data items within the response.
- Common patterns & dlt `data_selector`:
  - `{"data": [...]}` -> `data`
  - `{"records": [...]}` -> `records`
  - `{"data": {"records": [...]}}` -> `data.records`

## 3. Pagination Parameters (Check Per Endpoint!)

**APIs often use different pagination methods for different endpoints. Check EACH endpoint's documentation for its specific pagination details.**

- **Identify the Strategy**: Look for sections titled "Pagination", "Paging".
- **Common Strategies & dlt Mapping**:
  - **Cursor-based**: identify `cursor_path` (response next value), `cursor_param` (query to send cursor), `limit_param`. Use `type: cursor`.
  - **Offset-based**: identify `offset_param`, `limit_param`, optional `total_path`. Use `type: offset`.
  - **Page-based**: identify `page_param`, `limit_param`, optional `total_path`. Use `type: page`.
  - **Link Header-based**: Check for `Link` headers. Use `type: link_header` and `next_url_path: next`.
  - **No Pagination**: Fetch all in a single request.

## 4. Incremental Loading Parameters (Check Per Endpoint!)

Look for ways to fetch only new or updated data since the last run. The `incremental` config always requires `cursor_path` to be defined.

- **Timestamp-based**: identify `start_param` (query filter) and `cursor_path` (the timestamp field in the response item). Note the date format.
- **ID-based / Event-based**: identify `start_param` (query filter) and `cursor_path` (the ID/sequence field in the item).
- **Initial Value**: Determine a safe starting point (e.g. `"2023-01-01T00:00:00Z"`, `0`). Map to `initial_value`.
- **Optional End Param**: Optional `end_param` to match up to a specific record.

## 5. Verification Checklist

Before finalizing the configuration:
1. Verify Base URL format and version.
2. Confirm Authentication method and *all* required parameters/headers.
3. Verify Secret Handling pattern matches how the source is called.
4. **For EACH resource:** Identify its specific pagination strategy (cursor, offset, page, link, none).
5. **For EACH resource:** Extract the correct pagination parameters.
6. **For EACH resource:** Determine if incremental loading is possible and identify its strategy (timestamp, ID, etc.).
7. **For EACH resource:** Extract the correct incremental parameters (`cursor_path`, `initial_value`, `start_param`, etc.).
8. Validate the `data_selector` path for each resource by checking example responses.
9. Check for any required Global Headers AND Resource-Specific Headers.
