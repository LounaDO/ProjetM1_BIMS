import fileinput, re 
import requests, sys
import json

#------------------------------------------prosite---------------------------------------------------

def Prosite_ID(v_idun) : 
	url = 'https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json'.format(v_idun)			#URL Requête
	r = requests.get(url)												#Construction requête GET
	
	decoded = r.json()													
	id_prosite=[]														

	for h in decoded['matchset'] : 										
		id_pro = h["signature_ac"]										
		if not id_pro in id_prosite : 									
			id_prosite.append(id_pro)									
	return id_prosite

