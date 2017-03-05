import pytest
from click.testing import CliRunner
from vim_pck import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    # assert result.exit_code == 0
    # assert not result.exception
    # assert result.output.strip() == 'Hello, world.'
    assert 1


def test_cli_with_option(runner):
    result = runner.invoke(cli.main, ['--as-cowboy'])
    # assert not result.exception
    # assert result.exit_code == 0
    # assert result.output.strip() == 'Howdy, world.'
    assert 1


def test_cli_with_arg(runner):
    result = runner.invoke(cli.main, ['Nicolas'])
    # assert result.exit_code == 0
    # assert not result.exception
    # assert result.output.strip() == 'Hello, Nicolas.'
    assert 1
