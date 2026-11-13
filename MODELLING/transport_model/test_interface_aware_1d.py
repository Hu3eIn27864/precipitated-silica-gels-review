#!/usr/bin/env python3
"""Verification for exact interface-aware storage and hydraulic resistance."""
import math
import unittest
from interface_aware_1d import solve_interface_aware
from layered_reference import two_layer_mean_pressure_ratio, two_layer_eigenvalues
from multilayer_reference import multilayer_eigenvalues


class InterfaceAwareTests(unittest.TestCase):
    def test_uniform_material_matches_homogeneous_reference(self):
        r=solve_interface_aware([0.0,1.0],[1.0],[1.0],160,1.0,1e-5,200)
        exact=(8.0/math.pi**2)*sum(math.exp(-(2*k+1)**2*math.pi**2*0.002)/(2*k+1)**2 for k in range(500))
        self.assertAlmostEqual(r["mean_pressure_pa"][-1],exact,delta=2e-4)

    def test_off_grid_interface_matches_fixed_interface_series(self):
        a=0.37; L=1.0; t=0.005
        exact=two_layer_mean_pressure_ratio(t,1.0,1.0,2.0,0.15,L,a,180)
        errors=[]
        for n in (40,80,160):
            r=solve_interface_aware([0.0,a,L],[1.0,2.0],[1.0,0.15],
                                    n,L,2e-6,round(t/2e-6))
            errors.append(abs(r["mean_pressure_pa"][-1]-exact))
        self.assertLess(errors[1],errors[0])
        self.assertLess(errors[2],errors[1])
        self.assertLess(errors[-1],8e-4)

    def test_exact_cell_storage_and_crossed_face_resistance(self):
        # Interface x=.37 cuts the cell [0.35,.40] and the centre-to-centre
        # segment [0.3625,.3875]. Both integrals are exact.
        r=solve_interface_aware([0,.37,1],[1,2],[1,.1],40,1,1e-4,1)
        cap=r["cell_capacity_pa_inv_m"]
        self.assertAlmostEqual(cap[14],.02*1.0 + .005*2.0,places=14)
        resistance=.0075/1.0 + .0175/.1
        self.assertAlmostEqual(r["face_conductance_m_pa_s"][15],1/resistance,places=12)

    def test_global_conservation_and_positive_solution(self):
        r=solve_interface_aware([0,.37,.72,1],[1,2,.7],[1,.15,.6],
                                73,1,1e-5,100)
        self.assertLess(max(abs(v) for v in r["balance_residual_m"][1:]),2e-12)
        self.assertTrue(all(v>=0 for row in r["profiles_pa"] for v in row))
        self.assertTrue(all(b<a for a,b in zip(r["mean_pressure_pa"],r["mean_pressure_pa"][1:])))


    def test_off_grid_nonzero_flux_eigenmode_full_profile(self):
        # Exact eigenmode: continuous pressure and nonzero continuous flux at x=.37.
        a=0.37; L=1.0; t=0.005
        sigma=two_layer_eigenvalues(1.0,1.0,2.0,0.15,L,a,1)[0]
        k1=math.sqrt(sigma)
        k2=math.sqrt(sigma*2.0/0.15)
        b=L-a
        amp_left=math.sin(k2*b)
        amp_right=math.sin(k1*a)
        def mode(x):
            return (amp_left*math.sin(k1*x) if x <= a
                    else amp_right*math.sin(k2*(L-x)))
        p_left=amp_left*math.sin(k1*a)
        p_right=amp_right*math.sin(k2*b)
        q_left=amp_left*k1*math.cos(k1*a)
        q_right=-0.15*amp_right*k2*math.cos(k2*b)
        self.assertAlmostEqual(p_left,p_right,places=11)
        self.assertAlmostEqual(q_left,q_right,places=10)
        self.assertGreater(abs(q_left),0.1)
        errors=[]
        for n in (40,80,160):
            dx=L/n
            steps=round(t/(0.25*dx*dx))
            dt=t/steps
            centres=[(i+0.5)*dx for i in range(n)]
            initial=[mode(x) for x in centres]
            r=solve_interface_aware([0.0,a,L],[1.0,2.0],[1.0,0.15],
                                    n,L,dt,steps,
                                    initial_pressure_profile_pa=initial)
            numerical=r["profiles_pa"][-1]
            exact=[math.exp(-sigma*t)*mode(x) for x in centres]
            errors.append(math.sqrt(sum((u-v)**2 for u,v in zip(numerical,exact))/n))
        self.assertLess(errors[1],errors[0])
        self.assertLess(errors[2],errors[1])
        self.assertLess(errors[-1],2e-4)


    def test_three_layer_contact_resistance_slows_drainage_and_conserves(self):
        args=([0.0,0.23,0.71,1.0],[1.0,2.0,0.7],[1.0,0.15,0.6])
        plain=solve_interface_aware(*args,80,1.0,2e-5,100)
        contacted=solve_interface_aware(*args,80,1.0,2e-5,100,
                                         interface_contact_resistance_pa_s_m=[0.03,0.08])
        self.assertGreater(contacted["mean_pressure_pa"][-1],
                           plain["mean_pressure_pa"][-1])
        self.assertLess(max(abs(v) for v in contacted["balance_residual_m"][1:]),2e-12)
        self.assertTrue(all(v>=0 for row in contacted["profiles_pa"] for v in row))
        # Both interfaces lie strictly between cell centres; the exact series
        # resistance on the corresponding faces includes each contact jump.
        # Each physical interface is represented by a co-located minus/plus
        # trace pair, with exactly the prescribed contact conductance.
        for interface,rc in zip(args[0][1:-1],[0.03,0.08]):
            j=next(j for j in range(len(contacted["node_coordinates_m"])-1)
                   if contacted["node_coordinates_m"][j]==interface
                   and contacted["node_coordinates_m"][j+1]==interface)
            self.assertEqual(contacted["node_sides"][j:j+2],["minus","plus"])
            self.assertAlmostEqual(contacted["face_conductance_m_pa_s"][j+1],1.0/rc,places=12)


    def test_three_layer_contact_eigenmode_full_profile(self):
        boundaries=[0.0,0.23,0.71,1.0]
        storage=[1.0,2.0,0.7]
        mobility=[1.0,0.15,0.6]
        contacts=[0.03,0.08]
        widths=[b-a for a,b in zip(boundaries,boundaries[1:])]
        sigma=multilayer_eigenvalues(storage,mobility,widths,1,contacts)[0]
        wave=math.sqrt(sigma)
        def state_in_layer(p0,q0,si,li,z):
            k=wave*math.sqrt(si/li)
            return (p0*math.cos(k*z)+q0*math.sin(k*z)/(li*k),
                    -li*k*p0*math.sin(k*z)+q0*math.cos(k*z))
        def exact_mode(x):
            p,q=0.0,1.0
            for i,(left,right) in enumerate(zip(boundaries,boundaries[1:])):
                if x <= right:
                    return state_in_layer(p,q,storage[i],mobility[i],x-left)[0]
                p,q=state_in_layer(p,q,storage[i],mobility[i],right-left)
                if i < len(contacts):
                    p += contacts[i]*q
            raise AssertionError("coordinate outside slab")
        p,q=0.0,1.0
        for i,width in enumerate(widths[:-1]):
            p_left,q_left=state_in_layer(p,q,storage[i],mobility[i],width)
            p_right=p_left+contacts[i]*q_left
            self.assertAlmostEqual(p_right-p_left,contacts[i]*q_left,places=12)
            self.assertTrue(math.isfinite(q_left))
            p,q=p_right,q_left
        self.assertAlmostEqual(exact_mode(1.0),0.0,delta=2e-10)
        errors=[]
        for n in (40,80,160):
            dx=1.0/n
            steps=round(0.002/(0.1*dx*dx))
            dt=0.002/steps
            centres=[(i+0.5)*dx for i in range(n)]
            initial=[exact_mode(x) for x in centres]
            result=solve_interface_aware(
                boundaries,storage,mobility,n,1.0,dt,steps,
                initial_pressure_profile_pa=initial,
                interface_contact_resistance_pa_s_m=contacts)
            numerical=result["profiles_pa"][-1]
            exact=[math.exp(-sigma*0.002)*exact_mode(x) for x in centres]
            errors.append(math.sqrt(sum((u-v)**2 for u,v in zip(numerical,exact))/n))
        self.assertLess(errors[1],errors[0])
        self.assertLess(errors[2],errors[1])
        self.assertLess(errors[-1],5e-4)

    def test_contact_zero_limit_and_invalid_contact_geometry(self):
        base=solve_interface_aware([0,.37,1],[1,2],[1,.15],40,1,1e-5,10)
        zero=solve_interface_aware([0,.37,1],[1,2],[1,.15],40,1,1e-5,10,
                                   interface_contact_resistance_pa_s_m=[0.0])
        self.assertEqual(base["profiles_pa"],zero["profiles_pa"])
        with self.assertRaises(ValueError):
            solve_interface_aware([0,.37,1],[1,2],[1,.15],40,1,1e-5,10,
                                   interface_contact_resistance_pa_s_m=[-1.0])
        # x=.3625 is exactly a cell centre for N=40. The new formulation
        # represents it by two independent traces instead of rejecting it.
        centred=solve_interface_aware([0,.3625,1],[1,2],[1,.15],40,1,1e-5,5000,
                                      interface_contact_resistance_pa_s_m=[0.1])
        j=next(j for j in range(len(centred["node_coordinates_m"])-1)
               if centred["node_coordinates_m"][j]==.3625
               and centred["node_coordinates_m"][j+1]==.3625)
        self.assertEqual(centred["node_sides"][j:j+2],["minus","plus"])
        self.assertAlmostEqual(centred["face_conductance_m_pa_s"][j+1],10.0,places=12)
        jump=centred["node_profiles_pa"][-1][j+1]-centred["node_profiles_pa"][-1][j]
        self.assertGreater(abs(jump),1e-8)

    def test_invalid_initial_profile_rejected(self):
        with self.assertRaises(ValueError):
            solve_interface_aware([0.0,1.0],[1.0],[1.0],10,1.0,1e-4,1,
                                  initial_pressure_profile_pa=[1.0,2.0])

    def test_invalid_layer_partition_rejected(self):
        with self.assertRaises(ValueError):
            solve_interface_aware([0,.5,.4,1],[1,2,3],[1,1,1],20,1,1e-4,1)


if __name__=="__main__":
    unittest.main()
