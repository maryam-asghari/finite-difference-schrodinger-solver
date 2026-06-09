"""
Example applications of the finite-difference
Schrödinger solver.

Examples:
1. Infinite square well
2. Harmonic oscillator
3. Convergence analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
os.makedirs("figures", exist_ok=True)
os.makedirs("data", exist_ok=True)


from schrodinger_solver import schrodinger_solver

# ==================================================
# Infinite Square Well
# ==================================================

def box_potential(x):
    """
    Infinite square well potential.

    V(x) = 0 inside the box.
    """ 
    return np.zeros_like(x)

x_box, E_box, psi_box = schrodinger_solver(
    box_potential,
    L = 1,
    N = 400,
    num_states=5
)

print(E_box)


n = np.arange(1,len(E_box)+1)

E_exact_box = (n*np.pi)**2/8



error_rel_box = np.abs((E_box - E_exact_box)/E_exact_box)



df_box = pd.DataFrame({
    "n": n,
    "Numerical": E_box,
    "Exact": E_exact_box,
    "Relative Error": error_rel_box
    })

print()
print("Infinite Square Well")
print(df_box)

df_box.to_csv("data/box_energies.csv", index=False)


plt.figure()

plt.plot(n, error_rel_box, 'o-')

plt.xlabel("n")
plt.ylabel("Relative Error")

plt.title("Infinite Square Well: Relative Energy Error")

plt.grid(True)

plt.savefig("figures/box_error.png",
            dpi=300,
            bbox_inches="tight")




plt.figure()

for i in range(5):
    plt.plot(x_box, psi_box[:, i]+E_box[i], label=f"n={i+1}")

plt.xlabel("x")
plt.ylabel("Energy")
plt.title("Infinite Square Well Eigenfunctions (Offset by Energy)")
plt.legend()




plt.savefig("figures/box_eigenfunctions.png",
            dpi=300,
            bbox_inches="tight")

plt.figure()

for i in range(5):
    plt.plot(x_box, psi_box[:, i], label=f"n={i+1}")
    
plt.title("Infinite Square Well Wavefunctions")
plt.xlabel("x")
plt.ylabel("psi(x)")

plt.grid(True)
plt.legend()

plt.savefig("figures/box_wavefunctions.png",
            dpi=300,
            bbox_inches="tight")
# --------------------------------------------------
# Convergence test
# --------------------------------------------------
#
# The ground-state energy is computed for
# increasing grid resolutions N.
#
# A log-log fit is used to estimate the
# convergence order of the finite-difference
# discretization.
#
# --------------------------------------------------

N_values = [100,200,400,800,1600]

errors_box = []

for N in N_values:

    x, E, psi = schrodinger_solver(
        box_potential,
        L=1,
        N=N,
        num_states = 1
        )

    E_num = E[0]

    E_exact = np.pi**2/8
    
    error = abs(E_num - E_exact)/E_exact

    errors_box.append(error)


logN = np.log(N_values)
logError_box = np.log(errors_box)
 
print(N_values)
print(errors_box) 






slope_box, intercept_box = np.polyfit(
    logN,
    logError_box,
    1
    )


plt.figure()

plt.plot(
    logN,
    logError_box,
    'o-',
    label=f"Slope = {slope_box:.3f}"
    )

plt.legend()
plt.xlabel('log(N)')
plt.ylabel('log(Relative Error)')

plt.title("Infinite Square Well Convergence of Ground-State Energy")

plt.grid(True)
    

print()
print("Infinite Square Well Convergence Test")
print(f"Slope = {slope_box:.3f}")
print(f"Intercept = {intercept_box:.3f}")



plt.savefig("figures/box_convergence.png",
            dpi=300,
            bbox_inches="tight")


# ==================================================
# Harmonic Oscillator
# ==================================================


def harmonic_potential(x):
    """
    Harmonic oscillator potential.

    V(x) = 0.5 x^2
    """
    return 0.5*x**2



x_ho, E_ho, psi_ho = schrodinger_solver(
    harmonic_potential,
    L = 10,
    N = 1000,
    num_states = 10
    )

print(E_ho)


n = np.arange(len(E_ho))

E_exact_ho = n+0.5



error_rel_ho = np.abs((E_ho - E_exact_ho)/E_exact_ho)



df_ho = pd.DataFrame({
    "n": n,
    "Numerical": E_ho,
    "Exact": E_exact_ho,
    "Relative Error": error_rel_ho

    })
print()
print("Harmonic Oscillator")
print(df_ho)

df_ho.to_csv("data/ho_energies.csv", index=False)




plt.figure()

plt.plot(n, error_rel_ho, 'o-')

plt.xlabel("n")
plt.ylabel("Relative Error")

plt.title("Harmonic Oscillator: Relative Energy Error")

plt.grid(True)

plt.savefig("figures/ho_error.png",
            dpi=300,
            bbox_inches="tight")



plt.figure()

for i in range(5):
    plt.plot(x_ho, psi_ho[:, i]+E_ho[i], label=f"n={i}")

plt.xlabel("x")
plt.ylabel("Energy")
plt.title("Harmonic Oscillator Eigenfunctions (Offset by Energy)")

plt.legend()

plt.savefig("figures/ho_eigenfunctions.png",
            dpi=300,
            bbox_inches="tight")




plt.figure()

for i in range(5):
    plt.plot(x_ho, psi_ho[:, i], label=f"n={i}")

plt.title("Harmonic Oscillator Wavefunctions")
plt.xlabel("x")
plt.ylabel("psi(x)")
plt.legend()
plt.grid(True)

plt.savefig("figures/ho_wavefunctions.png",
            dpi=300,
            bbox_inches="tight")


# --------------------------------------------------
# Convergence test
# --------------------------------------------------
#
# The ground-state energy is computed for
# increasing grid resolutions N.
#
# A log-log fit is used to estimate the
# convergence order of the finite-difference
# discretization.
#
# --------------------------------------------------

errors_ho = []

for N in N_values:

    x, E, psi =schrodinger_solver(
        harmonic_potential,
        L=10,
        N=N,
        num_states=1
        )

    E_num = E[0]

    E_exact = 0.5
    
    error = abs(E_num - E_exact)/E_exact

    errors_ho.append(error)


logN = np.log(N_values)
logError_ho = np.log(errors_ho)
 
print(N_values)
print(errors_ho) 





slope_ho, intercept_ho = np.polyfit(logN, logError_ho, 1)

plt.figure()

plt.plot(
    logN,
    logError_ho,
    'o-',
    label=f"Slope = {slope_ho:.3f}"
    )
plt.legend()

plt.xlabel('log(N)')
plt.ylabel('log(Relative Error)')

plt.title("Harmonic Oscillator Convergence of Ground-State Energy")

plt.grid(True)
    


print()
print("Harmonic Oscillator Convergence Test")
print(f"Slope = {slope_ho:.3f}")
print(f"Intercept = {intercept_ho:.3f}")

plt.savefig("figures/ho_convergence.png",
            dpi=300,
            bbox_inches="tight")


plt.show()

