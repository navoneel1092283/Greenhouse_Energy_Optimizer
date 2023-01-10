# Example greenhouse_dim: 30 x 96 (feet^2) equal to 9.144 x 29.2608 (m^2)
# Example annual_electricity_demand: 1,600,000 KWh
# Example annual_heat_demand: 0.42515 KW/m2 = 307.5 kWh

# constants
solar_energy_m2 = 150 #KWh/m2
hydrogen2geothermal_ratio = 32

# Heat Pump Conversion Rate (Electric-to-Heat Energy), E2H = 4.5 KWh (3-6)
electricity2heat = 4.5
cost_gas = 0.298 #USD/KWh
cost_geo = 0.035 #USD/KWh
cost_hydrogen = 0.18 #USD/KWh



def energy_mix_model(greenhouse_area, annual_electricity_demand, annual_heat_demand, annual_max_hydro_energy, annual_max_geo_energy):
    # 1. Calculate the Heat Demand, HD = H * GA
    heat_demand = annual_heat_demand * greenhouse_area
    # 2.Calculate the electric energy required to generate the HD, EH = (HD/E2H)
    heat_energy = heat_demand / electricity2heat
    # 3. Total Electric Energy demand, TE = E + EH
    total_energy = annual_electricity_demand + heat_energy
    
    
    # 4. Total Solar Energy harnessed, TSE = SE * GA
    solar_energy = solar_energy_m2 * greenhouse_area
    # 5. Residual energy to obtain  = Electric Energy - Solar Energy, RE = TE - TSE
    residual_energy = total_energy - solar_energy
    # 6. Hydrogen Energy required, HE = (H2GT/(H2GT + 1)) * RE
    hydrogen_energy = (hydrogen2geothermal_ratio/(hydrogen2geothermal_ratio+1)) * residual_energy
    # Geothermal Energy required, GE = RE - HE
    geo_energy = residual_energy - hydrogen_energy
    
    #######################################################################################    
    if hydrogen_energy > annual_max_hydro_energy:
        hydrogen_energy = annual_max_hydro_energy
        
    if geo_energy > annual_max_geo_energy:
        geo_energy = annual_max_geo_energy
        
    natural_gas = total_energy - (solar_energy + hydrogen_energy + geo_energy)
    if natural_gas < 0:
        natural_gas = 0
    #######################################################################################
    
    # Mix: (GE/TE), (HE/TE), (SE/TE)
    # Total Cost of Natural Gas, TCNG = CNG * TE
    total_gas_cost = cost_gas * total_energy
    # Total Cost of Energy Mix, TEM = CGE*GE + CHE*HE
    total_mix_cost = abs(hydrogen_energy) * cost_hydrogen + abs(geo_energy) * cost_geo + abs(natural_gas) * cost_gas
    # Economical Value, EV = TCNG - TEM
    economical_value = total_gas_cost - total_mix_cost
    
    return solar_energy/total_energy, hydrogen_energy/total_energy, geo_energy/total_energy, natural_gas/total_energy, economical_value