"""CCFSM v0.3: bridge/morphology/eigenstress states for natural syneresis only."""
from dataclasses import dataclass
import math

def pos(x, name):
    x=float(x)
    if not math.isfinite(x) or x<=0: raise ValueError(f"{name} must be positive and finite")
    return x

@dataclass(frozen=True)
class CCFSMV03Parameters:
    bridge_density_infinity_mol_m3: float
    bridge_formation_rate_h: float
    fractal_dimension_initial: float
    fractal_dimension_increment: float
    contact_number_initial: float
    contact_number_increment: float
    morphology_rate_h: float
    bridge_contraction_volume_m3_mol: float
    stress_relaxation_rate_h: float
    hydraulic_rate_h: float
    natural_accessibility: float = 1.0
    def __post_init__(self):
        for n in ("bridge_density_infinity_mol_m3","bridge_formation_rate_h","morphology_rate_h","bridge_contraction_volume_m3_mol","stress_relaxation_rate_h","hydraulic_rate_h"):
            pos(getattr(self,n),n)
        if self.fractal_dimension_initial<=0 or self.fractal_dimension_initial+self.fractal_dimension_increment<=0: raise ValueError("fractal dimension must remain positive")
        if self.contact_number_initial<0 or self.contact_number_initial+self.contact_number_increment<0: raise ValueError("contact number must remain nonnegative")
        if not 0<self.natural_accessibility<=1: raise ValueError("natural_accessibility must lie in (0,1]")

@dataclass(frozen=True)
class CCFSMV03State:
    time_h: float
    bridge_density_mol_m3: float
    fractal_dimension: float
    contact_number: float
    residual_eigenstress_contraction: float
    relaxed_contraction: float
    intrinsic_shrinkage_potential: float
    observed_shrinkage: float

def _rhs(y,p):
    B,Df,z,sigma,eps,S=y
    bdot=p.bridge_formation_rate_h*(p.bridge_density_infinity_mol_m3-B)
    f=B/p.bridge_density_infinity_mol_m3
    Dfeq=p.fractal_dimension_initial+p.fractal_dimension_increment*f
    zeq=p.contact_number_initial+p.contact_number_increment*f
    chi_dot=p.bridge_contraction_volume_m3_mol*bdot
    dsigma=chi_dot-p.stress_relaxation_rate_h*sigma
    deps=p.stress_relaxation_rate_h*sigma
    q=-math.expm1(-(sigma+eps))
    dS=p.hydraulic_rate_h*(p.natural_accessibility*q-S)
    return (bdot,p.morphology_rate_h*(Dfeq-Df),p.morphology_rate_h*(zeq-z),dsigma,deps,dS)

def _rk4(y,h,p):
    f1=_rhs(y,p)
    f2=_rhs(tuple(a+h*b/2 for a,b in zip(y,f1)),p)
    f3=_rhs(tuple(a+h*b/2 for a,b in zip(y,f2)),p)
    f4=_rhs(tuple(a+h*b for a,b in zip(y,f3)),p)
    return tuple(a+h*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,f1,f2,f3,f4))

def simulate_natural_syneresis_v03(parameters,duration_h,time_step_h,
        initial_bridge_density_mol_m3=0.0,initial_fractal_dimension=None,
        initial_contact_number=None,initial_residual_eigenstress_contraction=0.0,
        initial_relaxed_contraction=0.0,initial_observed_shrinkage=0.0):
    """Integrate the natural-only v0.3 ODE using explicit RK4."""
    p=parameters
    if not isinstance(p,CCFSMV03Parameters): raise TypeError("parameters must be CCFSMV03Parameters")
    duration=float(duration_h); hmax=pos(time_step_h,"time_step_h")
    if not math.isfinite(duration) or duration<0: raise ValueError("duration_h must be finite and nonnegative")
    B=float(initial_bridge_density_mol_m3); Df=p.fractal_dimension_initial if initial_fractal_dimension is None else float(initial_fractal_dimension)
    z=p.contact_number_initial if initial_contact_number is None else float(initial_contact_number)
    sigma=float(initial_residual_eigenstress_contraction); eps=float(initial_relaxed_contraction); S=float(initial_observed_shrinkage)
    if not 0<=B<=p.bridge_density_infinity_mol_m3 or Df<=0 or z<0 or sigma<0 or eps<0: raise ValueError("inadmissible initial state")
    q=-math.expm1(-(sigma+eps))
    if not 0<=S<=p.natural_accessibility*q+1e-12: raise ValueError("initial S exceeds natural accessible contraction")
    y=(B,Df,z,sigma,eps,S); out=[]
    def save(t,v):
        b,df,cn,sg,rl,sh=v
        out.append(CCFSMV03State(t,b,df,cn,sg,rl,-math.expm1(-(sg+rl)),sh))
    t=0.0; save(t,y)
    while t<duration:
        h=min(hmax,duration-t); y=_rk4(y,h,p); t+=h
        B,Df,z,sigma,eps,S=y
        if B < -1e-10 or B>p.bridge_density_infinity_mol_m3+1e-8 or min(sigma,eps,S)<-1e-10:
            raise ArithmeticError("state left admissible region; reduce time_step_h")
        y=(min(max(B,0.0),p.bridge_density_infinity_mol_m3),Df,z,max(sigma,0.0),max(eps,0.0),max(S,0.0))
        save(t,y)
    return out

def hydraulic_rate_from_measured_properties_h(viscosity_pa_s,drainage_length_m,permeability_m2,effective_modulus_pa,geometry_factor=1.0):
    """Natural first-mode rate 3600*C*kappa*K/(mu*L^2), in h^-1."""
    mu=pos(viscosity_pa_s,"viscosity_pa_s"); L=pos(drainage_length_m,"drainage_length_m")
    k=pos(permeability_m2,"permeability_m2"); K=pos(effective_modulus_pa,"effective_modulus_pa"); C=pos(geometry_factor,"geometry_factor")
    return 3600*C*k*K/(mu*L*L)
