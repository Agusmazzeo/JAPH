import subprocess
from typing import List, Optional

from japh.utils.models.config import Service


class CommandExecutor:

    @staticmethod
    def set_up_docker_services(
        docker_compose_files: List[str],
        services: str,
        attached: Optional[bool] = False,
        background: Optional[bool] = False
    ):
        command = "docker-compose -f " + " -f ".join(docker_compose_files)
        action = " up " if attached else " up -d "
        subprocess.call(command + action + services, shell=True)
        if not attached and not background:
            subprocess.call(
                "docker-compose -f " +
                " -f ".join(docker_compose_files) + " logs -f",
                shell=True,
            )

    @staticmethod
    def restart_docker_services(
        docker_compose_files: List[str],
        services: str
    ):
        command = "docker-compose -f " + " -f ".join(docker_compose_files)
        action = " restart "
        subprocess.call(command + action + services, shell=True)

    @staticmethod
    def kill_docker_services(
        docker_compose_files: List[str],
        service_names: Optional[List[str]] = None,
        all_flag: Optional[bool] = False
    ):
        if all_flag and service_names is None:
            command = " down"
        else:
            command = " kill " + " ".join(service_names)
        subprocess.call("docker-compose -f " +
                        " -f ".join(docker_compose_files) + command, shell=True)

    @staticmethod
    def build_docker_services(
        docker_compose_files: List[str],
        service_names: Optional[List[str]] = None,
        no_cache: Optional[bool] = False
    ):
        command = " build "
        if no_cache:
            command = command + " --no-cache "

        command = command + " ".join(service_names)
        subprocess.call("docker-compose -f " +
                        " -f ".join(docker_compose_files) + command, shell=True)

    @staticmethod
    def set_up_shell_services(
        services: List[Service]
    ):
        for service in services:
            pre_start = service.pre_start
            pre_commands = " && ".join(
                pre_start) + " && " if pre_start is not None else ""
            subprocess.call(pre_commands + service.command,
                            cwd=service.volume, shell=True)
