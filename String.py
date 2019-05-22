import fileinput, re 
import requests, sys
import json


#--------------------------------String-------------------------------------------
def String_ID(v_idun) : 
	link = "<iframe src='https://string-db.org/api/image/network?identifiers=" + v_idun + "' > " + v_idun + " </iframe>"
	return link
	
		
		
