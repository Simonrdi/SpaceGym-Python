# Space-Gym

Space-Gym è un piccolo progetto web dedicato al mondo della palestra: l'idea è permettere agli utenti di registrarsi, accedere e prenotare uno spazio per allenarsi.

## Un progetto dei miei anni al liceo

Questo progetto è nato quando frequentavo ancora il liceo, prima di iniziare il mio percorso come **Programmatore Informatico presso l'Istituto CEFI**. Rappresenta una delle mie prime esperienze personali con lo sviluppo di un'applicazione web e raccoglie ciò che stavo imparando in quel periodo. È pubblicato così com'era, come testimonianza del mio percorso e dei miei primi esperimenti.

## Funzionalità presenti

- Pagine di presentazione del progetto e galleria di immagini.
- Registrazione e accesso con email e password.
- Accesso tramite Google OAuth.
- Pagina per visualizzare e prenotare uno spazio in una fascia oraria.
- Controllo delle prenotazioni che si sovrappongono.
- Invio di un'email dopo una prenotazione.
- Pagine dedicate agli allenamenti, ancora in lavorazione.

## Tecnologie

- Python e Flask
- SQLite
- HTML e CSS
- Authlib per l'autenticazione Google
- Flask-Mail per l'invio delle email

## Avvio in locale

È necessario avere Python installato. Dalla cartella del progetto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install Flask Authlib Flask-Mail python-dotenv
python flask_app.py
```

Su Windows, per attivare l'ambiente virtuale usare:

```powershell
.venv\Scripts\Activate.ps1
```

Prima di avviare l'applicazione, crea un file `.env` nella cartella del progetto copiando `.env.example` e inserisci le tue credenziali locali. Il file `.env` è escluso da Git; non pubblicarlo né condividerlo.

L'applicazione si avvia con il server di sviluppo Flask. La pagina iniziale è disponibile all'indirizzo `http://127.0.0.1:5000/prova`.

## Note sullo stato del progetto

Si tratta di un progetto didattico e incompleto, non di un'applicazione pronta per l'uso in produzione. Alcune sezioni sono indicate come work in progress e, per usare tutte le funzionalità, servono configurazioni valide per Google OAuth e per il servizio email. Il database SQLite viene creato all'avvio, ma gli spazi prenotabili devono essere presenti nella tabella `spaces`.

## Contesto e scopo

Il repository viene condiviso a scopo personale e didattico, per conservare e mostrare un progetto realizzato prima del mio percorso formativo al CEFI. Il codice e l'interfaccia riflettono lo stato e le conoscenze che avevo in quel momento.

È inoltre prevista una versione aggiornata di Space-Gym, che riprenderà l'idea originale e sarà realizzata con **ASP.NET Core MVC**. Questa futura versione rappresenterà una nuova evoluzione del progetto, sviluppata con competenze e tecnologie diverse.
# SpaceGym-Python
