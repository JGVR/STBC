import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    atlas_admin_user: str
    atlas_admin_pw: str
    atlas_conn_str: str
    atlas_db_name: str
    atlas_collection_name: str

config = Config(
    atlas_admin_user=os.getenv("ATLAS_ADMIN_USER"),
    atlas_admin_pw=os.getenv("ATLAS_ADMIN_PW"),
    atlas_conn_str=os.getenv("ATLAS_CONN_STR"),
    atlas_db_name=os.getenv("ATLAS_DB_NAME"),
    atlas_collection_name=os.getenv("ATLAS_COLLECTION_NAME")
)
