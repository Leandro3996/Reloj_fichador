
---

## Introducción — ¿Qué es MCP y por qué usarlo?

* MCP (Model Context Protocol) es un protocolo abierto desarrollado por Anthropic que permite que modelos de lenguaje (como Claude) se conecten con herramientas externas, bases de datos, APIs, etc. ([Claude Docs][1])

* En el contexto de bases de datos, un *MCP server* actúa como intermediario: recibe peticiones del agente (Claude), ejecuta consultas a la base de datos (usando permisos adecuados, normalmente en modo de solo lectura) y devuelve los resultados estructurados. ([Claude MCP][2])

* Claude Code (y Claude Desktop) soportan configurar servidores MCP tanto locales como remotos. ([Anthropic][3])

---

## Visión general del flujo

1. Tienes una base de datos PostgreSQL (local o remota).
2. Montas un servidor MCP que se conecta a esa base de datos (usando credenciales, cadena de conexión, etc.).
3. Configuras Claude / Claude Code para usar ese servidor MCP (lo declara en su configuración).
4. Desde Claude, puedes hacer preguntas en lenguaje natural que internamente se transforman en consultas SQL, se ejecutan en el servidor MCP, y los resultados se devuelven para que Claude los procese.

Este flujo asegura que Claude no necesite tener “acceso directo” al motor PostgreSQL, sino que todo pasa por el servidor MCP como capa de mediación y control.

---

## Paso a paso: conectar PostgreSQL con Claude/CODE vía MCP

A continuación tienes un tutorial genérico. Dependiendo de tu sistema operativo, herramientas preferidas (Node.js, Python, Docker, etc.) y permisos, algunos pasos pueden variar.

### Requisitos previos

* PostgreSQL ya funcionando, con usuario, base de datos, permisos adecuados.

* Claude Code / Claude Desktop instalados y funcionando. ([Claude Docs][4])

* Conocimientos básicos de SQL.

* Herramientas para correr un servidor MCP: por ejemplo, Node.js, Python, Docker, etc.

* Posiblemente acceso a red (si la base de datos está en otro host).

### 1. Elegir o montar un servidor MCP para PostgreSQL

Ya existe un **PostgreSQL MCP Server** oficial / de referencia que implementa capacidades de inspección de esquema y ejecución de consultas en modo lectura. ([Claude MCP][2])

Una opción común es usar la implementación del repositorio oficial de MCP servers: [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) (incluye un cascarón para PostgreSQL). ([Claude MCP][2])

También hay guías de la comunidad que describen cómo instalarlo vía npm u otras técnicas. ([Medium][5])

Por ejemplo, un fragmento de guía:

> npm install @modelcontextprotocol/server-postgres
> then run como:
> `npx @modelcontextprotocol/server-postgres postgresql://usuario:contraseña@host:puerto/baseDatos` ([Medium][5])

Este comando arranca el servidor MCP para PostgreSQL conectándose a tu base de datos mediante la cadena de conexión.

### 2. Configurar el servidor MCP

Un servidor MCP debe exponerse de forma que Claude Code lo pueda invocar. En muchos casos, el servidor escucha en un puerto local (por ejemplo, HTTP) o mediante stdin/stdout, dependiendo de la configuración del cliente MCP.

Uno de los ejemplos comunitarios ilustra un servidor hecho con **FastAPI / Python** que actúa como intermediario entre Claude y PostgreSQL:

```python
from fastapi import FastAPI, Request
import psycopg2
# ... configuración de conexión, definición de endpoints MCP
```

(Este ejemplo se ve en una guía de la comunidad) ([Medium][6])

Pero para ambientes más “plug & play”, la implementación oficial en Node.js que viene con el repositorio MCP es más directa. Configuras la cadena de conexión, posiblemente en una variable de entorno (por ejemplo, `DATABASE_URI`), y arrancas el servidor.

Adicionalmente, algunos MCP servers permiten configuraciones como “modo de solo lectura” para proteger la base de datos. ([Medium][5])

### 3. Declarar el MCP server en Claude / Claude Code

Una vez que el servidor MCP está corriendo, debes indicarle a Claude Code que lo utilice. Esto se hace mediante su configuración de MCP.

Ejemplo de estructura en el archivo `mcp.json` o configuración equivalente:

```json
{
  "mcpServers": {
    "postgresql-mcp": {
      "command": "node",
      "args": ["/ruta/al/servidor-postgres-mcp/build/index.js"],
      "disabled": false,
      "alwaysAllow": [],
      "env": {
        "DATABASE_URI": "postgresql://usuario:contraseña@host:puerto/baseDatos"
      }
    }
  }
}
```

En este ejemplo, se arranca el servidor con `node` y se le pasa la ruta al ejecutable del MCP server. Se provee la variable de entorno `DATABASE_URI` con la cadena de conexión.

Luego, Claude Code la leerá y podrá comunicarse con ese servidor para consultas.

Algunos clientes con interfases gráficas (como Claude Desktop) tienen menús o ajustes para “agregar un servidor MCP” desde la configuración. ([Scott Spence][7])
Una fuente menciona que el CLI de Claude tiene un comando tipo `claude mcp add` para guiar la configuración. ([Scott Spence][7])

También debes asegurarte de que el servidor MCP esté **activo** cuando Claude lo intente invocar.

### 4. Conexión remota (opcional)

A partir de junio de 2025, Claude Code agregó soporte para **servidores MCP remotos**, es decir, no tienen que estar en tu máquina local — pueden estar en un servidor accesible mediante URL. ([Anthropic][3])

En ese caso, solo necesitas proporcionar la URL del servidor MCP (y mecanismos de autenticación) en la configuración de Claude. No es necesario que Claude gestione el proceso de arranque local del servidor MCP.

### 5. Probar consultas desde Claude

Una vez todo esté configurado, en Claude puedes hacer algo como:

* “Muéstrame las tablas disponibles en la base de datos.”
* “Haz una consulta: `SELECT nombre, cuenta FROM clientes WHERE region = 'Córdoba'`.”
* “Resume los 5 últimos registros de la tabla ventas.”

Claude internamente consulta el recurso `/schema` (o similar) del MCP server para inspeccionar estructura, luego transforma tu solicitud en SQL, lo envía, recibe resultado y presenta.

Si todo sale bien, verás resultados tabulares o explicaciones generadas por Claude.

### 6. Seguridad y buenas prácticas

* Asegúrate de que el servidor MCP tenga permisos limitados (idealmente solo lectura) para evitar que Claude ejecute operaciones destructivas (DELETE, DROP, etc.).

* Usa conexiones seguras (SSL/TLS) si la base de datos está en un host remoto.

* No almacenes credenciales sensibles en el código: usa variables de entorno o gestión de secretos.

* Revisa el código del servidor MCP para asegurarte que no acepte comandos arbitrarios de shell ni permita inyección peligrosa.

* Hay trabajos de investigación que alertan sobre riesgos de seguridad en MCPs (por ejemplo, que un agente podría abusar de las capacidades del servidor) — conviene auditar. ([arxiv.org][8])

---

## Ejemplo concreto simplificado (con Node.js + Docker)

Para darte algo concreto, aquí va un mini ejemplo usando Docker + Node.js:

**Dockerfile (servidor MCP Postgres):**

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "build/index.js"]
```

**docker-compose.yml**:

```yaml
version: "3"
services:
  mcp-postgres:
    build: .
    environment:
      DATABASE_URI: "postgresql://usuario:contraseña@postgres:5432/mi_bd"
    depends_on:
      - postgres_db
    ports:
      - "4000:4000"  # puerto del servidor MCP

  postgres_db:
    image: postgres:15
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: contraseña
      POSTGRES_DB: mi_bd
    ports:
      - "5432:5432"
```

Luego, en la configuración de Claude / Claude Code apuntas el servidor MCP a `http://<host>:4000` (o como corresponda).

Este tipo de arquitectura permite separar el servidor de base de datos del servidor MCP, y Claude acceder al MCP sin tener que conocer detalles internos del motor PostgreSQL.

---


[1]: https://docs.anthropic.com/en/docs/claude-code/mcp?utm_source=chatgpt.com "Model Context Protocol (MCP) - Anthropic API"
[2]: https://www.claudemcp.com/servers/postgres?utm_source=chatgpt.com "PostgreSQL - Claude MCP Servers"
[3]: https://www.anthropic.com/news/claude-code-remote-mcp?utm_source=chatgpt.com "Remote MCP support in Claude Code - Anthropic"
[4]: https://docs.anthropic.com/en/docs/claude-code/setup?utm_source=chatgpt.com "Set up Claude Code - Anthropic API"
[5]: https://medium.com/towards-agi/how-to-setup-and-use-postgresql-mcp-server-e1c7ad2edc52?utm_source=chatgpt.com "How to Setup and Use PostgreSQL MCP Server - Medium"
[6]: https://medium.com/%40jalajagr/connecting-postgresql-to-claude-desktop-with-mcp-a-step-by-step-guide-c06adae1cab6?utm_source=chatgpt.com "Connecting PostgreSQL to Claude Desktop with MCP: A Step-by ..."
[7]: https://scottspence.com/posts/configuring-mcp-tools-in-claude-code?utm_source=chatgpt.com "Configuring MCP Tools in Claude Code - The Better Way"
[8]: https://arxiv.org/abs/2504.03767?utm_source=chatgpt.com "MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits"
