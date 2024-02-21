## Freesound Client

Un esempio di programma che permette di scaricare tracce audio da [Freesound](https://www.freesound.org) utlizzando delle parole chiavi di ricerca.

**DISCLAIMER**
La libreria ufficiale che implementa le funzionalità di questa repository è [freesound-python](https://github.com/MTG/freesound-python). Questa implementazione è stata sviluppata per scopi didattici.

#### Guida
Questo software dipende dalle librerie `requests` e `python-dotenv` che possono essere installate globalmente o localmente (in un ambiente virtuale `venv`) con il seguente comando:

```
pip install -r requirements.txt
```
oppure
```
pip3 install -r requirements.txt
```
Prima di iniziare aprite il file `.env`. Questo file potrebbe essere nascosto dal vostro sistema operativo per la presenza di un `.` davanti al nome. 
Una volta aperto il file è sufficiente modificare 2 informazioni:

```py
API_KEY=<your-api-key>
USER_ID=<your-user-id>
```
Entrambe queste informazioni posso essere copiate o generate da questa pagina: [https://freesound.org/apiv2/apply/](https://freesound.org/apiv2/apply/)
Per applicare è necessario essere registrati al sito.

per usare il programma lanciare:
```shell
python main.py
```
oppure
```shell
python3 main.py
```