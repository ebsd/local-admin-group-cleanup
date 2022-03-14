# Windows local admin group cleanup

Il s'agit de nettoyer le groupe "administrateurs local" de chaque machine Windows.
En entrée : une liste CSV de machine,compte,domaine AD du compte (inventaire.txt).

```
hostname,user,non_fqdn_userdomain
```

Le fichier vars.py contient mes variables :

```
# local admin username
adminuser = "adminuser"
# local admin user domain
domain = "domain.lan"
```

# Licence

WTFPL