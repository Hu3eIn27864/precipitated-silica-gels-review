"""CCFSM v0.4a recipe-to-aqueous-speciation equilibrium module.
Concentrations in mol/L. Davies is a limited dilute-solution approximation.
"""
from dataclasses import dataclass
import math

LOG_K_SILICIC_1 = -9.83
LOG_K_SILICIC_OVERALL_2 = -23.00
LOG_K_HSO4_ASSOC = 1.988
LOG_K_NASO4_PAIR = 0.94
DAVIES_A_25C = 0.509


def _finite(x, name):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _nonnegative(x, name):
    x = _finite(x, name)
    if x < 0:
        raise ValueError(f"{name} must be nonnegative")
    return x


def _positive(x, name):
    x = _finite(x, name)
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


def _pow10(x):
    return 10.0 ** max(-300.0, min(300.0, x))


@dataclass(frozen=True)
class SodiumSilicateRecipe:
    total_silica_mol_l: float
    silicate_modulus: float
    sulfuric_acid_mol_l: float
    sodium_hydroxide_mol_l: float = 0.0
    sodium_chloride_mol_l: float = 0.0
    dissolved_silica_fraction: float = 1.0
    temperature_k: float = 298.15
    pKw: float = 14.0
    pKa_silicic_1: float = 9.83
    pKa_silicic_overall_2: float = 23.0
    logK_hso4_association: float = LOG_K_HSO4_ASSOC
    logK_naso4_pair: float = LOG_K_NASO4_PAIR
    activity_model: str = "davies"
    max_davies_ionic_strength_mol_l: float = 0.5

    def __post_init__(self):
        _nonnegative(self.total_silica_mol_l, "total_silica_mol_l")
        _positive(self.silicate_modulus, "silicate_modulus")
        _nonnegative(self.sulfuric_acid_mol_l, "sulfuric_acid_mol_l")
        _nonnegative(self.sodium_hydroxide_mol_l, "sodium_hydroxide_mol_l")
        _nonnegative(self.sodium_chloride_mol_l, "sodium_chloride_mol_l")
        if not 0.0 <= _finite(self.dissolved_silica_fraction, "dissolved_silica_fraction") <= 1.0:
            raise ValueError("dissolved_silica_fraction must lie in [0, 1]")
        _positive(self.temperature_k, "temperature_k")
        _positive(self.pKw, "pKw")
        _finite(self.pKa_silicic_1, "pKa_silicic_1")
        _finite(self.pKa_silicic_overall_2, "pKa_silicic_overall_2")
        _finite(self.logK_hso4_association, "logK_hso4_association")
        _finite(self.logK_naso4_pair, "logK_naso4_pair")
        if self.activity_model not in ("ideal", "davies"):
            raise ValueError("activity_model must be 'ideal' or 'davies'")
        _positive(self.max_davies_ionic_strength_mol_l, "max_davies_ionic_strength_mol_l")

    @property
    def total_sodium_mol_l(self):
        return (2.0*self.total_silica_mol_l/self.silicate_modulus
                + self.sodium_hydroxide_mol_l + self.sodium_chloride_mol_l)

    @property
    def total_sulfate_mol_l(self):
        return self.sulfuric_acid_mol_l

    @property
    def total_chloride_mol_l(self):
        return self.sodium_chloride_mol_l

    @property
    def dissolved_silica_mol_l(self):
        return self.total_silica_mol_l*self.dissolved_silica_fraction

    @classmethod
    def from_stock_solutions(
        cls, *, silicate_stock_silica_mol_l, silicate_modulus,
        silicate_stock_volume_l, sulfuric_acid_stock_mol_l,
        sulfuric_acid_stock_volume_l, water_volume_l,
        naoh_stock_mol_l=0.0, naoh_stock_volume_l=0.0,
        nacl_stock_mol_l=0.0, nacl_stock_volume_l=0.0,
        **equilibrium_options
    ):
        vals = (silicate_stock_silica_mol_l, silicate_stock_volume_l,
                sulfuric_acid_stock_mol_l, sulfuric_acid_stock_volume_l,
                water_volume_l, naoh_stock_mol_l, naoh_stock_volume_l,
                nacl_stock_mol_l, nacl_stock_volume_l)
        for v in vals:
            _nonnegative(v, "stock concentration/volume")
        _positive(silicate_modulus, "silicate_modulus")
        vtot = sum((silicate_stock_volume_l, sulfuric_acid_stock_volume_l,
                    water_volume_l, naoh_stock_volume_l, nacl_stock_volume_l))
        _positive(vtot, "total mixed volume")
        return cls(
            total_silica_mol_l=silicate_stock_silica_mol_l*silicate_stock_volume_l/vtot,
            silicate_modulus=silicate_modulus,
            sulfuric_acid_mol_l=sulfuric_acid_stock_mol_l*sulfuric_acid_stock_volume_l/vtot,
            sodium_hydroxide_mol_l=naoh_stock_mol_l*naoh_stock_volume_l/vtot,
            sodium_chloride_mol_l=nacl_stock_mol_l*nacl_stock_volume_l/vtot,
            **equilibrium_options)


@dataclass(frozen=True)
class SpeciationResult:
    pH: float
    ionic_strength_mol_l: float
    activity_model: str
    gamma_monovalent: float
    gamma_divalent: float
    sodium_free_mol_l: float
    sodium_sulfate_pair_mol_l: float
    sulfate_mol_l: float
    bisulfate_mol_l: float
    chloride_mol_l: float
    h4sio4_mol_l: float
    h3sio4_mol_l: float
    h2sio4_mol_l: float
    hydrogen_mol_l: float
    hydroxide_mol_l: float
    charge_residual_mol_l: float
    dissolved_silicon_residual_mol_l: float
    sulfate_balance_residual_mol_l: float
    sodium_balance_residual_mol_l: float

    @property
    def dissolved_silicon_total_mol_l(self):
        return self.h4sio4_mol_l+self.h3sio4_mol_l+self.h2sio4_mol_l


def _gammas(ionic, recipe):
    if recipe.activity_model == "ideal":
        return 1.0, 1.0
    # Cap only trial gamma values during pH bracketing. The final solution
    # is rejected below if its self-consistent ionic strength exceeds limit.
    i_eval = min(ionic, recipe.max_davies_ionic_strength_mol_l)
    root = math.sqrt(max(i_eval, 0.0))
    term = root/(1.0+root)-0.3*i_eval
    return (_pow10(-DAVIES_A_25C*term),
            _pow10(-4.0*DAVIES_A_25C*term))


def _pairing(na_total, sulfate_total, g1, g2, a_h, log_k_assoc, log_k_pair):
    if na_total <= 0.0 or sulfate_total <= 0.0:
        return 0.0, na_total, 0.0, 0.0, 0.0
    k_assoc, k_pair = _pow10(log_k_assoc), _pow10(log_k_pair)
    coeff = 1.0/g2+k_assoc*a_h/g1
    upper = min(na_total, sulfate_total)
    def f(pair):
        aso4 = (sulfate_total-pair)/coeff
        return pair-k_pair*(na_total-pair)*aso4
    lo, hi = 0.0, upper
    for _ in range(100):
        mid = 0.5*(lo+hi)
        if f(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    pair = 0.5*(lo+hi)
    aso4 = (sulfate_total-pair)/coeff
    na_free = na_total-pair
    so4 = aso4/g2
    hso4 = k_assoc*a_h*aso4/g1
    return pair, na_free, aso4, so4, hso4


def _at_pH(pH, recipe, ionic_guess):
    g1, g2 = _gammas(ionic_guess, recipe)
    ah, aoh = _pow10(-pH), _pow10(pH-recipe.pKw)
    pair, na, aso4, so4, hso4 = _pairing(
        recipe.total_sodium_mol_l, recipe.total_sulfate_mol_l,
        g1, g2, ah, recipe.logK_hso4_association, recipe.logK_naso4_pair)
    csi = recipe.dissolved_silica_mol_l
    k1 = _pow10(-recipe.pKa_silicic_1)
    k2overall = _pow10(-recipe.pKa_silicic_overall_2)
    f1, f2 = k1/(ah*g1), k2overall/(ah*ah*g2)
    h4 = csi/(1.0+f1+f2)
    h3, h2 = h4*f1, h4*f2
    h, oh = ah/g1, aoh/g1
    cl = recipe.total_chloride_mol_l
    charge = na+h-oh-hso4-2.0*so4-pair-h3-2.0*h2-cl
    ionic_calc = 0.5*(na+h+oh+hso4+4.0*so4+pair+h3+4.0*h2+cl)
    return ionic_calc, dict(g1=g1,g2=g2,pair=pair,na=na,so4=so4,
        hso4=hso4,h4=h4,h3=h3,h2=h2,h=h,oh=oh,cl=cl,charge=charge)


def _equilibrated_at_pH(pH, recipe):
    ionic = max(1e-12, 0.5*(recipe.total_sodium_mol_l
        +2.0*recipe.total_sulfate_mol_l+recipe.total_chloride_mol_l
        +recipe.dissolved_silica_mol_l))
    data = None
    for _ in range(500):
        calc, data = _at_pH(pH, recipe, ionic)
        new = 0.5*ionic+0.5*calc
        if abs(new-ionic) <= 1e-11*max(1.0,new):
            ionic = new
            _, data = _at_pH(pH, recipe, ionic)
            return ionic, data
        ionic = new
    raise RuntimeError("ionic-strength/activity iteration did not converge")


def solve_sodium_silicate_sulfuric_acid(recipe, pH_min=-2.0, pH_max=16.0):
    """Solve pH by mass action, analytical balances and electroneutrality."""
    if not isinstance(recipe, SodiumSilicateRecipe):
        raise TypeError("recipe must be SodiumSilicateRecipe")
    pH_min, pH_max = _finite(pH_min,"pH_min"), _finite(pH_max,"pH_max")
    if pH_min >= pH_max:
        raise ValueError("pH_min must be less than pH_max")
    def charge(pH):
        ionic, d = _equilibrated_at_pH(pH, recipe)
        return d["charge"], ionic, d
    ngrid, previous, bracket = 360, None, None
    for i in range(ngrid+1):
        pH = pH_min+(pH_max-pH_min)*i/ngrid
        val, _, _ = charge(pH)
        if previous is not None and previous[1]*val <= 0.0:
            bracket = (previous[0],pH)
            break
        previous = (pH,val)
    if bracket is None:
        raise ValueError("electroneutrality root not bracketed; check recipe totals, counterions and pH bounds")
    lo, hi = bracket
    flo = charge(lo)[0]
    for _ in range(120):
        mid = 0.5*(lo+hi)
        fm = charge(mid)[0]
        if abs(fm)<1e-12 or hi-lo<1e-11:
            lo=hi=mid
            break
        if flo*fm <= 0.0:
            hi=mid
        else:
            lo,flo=mid,fm
    pH=0.5*(lo+hi)
    ionic,d=_equilibrated_at_pH(pH,recipe)
    if (recipe.activity_model == "davies"
            and ionic > recipe.max_davies_ionic_strength_mol_l):
        raise ValueError(
            f"final self-consistent I={ionic:.5g} mol/L exceeds Davies limit; "
            "use measured activities or a validated Pitzer/SIT model")
    si_res=d["h4"]+d["h3"]+d["h2"]-recipe.dissolved_silica_mol_l
    s_res=d["so4"]+d["hso4"]+d["pair"]-recipe.total_sulfate_mol_l
    na_res=d["na"]+d["pair"]-recipe.total_sodium_mol_l
    return SpeciationResult(
        pH,ionic,recipe.activity_model,d["g1"],d["g2"],d["na"],d["pair"],
        d["so4"],d["hso4"],d["cl"],d["h4"],d["h3"],d["h2"],d["h"],d["oh"],
        d["charge"],si_res,s_res,na_res)
