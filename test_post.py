import requests

url = 'http://127.0.0.1:5000/login'
donnees = {'username': 'ddu', 'password': 'p'}

# Envoi de la requête POST
reponse = requests.post(url, data=donnees)

print(reponse.text) # Affichera le retour de votre serveur Flask