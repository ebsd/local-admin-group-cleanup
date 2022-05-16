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

## Troubleshooting

### IndexError

Attention, il ne faut aucun \newline à la fin du fichier inventaire.txt, sinon :

```
    host = row[0]
IndexError: list index out of range
```

### KErberos error

Le domaine est case sensitive dans vars.py, mieux vaut utiliser les majuscules. Sinon, selon la config de /etc/krb5.conf, le ticket ne sera pas "retouvé".

```
Error:authGSSClientInit() failed: (('Unspecified GSS failure.  Minor code may provide more information', 851968), ("Can't find client principal xxxx@domain.lan in cache collection", -1765328243))
```


## Licence

WTFPL