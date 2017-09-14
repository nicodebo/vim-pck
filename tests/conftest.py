import pytest
import configparser
import os


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return(tmpdir_factory)


@pytest.fixture()
def write_conf_1(temp_dir, monkeypatch):
    """ A clean configuration file

    1. Write a vimpck configuration file and save it
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'ConfigFile'
    basepath = temp_dir.mktemp(dirtest)
    confpath = basepath.join('config.ini')
    config['SETTING'] = {'pack_path': basepath}
    config['https://github.com/tpope/vim-commentary'] = \
        {'package': 'common',
            'type': 'start'}
    config['https://github.com/tpope/vim-dispatch'] = \
        {'package': 'common',
            'type': 'opt'}
    config['https://github.com/mustache/vim-mustache-handlebars'] = \
        {'package': 'filetype',
            'type': 'start'}
    config['https://github.com/altercation/vim-colors-solarized'] = \
        {'package': 'colors',
            'type': 'start'}
    with open(confpath, 'w') as configfile:
        config.write(configfile)
    monkeypatch.setitem(os.environ, 'VIMPCKRC', str(confpath))
    print(os.environ["VIMPCKRC"])


@pytest.fixture()
def write_conf_2(temp_dir, monkeypatch):
    """ a erroneous configuration file, missing type key

    1. Write a vimpck configuration file
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'install_cmd'
    basepath = temp_dir.mktemp(dirtest)
    confpath = basepath.join('config.ini')
    config['SETTING'] = {'pack_path': basepath}
    config['https://github.com/tpope/vim-commentary'] = \
        {'package': 'common',
            'type': 'start'}
    config['https://github.com/tpope/vim-dispatch'] = \
        {'package': 'common',
            'type': 'opt'}
    config['https://github.com/mustache/vim-mustache-handlebars'] = \
        {'package': 'filetype',
            'type': 'start'}
    config['https://github.com/altercation/vim-colors-solarized'] = \
        {'package': 'colors',
            'type': 'start'}
    config['https://github.com/neomake/neomake'] = \
        {'package': 'linter'}
    with open(confpath, 'w') as configfile:
        config.write(configfile)
    monkeypatch.setitem(os.environ, 'VIMPCKRC', str(confpath))
    print(os.environ["VIMPCKRC"])


@pytest.fixture()
def write_conf_3(temp_dir, monkeypatch):
    """ another erroneous configuration file, wrong package value and missing
    type key for two different entry

    1. Write a vimpck configuration file with an error (/filetype instead of
    filetype for package field of vim-mustache-handlebars and tpop instead of
    tpope in vim-commentary github url)
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'install_cmd'
    basepath = temp_dir.mktemp(dirtest)
    confpath = basepath.join('config.ini')
    config['SETTING'] = {'pack_path': basepath}
    config['https://github.com/tpope/vim-commentary'] = \
        {'package': 'common',
            'type': 'start'}
    config['https://github.com/tpope/vim-dispatch'] = \
        {'package': 'common',
            'type': 'opt'}
    config['https://github.com/mustache/vim-mustache-handlebars'] = \
        {'package': '/filetype',
            'type': 'start'}
    config['https://github.com/altercation/vim-colors-solarized'] = \
        {'package': 'colors',
            'type': 'start'}
    config['https://github.com/neomake/neomake'] = \
        {'package': 'linter'}
    with open(confpath, 'w') as configfile:
        config.write(configfile)
    monkeypatch.setitem(os.environ, 'VIMPCKRC', str(confpath))

@pytest.fixture()
def write_conf_4(temp_dir, monkeypatch):
    """ A clean configuration file with freeze flag

    1. Write a vimpck configuration file and save it
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'ConfigFile'
    basepath = temp_dir.mktemp(dirtest)
    confpath = basepath.join('config.ini')
    config['SETTING'] = {'pack_path': basepath}
    config['https://github.com/tpope/vim-commentary'] = \
        {'package': 'common',
            'type': 'start',
            'freeze': 'true'}
    config['https://github.com/tpope/vim-dispatch'] = \
        {'package': 'common',
            'type': 'opt'}
    config['https://github.com/mustache/vim-mustache-handlebars'] = \
        {'package': 'filetype',
            'type': 'start'}
    config['https://github.com/altercation/vim-colors-solarized'] = \
        {'package': 'colors',
            'type': 'start',
            'freeze': 'false'}
    with open(confpath, 'w') as configfile:
        config.write(configfile)
    monkeypatch.setitem(os.environ, 'VIMPCKRC', str(confpath))
    print(os.environ["VIMPCKRC"])

