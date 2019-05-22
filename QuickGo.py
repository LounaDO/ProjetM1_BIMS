import fileinput, re 
import requests, sys
import json

#-----------------------------------------Récupération des biological_process---------------------------------------------------------

def BP_GO(v_idun) : 
	requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect=biological_process&geneProductId={}".format(v_idun)		#URL Requête
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})		#Construction requête GET

	if not r.ok:
		r.raise_for_status()
		sys.exit()														

	responseBody = r.text												
	data=json.loads(responseBody)										

	proc=[]																
	linkGoBP = [] 														
	url = "https://www.ebi.ac.uk/QuickGO/term/"							
	for k in data['results']:											
		GOprocess = k['goName']											
		go_id = k['goId']												
		if not GOprocess in proc : 
			proc.append(GOprocess)										
			GOprocess = k['goName']
			go_id = k['goId']
			linkGoBP.append('<a href="{}{}">{}</a>\n'.format(url, go_id, GOprocess))		
	return linkGoBP
	
	
#-----------------------------------------Récupération des cellular component-----------------------------------------------------

def CC_GO(v_idun) : 
	requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect=cellular_component&geneProductId={}".format(v_idun)		#URL Requête
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})		#Construction requête GET

	if not r.ok:
		r.raise_for_status()
		sys.exit()														

	responseBody = r.text												
	data=json.loads(responseBody)										

	comp=[]																
	linkGoCC = []														
	url = "https://www.ebi.ac.uk/QuickGO/term/"							

	for j in data['results'] : 											
		Gocomp = j["goName"]											
		if not Gocomp in comp : 
			comp.append(Gocomp)											
			Gocomp = j["goName"]
			go_id = j['goId']											
			linkGoCC.append('<a href="{}{}">{}</a>\n'.format(url, go_id, Gocomp))		
	return linkGoCC


#-----------------------------------------Récupération des molecular function--------------------------------

def MF_GO(v_idun) : 
	requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect=molecular_function&geneProductId={}".format(v_idun)		#URL Requête
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})		#Construction requête GET

	if not r.ok:
		r.raise_for_status()
		sys.exit()														

	responseBody = r.text												
	data=json.loads(responseBody)										

	fun=[]																
	linkGoMF = []														
	url = "https://www.ebi.ac.uk/QuickGO/term/"							

	for h in data['results'] : 
		Gofun = h["goName"]
		if not Gofun in fun : 
			fun.append(Gofun)
			Gofun = h["goName"]
			go_id = h['goId']
			linkGoMF.append('<a href="{}{}">{}</a>\n'.format(url, go_id, Gofun))
	return linkGoMF
