# Velero MCP Server

The **Velero MCP Server** is an open-source **Model Context Protocol (MCP)** server that exposes **read-only, safe, structured access** to Velero backup and schedule resources running inside any Kubernetes cluster.

It allows AI agents (ChatGPT, Claude, Cursor, GitHub Copilot, etc.) to:

- 🔍 Inspect **Velero backups**
- 🔄 Inspect **Velero schedules**
- 📄 Generate **Velero Backup YAML manifests**
- 🧩 Access Velero data as **MCP resources**
- 🔐 Safely interact with your cluster in **read-only mode**

This project helps platform engineers automate workflows using AI while ensuring **zero-risk**, **low-privilege**, and **read-only** access to critical cluster configuration.

---

## ⭐ Why This Project Exists

Velero is commonly used for:

- Kubernetes namespace & cluster backups  
- Disaster recovery  
- Cluster migrations  
- Persistent volume snapshot management  

But until now, **no MCP server existed** to expose Velero CRDs to LLM-based tools in a safe, structured way.

This project provides:

- A consistent API for querying Velero  
- Strong typed models  
- Complete read-only safety  
- Guaranteed LLM-friendly output  
- Ready integration with GitOps

---

## 🚀 Features

### 🔧 MCP Tools

#### `list_velero_backups(namespace?: str)`
Returns a list of Velero Backup CRs.

#### `get_velero_backup(name: str, namespace?: str)`
Returns a detailed structured backup object.

#### `list_velero_schedules(namespace?: str)`
Lists Velero Schedule CRs including cron, paused state, and last backup.

#### `generate_velero_backup_yaml(...)`
Generates **read-only YAML** for a Velero `Backup`.

---

## 📦 MCP Resource Endpoints

| Resource               | Description                                   |
|------------------------|-----------------------------------------------|
| `velero://backups`     | All backups in default namespace               |
| `velero://schedules`   | All schedules in default namespace             |

These allow LLMs to explore Velero state without calling tools.

---

## 🏗 Architecture

- Python 3.10+
- MCP (official Model Context Protocol SDK)
- Kubernetes Python Client
- Pydantic models
- Safe, read-only design
- No `kubectl`, no exec, no side effects

Flow:

```
MCP Client → Velero MCP Server → Kubernetes API → Velero CRDs
```

---

## 🔐 Security Model

### Designed to be 100% safe
The server **never**:

- Creates backups  
- Runs restores  
- Deletes backup objects  
- Writes anything to Kubernetes  

Only reads CRDs via the Kubernetes API.

### RBAC Required:
```
get, list on:
- backups.velero.io
- schedules.velero.io
```

---

## 📥 Installation

```bash
git clone https://github.com/YOUR-ORG/velero-mcp-server.git
cd velero-mcp-server

python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install .
```

For development:

```bash
pip install ".[dev]"
```

---

## ⚙️ Configuration

### Environment Variables

| Variable            | Description                         | Default |
|--------------------|-------------------------------------|---------|
| `KUBECONFIG`       | Path to kubeconfig                  | auto    |
| `VELERO_NAMESPACE` | Velero namespace                    | velero |

### K8s auth order:
1. In-cluster ServiceAccount  
2. `$KUBECONFIG`  
3. `~/.kube/config`

---

## ▶️ Running the Server

Start the server in stdio mode (required by MCP):

```bash
python -m velero_mcp_server.server
```

---

## 🧩 Example MCP Client Configuration

### ChatGPT MCP configuration

```json
{
  "mcpServers": {
    "velero-mcp": {
      "command": "python",
      "args": ["-m", "velero_mcp_server.server"],
      "env": {
        "KUBECONFIG": "/path/to/kubeconfig",
        "VELERO_NAMESPACE": "velero"
      }
    }
  }
}
```

### Claude Desktop

```json
"mcpServers": {
  "velero-mcp": {
    "command": "python",
    "args": ["-m", "velero_mcp_server.server"],
    "env": {
      "KUBECONFIG": "/path/to/kubeconfig",
      "VELERO_NAMESPACE": "velero"
    }
  }
}
```

---

## 🧪 Example Usage (AI Agent)

### List failed backups
> “Call `list_velero_backups` and filter phase = Failed.”

### Inspect a backup
> “Use `get_velero_backup` for `prod-full` and tell me included namespaces.”

### Generate a manifest
> “Generate a Velero backup YAML including namespaces `db`, `logging`, TTL=168h.”

Produces:

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: prod-backup
  namespace: velero
spec:
  includedNamespaces:
    - db
    - logging
  ttl: 168h
```

---

## 🛠 Development

Run linters:

```bash
ruff check velero_mcp_server
```

Type-check:

```bash
mypy velero_mcp_server
```

Run tests:

```bash
pytest
```

---

## 🤝 Contributing

We **welcome contributions** of all kinds:

- Add Velero Restore / VolumeSnapshot support  
- Improve error handling  
- Add more MCP resources  
- Add a Helm chart  
- Add logging or metrics  
- Improve documentation  

Read the full **CONTRIBUTING.md**.

---

## 📜 License

This project is licensed under the **MIT License**, allowing:

- Commercial use  
- Private use  
- Modification  
- Distribution  

---

## 🗺 Roadmap

Planned improvements:

- Add support for Restore CRDs  
- Snapshot objects  
- Restore impact analysis  
- Write-enabled mode (behind strict flags)  
- Publish to PyPI  
- Helm chart for cluster deployment  

If you'd like to help shape the direction, please open an issue!