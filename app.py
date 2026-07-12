import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Web Page Styling & Configuration
st.set_page_config(page_title="PBH Lab Dashboard", layout="wide")
st.title("🌌 Primordial Black Hole Hawking Evaporation Laboratory")
st.write("An interactive quantum-thermodynamic simulator parsing Schwarzschild decay structures across cosmological eras.")

# Physical Constants (SI Units)
G = 6.67430e-11        
hbar = 1.0545718e-34   
c = 299792458          
kB = 1.380649e-23      
yr_to_sec = 3.154e7    
age_universe = 13.8e9  

# Layout: Split page into interactive control panel and analytical visuals
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ Physical Controls")
    # Streamlit native slider element
    log_initial_mass = st.slider("Initial Formation Mass Log10(grams):", min_value=14.0, max_value=16.5, value=15.0, step=0.05)
    
    # Mathematical Calculations
    M_init_g = 10**log_initial_mass
    M_init_kg = M_init_g / 1000.0
    t_evap_sec = (5120 * np.pi * (G**2) * (M_init_kg**3)) / (hbar * (c**4))
    t_evap_yr = t_evap_sec / yr_to_sec
    r_sch_init = (2 * G * M_init_kg) / (c**2)
    temp_init = (hbar * (c**3)) / (8 * np.pi * G * M_init_kg * kB)

    # Real-time Status Assessment
    if t_evap_yr >= age_universe:
        st.success(f"🟢 STABLE RELIC\n\nSurvives for {t_evap_yr:.2e} years. Viable Cold Dark Matter candidate.")
    else:
        st.error(f"💥 EVAPORATED CONSTRAINT\n\nDissolved {age_universe - t_evap_yr:.2e} years ago into diffuse gamma rays.")

    # High-impact metric panels
    st.metric("Initial Horizon Radius", f"{r_sch_init:.2e} meters")
    st.metric("Initial Hawking Temperature", f"{temp_init:.2e} Kelvin")
    st.metric("Total System Lifespan", f"{t_evap_yr:.2e} Years")

with col2:
    st.subheader("📊 Dynamic Analytical Charts")
    
    # Build dynamic timeline arrays
    time_steps = np.linspace(0, t_evap_sec, 200)
    mass_evolution_kg = M_init_kg * (1 - time_steps / t_evap_sec)**(1/3)
    mass_evolution_kg = np.clip(mass_evolution_kg, 1e-5, None)
    temp_evolution_K = (hbar * (c**3)) / (8 * np.pi * G * mass_evolution_kg * kB)

    # Render data charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    plt.style.use('dark_background')
    
    ax1.plot(time_steps / yr_to_sec, mass_evolution_kg * 1000, color='cyan', lw=2)
    ax1.set_title("Mass Decay Profile")
    ax1.set_xlabel("Time (Years)")
    ax1.set_ylabel("Mass (grams)")
    ax1.grid(True, linestyle='--', alpha=0.2)

    ax2.plot(time_steps / yr_to_sec, temp_evolution_K, color='orangered', lw=2)
    ax2.set_yscale('log')
    ax2.set_ylabel("Temperature (Kelvin)")
    ax2.set_title("Hawking Thermal Runaway Loop")
    ax2.set_xlabel("Time (Years)")
    ax2.grid(True, linestyle='--', alpha=0.2)
    
    st.pyplot(fig)
