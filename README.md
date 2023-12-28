## Freesound Client

Un esempio di programma che permette di scaricare tracce audio da [Freesound](https://www.freesound.org) utlizzando delle parole chiavi di ricerca.

**DISCLAIMER**
La libreria ufficiale che implementa le funzionalità di questa repository è [freesound-python](https://github.com/MTG/freesound-python). Questa implementazione è stata sviluppata a scopi didattici.

*Questo software non dipende da nessuna libreria.*

#### Guida
Per utilizzare questo software è sufficiente modificare 2 informazioni all'interno del file `main.py`

```py
API_KEY = "R3Lr87TlcOtRKr6nF7Vn4mwrM7yweskqFAuP6XUV"
USER_ID = "7P2hZ9y6CkbGhVYWrgFr"
```
Entrambe queste informazioni posso essere copiate o generate da questa pagina: [https://freesound.org/apiv2/apply/](https://freesound.org/apiv2/apply/)
Per applicare è necessario essere registrati al sito.

È possibile inoltre modificare la cartella dove verrano scaricati i file audio individuati con la ricerca, modificando la variabile `out_folder` nel file `main.py`. Il valore di default è:
```py
out_folder = "sound_lib/"
```

per usare il programma lanciare:
```shell
python main.py
```
oppure
```shell
python3 main.py
```

È possibile interrompere l'esecuzione del programma in qualsiasi momento con la combinazione di tasti `Ctrl+c` (comando valido sia per Windows che per MacOS)