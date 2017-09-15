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


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('plug', required=False, nargs=-1)
# @click.option('--force', '-f', is_flag=True, help='force upgrade')
def upgrade(**kwargs):
    """Upgrade installed package(s)"""
    command.upgrade_cmd(**kwargs)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-r', is_flag=True, help='Remove entry from configuration file')
@click.argument('plug', required=True, nargs=-1)
def rm(**kwargs):
    """Remove specified package(s)"""
    command.remove_cmd(**kwargs)


@click.command()
@click.pass_context
def help(ctx):
    """ Display help message """
    print(ctx.parent.get_help())


@click.command(context_settings=CONTEXT_SETTINGS)
def clean():
    """Remove unused plugins"""
    command.clean_cmd()


main.add_command(install)
main.add_command(ls)
main.add_command(upgrade)
main.add_command(rm)
main.add_command(help)
main.add_command(clean)


if __name__ == '__main__':
    main()
