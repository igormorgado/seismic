"""Setup for Seismic"""

from setuptools import setup, find_packages

#packages=['seismic'],

setup(
    name='seismic',
    version='0.0.1',
    packages = find_packages(),
    install_requires=['numpy', 'zarr'],
    description='Seismic algorithms',
    url='http://github.com/igormorgado/seismic',
    license='GNU/GPLv2',
    python_requires='>=3.5, <4',
    author='Igor Morgado',
    author_email='morgado.igor@gmail.com',
    keywords=['seismic', 'numpy', 'jupyter'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    long_description="""\
Seismic Algorityms
-------------------------------------------------

More description will come."""

)
