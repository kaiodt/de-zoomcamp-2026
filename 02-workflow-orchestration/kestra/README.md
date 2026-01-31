# Kestra Local Setup

This directory contains the configuration to run Kestra locally using Docker Compose, including integration with PostgreSQL, pgAdmin, and Google Gemini AI.


## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) installed.
- A Google Cloud Platform (GCP) account and a Service Account with necessary permissions.
- A Google AI Studio API Key for Gemini integration.


## Setup Instructions

### Configure Environment Variables

1.  Copy the `.env.example` file to a new file named `.env`:

    ```bash
    cp .env.example .env
    ```

2.  Open the `.env` file and update the variables with your information.


### GCP Service Account Credentials

1.  Obtain your GCP Service Account credentials in JSON format.

2.  Save it as `service-account.json` in this directory.

3.  Encode the JSON file to Base64:

    ```bash
    base64 -i service-account.json
    ```

4.  Copy the resulting Base64 string and paste it into the `SECRET_GCP_SERVICE_ACCOUNT` variable in your `.env` file.


### 3. Google Gemini API Key

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).

2.  Create a new API Key.

3.  Add the key to the `GEMINI_API_KEY` variable in your `.env` file.


### 4. Run Kestra

Start the Kestra stack using Docker Compose:

```bash
docker compose up -d
```

This will start:

- **Kestra**: The orchestration engine (accessible at [http://localhost:8080](http://localhost:8080)).

- **Kestra PostgreSQL**: Used by Kestra for internal storage.

- **PostgreSQL**: Used as a sample destination database.

- **pgAdmin**: Database management tool (accessible at [http://localhost:8085](http://localhost:8085)).


## Flows

The flows used in the lessons can be found in the `../flows` directory. You can import these YAML files directly into Kestra.
