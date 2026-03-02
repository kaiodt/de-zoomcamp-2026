"""dlt pipeline to ingest NYC Taxi rides data from a REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def taxi_pipeline_rest_api_source():
    """Extract NYC Taxi rides data from the Data Engineering Zoomcamp API.

    This source fetches paginated records of taxi rides, using page-number
    pagination with 1,000 items per page, starting from page 1.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": (
                "https://us-central1-dlthub-analytics.cloudfunctions.net/"
                "data_engineering_zoomcamp_api/"
            ),
            "paginator": {
                "type": "page_number",
                "page_param": "page",
                "base_page": 1,
                "total_path": None,
                "stop_after_empty_page": True,
            }
        },
        "resource_defaults": {
            "write_disposition": "replace",
            "endpoint": {
                "params": {
                    "limit": 1000,
                },
            },
        },
        "resources": [
            {
                "name": "taxi_rides",
                "endpoint": {
                    "path": "taxi_rides"
                }
            }
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    progress="log",
)
if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline_rest_api_source())
    print(load_info)  # noqa: T201
