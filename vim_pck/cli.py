import click
from vim_pck import command

# enable -h as an help flag
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Vim package manager"""
    pass


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', help='use configuration file')
def install(**kwargs):
    """Install package(s)"""
    command.install_cmd(**kwargs)


main.add_command(install)

if __name__ == '__main__':
    main()
