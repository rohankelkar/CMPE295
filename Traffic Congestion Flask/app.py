from flask import Flask, request, render_template, jsonify
import pickle
from flask_cors import CORS
import pandas as pd
import numpy
import simplejson as json

app= Flask(__name__)
CORS(app)


modelada = pickle.load( open('adaboost_model.pkl','rb'))
modelforest = pickle.load( open('forest_model.pkl','rb'))
modellinear=pickle.load( open('linear_reg_model.pkl','rb'))
modelxg = pickle.load( open('model.pkl','rb'))
@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    return "Hello, world!"

@app.route('/result', methods=['POST'])
def result():
	print("hey")
	bin_data1 = request.stream.read()
	print(bin_data1)
	bin_data = json.loads(bin_data1)

	#req_data = request.json()
	
	#print(req_data)
	
	print(bin_data)
	print(bin_data['startlat'])
	#print(bin_data[1])
	#language = req_data['endlat']
	#print(language)
	startlat= bin_data['startlat']
	type1=bin_data['type']
	print(type1)
	startlong= bin_data['startlong']
	endlat= bin_data['endlat']
	endlong= bin_data['endlong']
	print(type(startlat))
	print(startlong)
	print(endlat)
	print(endlong)
	
	li=[float(startlat), float(startlong), float(endlat), float(endlong)]
	model_columns= ['Pickup Centroid Latitude', 'Pickup Centroid Longitude',
       'Dropoff Centroid Latitude', 'Dropoff Centroid Longitude']
	li = pd.DataFrame([li],columns=model_columns)
	if type1=="Xgboost":
		x = modelxg.predict(li)
		print("XGo")
		print(x)
		a= str(x)
		a= str(a).replace('[','').replace(']','')
		data = {'responsetime': a}
		return jsonify(data)
	elif type1=="Adaboost":
		x = modelada.predict(li)
		print("Adao")
		print(x)
		a= str(x)
		a= str(a).replace('[','').replace(']','')
		data = {'responsetime': a}
		return jsonify(data)

	elif type1=="Linear":
		x = modellinear.predict(li)
		print("Lin")
		print(x)
		a= str(x)
		a= str(a).replace('[','').replace(']','')
		data = {'responsetime': a}
		return jsonify(data)
	elif type1=="Forest":
		x = modelforest.predict(li)
		print("For")
		a= str(x)
		a= str(a).replace('[','').replace(']','')
		data = {'responsetime': a}
		return jsonify(data)
	
