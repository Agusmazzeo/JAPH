#!./venv/bin/python3
from typing import List, Optional

import typer

from japh.reader.yaml_reader import YAMLReader
from japh.executor.executor import CommandExecutor
from japh.utils.exceptions import IncompleteConfigFile, ConfigNotFound

global config

app = typer.Typer(help="Hi Im Just Another Project Handler!")


@app.command()
def up(
    project: str,
    name: Optional[List[str]] = typer.Option(
        help="Services' name to set up", default=None),
    type: Optional[List[str]] = typer.Option(
        help="Services' type to set up", default=None),
    attached: Optional[bool] = typer.Option(
        help="Flag for creating containers attached to shell execution", default=False),
    background: Optional[bool] = typer.Option(
        help="Flag for setting on service's logs", default=False),
    file_dir: Optional[str] = typer.Option(
        help="Config file path", default="config.yaml")
):
    config = YAMLReader(file_dir)
    projects_conf = config.config_data.projects
    if projects_conf is None:
        raise IncompleteConfigFile()

    docker_services_names = config.get_docker_services_names(
        project, service_type=type, service_name=name)
    shell_services = config.get_shell_services(
        project, service_type=type, service_name=name)

    if docker_services_names != "":
        log_string = "\n- "+"\n- ".join(["\n- ".join(
            [service.name for service in shell_services]), "\n- ".join(docker_services_names.split(" "))])
        project = typer.style(project, bold=True)
        log_string = typer.style(log_string, bold=True, fg="green")
        typer.echo(f"Starting services for project {project}: {log_string}\n")
        CommandExecutor.set_up_docker_services(
            docker_compose_files=config.docker_files,
            services=docker_services_names,
            attached=attached,
            background=background
        )
    if shell_services != []:
        CommandExecutor.set_up_shell_services(shell_services)

    if docker_services_names == "" and shell_services == []:
        typer.echo(
            "There are no configured services with given values. Try again!")


@app.command()
def down(
    file_dir: Optional[str] = typer.Option(
        help="Config file path", default="config.yaml")
):
    typer.secho("Shutting down every service... Bye!\n", fg='red')
    config = YAMLReader(file_dir)
    CommandExecutor.kill_docker_services(config.docker_files, all_flag=True)


@app.command()
def restart(
    project: str,
    name: Optional[List[str]] = typer.Option(
        help="Service name to restart", default=None),
    file_dir: Optional[str] = typer.Option(
        help="Config file path", default="config.yaml")
):
    config = YAMLReader(file_dir)
    projects_conf = config.config_data.projects
    if projects_conf == None:
        raise IncompleteConfigFile()

    docker_services_names = "\n- " + \
        "\n- ".join(config.get_docker_services_names(project,
                    service_name=name).split(" "))

    if docker_services_names != "":
        project = typer.style(project, bold=True)
        log_string = typer.style(docker_services_names, bold=True, fg="green")
        typer.echo(
            f"Restarting services for project {project}: {log_string}\n")
        CommandExecutor.restart_docker_services(
            docker_compose_files=config.docker_files,
            services=docker_services_names
        )
    if docker_services_names == "":
        typer.echo(
            "There are no configured services with given values. Try again!")


@app.command()
def recreate(
    project: str,
    name: Optional[List[str]] = typer.Option(
        help="Service name to recreate", default=None),
    file_dir: Optional[str] = typer.Option(
        help="Config file path", default="config.yaml")
):
    config = YAMLReader(file_dir)
    projects_conf = config.config_data.projects
    if projects_conf is None:
        raise IncompleteConfigFile()

    docker_services_names = config.get_docker_services_names(
        project, service_name=name)

    if docker_services_names != "":
        project = typer.style(project, bold=True)
        log_string = typer.style(docker_services_names, bold=True, fg="green")
        typer.echo(
            f"Recreating services for project {project}: {log_string}\n")
        CommandExecutor.kill_docker_services(
            config.docker_files, service_names=name)
        CommandExecutor.set_up_docker_services(
            docker_compose_files=config.docker_files,
            services=docker_services_names
        )
    if docker_services_names == "":
        typer.echo(
            "There are no configured services with given values. Try again!")


@app.command()
def build(
    project: str,
    name: List[str] = typer.Option(help="Service name to build", default=None),
    no_cache: bool = typer.Option(help="Service name to build", default=False),
    file_dir: Optional[str] = typer.Option(
        help="Config file path", default="config.yaml")
):
    config = YAMLReader(file_dir)
    projects_conf = config.config_data.projects
    if projects_conf is None:
        raise IncompleteConfigFile()

    docker_services_names = config.get_docker_services_names(
        project, service_name=name)

    if docker_services_names != "":
        project = typer.style(project, bold=True)
        log_string = typer.style(docker_services_names, bold=True, fg="green")
        typer.echo(f"Building services for project {project}: {log_string}\n")
        CommandExecutor.build_docker_services(
            config.docker_files, service_names=name, no_cache=no_cache)
    if docker_services_names == "":
        typer.secho(
            "There are no configured services with given values. Try again!", fg="yellow")


def start_app():
    try:
        app()
    except ConfigNotFound as ex:
        typer.secho(f"Not config file found as '{ex}'", fg="red")
    except IncompleteConfigFile:
        typer.secho(
            "Given config file is incomplete or has a wrong format...", fg="red")


if __name__ == "__main__":
    start_app()
