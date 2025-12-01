from kubernetes import client, config
from kubernetes.config import ConfigException
from typing import Optional, List
from .models import BackupSummary, ScheduleSummary
VELERO_API_GROUP='velero.io'; VELERO_API_VERSION='v1'
BACKUP_PLURAL='backups'; SCHEDULE_PLURAL='schedules'
def _load():
    try: config.load_incluster_config()
    except: config.load_kube_config()
def _api():
    _load(); return client.CustomObjectsApi()
def _ns(n): return n or "velero"
def list_backups(namespace=None):
    api=_api(); ns=_ns(namespace)
    raw=api.list_namespaced_custom_object(VELERO_API_GROUP,VELERO_API_VERSION,ns,BACKUP_PLURAL)
    out=[]
    for i in raw.get("items",[]):
        m=i.get("metadata",{}); s=i.get("spec",{}); st=i.get("status",{})
        out.append(BackupSummary(
            name=m.get("name",""), namespace=m.get("namespace",ns),
            phase=st.get("phase"), created_at=m.get("creationTimestamp"),
            storage_location=s.get("storageLocation"),
            included_namespaces=s.get("includedNamespaces"),
            excluded_namespaces=s.get("excludedNamespaces"),
            ttl=s.get("ttl"), labels=m.get("labels") or {}
        ))
    return out
def get_backup(name,namespace=None):
    api=_api(); ns=_ns(namespace)
    i=api.get_namespaced_custom_object(VELERO_API_GROUP,VELERO_API_VERSION,ns,BACKUP_PLURAL,name)
    m=i.get("metadata",{}); s=i.get("spec",{}); st=i.get("status",{})
    return BackupSummary(
        name=m.get("name",""), namespace=m.get("namespace",ns),
        phase=st.get("phase"), created_at=m.get("creationTimestamp"),
        storage_location=s.get("storageLocation"),
        included_namespaces=s.get("includedNamespaces"),
        excluded_namespaces=s.get("excludedNamespaces"),
        ttl=s.get("ttl"), labels=m.get("labels") or {}
    )
def list_schedules(namespace=None):
    api=_api(); ns=_ns(namespace)
    raw=api.list_namespaced_custom_object(VELERO_API_GROUP,VELERO_API_VERSION,ns,SCHEDULE_PLURAL)
    out=[]
    for i in raw.get("items",[]):
        m=i.get("metadata",{}); s=i.get("spec",{}); st=i.get("status",{})
        tmpl=s.get("template",{}).get("spec",{})
        last=None
        if isinstance(st.get("lastBackup"),dict):
            last=st["lastBackup"].get("name")
        out.append(ScheduleSummary(
            name=m.get("name",""), namespace=m.get("namespace",ns),
            schedule=s.get("schedule",""),
            template_included_namespaces=tmpl.get("includedNamespaces"),
            template_excluded_namespaces=tmpl.get("excludedNamespaces"),
            last_backup_name=last,
            paused=bool(s.get("paused",False)),
            labels=m.get("labels") or {}
        ))
    return out
