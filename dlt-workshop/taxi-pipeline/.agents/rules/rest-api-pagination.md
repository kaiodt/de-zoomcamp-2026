
# dlt REST API Pagination Configuration Guide

This workflow explains how to configure different pagination strategies for the `dlt` `rest_api` source. Understanding the API's specific pagination method is crucial for correct configuration.

If you are unsure what type of pagination to use due to lack of information from the api, consider curl-ing for responses (you can probably find credentials in secrets if needed)

We will use class based paginators and not declartive.

**Key Principle: Endpoint-Specific Pagination**

While you can set a default paginator at the `client` level, many APIs use *different* pagination methods for different endpoints. Always check the documentation for *each specific endpoint*. Define the `paginator` configuration within that specific resource's `endpoint` section to override the client-level setting.

## DLT RESTClient Paginators Guide

To specify the pagination configuration, use the `paginator` field in the `client` or `endpoint` configurations. You should use a dictionary with a string alias in the `type` field along with the required parameters.

### Available Paginators

#### 1. json_link
Description: Paginator for APIs where the next page's URL is included in the response JSON body (e.g. in a field like "next" or within a "pagination" object).

Parameters:
- `type`: `"json_link"`
- `next_url_path` (str, optional): JSONPath to the key in the response JSON that contains the next page URL.

Example: `next_url_path="pagination.next"`

#### 2. header_link
Description: Paginator for APIs where the next page's URL is provided in an HTTP header (commonly the Link header with rel="next").

Parameters:
- `type`: `"header_link"`
- `links_next_key` (str, optional): The relation key in the Link response header that identifies the next page's URL (Default is `"next"`).

#### 3. offset
Description: Paginator for APIs that use numeric offset/limit parameters in query strings to paginate results.

Parameters:
- `type`: `"offset"`
- `limit` (int, required): Maximum number of items to retrieve per request
- `offset` (int, optional): Starting offset (default 0)
- `offset_param` (str, optional): Query param name for offset value (default `"offset"`)
- `limit_param` (str, optional): Query param name for page size limit (default `"limit"`)
- `total_path` (str or None, optional): JSONPath to the total number of items in response (default `"total"`)
- `stop_after_empty_page` (bool, optional): Whether to stop when an empty page is encountered (default True)

#### 4. page_number
Description: Paginator for APIs that use page number indexing in their queries (e.g. `page=1`, `page=2`).

Parameters:
- `type`: `"page_number"`
- `base_page` (int, optional): Starting page index as expected by API (default 0)
- `page` (int, optional): Initial page number
- `page_param` (str, optional): Query param name for page number (default `"page"`)
- `total_path` (str or None, optional): JSONPath to the total number of pages (or total items) in response (default `"total"`)
- `maximum_page` (int, optional): Maximum page number to request
- `stop_after_empty_page` (bool, optional): Whether to stop when an empty page is encountered (default True)

#### 5. cursor
Description: Paginator for APIs that use a cursor or token in the JSON response to indicate the next page.

Parameters:
- `type`: `"cursor"`
- `cursor_path` (str, optional): JSONPath to the cursor/token in response JSON (defaults to `"cursors.next"`)
- `cursor_param` (str, optional): Name of query parameter to send the cursor in (defaults to `"after"`)

#### 6. single_page
Description: The response will be interpreted as a single-page response, ignoring possible pagination metadata.
