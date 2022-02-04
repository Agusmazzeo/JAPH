from unittest.mock import patch, MagicMock

from typer.testing import CliRunner

from japh.main import app


class TestApp():

    runner = CliRunner()

    @patch("japh.main.CommandExecutor")
    def test_up_command_without_project(
        self,
        mocked_command_executor: MagicMock
    ):
        result = self.runner.invoke(app, ["up", "OpsConsole"])

        assert result.exit_code == 0
        mocked_command_executor.set_up_docker_services.assert_called()
        mocked_command_executor.set_up_shell_services.assert_called()
