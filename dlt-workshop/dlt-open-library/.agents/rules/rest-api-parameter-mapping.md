---
trigger: glob
globs: **/*.py
---

## 6. Enhanced Parameter Mapping (API Terminology -> dlt Config)

Map diverse API documentation terms to consistent `dlt` parameters. Identify the API's term first, then find the corresponding `dlt` key.

```yaml
client:
  base_url:
    common_api_terms: ["Base URL", "API Endpoint", "Root URL", "Service URL"]
    dlt_parameter: "client.base_url"
    notes: "Include version path (e.g., /v1/)"
  
  auth:
    api_key_value:
      common_api_terms: ["API Key", "Access Token", "Secret", "Token", "Key"]
      dlt_parameter: "client.auth.api_key"
      notes: "Handled via Secret Handling patterns"
    
    api_key_param_name:
      common_api_terms: ["api_key", "token", "key", "access_token"]
      dlt_parameter: "client.auth.name"
      notes: "Query param name or Header name"
    
    api_key_location:
      common_api_terms: ["Query parameter", "Header"]
      dlt_parameter: "client.auth.location"
      notes: "query or header"
    
    bearer_token:
      common_api_terms: ["Bearer Token", "JWT"]
      dlt_parameter: "client.auth.token"
      notes: "Handled via Secret Handling patterns"

pagination:
  note: "Define per-resource if strategies differ!"
  
  next_cursor_source:
    common_api_terms: ["next_cursor", "next_page", "nextToken", "marker"]
    dlt_parameter: "paginator.cursor_path"
    notes: "JSON path in response"
  
  next_cursor_param:
    common_api_terms: ["cursor", "page_token", "after", "next", "marker"]
    dlt_parameter: "paginator.cursor_param"
    notes: "Query param name to send cursor"
  
  offset_param:
    common_api_terms: ["offset", "skip", "start", "startIndex"]
    dlt_parameter: "paginator.offset_param"
    notes: "Query param name"
  
  page_number_param:
    common_api_terms: ["page", "page_number", "pageNum"]
    dlt_parameter: "paginator.page_param"
    notes: "Query param name"
  
  page_size_param:
    common_api_terms: ["limit", "per_page", "page_size", "count", "maxItems"]
    dlt_parameter: "paginator.limit_param"
    notes: "Query param name"
  
  total_items_source:
    common_api_terms: ["total", "total_count", "total_results", "count"]
    dlt_parameter: "paginator.total_path"
    notes: "Optional JSON path in response"
  
  link_header_relation:
    common_api_terms: ["next", "last"]
    dlt_parameter: "paginator.next_url_path"
    notes: "rel value in Link header"

incremental:
  note: "Define per-resource if strategies differ!"
  
  timestamp_param:
    common_api_terms: ["since", "updated_since", "modified_since", "from"]
    dlt_parameter: "incremental.start_param"
    notes: "Query param name"
  
  timestamp_source:
    common_api_terms: ["updated_at", "modified", "last_updated", "ts"]
    dlt_parameter: "incremental.cursor_path"
    notes: "JSON path in response item"
  
  id_sequence_param:
    common_api_terms: ["since_id", "min_id", "after_id", "sequence"]
    dlt_parameter: "incremental.start_param"
    notes: "Query param name"
  
  id_sequence_source:
    common_api_terms: ["id", "event_id", "sequence_id", "_id"]
    dlt_parameter: "incremental.cursor_path"
    notes: "JSON path in response item"
  
  initial_value:
    common_api_terms: ["N/A"]
    dlt_parameter: "incremental.initial_value"
    notes: "Start value for first run"

data:
  data_array_path:
    common_api_terms: ["data", "results", "items", "records", "entries"]
    dlt_parameter: "endpoint.data_selector"
    notes: "JSON path to the list of items"
```

## 7. Verification Checklist

Before finalizing the configuration:
1.  Verify Base URL format and version.
2.  Confirm Authentication method and *all* required parameters/headers.
3.  Verify Secret Handling pattern matches how the source is called.
4.  **For EACH resource:** Identify its specific pagination strategy (cursor, offset, page, link, none).
5.  **For EACH resource:** Extract the correct pagination parameters (`cursor_path`, `cursor_param`, `offset_param`, `page_param`, `limit_param` etc.) based on its strategy.
6.  **For EACH resource:** Determine if incremental loading is possible and identify its strategy (timestamp, ID, etc.).
7.  **For EACH resource:** Extract the correct incremental parameters (`cursor_path`, `initial_value`, `start_param`, etc.) based on its strategy.
8.  Validate the `data_selector` path for each resource by checking example responses.
9.  Check for any required Global Headers AND Resource-Specific Headers.