from mcp.server.fastmcp import FastMCP, ToolError
import json
from typing import Optional, List
from .kube import list_backups,get_backup,list_schedules
from .models import BackupSummary,ScheduleSummary
mcp=FastMCP('velero-mcp-server','Velero MCP Server')
@mcp.tool
def list_velero_backups(namespace:Optional[str]=None)->List[BackupSummary]:
    try: return list_backups(namespace)
    except Exception as e: raise ToolError(str(e))
@mcp.tool
def get_velero_backup(name:str,namespace:Optional[str]=None)->BackupSummary:
    try: return get_backup(name,namespace)
    except Exception as e: raise ToolError(str(e))
@mcp.tool
def list_velero_schedules(namespace:Optional[str]=None)->List[ScheduleSummary]:
    try: return list_schedules(namespace)
    except Exception as e: raise ToolError(str(e))
@mcp.tool
def generate_velero_backup_yaml(name:str,included_namespaces=None,excluded_namespaces=None,
                                storage_location=None,ttl=None,velero_namespace=None)->str:
    ns=velero_namespace or "velero"; spec={}
    if included_namespaces: spec["includedNamespaces"]=included_namespaces
    if excluded_namespaces: spec["excludedNamespaces"]=excluded_namespaces
    if storage_location: spec["storageLocation"]=storage_location
    if ttl: spec["ttl"]=ttl
    return json.dumps({
        "apiVersion":"velero.io/v1","kind":"Backup",
        "metadata":{"name":name,"namespace":ns},"spec":spec
    },indent=2)
@mcp.resource("velero://backups")
def r1(): return list_backups()
@mcp.resource("velero://schedules")
def r2(): return list_schedules()
def main(): mcp.run("stdio")
if __name__=='__main__': main()
