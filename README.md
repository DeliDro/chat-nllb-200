# cisse-project-nllb-200

## Objectifs

* Chaque utilisateur sélectionne sa langue

* Il peut écrire/recevoir un message

* Les messages sont automatiquement traduits

## Base de données

* ``USERS``:  
    * ``user``: Nom d'utilisateur
    * ``password``: Mot de passe crypté

* ``MESSAGES``:
    * ``id``: Identifiant
    * ``texte``: Contenu
    * ``expediteur``: Celui qui envoie
    * ``destinataire``: Celui qui reçoit
    * ``langue``: Langue utilisée par l'expéditeur

* ``TRADUCTIONS``:
    * ``id``: Identifiant dans ``MESSAGES``
    * ``texte``: Traduction par NLLB-200
    * ``langue``: Langue utilisée par le destinataire


```sql
SELECT m.Id, t.texte, m.expediteur
FROM MESSAGES m, TRADUCTIONS t
WHERE 
    m.destinataire = user
    AND m.id > idDernierMessage
    AND m.id = t.id
```