"""
Module pour la gestion des utilisateurs dans la base de données
"""
import os
import sqlite3
import bcrypt
import requests
import json

# Obtenir le répertoire de travail actuel
current_directory = os.getcwd()

# Chemin complet vers la base de données dans le répertoire actuel
DB_PATH = os.path.join(current_directory, "../../volumes/sql",'messagerie.db')
print(DB_PATH)

def init_database():

    # Connexion à la base de données SQLite
    # Si la base de données n'existe pas, elle sera créée.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Création de la table USERS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            user TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            langue VARCHAR(10),
            fonction VARCHAR(100),
            departement VARCHAR(100),
            pays VARCHAR(50),
            actif BOOLEAN DEFAULT TRUE
        );
    ''')

    # Création de la table MESSAGES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MESSAGES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT NOT NULL,
            expediteur TEXT NOT NULL,
            destinataire TEXT NOT NULL,
            FOREIGN KEY(expediteur) REFERENCES USERS(user),
            FOREIGN KEY(destinataire) REFERENCES USERS(user)
        );
    ''')

    # Création de la table TRADUCTIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TRADUCTIONS (
            id INTEGER,
            texte TEXT NOT NULL,
            FOREIGN KEY(id) REFERENCES MESSAGES(id)
        );
    ''')

    # Validation des modifications
    conn.commit()

    # Fermeture de la connexion
    conn.close()

    print("La base de données et les tables ont été créées avec succès.")

def creer_utilisateur(user, password, langue, fonction, departement, pays):
    # Cryptage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT
            INTO USERS (user, password, langue, fonction, departement, pays)
            VALUES (?, ?, ?, ?, ?, ?);
        ''', (user, hashed_password, langue, fonction, departement, pays))
        conn.commit()
        return True  # Indique que l'utilisateur a été créé avec succès
    except sqlite3.IntegrityError:
        return False  # Indique que l'utilisateur existe déjà
    finally:
        conn.close()

def verifier_identifiants(user, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Récupérer le mot de passe crypté depuis la base de données pour l'utilisateur donné
        cursor.execute('SELECT password, langue, fonction, departement, pays FROM USERS WHERE user = ?', (user,))
        result = cursor.fetchone()
        
        if result is None:
            return {}  # L'utilisateur n'existe pas
        
        # Récupération du mot de passe crypté
        hashed_password = result[0]
        
        # Vérification du mot de passe en utilisant bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return {
                "user": user,
                "langue": result[1],
                "fonction": result[2],
                "departement": result[3],
                "pays": result[4]
            }  # Le mot de passe est correct
        else:
            return {}  # Le mot de passe est incorrect
    finally:
        conn.close()

def chercher_derniers_messages(user, id_dernier_message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Récupérer le mot de passe crypté depuis la base de données pour l'utilisateur donné
        cursor.execute(
            'SELECT M.id, M.expediteur, T.texte '
            'FROM Messages M, Traductions T '
            'WHERE M.destinataire = ? AND M.id > ? AND M.id = T.id',
            (user, id_dernier_message)
        )
        result = cursor.fetchall()

        return result
    
    except sqlite3.Error as e:
        print("ERROR:", e)

    finally:
        conn.close()
    
    return []

def ajouter_message(texte, expediteur, destinataire):
    conn = sqlite3.connect(DB_PATH)

    try:
        # Début de la transaction
        conn.execute('BEGIN')

        # Créer un message
        conn.execute('''
            INSERT INTO MESSAGES (texte, expediteur, destinataire) 
            VALUES (?, ?, ?);
        ''', (texte, expediteur, destinataire))

        # Retrouver l'id du message créé
        last_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        # Déterminé la langue du destinataire
        langue_destinataire = get_langue(destinataire)

        # Traduction du message
        traduction = traduire(
            texte = texte,
            langue_source = get_langue(expediteur),
            langue_cible = langue_destinataire
        )

        # Ajouter la tradcution dans la BD
        conn.execute('''
            INSERT INTO TRADUCTIONS (id, texte) 
            VALUES (?, ?);
        ''', (last_id, traduction))
        
        # Intégration cohérente de toutes les informations Message + Traduction
        conn.commit()
        
        return True  # Indique que le message a été ajouté avec succès
    
    except sqlite3.Error as e:
        # Rollback si la transaction a échoué
        conn.rollback()
        print("ERROR:", e)
    
    finally:
        conn.close()

def traduire(texte, langue_source, langue_cible):
    headers = {"Content-Type": "application/json"}
    
    try:
        payload = {
            "texte": texte,
            "langue_source": langue_source,
            "langue_cible": langue_cible,
        }

        # Réponse de l'appel POST pour la traduction
        response = requests.post(
            "http://localhost:8090/traduire",
            headers = headers,
            data = json.dumps(payload)
        )
        
        # Vérification de la réponse
        response.raise_for_status()  # Erreur si la réponse n'est pas de type 2XX
        
        # Lecture de la réponse
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print("ERROR:", e)
        return None

def get_langue(user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT langue FROM USERS WHERE user = ?", (user,))
        result = cursor.fetchone()[0]
        
        return result  # Indique que le message a été ajouté avec succès
    
    except sqlite3.Error as e:
        # Rollback the transaction if there's an error
        conn.rollback()
        print("ERROR:", e)
    
    finally:
        conn.close()

    return ""

if __name__ == "__main__":
    init_database()

    creer_utilisateur(
        user = "test@test.com",
        password = "1234",
        langue = "en",
        fonction = "SPM",
        departement = "Log",
        pays = "USA"
    )

    creer_utilisateur(
        user = "semirat216@gmail.com",
        password = "1234",
        langue = "fr",
        fonction = "Alt DA",
        departement = "DS2P",
        pays = "France"
    )

    ajouter_message(
        texte = "Bonjour, comment va la famille ?",
        expediteur = "semirat216@gmail.com",
        destinataire = "test@test.com"
    )

    a = chercher_derniers_messages(
        "test@test.com",
        0
    )
    print(a)