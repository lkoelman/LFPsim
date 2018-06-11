"""
A setuptools based setup module.

USAGE
-----

Install editable version (symlink to this directory):

    >>> python setup.py develop

Or, equivalently:

    >>> pip install -e path_to_repository

Build NMODL files:

    >>> python setup.py build
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# Custom build steps. You can either inherit from the base class 
# distutils.cmd.Command or from one of the built-in classes: 
# distutils.command.build<''/'_clib'/'_ext'/'_py'/'_scripts'>
from distutils.command.build import build as BuildCommand
# from distutils.cmd import Command as BuildCommand

# To use a consistent encoding
from codecs import open
from os import path
import os
import subprocess

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme_contents = f.read()


BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Build NMODL mechanisms
nmodl_mechanism_dirs = [
    '.'
]

class Build_NMODL(BuildCommand):
    """
    Try to compile NEURON NMODL mechanisms.
    """

    description = 'compile NEURON NMODL source files'


    def run(self):
        """
        Run our custom build step
        """

        BuildCommand.run(self)

        nrnivmodl = self._find_executable("nrnivmodl")
        
        if nrnivmodl:
            print("nrnivmodl found at", nrnivmodl)

            # Build mechanism files
            for mech_dir in nmodl_mechanism_dirs:
                # run `nrnivmodl` on our directory
                result, stdout = self._run_sys_command(nrnivmodl, os.path.join(
                    BASEDIR, mech_dir))
            
                if result != 0:
                    print("Unable to compile NMODL files in {dir}. Output was:\n"
                          "\t{output}".format(dir=mech_dir, output=stdout))
                else:
                    print("Successfully compiled NMODL files in {}.".format(mech_dir))
        
        else:
            print("Unable to find nrnivmodl. "
                  "You will have to compile NEURON .mod files manually.")


    def _find_executable(self, command):
        """
        Try to find an executable file.
        """
        path = os.environ.get("PATH", "").split(os.pathsep)
        cmd = ''
        for dir_name in path:
            abs_name = os.path.abspath(os.path.normpath(os.path.join(dir_name, command)))
            if os.path.isfile(abs_name):
                cmd = abs_name
                break
        return cmd


    def _run_sys_command(self, path, working_directory):
        p = subprocess.Popen(path, shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True,
                             close_fds=True, cwd=working_directory)
        result = p.wait()
        stdout = p.stdout.readlines()
        return result, stdout


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    name='LFPsim', 
    version='0.1.0',

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description=('Simulation scripts to compute Local Field Potentials (LFP) '
                 'of cable compartmental models implemented with NEURON'),
    long_description=readme_contents,  # Optional
    url='https://github.com/lkoelman/LFPsim',  # Optional
    author='Harilal Parasuram, Shyam Diwakar, Lucas Koelman',
    author_email='harilalp@am.amrita.edu, shyam@amrita.edu, lucas.koelman@ucdconnect.ie', 
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Neuroscience',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU Lesser General Public '
        'License v3 (LGPLv3)',
        
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',

        'Operating System :: POSIX',
        'Natural Language :: English',
    ],
    keywords='computational neuroscience simulation neuron',

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    # packages=['lfpsim'],
    packages=find_packages(exclude=['LFP_traces']),

    # dependencies installed automatically by Pip
    # install_requires=[ 'numpy'],

    # Additional dependencies installed using the "extras" syntax, for example:
    # `pip install myproject[dev]`
    # extras_require={'dev': ['nose']},

    # Extra build steps defined as subclasses of distutils.cmd.Command:
    # These are invoked as `python setup.py <key>`
    cmdclass={'build_mechs': Build_NMODL},

    project_urls={  # Optional
        'Lab Website': 'www.amrita.edu/compneuro',
        'University Website': 'www.amrita.edu',
        'Source': 'https://github.com/lkoelman/LFPsim/',
        # 'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    },
)
