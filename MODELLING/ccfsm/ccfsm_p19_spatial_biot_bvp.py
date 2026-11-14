"""CCFSM P19: variational spatial 3D Biot/eigenstrain BVP assembler.
Small-strain linear quasi-static mechanics on user-supplied FE quadrature.
Engineering strain order (xx,yy,zz,2xy,2yz,2xz); stress order
(xx,yy,zz,xy,yz,xz). No mesh generator or fluid time integrator.
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class P19Parameters:
    lame_lambda_pa: float
    shear_modulus_pa: float
    biot_modulus_pa: float
    biot_coefficient: float
    def validate(self):
        v=(self.lame_lambda_pa,self.shear_modulus_pa,self.biot_modulus_pa,self.biot_coefficient)
        if any(not math.isfinite(float(x)) for x in v): raise ValueError("parameters must be finite")
        if self.lame_lambda_pa<0 or self.shear_modulus_pa<=0 or self.biot_modulus_pa<=0 or not 0<=self.biot_coefficient<=1:
            raise ValueError("invalid elastic/Biot parameters")

def _f(x,n):
    x=float(x)
    if not math.isfinite(x): raise ValueError(n+" must be finite")
    return x

def _dot(a,b): return sum(x*y for x,y in zip(a,b))
def _mv(a,x): return [_dot(r,x) for r in a]
def _tr(a): return [list(c) for c in zip(*a)]
def _solve(a,b):
    n=len(b); m=[[float(a[i][j]) for j in range(n)]+[float(b[i])] for i in range(n)]
    scale=max((abs(x) for r in a for x in r),default=1.0)
    for k in range(n):
        q=max(range(k,n),key=lambda i:abs(m[i][k]))
        if abs(m[q][k])<=1e-13*max(1.0,scale): raise ValueError("singular system: insufficient displacement constraints")
        m[k],m[q]=m[q],m[k]; d=m[k][k]
        for j in range(k,n+1): m[k][j]/=d
        for i in range(n):
            if i==k: continue
            z=m[i][k]
            for j in range(k,n+1): m[i][j]-=z*m[k][j]
    return [m[i][n] for i in range(n)]

def p19_solve_spatial_biot_bvp(ndof,quadrature,parameters,dirichlet,boundary_quadrature=(),tolerance=1e-9):
    """Solve weak 3D equilibrium. Volume: B(6,ndof), weight, eigenstrain, fluid_content_increment.
    Boundary: N(3,ndof), outward total traction vector, area weight.
    Dirichlet maps displacement DOF index to prescribed value.
    """
    parameters.validate(); n=int(ndof)
    if n<1 or n!=ndof or not quadrature: raise ValueError("positive ndof and nonempty quadrature required")
    tol=_f(tolerance,"tolerance")
    if tol<=0: raise ValueError("tolerance must be positive")
    la,g,M,a=parameters.lame_lambda_pa,parameters.shear_modulus_pa,parameters.biot_modulus_pa,parameters.biot_coefficient
    C=[[0.0]*6 for _ in range(6)]
    for i in range(3):
        for j in range(3): C[i][j]=la+(2*g if i==j else 0.0)
    for i in range(3,6): C[i][i]=g
    I=[1.,1.,1.,0.,0.,0.]
    K=[[0.]*n for _ in range(n)]; F=[0.]*n; qdata=[]
    for q in quadrature:
        B=q["B"]
        if len(B)!=6 or any(len(r)!=n for r in B): raise ValueError("B must be 6 x ndof")
        B=[[_f(x,"B entry") for x in r] for r in B]
        w=_f(q["weight"],"volume weight"); c=_f(q["eigenstrain"],"eigenstrain")
        z=_f(q["fluid_content_increment"],"fluid content increment")
        if w<=0: raise ValueError("volume weights must be positive")
        src=[x+y for x,y in zip(_mv(C,[c,c,c,0,0,0]),[a*M*z*v for v in I])]
        Bt=_tr(B)
        for i in range(n):
            F[i]+=w*_dot(Bt[i],src)
            for j in range(n):
                col=[B[k][j] for k in range(6)]; cc=_mv(C,col); vol=a*a*M*sum(col[:3])
                cc=[cc[k]+vol*I[k] for k in range(6)]
                K[i][j]+=w*_dot(Bt[i],cc)
        qdata.append((B,w,c,z))
    bdata=[]
    for face in boundary_quadrature:
        N=face["N"]
        if len(N)!=3 or any(len(r)!=n for r in N): raise ValueError("N must be 3 x ndof")
        N=[[_f(x,"N entry") for x in r] for r in N]
        t=[_f(x,"traction") for x in face["traction"]]
        if len(t)!=3: raise ValueError("traction must have three components")
        w=_f(face["weight"],"boundary weight")
        if w<=0: raise ValueError("boundary weights must be positive")
        Nt=_tr(N)
        for i in range(n): F[i]+=w*_dot(Nt[i],t)
        bdata.append((N,t,w))
    fixed={}
    for key,value in dirichlet.items():
        i=int(key)
        if i<0 or i>=n or i in fixed: raise ValueError("invalid Dirichlet DOF")
        fixed[i]=_f(value,"Dirichlet displacement")
    free=[i for i in range(n) if i not in fixed]; u=[0.]*n
    for i,v in fixed.items(): u[i]=v
    if free:
        Kr=[[K[i][j] for j in free] for i in free]
        Fr=[F[i]-sum(K[i][j]*u[j] for j in fixed) for i in free]
        for i,v in zip(free,_solve(Kr,Fr)): u[i]=v
    R=[sum(K[i][j]*u[j] for j in range(n))-F[i] for i in range(n)]
    strains=[]; stresses=[]; pressures=[]; energy=conjugate=0.
    for B,w,c,z in qdata:
        eps=_mv(B,u); tr=sum(eps[:3]); el=[eps[0]-c,eps[1]-c,eps[2]-c,*eps[3:]]
        p=M*(z-a*tr); sig=_mv(C,el); sig=[sig[i]-a*p*I[i] for i in range(6)]
        tre=sum(el[:3]); energy+=w*(.5*la*tre*tre+g*sum(x*x for x in el)+.5*M*(z-a*tr)**2)
        conjugate+=w*(-(3*la+2*g)*tre)
        strains.append(tuple(eps)); stresses.append(tuple(sig)); pressures.append(p)
    work=sum(w*_dot(t,_mv(N,u)) for N,t,w in bdata)
    fr=max((abs(R[i]) for i in free),default=0.); reaction=max((abs(R[i]) for i in fixed),default=0.)
    scale=max(1.,*(abs(x) for x in F),*(abs(x) for x in R))
    return {"displacement_dofs":tuple(u),"strain_voigt_engineering":tuple(strains),
      "stress_voigt_pa":tuple(stresses),"pore_pressure_pa":tuple(pressures),
      "stored_energy_j":energy,"boundary_traction_work_j":work,
      "eigenstrain_conjugate_integral_pa_m3":conjugate,
      "free_dof_equilibrium_residual":fr,"dirichlet_reaction_residual":reaction,
      "free_dof_equilibrium_verified":fr<=tol*scale,
      "quadrature_points":len(qdata),"boundary_quadrature_points":len(bdata)}
