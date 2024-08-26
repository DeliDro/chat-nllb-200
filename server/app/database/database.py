"""
Module pour la gestion des utilisateurs dans la base de données
"""
import os
import sqlite3
import bcrypt

# Obtenir le répertoire de travail actuel
current_directory = os.getcwd()

# Chemin complet vers la base de données dans le répertoire actuel
DB_PATH = os.path.join(current_directory, "volumes/sql",'messagerie.db')

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
            inactif BOOLEAN,
        );
    ''')

    # Création de la table MESSAGES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MESSAGES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT NOT NULL,
            expediteur TEXT NOT NULL,
            destinataire TEXT NOT NULL,
            langue TEXT NOT NULL,
            FOREIGN KEY(expediteur) REFERENCES USERS(user),
            FOREIGN KEY(destinataire) REFERENCES USERS(user)
        );
    ''')

    # Création de la table TRADUCTIONS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TRADUCTIONS (
            id INTEGER,
            texte TEXT NOT NULL,
            langue TEXT NOT NULL,
            FOREIGN KEY(id) REFERENCES MESSAGES(id)
        );
    ''')

    # Validation des modifications
    conn.commit()

    # Fermeture de la connexion
    conn.close()

    print("La base de données et les tables ont été créées avec succès.")

def creer_utilisateur(user, password):
    # Cryptage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO USERS (user, password) VALUES (?, ?);
        ''', (user, hashed_password))
        conn.commit()
        return True  # Indique que l'utilisateur a été créé avec succès
    except sqlite3.IntegrityError:
        return False  # Indique que l'utilisateur existe déjà
    finally:
        conn.close()

def verifier_identifiants(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Récupérer le mot de passe crypté depuis la base de données pour l'utilisateur donné
        cursor.execute('SELECT password FROM USERS WHERE user = ?', (username,))
        result = cursor.fetchone()
        
        if result is None:
            return False  # L'utilisateur n'existe pas
        
        # Récupération du mot de passe crypté
        hashed_password = result[0]
        
        # Vérification du mot de passe en utilisant bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True  # Le mot de passe est correct
        else:
            return False  # Le mot de passe est incorrect
    finally:
        conn.close()

# Fonction pour ajouter un message
def ajouter_message(texte, expediteur, destinataire, langue):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO MESSAGES (texte, expediteur, destinataire, langue) 
            VALUES (?, ?, ?, ?);
        ''', (texte, expediteur, destinataire, langue))
        conn.commit()
        return True  # Indique que le message a été ajouté avec succès
    except sqlite3.IntegrityError:
        return False  # Indique qu'une erreur s'est produite (par exemple, clé étrangère invalide)
    finally:
        conn.close()

# Fonction pour ajouter une traduction
def ajouter_traduction(message_id, texte_traduit, langue):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO TRADUCTIONS (id, texte, langue) 
            VALUES (?, ?, ?);
        ''', (message_id, texte_traduit, langue))
        conn.commit()
        return True  # Indique que la traduction a été ajoutée avec succès
    except sqlite3.IntegrityError:
        return False  # Indique qu'une erreur s'est produite (par exemple, message non existant)
    finally:
        conn.close()