import fileinput, re 
import requests, sys
import json

	
#------------------------------------------------------NCBI ID-----------------------------------------------------

def NCBI_ID(specie, gene) : 
	server = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	ext = "esearch.fcgi?db=gene&term="+specie+"[ORGN]+AND+"+gene+"[GENE]&idtype=acc&retmode=json"			#URL de requête
	 
	r = requests.get(server+ext)                                		#Requête GET NCBI
 
	if not r.ok :
		r.raise_for_status()
		sys.exit()										   				

	decoded = r.json()                                        			
	NCBIid = []                                              		    
	idN = decoded['esearchresult']['idlist']                 	 		
	NCBIid.append(idN[0])                                     			
	return NCBIid
	
	
#----------------------------------------------------NCBI Full name----------------------------------------------------

def NCBI_FN(v_ncbiID) : 
	for idncbi in v_ncbiID : 												
		server = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		ext = "esummary.fcgi?db=gene&id="+idncbi+"&version=2.0&retmode=xml"		#URL de requête

		r = requests.get(server+ext)											#Requête GET 
 
		if not r.ok :
			r.raise_for_status()
			sys.exit()														 

		decoded = r.text													 
		NCBIFN = []															 
		name_list = re.findall('<Description>(.*)</Description>', decoded)   #Expression régulière pour récupérer tout ce qui se trouve entre les balises 'Description' dans le xml
		if name_list != [""]: 												 
			full_name = name_list[0] 										 
			NCBIFN.append(full_name)									     
	return NCBIFN 																			
	
	
#------------------------------------RefSeq transcrits ID NM_ et XM_ -------------------------------------------

def RefSeq_TID (specie, gene) : 
	server = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	ext = "esearch.fcgi?db=nucleotide&term="+specie+"[ORGN]+AND+"+gene+"[GENE]&idtype=acc&retmode=json"		#URL de requête
	 
	r = requests.get(server+ext)											#Requête GET NCBI
 
	if not r.ok :
		r.raise_for_status()
		sys.exit()														

	decoded = r.json()													
	NCBInu = [] 														
	NUN = decoded['esearchresult']['idlist']							
	for i in NUN : 														
		if (re.search("NM_", i)) or (re.search("XM_", i)): 				#Expression régulière pour récupérer seulement les id commençant par NM et XM
			NCBInu.append(i)											
	return NCBInu


#-------------------------------------------RefSeq protein ID NP_-----------------------------------------------

def RefSeq_PID (specie, gene) : 
	server = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	ext = "esearch.fcgi?db=protein&term="+specie+"[ORGN]+AND+"+gene+"[GENE]&idtype=acc&retmode=json"		#URL de requête
	 
	r = requests.get(server+ext)											#Requête GET 
 
	if not r.ok :
		r.raise_for_status()
		sys.exit()														

	decoded = r.json()													
	NCBIprot = [] 														
	NUP = decoded['esearchresult']['idlist']							
	for j in NUP : 														
		if (re.search("NP_", j)) or (re.search("XP_", j)): 				#Expression régulière pour récupérer seulement les id commençant par NP et XP 
			NCBIprot.append(j)											
	return NCBIprot
	

#----------------------------------------------KEGG ID----------------------------------------------------

def Kegg(v_ncbiID) :
	for ncbiid in v_ncbiID : 													
		url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(ncbiid)	#URL de requête
		r = requests.get(url)													#Requête GET 
		
		KEGG_ID = []													
		kegg = r.text.rstrip()
		listK = kegg.split("\t") 										
		Keggid = listK[1]												
		KEGG_ID.append(Keggid)											
	return KEGG_ID
	
	
#------------------------------------------------KEGG PATHWAYS---------------------------------------------
	
def Kegg_path(v_keggid) : 
	for keggid in v_keggid : 											
		url_path = "http://rest.kegg.jp/get/+{}".format(keggid)			#URL de requête
		r = requests.get(url_path)										#Requête GET 
		
		KEGG_PATH1 = []													#Création d'une liste vide pour l'id pathways
		KEGG_PATH2 = []													#Création d'une liste pour le nom du pathways
		KEGG_PATH0 = []													#Création d'une liste pour récupérer les pathways entier
		letters = keggid[:3] 											
		regex_path = " (" + letters + "\d{5})  (.*)" 					#Définir le motif comme commencant par les 3 premières lettres de l'id KEGG suivit de 5 chiffres
		list_id_name = re.findall(regex_path, r.text)					#Expression régulière pour rechercher le motif précédant dans la sortie en txt 
		KEGG_PATH0.append(list_id_name) 								
		for keggpath in KEGG_PATH0 : 									
			for Keggpath in keggpath : 									
				if not Keggpath[0] in KEGG_PATH1 : 						
					KEGG_PATH1.append(Keggpath[0])						
				if not Keggpath[1] in KEGG_PATH2 : 
					KEGG_PATH2.append(Keggpath[1])						
	return KEGG_PATH1, KEGG_PATH2										#Besoin de séparer les deux champs car on utilisera le premier (id) pour la construction d'un lien
