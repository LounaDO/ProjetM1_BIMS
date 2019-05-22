#Main 

from Ensembl import *
from NCBI import * 
from Uniprot import *
from QuickGo import *
from pfam import *
from PDB import *
from String import *
from prosite import *
										#import de tous mes script et donc des fonctions
import fileinput, re 
import requests, sys
import json

'''
Recherche des fonctions et écriture du résultat dans le fichier index.html
'''

#-------------- Ouverture du fichier de gènes et espèces et parcours des lignes + création de 2 listes : gènes et espèces----------

tempfile = open('headresult.html','r')      #ouverture du fichier html head
outputfile = open('index.html','w')     #Création du corps du tableau 
outputfile.write(tempfile.read())
tempfile.close()

for line in fileinput.input ("GeneSymbols.txt"):         
	outputfile.write("<tr>")
	liste = line.split("\t")							
	gene = liste[0]										
	specie = liste[1]									
	specie_sub = re.sub("\s","_",specie[:-1])			
	print(gene)
	print (specie)			

#------------------------------------------Colonne GENE-------------------------------------------------	
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>") #Permet de définir une taille de case et si trop grande ajouter des scrollbar
	outputfile.write(gene)								
	outputfile.write("</div>")
	outputfile.write("</td>")
#------------------------------------------Colonne ESPECE-------------------------------------------------
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; overflow-x:auto;'>")
	outputfile.write(specie)							
	outputfile.write("</div>")
	outputfile.write("</td>")
#-------------------------------------------NCBI ID------------------------------------------------
	print("NCBI...."+'\n')
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_ncbiID = NCBI_ID(specie, gene)
	for ncbi_ID in v_ncbiID : 
		outputfile.write("<a href='https://www.ncbi.nlm.nih.gov/gene/?term="+ncbi_ID+"'>"+ncbi_ID+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")

#---------------------------------------------NCBI Full Name------------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_ncbifn = NCBI_FN(v_ncbiID) 
	for ncbifullname in v_ncbifn : 
		outputfile.write(ncbifullname)
	outputfile.write("</div>")
	outputfile.write("</td>")
#-----------------------------------------Transcript id Refseq--------------------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	print("Transcript Refseq....."+'\n')
	v_ncbitID = RefSeq_TID (specie, gene)
	for ncbi_TID in v_ncbitID : 
		outputfile.write("<a href='https://www.ncbi.nlm.nih.gov/nuccore/"+ncbi_TID+"'>"+ncbi_TID+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")
#-------------------------------------------Proteins id Refseq---------------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	print("Proteine Refseq....."+'\n')
	v_ncbipID = RefSeq_PID (specie, gene)
	for ncbi_PID in v_ncbipID : 
		outputfile.write("<a href='https://www.ncbi.nlm.nih.gov/protein/"+ncbi_PID+"'>"+ncbi_PID+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>") 
#----------------------------------------------KEGG id---------------------------------------------
	print('KEGG....\n')
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_keggid = Kegg(v_ncbiID)
	for keggid in v_keggid : 
		outputfile.write("<a href = 'https://www.genome.jp/dbget-bin/www_bget?"+keggid+"'>"+keggid+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")
#------------------------------------------------KEGG Pathway-------------------------------------------
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_keggpath1 = Kegg_path(v_keggid)[0]
	v_keggpath2 = Kegg_path(v_keggid)[1]
	for keggpath1 in v_keggpath1 :
		outputfile.write("<a href='https://www.genome.jp/kegg-bin/show_pathway?"+keggpath1+"'>"+keggpath1+"</a><br>\n")
	for keggpath2 in v_keggpath2 : 
		outputfile.write(keggpath2+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")
#---------------------------------------------Ensembl ID----------------------------------------------
	print("Gene id Ensembl...."+'\n')
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_idEn = EnsEMBL_ID(specie_sub, gene) 
	for idens in v_idEn : 
		outputfile.write("<a href='https://www.ensembl.org/"+specie_sub+"/Gene/Summary?g="+idens+"'>"+idens+"</a><br>\n")
	outputfile.write("<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")
	
#-------------------------------------------Ensembl Genome Browser---------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	ID_Ens=[]
	ID_Ens=EnsEMBL_ID(specie_sub, gene) 
	outputfile.write("<a href="+str(Genome_B(ID_Ens[0],specie_sub)[0])+">"+ID_Ens[0]+"</a>")
	if len(ID_Ens)!=1:
		outputfile.write('\n')
		outputfile.write("<br>")
		outputfile.write("<a href="+str(Genome_B(ID_Ens[1],specie_sub)[0])+">"+ID_Ens[1]+"</a>")
	outputfile.write("</div>")
	outputfile.write("</td>")
	
#-------------------------------------------Ensembl Ortholog---------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_orth=Orthologs(v_idEn, specie_sub)
	outputfile.write(v_orth+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")

#-------------------------------------------Ensembl Transcript ID------------------------------------------------
	print("Transcript Ensembl.."+'\n')
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	#print (v_idEn)
	v_ensembltid = EnsEMBL_TID(v_idEn)
	for idt in v_ensembltid : 
		outputfile.write("<a href='https://www.ensembl.org/Homo_sapiens/Transcript/Summary?db=core;t="+idt+"'>"+idt+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")
	
	print('Proteins Ensembl.....'+'\n')

#-----------------------------------------------Ensembl Proteins ID--------------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_ensemblpid = EnsEMBL_PID(v_idEn)
	for idp in v_ensemblpid : 
		#print (idp)
		outputfile.write(idp+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")
#----------------------------------------------Uniprot ID---------------------------------------------
	print('Id Uniprot.....'+'\n')
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_idun = Uniprot_ID(specie, gene)
	outputfile.write("<a href='https://www.uniprot.org/uniprot/"+v_idun+"'>"+v_idun+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")
#---------------------------------------------Protein name UNIPROT--------------------------------------------
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	outputfile.write(Uniprot_name(specie, gene))
	outputfile.write("</div>")
	outputfile.write("</td>")
#----------------------------------------------GO Biological Process-------------------------------------------
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_gobp = BP_GO(v_idun)
	for gop in v_gobp : 
		outputfile.write(gop+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")
#-----------------------------------------------GO Molecular fonction-------------------------------------------
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_gomf = MF_GO(v_idun)
	for gof in v_gomf : 
		outputfile.write(gof+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")

#------------------------------------------------GO Cellular Component-----------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_gocc = CC_GO(v_idun)
	for goc in v_gocc : 
		outputfile.write(goc+"<br>")
	outputfile.write("</div>") 
	outputfile.write("</td>")
#---------------------------------------------------PDB ID----------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	print('PDB id.....'+'\n')
	v_pdbid = PDB_id(v_idun)
	for pdbid in v_pdbid : 
		if pdbid != "Not ID PDB" : 
			outputfile.write("<a href='https://www.rcsb.org/structure/"+pdbid+"'>"+pdbid+"</a><br>\n")
		else : 
			outputfile.write("Not ID PDB")
	outputfile.write("</div>")
	outputfile.write("</td>")
#---------------------------------------------------PDB structure----------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_pdbstru = PDB_structure(v_pdbid)
	for pdbs in v_pdbstru : 
		outputfile.write(pdbs+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")
#-----------------------------------------------Interactions (STRING)------------------------------------------
	print("String...."+'\n')
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	outputfile.write(String_ID(v_idun))
	outputfile.write("<a href='https://string-db.org/api/image/network?identifiers=" + v_idun + "' > " + v_idun + " </a>")
	outputfile.write("</div>")
	outputfile.write("</td>")
#----------------------------------------------------PROSITE id---------------------------------------
	print("prosite...."+'\n')
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_proID = Prosite_ID(v_idun)
	for proID in v_proID : 
		outputfile.write("<a href='https://prosite.expasy.org/"+proID+"'>"+proID+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")
#-----------------------------------------------------PFAM id--------------------------------------
	print("Pfam...."+'\n')
	outputfile.write("<td>") 
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	v_pfamid = Pfam_ID(v_idun)
	outputfile.write("<a href='http://pfam.xfam.org/family/"+v_pfamid+"'>"+v_pfamid+"</a><br>\n")
	outputfile.write("</div>")
	outputfile.write("</td>")
#-----------------------------------------------------PFAM domain----------------------------------------
	outputfile.write("<td>")
	outputfile.write("<div style='height:150px; width = 150px; overflow-x:auto; overflow-y:auto'>")
	outputfile.write(pfam_domain(v_pfamid)+"<br>")
	outputfile.write("</div>")
	outputfile.write("</td>")
	outputfile.write("</tr>")
end_file=open('endresult.html','r')
outputfile.write(end_file.read())
outputfile.write("</html>")

