import fileinput, re 
import requests, sys
import json

#----------------------------------PDB ID------------------------------------------------

def PDB_id(v_idun) :
	url = "https://www.rcsb.org/pdb/rest/search"						#URL de requête 
	data= """ 
	<orgPdbQuery>
	<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
	<accessionIdList>{}</accessionIdList>
	</orgPdbQuery>
	""".format(v_idun)													#query
	header={"Content-Type":"Application/x-www-form-urlencoded"}			#head

	r = requests.post(url,data=data,headers=header)						#Construction de la requête POST 
	
	result2=r.text														
	pdb_id =[]															
	if result2 != "null\n":												
		result3=re.sub("(:\d{1})","",result2)							#Expression régulière pour enlever les ':' suivit d'un nombre
		result4=result3[:-1]											
		list_pdb=result4.split("\n")									
		for pdb in list_pdb :											#Parcours de la liste id pdb car il y a des doublons
			if not pdb in pdb_id : 
				pdb_id.append(pdb)										
	else : 
		pdb_id.append("Not ID PDB")										
	return pdb_id


#----------------------------------PDB STRUCTURE--------------------------------------------------

def PDB_structure(v_pdbid) :
	i=0
	pdb_struc = []														
	while i < len(v_pdbid) : 
		for idpdb in v_pdbid : 											
			if idpdb != "Not ID PDB" :  								
				url = "https://www.rcsb.org/pdb/json/describePDB?structureId={}".format(idpdb)	#URL avec requête 
				r = requests.get(url)									#Construction de la requête GET
		
				decoded = r.json()										
				for h in decoded : 										
					struc_PDB = h['title']								
				pdb_struc.append(struc_PDB)								
			else : 
				pdb_struc.append("Not ID PDB")							
			i = i+1
		return pdb_struc
			



