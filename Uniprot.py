import fileinput, re 
import requests, sys
import json
	
# ---------------------------------- Récupération id uniprot-------------------------------------

def Uniprot_ID(specie, gene) : 
	requestURL = "https://www.uniprot.org/uniprot/?query=organism:"+specie+"+AND+gene:"+gene+"&sort=score&columns=entry name,id,reviewed,protein names,genes,organism,length&format=tab"  #URL requête
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})               #Construction de la requête GET

	if not r.ok:
		r.raise_for_status()
		sys.exit()														

	responseBody = r.text												
	resp=responseBody.split("\t") 										
	idun=resp[7]														
	return idun
	
	
#--------------------------------Récupération des noms entiers -----------------------------------

def Uniprot_name(specie, gene) : 
	requestURL = "https://www.uniprot.org/uniprot/?query=organism:"+specie+"+AND+gene:"+gene+"&sort=score&columns=entry name,id,reviewed,protein names,genes,organism,length&format=tab"  #URL requête
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})				 #Construction de la requête GET

	if not r.ok:
		r.raise_for_status()
		sys.exit()														

	responseBody = r.text												
	resp=responseBody.split("\t") 										
	pn=resp[9]															#Récupération du 10ème champs correspondant au id uniprot
	return pn
