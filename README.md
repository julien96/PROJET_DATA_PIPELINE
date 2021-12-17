# PROJET_DATA_PIPELINE


TRAVAUX EFFECTUÉS

Réalisé par : 
-Julien ALI
-Zayd YOUMIR
-Ossama BOUGNINE
-Enguerran MARTINET

Partie Spark:
1-Nous utilisons la commande spark/bin/spark-submit fichier.py pour executer nos jobs spark . 
2-Dans le job spark python nous préparons les données (nettoyage des données, suppression des doublons, valeurs aberrantes, jointure/croisement des sources de données, changement de type, nom des colonnes, etc …)

Partie Nifi:
1-La commande : bin/nifi.sh start nous permet de lancer le service nifi 
2-Ensuite on accède à la page web nifi grâce à https:localhost:8443/nifi qui nous dirige vers la page de login.
3-Nous avons un processeur GetFile qui récupère les données qui sont ensuite dirigé vers un flow de processeur qui fait une vérification sur les données .
4-Une fois les données traitées elles sont dirigées vers kafka.

Partie kafka :
1- Lancer le service zookeeper : quant à lui, assure la gestion de la configuration distribuée, ainsi que la coordination des brokers et le suivi de l’état des services gravitants autour de Kafka.

2- Lancer le service kafka broker : Les brokers servent de pivot entre les différents services. Ils sauvegardent les données qui transitent, tout en assurant une redondance des données afin d’avoir une forte tolérance aux pannes.

3-Créer les topic ValidatedRecords et RejectedRecords : un topic correspond à une unité logique contenant des messages d’une même catégorie.Afin de limiter la contention lors des actions d’écriture et de lecture, un topic est décomposé en partitions assurant un maximum de parallélisme. Le nombre maximum de consommateur agissant en simultané est directement corrélé au maximum de partitions configurées.
pour notre cas on a choisi des topics de 3 partitions.

-	sur nifi on a travaillé par les processeurs consummeKafka et publishKafka pour consommer nos données de nifi dans deux topics ( valid et invalid data ) et les publier dans un fichier HDFS


Partie AIRFLOW : 
1-Nous définissons le répertoire de airflow avec la commande :
export AIRFLOW_HOME=airflow
2-Ensuite nous démarrons notre airflow avec la commande :
airflow standalone
3-Dans le dossier dags nous laissons notre code python contenant nos tasks à exécuter .
4-Nous accédons à notre page web airflow après le login avec l’url:
https://localhost:8080
5-Enfin nous activons nos dags

Partie NifiRegistry : 

1-Nous avons créé un repository sur Github, puis généré le Personal access token.
2-Nous allons cloner le repository dans le dossier Nifi-Registry.
3-Nous modifions le fichier Nifi-registry/conf/providers.xml, et plus précisément la partie flowPersistenceProvider pour mettre nos informations github. Ainsi, les buckets seront enregistré dans notre repository github au lieu de s’enrigster en local.
4-Nous créons un nouveau bucket sur nifi-registry.
5-Nous allons configurer un nouveau registry client sur Nifi pour faire le versionning dans ce bucket.
6-Et finalement, quand on commence le versionning sur un process group, ce dernier va être directement commit dans le Github.

