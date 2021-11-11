from typing import Optional, List
from pydantic import BaseModel


class Service(BaseModel):
    name: str
    type: str
    pre_start: Optional[List[str]] = None
    command: Optional[str] = None
    volume: Optional[str] = None


class Project(BaseModel):
    title: str
    description: str
    services: List[Service]


class Config(BaseModel):
    projects: List[Project]
    docker_compose_files: List[str]

