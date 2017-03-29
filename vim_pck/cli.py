import click
from vim_pck import command

# enable -h as an help flag
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Vim package manager"""
    pass


@click.command(context_settings=CONTEXT_SETTINGS)
def install(**kwargs):
    """Install package(s)"""
    command.install_cmd(**kwargs)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--start', is_flag=True, help='list autostart packages')
@click.option('--opt', is_flag=True, help='list optional packages')
def ls(**kwargs):
    """List installed package(s)"""
    print(*command.ls_cmd(**kwargs), sep='\n')


main.add_command(install)
main.add_command(ls)


if __name__ == '__main__':
    main()
