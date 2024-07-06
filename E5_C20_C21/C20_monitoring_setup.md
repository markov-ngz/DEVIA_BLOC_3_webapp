# Procédure d'installation et de configuration de la solution de monitoring

## 1. Lancement des applications 
<b>En local sur une machine avec docker installé : </b>

1. Télécharger le fichier demo/docker-compose.yml du répertoire
2. En gardant le même réseau, configurer les images/volumes <b>des applications utilisées</b> pour correspondre au besoin 
3. Dans le répertoire courant , créer un dossier prometheus
4. C/C les fichiers alert_prometheus.yml et prometheus.yml
5. Modifier les fichiers pour faire correspondre aux besoins ( DNS ...)
6. Créer un fichier .prom_pwd et mettez-y votre mot de passe pour vous authentifier auprès de votre application
7. Lancer les conteneurs avec la commande ```docker compose up -d ```



## 2. Configuration des applications

### 2.1 Prometheus 
Vérifier la bonne configuration de Prometheus avec l'application : 
nom d'utilisateur par défaut :  <br>
mot de passe par défaut :   

Les métriques de votre application doivent pour voir être visualisées comme telle : 


### 2.2 Grafana 
admin mot de passe
lien avec prometheus 
lien avec docker
tableau de bord