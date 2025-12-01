from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
class BackupSummary(BaseModel):
    name:str; namespace:str; phase:Optional[str]; created_at:Optional[datetime]
    storage_location:Optional[str]; included_namespaces:Optional[List[str]]
    excluded_namespaces:Optional[List[str]]; ttl:Optional[str]; labels:Dict[str,str]={}
class ScheduleSummary(BaseModel):
    name:str; namespace:str; schedule:str
    template_included_namespaces:Optional[List[str]]
    template_excluded_namespaces:Optional[List[str]]
    last_backup_name:Optional[str]; paused:bool=False; labels:Dict[str,str]={}
