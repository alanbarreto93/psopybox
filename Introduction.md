# Introduction #

PyPSO was developed to be a generic complete particle swarm optimization framework written in pure python, the main goals of PyPSO are:

  * Written in pure python, to maximize the cross-platform issue;
  * Easy to use API, the API must be easy for end-user
  * See the evolution, the user can see and interact with the evolution statistics, graphs and etc;
  * Extensible, the API is extensible, the user can create new representations, swarm operators like communicator, topologies and etc.
  * Fast, the design must be optimized for peformance
  * Common features, the framework must implement the common features: topologies like global topology, local topologies. Communicators schemes like Global Communicators, etc.
  * Default - parameters, we must have default operators, settings, etc. in all options
  * Open-source, the source is for everyone, not for only one.

# Requirements #

PyPSO can be executed on **Windows**, **Linux** and **Mac** platforms.

**Note:** On the Mac platform,  the PyPSO 0.1 can't enter on the Interactive Mode.


Pyevolve requires the follow modules:

  * Python 2.5+
  * Optional, for graph plotting:  Matplotlib 0.98.4+
> > The matplotlib  is required to plot the graphs.



# Downloads #

## Windows ##

Installers for Microsoft Windows platform:

  * PyPSO v.0.1 (installer) for Python 2.5
This is an .exe installer for Microsoft Windows XP/Vista

## Linux ##

Installation package for Linux platform:

  * PyPSO  v.0.1 (egg package) for Python 2.5
This is an egg package file

## Mac ##

Installation package for Mac OS platform:

  * PyPSO v.0.1 (.tar package) for Python 2.5
This is the .tar archive compressed with the build script.



# Examples and Source code #

  * PyPSO v.0.1 source code (package)
This is an package with the PyPSO source code
  * Examples for PyPSO v.0.1 (package)
This is an package with the PyPSO examples


# Installation #

You can download the specific PyPSO from the Downloads section, or using the python setup.py.

The installation can be easy done by using the python setup script:

The installation can be easy done by using the python setup.py :

```
  $ python setup.py install
```

This command will automatic install a suitable version of pyPSO, once you have installed, you can test:

```
>>> import pypso
>>> print pypso.__version__
'0.1'
```


# PSO Features #

## Representations ##

  * 1D List

**Note**  It's important to note, that the 1D List can carry any type of python objects or primitives.


# Particle Swarm Optimization Algorithms Literature #
In this section, you will find study material to learn more about PSO Algorithms.

## Books ##
Goldberg, David E (1989), Genetic Algorithms in Search, Optimization and Machine Learning, Kluwer Academic Publishers, Boston, MA.

Goldberg, David E (2002), The Design of Innovation: Lessons from and for Competent Genetic Algorithms, Addison-Wesley, Reading, MA.

Fogel, David B (2006), Evolutionary Computation: Toward a New Philosophy of Machine Intelligence, IEEE Press, Piscataway, NJ. Third Edition

Holland, John H (1975), Adaptation in Natural and Artificial Systems, University of Michigan Press, Ann Arbor

Michalewicz, Zbigniew (1999), Genetic Algorithms + Data Structures = Evolution Programs, Springer-Verlag.

### See also ###
Wikipedia: Genetic Algorithms
The Wikipedia article about Genetic Algorithms.


## Sites ##


# Glossary / Concepts #

**Fitness score**
The fitness score represents the current score of  how good is the individual relative to the swarm in that interaction.
**Evaluation function**
Also called Fitness Function or Objective Function, the evaluation function is the function which evaluates the particle, giving it a fitness score. The objective of this function is to quantify the solutions (individuals, particles)

### See also ###
Wikipedia: Fitness Function
An article talking about the Evaluation function, or the “Fitness Function”.

**Particle Base**
The particle base is the particle which are used as configuration base for all the new replicated particles.

**Interactive mode**
PyPSO have an interactive mode, you can enter in this mode by pressing ESC key before the end of the evolution. When you press ESC, a python environment will be load. In this environment, you have some analysis functions and you can interact with the swarm of particles at the specific iteration.

**Step callback function**
This function, when attached to the PSO Engine (PSO.SimplePSO), will be called every iteration. It receives one parameter, the PSO Engine by itself.