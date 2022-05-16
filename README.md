# Windows local admin group cleanup

Il s'agit de nettoyer le groupe "administrateurs local" de chaque machine Windows.
En entrée : une liste CSV de machine,compte,domaine AD du compte (inventaire.txt).

```
hostname,user,non_fqdn_userdomain
```

Le fichier `vars.py` contient mes variables :

```
# local admin username
adminuser = "adminuser"
# local admin user domain
domain = "domain.lan"
```

## Démarrage auto

Via un cron, acviter le venv. La 1ère ligne correspond à la variable PATH qui doit être utilisée dans crond. Sans cette variable PATH, le script ne saura où est situé la commande fping.

```
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
36 09 16 5 * source ~/python/check-hotfixes/python3.9/bin/activate && cd ~/python/local-admin-group-cleanup && python3.9 local-admin-grp-cleanup.py
```


## Licence

WTFPL