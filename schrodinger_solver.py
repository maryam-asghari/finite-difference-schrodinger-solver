
"""
Finite-difference solver for the one-dimensional
time-independent Schrödinger equation.

Author: Maryam Asghari
Version: 1.0
Date: June 2026
"""

import numpy as np


def schrodinger_solver(V_func, L=5.0, N=400, num_states=5):

    """
    Solve the 1D time-independent Schrödinger equation
    using a finite-difference discretization
    in dimensionless units (ħ = m = 1).

    Parameters
    ----------
    V_func : callable
        Potential function V(x).
    L : float
        Half-width of the computational domain.
    N : int
        Number of interior grid points.
    num_states : int
        Number of eigenstates to return.

    Returns
    -------
    x_internal : ndarray
        Interior grid points.
    energies : ndarray
        Lowest energy eigenvalues.
    wavefunctions : ndarray
        Corresponding normalized eigenfunctions.
    """



    # Create a uniform spatial grid
    x = np.linspace(-L, L, N+2)
    dx = x[1] - x[0]

    # Exclude boundary points.
    # Dirichlet boundary conditions: psi(-L)= psi(L)=0
    x_internal = x[1:-1]
    

    # Finite-difference approximation of d²/dx² 
    D2 = np.zeros((N, N))

    for i in range(N):
        D2[i, i] = -2

    for i in range(N-1):
        D2[i, i+1] = 1
        D2[i+1, i] = 1

    D2 = D2/dx**2

    # Build potential matrix
    V = np.diag(V_func(x_internal))

    # Assemble the Hamiltonian matrix H = T + V
    H = -0.5*D2 + V

    # Compute eigenvalues and eigenvectors
    energies, wavefunctions = np.linalg.eigh(H)

    # Normalize eigenfunctions:
    # Integral |psi(x)|^2 dx = 1
    for i in range(num_states):
        psi = wavefunctions[:, i]

        norm = np.sqrt(np.sum(np.abs(psi)**2)*dx)

        wavefunctions[:, i] = psi / norm

    return x_internal, energies[:num_states], wavefunctions[:, :num_states]

