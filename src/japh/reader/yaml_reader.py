import os
import yaml
from typing import Dict, Optional, List

from japh.utils.exceptions import ProjectNotFound, ConfigNotFound, RepeatedProjectName
from japh.utils.models import Config, Project, Service

class YAMLReader:

    def __init__(self, config_file: Optional[str]=None):
        if not os.path.isfile(config_file):
            raise ConfigNotFound(config_file)
        self.config_data = YAMLReader.load_config(config_file)

    @property
    def docker_files(self):
        return self.config_data.docker_compose_files

    @property
    def projects(self):
        return self.config_data.projects
    
    def get_project_list(self, project) -> List[Project]:
        project_list = list(filter(lambda x: x.title == project, self.config_data.projects))
        project_len = len(project_list)
        if project_len == 0:
            raise ProjectNotFound()
        if project_len > 1:
            raise RepeatedProjectName()
        return project_list

    def get_docker_services_names(
        self,
        project: str,
        service_type: Optional[List[str]] = None,
        service_name: Optional[List[str]] = None
    ) -> str:
        project_list = self.get_project_list(project)
        docker_services = " ".join(
            [
                service.name for service in project_list[0].services
                if service.command is None and 
                (service_type is None or len(service_type)==0 or service.type in service_type) and
                (service_name is None or len(service_name)==0 or service.name in service_name)
            ]
        )

        return docker_services
    
    def get_shell_services(
        self,
        project: str,
        service_type: Optional[List[str]] = None,
        service_name: Optional[List[str]] = None
    ) -> List[Service]:
        project_list = self.get_project_list(project)
        shell_services = [
            service for service in project_list[0].services 
            if service.command is not None and
                (service_type is None or len(service_type)==0 or service.type in service_type) and
                (service_name is None or len(service_name)==0 or service.name in service_name)
        ]
        return shell_services

    @staticmethod
    def load_config(config_file: Optional[str]=None) -> Config:
        file_dir = config_file or os.getenv("CONFIG_FILE", None)
        if file_dir is None:
            raise ConfigNotFound()
        with open(file_dir) as file:
            data = yaml.load(file, Loader=yaml.CLoader)
            return Config.parse_obj(data)