from phaseportrait import PhasePortrait2D

def dF(r, θ, *, μ=0.5,η=0):
    return μ*r*(1 - r*r), 1+η*θ


example = PhasePortrait2D(dF, [-3, 3], Density=2, Polar=True, Title='Limit cycle')
example.add_slider('μ', valinit=0.5)
example.add_slider('η', valinit=0.0)
example.add_nullclines()
example.plot()