import requests

""" la funcio rep la url que posi l'usuari per connectar-se i buscar missatges d'error greus en la pagina
i extreure informacio del servidor oculta als headers. si a l'informacio del servidor es troben headers
com el server o el x-powered-by es perillos ja que informen sobre el software que s'utilitza  i el llenguatge
de programacio, llavors la funcio ho imprimeix perque es una fuga d'info
"""
def analisis_headers(url):
	try:
		resposta = requests.get(url) #per obtindre el contingut de la url
		headers = resposta.headers #aixo llegeix les dades tecniques ocultes
		missatges_error = resposta.text #per obtindre el codi html visible
		errors_greus = ["Internal Server Error", "Fatal Error", "Syntax Error"] #perque la busca sigui especifica d'errors greus

		print("- RESULTAT D'ERRORS TROBATS -")
		for error in errors_greus:
			if error in missatges_error:
				print("ALERTA, error trobat:", error) #que imprimeixi si es troba un error greu nomes
		print("- RESULTAT D'INFORMACIO DEL SERVIDOR -")
		for key,value in headers.items():
			if key.lower() == 'server' or key.lower() == 'x-powered-by':
				print(key,value)
	except:
		print("error, no s'ha pogut connectar, torna a escriure la url")

url = input("introdueix la url a analitzar: ") 
analisis_headers(url)