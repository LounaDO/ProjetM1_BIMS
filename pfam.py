import fileinput, re 
import requests, sys
import json
	

#------------------------------------------------pfam ID -------------------------------------------

def Pfam_ID(idun) : 													# id uniprot en argument
	url = "http://pfam.xfam.org/protein/{}?output=xml".format(idun)     
	r = requests.get(url)												# Requête GET

	Pfam_ACC = re.findall("PF[\d]{5}",r.text)							# expression régulière pour récupérer les id motif : 'PF' suivit de 5 chiffres					
	return Pfam_ACC[0]													# Obtention des id pfam avec un meilleur score


#--------------------------------------------------pfam domain--------------------------------------

def pfam_domain(v_pfamid) :  
	link = "<a href= 'https://pfam.xfam.org/family/"+v_pfamid+"/#tabview=tab1' > " +v_pfamid+ "</a>"         #lien vers domaine pfam à partir de l'id
	return link
