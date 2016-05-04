# penning
A 3D visualization of a charged ion's trajectory inside an ideal
Penning Trap (based on [TITAN](http://titan.triumf.ca/) of TRIUMF).
This program was created as part of a project for
[UBC Undergraduate Research Organization](http://www.uroubc.ca/)

**Mentor**: Brian Kootte (TITAN Group at Triumf)  
**Group**: Dilyn Fullerton, Shiv Mittal, and Michael Stone

See  https://youtu.be/qSwObWUZUB4 for the program in action

### DESCRIPTION:

Penning Traps are a type of precision mass spectrometer used to
measure ions in very brief periods of time. This makes the penning
trap highly useful when measuring masses of short-lived ions produced
by a particle accelerator such as TRIUMF. These measurements provide a
means of testing the nuclear shell model and the astrophysical
nucleosynthesis of heavy elements [1]. Inside Penning traps, ions are
trapped by a superimposed axial magnetic field and quadrupole electric
potential. The trajectory the ion follows is known as an epitrochoid.
Using vPython, we created a customizable 3D visualization of an ion
following such a trajectory using parametric equations. It depicts the
motion of a particle inside an ideal Penning trap with the
specifications of TITAN at TRIUMF.

### ABOUT THE PROGRAM:

* Designed entirely in Python 2 with visual library extension
([vPython](http://www.vpython.org/))
* Renders a 3-D animation of a charged particle with given initial
position and velocity inside a Penning Trap
* Assumes ideal Penning Trap (i.e. Ideal electric, magnetic fields
and perfect vacuum)
* Loops according to a time step, producing the particle’s position
based
on parametric equations and parameters determined from initial conditions
* Simple class structures allow for easy creation of arbitrary ions,
penning trap parameters, and setups for use in the animation

### SOURCES:

[1] A. Chaudhuri, C. Andreoiu, M. Brodeur, T. Brunner, U. Chowdhury, S. Ettenauer, A. T. Gallant, A. Grossheim, G. Gwinner, R. Klawitter, A. A. Kwiatkowski, K. G. Leach, A. Lennarz, D. Lunney, T. D. Macdonald, R. Ringle, B. E. Schultz, V. V. Simon, M. C. Simon, J. Dilling “TITAN: an ion trap for accurate mass measurements of ms-half-life nuclides” Applied Physics B 99-105 (Jan 2014)
[2] V. V. Simon, T. Brunner, U. Chowdhury, B. Eberhardt, S. Ettenauer, A. T. Gallant, E. Mané, M. C. Simon, P. Delheij, M. R. Pearson, G. Audi, G. Gwinner, D. Lunney, H. Schatz, and J. Dilling “Penning-trap mass spectrometry of highly charged, neutron-rich Rb and Sr isotopes in the vicinity of A≈100” Phys. Rev. C 85 (2012)
[3] K. Blaum, Yu. N. Novikov & G. Werth “Penning traps as a versatile tool for precise experiments in fundamental physics” Contemporary Physics 51 149-175 (2010)
