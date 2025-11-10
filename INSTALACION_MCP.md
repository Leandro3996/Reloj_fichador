Option 2: Manual Configuration

Using NPM/PNPM Global Installation:

First, install the package globally:

# Using npm
npm install -g @benborla29/mcp-server-mysql

# Using pnpm
pnpm add -g @benborla29/mcp-server-mysql

Then add the server to Claude Code:

claude mcp add mcp_server_mysql \
  -e MYSQL_HOST="127.0.0.1" \
  -e MYSQL_PORT="3306" \
  -e MYSQL_USER="root" \
  -e MYSQL_PASS="your_password" \
  -e MYSQL_DB="your_database" \
  -e ALLOW_INSERT_OPERATION="false" \
  -e ALLOW_UPDATE_OPERATION="false" \
  -e ALLOW_DELETE_OPERATION="false" \
  -- npx @benborla29/mcp-server-mysql

Using Local Repository (for development):

If you're running from a cloned repository:

claude mcp add mcp_server_mysql \
  -e MYSQL_HOST="127.0.0.1" \
  -e MYSQL_PORT="3306" \
  -e MYSQL_USER="root" \
  -e MYSQL_PASS="your_password" \
  -e MYSQL_DB="your_database" \
  -e ALLOW_INSERT_OPERATION="false" \
  -e ALLOW_UPDATE_OPERATION="false" \
  -e ALLOW_DELETE_OPERATION="false" \
  -e PATH="/path/to/node/bin:/usr/bin:/bin" \
  -e NODE_PATH="/path/to/node/lib/node_modules" \
  -- /path/to/node /full/path/to/mcp-server-mysql/dist/index.js

Replace:

    /path/to/node with your Node.js binary path (find with which node)
    /full/path/to/mcp-server-mysql with the full path to your cloned repository
    Update MySQL credentials to match your environment
