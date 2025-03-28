# Health Check Server

A simple HTTP server that provides health check and status endpoints.

## Requirements

- Python 3.x

## Installation

No additional dependencies are required as this server uses Python's standard library modules.

## Usage

Start the server by running:

```bash
python3 health.py [-p PORT] [-s STATUS_FILE]
```

Options:
- `-p, --port`: Port number to run the server on (default: 3033)
- `-s, --status-file`: Path to the status.json file (default: status.json)

Examples:
```bash
# Run with default settings
python3 health.py

# Run on specific port
python3 health.py -p 3033

# Run with custom status file
python3 health.py -s custom_status.json

# Run with both custom port and status file
python3 health.py -p 3033 -s custom_status.json
```

## Default Status File

The server comes with a default `status.json` file that contains:
```json
{
    "status": "operational",
    "last_updated": "2024-03-28T00:00:00Z",
    "services": {
        "database": "healthy",
        "cache": "healthy",
        "api": "healthy"
    }
}
```

You can modify this file or provide your own status file using the `-s` option.

## Endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: 
  ```json
  {"status": "healthy"}
  ```
- **Status Code**: 200 OK

### Status
- **URL**: `/status`
- **Method**: GET
- **Response**: 
  - Success (200 OK): Contents of the configured status file
  - Error (404 Not Found):
    ```json
    {"error": "Status file not found: <filename>"}
    ```

## Error Handling

- Non-existent endpoints return a 404 status code with "Not found" message
- If the status file is not found, the status endpoint returns a 404 status code

## Notes

- The server binds to `0.0.0.0` to accept connections from any interface
- Make sure the desired port is not in use before starting the server
- The status file path is relative to the directory where you run the server
