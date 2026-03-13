"""
Visualization utilities for the Ultimate Null Field System
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class FieldVisualizer:
    """Visualize magnetic fields in 2D and 3D"""
    
    @staticmethod
    def set_publication_style():
        """Set matplotlib style for publication-quality figures"""
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['lines.linewidth'] = 2
    
    def plot_field_profile(self, z_positions, B_fields, title="Magnetic Field Profile"):
        """
        Plot B-field along axis
        """
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Linear plot
        axes[0].plot(z_positions*1000, B_fields*1e6, 'b-', linewidth=2)
        axes[0].set_xlabel('Position along axis [mm]')
        axes[0].set_ylabel('B-field [μT]')
        axes[0].set_title(title + ' - Linear Scale')
        axes[0].grid(True, alpha=0.3)
        
        # Log scale for null region
        B_abs = np.abs(B_fields)
        B_abs[B_abs < 1e-18] = 1e-18  # Avoid log(0)
        axes[1].semilogy(z_positions*1000, B_abs*1e15, 'r-', linewidth=2)
        axes[1].set_xlabel('Position along axis [mm]')
        axes[1].set_ylabel('|B-field| [fT]')
        axes[1].set_title(title + ' - Logarithmic Scale')
        axes[1].grid(True, alpha=3)
        
        plt.tight_layout()
        return fig
    
    def plot_field_map_2d(self, X, Y, B_magnitude, title="2D Field Map"):
        """
        Create 2D contour plot of field magnitude
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        contour = ax.contourf(X*1000, Y*1000, B_magnitude*1e12, 
                              levels=50, cmap='viridis')
        plt.colorbar(contour, ax=ax, label='B-field [pT]')
        
        ax.set_xlabel('X [mm]')
        ax.set_ylabel('Y [mm]')
        ax.set_title(title)
        ax.set_aspect('equal')
        
        # Mark the null region
        ax.contour(X*1000, Y*1000, B_magnitude*1e12, 
                  levels=[1.0], colors='red', linewidths=2)
        
        return fig
    
    def plot_3d_field_interactive(self, X, Y, Z, B, title="3D Field Visualization"):
        """
        Create interactive 3D plot using Plotly
        """
        fig = go.Figure(data=go.Volume(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=B.flatten()*1e12,
            isomin=0.1,
            isomax=10,
            opacity=0.1,
            surface_count=20,
            colorscale='Viridis',
            colorbar_title='B-field [pT]'
        ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='X [mm]',
                yaxis_title='Y [mm]',
                zaxis_title='Z [mm]',
                aspectmode='cube'
            ),
            width=800,
            height=800
        )
        
        return fig
    
    def plot_resonance_curve(self, frequencies, amplitude, phase, f0, Q):
        """
        Plot resonance characteristics
        """
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Amplitude response
        axes[0].plot(frequencies/1e3, amplitude, 'b-', linewidth=2)
        axes[0].axvline(f0/1e3, color='r', linestyle='--', label=f'f0 = {f0/1e3:.3f} kHz')
        axes[0].set_xlabel('Frequency [kHz]')
        axes[0].set_ylabel('Amplitude [arb.]')
        axes[0].set_title(f'Amplitude Response (Q = {Q:.1f})')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Phase response
        axes[1].plot(frequencies/1e3, phase*180/np.pi, 'g-', linewidth=2)
        axes[1].axvline(f0/1e3, color='r', linestyle='--')
        axes[1].axhline(-90, color='gray', linestyle=':', alpha=0.5)
        axes[1].axhline(-180, color='gray', linestyle=':', alpha=0.5)
        axes[1].set_xlabel('Frequency [kHz]')
        axes[1].set_ylabel('Phase [degrees]')
        axes[1].set_title('Phase Response')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_magnet_array(self, magnet_positions, magnet_strengths):
        """
        Visualize the graded magnet array
        """
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot magnets as spheres with size proportional to strength
        scatter = ax.scatter(magnet_positions[:, 0]*1000, 
                           magnet_positions[:, 1]*1000,
                           magnet_positions[:, 2]*1000,
                           c=magnet_strengths, 
                           s=np.abs(magnet_strengths)*100,
                           cmap='plasma',
                           alpha=0.7)
        
        plt.colorbar(scatter, ax=ax, label='Magnet strength [T]')
        
        ax.set_xlabel('X [mm]')
        ax.set_ylabel('Y [mm]')
        ax.set_zlabel('Z [mm]')
        ax.set_title('Graded Magnet Array Configuration')
        
        return fig

class ThermalVisualizer:
    """Visualize thermal behavior"""
    
    def plot_temperature_profile(self, positions, temperatures, title="Temperature Profile"):
        """
        Plot temperature distribution
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(positions*1000, temperatures, 'r-', linewidth=2)
        ax.axhline(77, color='b', linestyle='--', label='LN2 (77K)')
        ax.axhline(4.2, color='c', linestyle='--', label='LHe (4.2K)')
        
        ax.set_xlabel('Position along axis [mm]')
        ax.set_ylabel('Temperature [K]')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_thermal_noise(self, frequencies, temp_K):
        """
        Plot thermal noise spectrum
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['red', 'blue', 'green', 'orange']
        for i, temp in enumerate(temp_K):
            # Johnson-Nyquist noise
            V_noise = np.sqrt(4 * 1.38e-23 * temp * 50 * frequencies)  # 50Ω load
            ax.loglog(frequencies, V_noise, color=colors[i % len(colors)], 
                     linewidth=2, label=f'{temp} K')
        
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Noise voltage [V/√Hz]')
        ax.set_title('Thermal Noise Spectrum')
        ax.legend()
        ax.grid(True, alpha=0.3, which='both')
        
        return fig

# Create global instance
visualizer = FieldVisualizer()
thermal_viz = ThermalVisualizer()