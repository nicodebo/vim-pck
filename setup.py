"""
command-line (n)vim package manager
"""
from setuptools import find_packages, setup

dependencies = ['click', 'configobj']

setup(
    name='vim-pck',
    use_scm_version=True,
    url='https://github.com/nicodebo/vim-pck',
    license='MIT',
    author='Nicolas Débonnaire',
    author_email='nico.debo@openmailbox.org',
    description='command-line (n)vim package manager',
    keywords='vim, nvim, neovim, command-line, cli, package',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6',
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'vimpck = vim_pck.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)
