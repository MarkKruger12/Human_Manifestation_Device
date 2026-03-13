"""
Core physics calculations for the Ultimate Null Field System
"""
import numpy as np
from scipy import constants, special
from dataclasses import dataclass

@dataclass
class FundamentalConstants:
    """All fundamental physical constants in SI units"""
    # EM constants
    mu0: float = 4 * np.pi * 1e-7  # Vacuum permeability [H/m]
    epsilon0: float = 8.8541878128e-12  # Vacuum permittivity [F/m]
    c: float = 299792458  # Speed of light [m/s]
    Z0: float = 376.730313668  # Vacuum impedance [Ω]
    
    # Quantum constants
    h: float = 6.62607015e-34  # Planck constant [J⋅s]
    hbar: float = 1.054571817e-34  # Reduced Planck [J⋅s]
    e: float = 1.602176634e-19  # Electron charge [C]
    me: float = 9.1093837015e-31  # Electron mass [kg]
    mp: float = 1.67262192369e-27  # Proton mass [kg]
    kB: float = 1.380649e-23  # Boltzmann constant [J/K]
    NA: float = 6.02214076e23  # Avogadro constant [mol^-1]
    
    # Magnetic constants
    muB: float = 9.2740100783e-24  # Bohr magneton [J/T]
    muN: float = 5.0507837461e-27  # Nuclear magneton [J/T]
    gamma_e: float = 1.76085963023e11  # Electron gyromagnetic ratio [rad/(s⋅T)]
    gamma_p: float = 2.6752218744e8  # Proton gyromagnetic ratio [rad/(s⋅T)]

class FieldCalculations:
    """Magnetic field calculations for various geometries"""
    
    def __init__(self):
        self.const = FundamentalConstants()
    
    def point_dipole_field(self, m_vector, r_vector):
        """
        Magnetic field from a point dipole
        
        Parameters:
        -----------
        m_vector : array_like
            Magnetic moment vector [A·m²]
        r_vector : array_like
            Position vector from dipole [m]
        
        Returns:
        --------
        array_like : B-field vector [T]
        """
        r = np.linalg.norm(r_vector)
        if r < 1e-15:
            return np.zeros(3)
        
        r_hat = r_vector / r
        m_dot_r = np.dot(m_vector, r_hat)
        
        B = (self.const.mu0 / (4 * np.pi * r**3)) * (
            3 * r_hat * m_dot_r - m_vector
        )
        return B
    
    def circular_loop_field(self, I, R, z):
        """
        Magnetic field on axis of circular current loop
        
        Parameters:
        -----------
        I : float
            Current [A]
        R : float
            Loop radius [m]
        z : float
            Distance from center along axis [m]
        
        Returns:
        --------
        float : B-field along axis [T]
        """
        Bz = (self.const.mu0 * I * R**2) / (2 * (R**2 + z**2)**(3/2))
        return Bz
    
    def helmholtz_coil_pair(self, I, R, d, z):
        """
        Field from Helmholtz coil pair
        
        Parameters:
        -----------
        I : float
            Current in each coil [A] (same direction)
        R : float
            Coil radius [m]
        d : float
            Separation between coils [m]
        z : float
            Position along axis (center at z=0) [m]
        
        Returns:
        --------
        float : Total B-field [T]
        """
        B1 = self.circular_loop_field(I, R, z - d/2)
        B2 = self.circular_loop_field(I, R, z + d/2)
        return B1 + B2

class ResonanceCalculator:
    """Calculate resonance parameters for the coil system"""
    
    def __init__(self):
        self.const = FundamentalConstants()
    
    def lc_resonance(self, L, C):
        """Calculate resonant frequency from L and C"""
        return 1 / (2 * np.pi * np.sqrt(L * C))
    
    def required_capacitance(self, f, L):
        """Calculate capacitance needed for resonance at frequency f"""
        omega = 2 * np.pi * f
        return 1 / (omega**2 * L)
    
    def quality_factor(self, f, L, R):
        """Calculate Q factor from resistance"""
        omega = 2 * np.pi * f
        return omega * L / R
    
    def bandwidth(self, f, Q):
        """Calculate bandwidth from Q factor"""
        return f / Q
    
    def stored_energy(self, L, I):
        """Calculate energy stored in inductor"""
        return 0.5 * L * I**2
    
    def loss_per_cycle(self, L, I, Q):
        """Calculate energy loss per RF cycle"""
        E_stored = self.stored_energy(L, I)
        return 2 * np.pi * E_stored / Q

class QuantumLimitCalculator:
    """Calculate quantum limits for field sensing"""
    
    def __init__(self):
        self.const = FundamentalConstants()
    
    def spin_projection_noise(self, volume, T_measurement, spin_density=1e28):
        """
        Calculate B-field sensitivity from spin projection noise
        
        Parameters:
        -----------
        volume : float
            Sensing volume [m³]
        T_measurement : float
            Measurement time [s]
        spin_density : float
            Spin density [m⁻³]
        
        Returns:
        --------
        float : Minimum detectable B-field [T]
        """
        N_spins = spin_density * volume
        gamma = self.const.gamma_e
        
        # Heisenberg limit
        deltaB = self.const.hbar / (gamma * np.sqrt(N_spins * T_measurement))
        return deltaB
    
    def thermal_noise(self, volume, T_measurement, spin_density=1e28, temp_K=300):
        """
        Calculate B-field sensitivity from thermal noise
        
        Returns:
        --------
        float : Minimum detectable B-field [T]
        """
        N_spins = spin_density * volume
        gamma = self.const.gamma_e
        
        deltaB = np.sqrt(2 * self.const.kB * temp_K * self.const.mu0 / 
                        (gamma**2 * self.const.hbar * N_spins * T_measurement))
        return deltaB
    
    def quantum_limit(self, volume, T_measurement, spin_density=1e28, temp_K=300):
        """
        Calculate overall quantum limit (max of projection and thermal noise)
        """
        proj = self.spin_projection_noise(volume, T_measurement, spin_density)
        thermal = self.thermal_noise(volume, T_measurement, spin_density, temp_K)
        return max(proj, thermal)

class MaterialDatabase:
    """Material properties database"""
    
    @staticmethod
    def copper(temperature=300):
        """Copper properties at specified temperature"""
        if temperature == 300:
            return {
                'resistivity': 1.724e-8,
                'thermal_conductivity': 401,
                'skin_depth_coeff': lambda f: np.sqrt(2*1.724e-8/(2*np.pi*f*4*np.pi*1e-7))
            }
        elif temperature == 77:
            return {
                'resistivity': 2.0e-9,
                'thermal_conductivity': 1000,
                'skin_depth_coeff': lambda f: np.sqrt(2*2.0e-9/(2*np.pi*f*4*np.pi*1e-7))
            }
        elif temperature == 4:
            return {
                'resistivity': 1.0e-10,
                'thermal_conductivity': 10000,
                'skin_depth_coeff': lambda f: np.sqrt(2*1.0e-10/(2*np.pi*f*4*np.pi*1e-7))
            }
        else:
            raise ValueError(f"Temperature {temperature}K not in database")
    
    @staticmethod
    def ndfeb(grade='N52'):
        """NdFeB magnet properties"""
        magnets = {
            'N50': {'Br': 1.45, 'Hc': 876e3, 'BH_max': 398e3},
            'N52': {'Br': 1.48, 'Hc': 995e3, 'BH_max': 414e3},
            'N55': {'Br': 1.55, 'Hc': 995e3, 'BH_max': 438e3}
        }
        return magnets.get(grade, magnets['N52'])
    
    @staticmethod
    def rebco():
        """REBCO superconductor properties"""
        return {
            'Tc': 92,
            'Jc_77K': 3e10,
            'Ic_77K': 500,
            'thickness': 0.1e-3,
            'width': 4e-3
        }

# Create global instances for easy import
constants = FundamentalConstants()
field_calc = FieldCalculations()
resonance = ResonanceCalculator()
quantum = QuantumLimitCalculator()
materials = MaterialDatabase()