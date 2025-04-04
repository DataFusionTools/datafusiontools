.. Data fusion tools documentation master file, created by
   sphinx-quickstart on Wed Nov  3 10:43:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Data fusion tools' documentation!
=============================================
DataFusionTools is a collection of tools that can be used to perform
data fusion tasks. The tools are developed by the consortium of
Deltares, TNO, HKV, Fugro and Geodan.
The tools are developed in the context of the project DigiTwin
Waterkering en Ondergrond.
The tools are developed in Python and are available as a package on
the following `link <https://bitbucket.org/DeltaresGEO/datafusiontools/>`_.

.. | | image:: _static/datafusion.png
   :width: 600
   :align: center

Installation
============

DataFusionTools is a collection of several subpackages or distributions that can be either installed separately or as a whole project. Each subpackage may have a few heavy dependencies attached, therefore it is not recommended to install the whole DataFusionTools package if only a subpackage is needed in a project.

It is recommended to install DataFusionTools in a python virtual environment.
The main purpose of Python virtual environments is to create an isolated environment
for Python projects. This means that each project can have its own dependencies,
regardless of what dependencies every other project has.
This avoids issues with packages dependencies.
The virtual environment should be installed and activated before the installation of DataFusionTools.
To create a virtual environment with python/pip follow this `link <https://docs.python.org/3/library/venv.html>`_.
To create a virtual environment with conda follow this `link <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands>`_.


Installing DataFusionTools as a package
---------------------------------------
To install DataFusionTools, run the following code:

.. code-block::

   pip install git+https://bitbucket.org/DeltaresGEO/datafusiontools.git


Installing a subpackage
-----------------------
To install a specific subpackage (sensitivity in this example), run the following:

.. code-block::

   pip install git+https://bitbucket.org/DeltaresGEO/datafusiontools.git@master#subdirectory=DataFusionTools/sensitivity

The subpackage is then imported in python:

.. code-block:: python

   import datafusiontools.sensitivity

The installable sukpackages are: interpolation, machine_learning, sensitivity, spatial_utils, d_series_parser and visualisation.


Using the package as a developer
================================

To install the package as a developer, you need first to check out the repository. Then, run the following command in the root of the repository:

.. code-block::

   pip install -e .[testing]

This will install the package in editable mode, so that any changes you make to the code will be reflected in the installed package.
The [testing] flag will also install the dependencies needed for running the tests.

Developers
==========

Consortium consists of:

- `Deltares <www.deltares.nl>`_
- `TNO <www.tno.nl>`_
- `Fugro <www.fugro.com/nl>`_
- `Geodan <www.geodan.nl>`_
- `HKV <www.hkv.nl>`_

The Tutorials
==============

This part of the documentation includes the tutorials.

.. toctree::
   :maxdepth: 3

   tutorials/tutorial_neural_network
   tutorials/tutorial_interpolation_2d_slice
   tutorials/tutorial_ahn_surface_line
   tutorials/tutorial_bnn
   tutorials/tutorial_create_dstabilty_file
   tutorials/tutorial_sensitivity_study
   tutorials/tutorial_cluster_2d_surface.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Package documentation
=====================

.. toctree::
   :maxdepth: 3

   DataFusionTools


Bibliography
============

.. toctree::
   :maxdepth: 1

   bibliography
