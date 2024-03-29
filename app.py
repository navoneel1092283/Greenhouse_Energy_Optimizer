import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from flask import Flask, request, jsonify, render_template
from model import energy_mix_model
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def recommend():
	dimensions = request.form.get("dimensions")
	area = float(dimensions.split(' ')[0])*float(dimensions.split(' ')[2])

	annual_electricity_demand = float(request.form.get("electricity"))

	annual_heat_demand = float(request.form.get("heat"))

	hydrogen_available = float(request.form.get("hydro"))

	geo_available = float(request.form.get("geo"))


	solar, hydrogen, geothermal, _, economical_value = energy_mix_model(area, annual_electricity_demand, annual_heat_demand, hydrogen_available, geo_available)

	solar = round(solar*100, 2)
	hydrogen = round(hydrogen*100, 2)
	geothermal = round(geothermal*100, 2)

	natural_gas = 100 - (solar + hydrogen + geothermal)


	energy_fractions = [solar, hydrogen, geothermal, natural_gas]
	sources = ['Solar Energy', 'Hydrogen Energy', 'Geothermal Energy', 'Natural Gas']


	energy_fractions = [0 if round(energy, 1) <= 0 else energy for energy in energy_fractions]
	zero_energy_fractions= [i for i in range(4) if energy_fractions[i] == 0]

	energy_source_dict = {sources[i]:energy_fractions[i] for i in range(4) if i not in zero_energy_fractions}
	sources = list(energy_source_dict.keys())
	energy_fractions = list(energy_source_dict.values())
	#colors = sns.color_palette('pastel')[:len(sources)]

	economical_value = round(economical_value, 2)
	if economical_value > 0:
		display_message = 'Recommended Energy-mix composition can save ' + str(economical_value) + ' USD excluding solar panel installation costs.'
	else:
		display_message = 'Recommended Energy-mix composition'
        
        
	energy_mix_df = pd.DataFrame({'Energy Source': sources,
                                  'Energy Fraction': energy_fractions})
        

	#plt.figure(figsize = (8, 8))
	#plt.rcParams['font.size'] = 9
	#plt.pie(energy_fractions, labels = sources, colors = colors, autopct='%.2f%%')
	#plt.title(display_message)
	#plt.savefig('static/output.png')
    
	fig = px.pie(energy_mix_df, values='Energy Fraction', names='Energy Source')
	username = 'nchakrabarty'
	api_key = 'PJuwonDUbCi4Vdbbru54'
    
	chart_studio.tools.set_credentials_file(username = username, api_key = api_key)
	output_plotlink = py.plot(fig, filename = 'Energy-mix Composition', auto_open = False)
	output_plotlink = output_plotlink.split(':')[1][:-1] + '.embed'
    
    
	return render_template('index.html', output_text = display_message, output_plotlink = output_plotlink)

if __name__ == "__main__":
    app.run(debug=True)
