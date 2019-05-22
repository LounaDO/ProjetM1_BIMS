import fileinput, re 
import requests, sys
import json


#--------------------------------------- Récupération des ID de gène sur ensembl-----------------------------------------------

def EnsEMBL_ID(specie_sub, gene) : 
	server = "https://rest.ensembl.org"
	ext = "/xrefs/symbol/"+specie_sub+"/"+gene+"?"                                 #URL de requête
	 
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})   #Requête GET EnsEMBL
 	
	if not r.ok:
		server = "https://rest.ensemblgenomes.org"
		ext = "/xrefs/symbol/"+specie_sub+"/"+gene+"?"
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})   #Pour les plantes, champignons, protiste...

		if not r.ok :
			r.raise_for_status()
			sys.exit()													
 
	decoded = r.json()                  								

	k=0
	idEnsembl = []                      								
	while k < len(decoded) :            								
		idEn = decoded[k]['id']         								
		idEnsembl.append(idEn)          								
		k=k+1
	return idEnsembl                    								
	

#--------------------------------------Récupération des ID des transcripts sur ensembl--------------------------------------------------

def EnsEMBL_TID(v_idEn) :
	i=0
	idtranscript = []                                                   
	while i < len(v_idEn) : 
		for idens in v_idEn :                                           
			server2 = "https://rest.ensembl.org"
			ext2 = "/overlap/id/"+idens+"?feature=transcript"             

			r2 = requests.get(server2+ext2, headers={ "Content-Type" : "application/json"})        #Requête GET ensembl 
 
			if not r2.ok:
				server2 = "https://rest.ensemblgenomes.org"
				ext2 = "/overlap/id/"+idens+"?feature=transcript"                                 
 
				r2 = requests.get(server2+ext2, headers={ "Content-Type" : "application/json"})
		
				if not r2.ok:  		
					r2.raise_for_status()
					sys.exit()											
 
			decoded2 = r2.json()                                        
			
			j=0
			while j < len(decoded2) :                                   
				transID = decoded2[j]['transcript_id']                  
				if not transID in idtranscript : 
					idtranscript.append(transID)						
				j=j+1
			i = i+1
	return idtranscript													
	
	
#----------------------------------------Récupération des ID des protéines sur ensembl-----------------------------------------------
		
def EnsEMBL_PID(v_idEn) : 
	l = 0 
	prot=[]																
	while l < len(v_idEn) :
		for idens in v_idEn : 											
			server3 = "https://rest.ensembl.org"
			ext3 = "/overlap/id/"+idens+"?feature=cds"

			r3 = requests.get(server3+ext3, headers={ "Content-Type" : "application/json"})		 #Requête GET ensembl 
	
			if not r3.ok : 
				server3 = "https://rest.ensemblgenomes.org"
				ext3 = "/overlap/id/"+idens+"?feature=cds"				
			
				r3 = requests.get(server3+ext3, headers={ "Content-Type" : "application/json"})

				if not r3.ok : 
					r3.raise_for_status()
					sys.exit()											
			
			decoded3 = r3.json()										
			for h in decoded3 : 										
				protID = h['id']						    			
				if not protID in prot : 								
					prot.append(protID)									
			l = l +1
		return prot														
	
		
#----------------------------------------------------Génome Browser------------------------------------------------------------------------------------	

def Genome_B(v_idEn, specie_sub):
	db_list = ["ensembl", "plants.ensembl", "bacteria.ensembl", "fungi.ensembl", "protists.ensembl", "metazoa.ensembl"]  #Création d'une liste de banque de données ensembl
	for db in db_list:																									 
		final_url = "http://{}.org/{}/Gene/Summary?db=core;g={}".format(db, specie_sub,v_idEn)
		test_url = requests.get(final_url)																				 #Requête GET ensembl
		if test_url.ok: 																							 	 
			result=test_url.url
			url = "http://www.{}.org/{}/Location/View?db=core;g={}".format(db, specie_sub,v_idEn)					     #URL vers Génome browser 
			break 
	return result,url								


#------------------------------------------------------Orthologue----------------------------------------------------------------------------------------------

def Orthologs(v_idEn, specie_sub) : 
	for idens in v_idEn : 					
		link = "<a href= 'https://www.ensembl.org/"+specie_sub+"/Gene/Compara_Ortholog?db=core;g="+idens+"'> ortholog </a>"			#lien ortholog
	return link								
