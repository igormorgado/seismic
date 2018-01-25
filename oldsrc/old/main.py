"""
Implements the Wave propagation with finite differences

TODO: Boundary conditions **MUST** be added on differentiations, otherwise
      it will collapse after N/2 iterations.
"""

# pylint: disable=locally-disabled,no-value-for-parameter
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

import source
import velocity2d
import wave
import imaging


def main():
    """Main scope"""

    ############################################
    # Simulation invariants
    ############################################
    nx = 1000        # X coord discretization
    nz = 1000        # Z coord discretization
    nt = 3000       # Number of steps
    dx = 5          # Size of x step
    dz = 5          # Size of z step
    dt = 0.001      # Size of t step
    ############################################

    ttime = nt*dt   # Record time (in seconds)
    frames = 1000    # Number of frames to record

    # Creates and clean up the time step pressure field
    # P[0] = Past
    # P[1] = Actual
    # P[2] = Future
    P = np.zeros((3, nx, nz), dtype='float64')

    # Defining the source tuple
    Source = namedtuple('Source', ['x', 'z', 'source_function', 'source_params'])

    # Define the velocity field
    V = velocity2d.parallel_planes(nx, nz)

    # Define the sources
    sources = [
        # Source(int(nx/3), int(nz*0.05), source.gauss, {'cut_frequency':60}),
        Source(int(nx/2), int(nz*0.05), source.gauss, {'cut_frequency':60}),
        # Source(int(nx*2/3), int(nz*0.05), source.gauss, {'cut_frequency':60}),
    ]

    sismogram = []

    # Iterate over time from 0 to 'ttime'  with 'dt' steplength
    for step, t in enumerate(np.arange(0, ttime, dt)):

        # Apply all sources into the velocity field i
        for s in sources:
            period = source.gauss_period(s.source_params['cut_frequency'])
            P[1, s.x, s.z] = s.source_function(t-period, **s.source_params)

        #Apply the propagation inside the Pressure Field
        P[2][2:-2, 2:-2] = (
            wave.discrete_wave_step_2d(P[1], V, dx, dz, dt) +
            wave.discrete_time_step_2d(P)[2:-2, 2:-2]
        )

        #Apply the propagation on borders
        wave.non_reflexive_border_2d(P, V, dx, dz, dt)

        # Adding some images for animation
        if step % (nt/frames) == 0:
            #imaging.savefig(P[2], step, t, dt)
            fname="-{:04d}".format(step)
            np.savez_compressed("data/wavefield-" + fname, P[2])
            sismogram.append(P[2,0])
            #imaging.show_wave(P[2], step, t, dt)
            print("Step {}/{}".format(step, nt))

        # Move time steps
        P[0], P[1] = P[1], P[2]

    np.savez_compressed("data/sismogram", sismogram)

if __name__ == "__main__":
    main()
