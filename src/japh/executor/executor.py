import subprocess
from typing import Dict, List, Optional

from japh.utils.models.config import Service

class CommandExecutor:

    @staticmethod
    def set_up_docker_services(
        docker_compose_files: List[str],
        services: str,
        attached: Optional[bool]=False,
        background: Optional[bool]=False
    ):
        command = "docker-compose -f " + " -f ".join(docker_compose_files)
        action = " up " if attached else " up -d "
        subprocess.call( command + action + services, shell=True)
        if not attached and not background:
            subprocess.call(
                "docker-compose -f " + " -f ".join(docker_compose_files) + " logs -f",
                shell=True, 
            )


    @staticmethod
    def restart_docker_services(
        docker_compose_files: List[str],
        services: str   
    ):
        command = "docker-compose -f " + " -f ".join(docker_compose_files)
        action = " restart "
        subprocess.call( command + action + services, shell=True)

    
    @staticmethod
    def kill_docker_services(
        docker_compose_files: List[str],
    ):
        subprocess.call("docker-compose -f " + " -f ".join(docker_compose_files) + " down", shell=True)

    @staticmethod
    def set_up_shell_services(
        services: List[Service]
    ):
        for service in services:
            pre_start = service.pre_start
            pre_commands = " && ".join(pre_start) + " && " if pre_start is not None else ""
            subprocess.call(pre_commands + service.command, cwd=service.volume, shell=True)
