from unittest.mock import patch, call

from japh.utils.models.config import Service
from executor.executor import CommandExecutor

class TestCommandExecutor:

    @patch("executor.executor.subprocess")
    def test_set_up_docker_services_default(
        self,
        mock_subprocess
    ):
        """Test set_up_docker_services method only with
        default values.
        """

        docker_compose_files = ["docker1", "docker2"]
        services = "test1 test2"

        CommandExecutor.set_up_docker_services(
            docker_compose_files=docker_compose_files,
            services=services
        )

        expected_calls = [
            call.call("docker-compose -f docker1 -f docker2 up -d test1 test2", shell=True),
            call.call("docker-compose -f docker1 -f docker2 logs -f", shell=True)
        ]

        assert mock_subprocess.mock_calls == expected_calls

    @patch("executor.executor.subprocess")
    def test_set_up_docker_services_attached(
        self,
        mock_subprocess
    ):
        """Test set_up_docker_services method only with
        attached attribute.
        """

        docker_compose_files = ["docker1", "docker2"]
        services = "test1 test2"

        CommandExecutor.set_up_docker_services(
            docker_compose_files=docker_compose_files,
            services=services,
            attached=True
        )

        expected_calls = [
            call.call("docker-compose -f docker1 -f docker2 up test1 test2", shell=True),
        ]
        
        assert mock_subprocess.mock_calls == expected_calls

    @patch("executor.executor.subprocess")
    def test_set_up_docker_services_backgroung(
        self,
        mock_subprocess
    ):
        """Test set_up_docker_services method only with
        background attribute.
        """

        docker_compose_files = ["docker1", "docker2"]
        services = "test1 test2"

        CommandExecutor.set_up_docker_services(
            docker_compose_files=docker_compose_files,
            services=services,
            background=True
        )

        expected_calls = [
            call.call("docker-compose -f docker1 -f docker2 up -d test1 test2", shell=True),
        ]
        
        assert mock_subprocess.mock_calls == expected_calls

    @patch("executor.executor.subprocess")
    def test_kill_docker_services(
        self,
        mock_subprocess
    ):
        """Test set_up_docker_services method only with
        default values.
        """

        docker_compose_files = ["docker1", "docker2"]

        CommandExecutor.kill_docker_services(
            docker_compose_files=docker_compose_files
        )

        expected_calls = [
            call.call("docker-compose -f docker1 -f docker2 down", shell=True),
        ]
        
        assert mock_subprocess.mock_calls == expected_calls

    @patch("executor.executor.subprocess")
    def test_set_shell_services(
        self,
        mock_subprocess
    ):
        """Test set_up_docker_services method only with
        background attribute.
        """

        service1 = Service(**{
            "name": "test1",
            "type": "BE",
            "command": "test start",
            "volume": "../vol/"
        })

        service2 = Service(**{
            "name": "test2",
            "type": "UI",
            "pre_start": ["install"],
            "command": "test start2",
            "volume": "../vol2/"
        })

        CommandExecutor.set_up_shell_services(
            services=[service1, service2],
        )

        expected_calls = [
            call.call("test start", cwd="../vol/", shell=True),
            call.call("install && test start2", cwd="../vol2/", shell=True),
        ]
        
        assert mock_subprocess.mock_calls == expected_calls