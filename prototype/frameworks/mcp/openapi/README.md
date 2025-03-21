## Commands to run
### Install required dependencies
pip install -r requirements.txt

### Run the MCP OpenAPI tool server with your remote OpenAPI spec
python mcp_server.py http://localhost:5001/openapi.json --transport sse