# Validazione, Modellazione e Arricchimento Dati

Questa applicazione, costruita in python con Streamlit, è progettata per semplificare la gestione e l'analisi delle liste utente esportate dalle sedi tramite un'interfaccia intuitiva.

## Accesso all'Applicazione

L'applicazione è già ospitata e pronta all'uso.

Per accedervi:

1. **Visita l'URL dedicato**.
2. **Inserisci la password**.

## Caratteristiche

- **Caricamento File**: Importa file in formato CSV o Excel direttamente dalla barra laterale.
- **Mappatura Campi**: Associa le colonne del tuo file ai campi richiesti (Nome, Cognome, Sesso, Data di Nascita, Città, Email).
- **Analisi del DataFrame**: Visualizza un'anteprima dei dati e identifica eventuali problemi.
- **Gestione dei Record Anomali**: Scarica i record senza email, con email non valide o duplicate (per la gestione manuale).
- **Formattazione e Modellazione**: Formatta correttamente i campi Nome, Cognome, Città ed Email.
- **Arricchimento dei Dati (Età)**: Aggiunge informazioni addizionali come età in numero intero e gruppo di età di appartenenza.
  - *Minorenni: < 18*
  - *Ragazzi: >= 18 e < 25*
  - *Giovani adulti: >= 25 e < 40*
  - *Adulti: >= 40 e < 60*
  - *Senior: >=60*
- **Arricchimento dei Dati (Località)**: Integra dati sulla località includendo provincia, regione e CAP utilizzando un database dei comuni italiani.
  - *Per le località con CAP multilpli viene sempre applicato un solo CAP in quanto nei dati grezzi non c'è alcun dato utile per il calcolo specifico.
    es. Genova è sempre 16121.*
- **Segmentazione e Download**: Suddivide i dati in segmenti specifici e permette di scaricarli singolarmente o in un archivio ZIP.

## Sicurezza dei Dati

La sicurezza e la privacy dei dati sono una priorità assoluta per questa applicazione. Per garantire la protezione delle informazioni caricate dagli utenti, vengono adottate le seguenti misure:

- **Nessuna memorizzazione dei dati**: Tutti i file caricati dagli utenti vengono processati esclusivamente in memoria durante la sessione attiva.
  Nessun dato viene salvato permanentemente su server, database o altri supporti di archiviazione.

- **Eliminazione automatica**: Al termine della sessione o della chiusura dell'applicazione, tutti i dati elaborati vengono eliminati immediatamente dalla memoria.

- **Nessun log dei risultati**: Gli output generati dall'applicazione, inclusi file elaborati, segmentati o arricchiti, non vengono memorizzati o registrati in alcun modo.

- **Download sicuro**: Gli utenti devono scaricare i dati elaborati direttamente senza alcuna conservazione temporanea sul server.

Queste misure assicurano che le informazioni sensibili rimangano al sicuro e sotto il completo controllo dell'utente utilizzatore, senza alcun rischio di archiviazione non autorizzata.

## Utilizzo dell'Applicazione

### 1. Accedi all'App

- Utilizza il link fornito e inserisci la password per accedere.

### 2. Carica un File

- Vai alla **barra laterale** e utilizza il widget di upload per caricare il tuo file CSV o Excel.

### 3. Mappa le Colonne

- Associa le colonne del tuo file ai campi richiesti tramite i menu a tendina nella barra laterale.

### 4. Analizza e Formatta i Dati

- Visualizza un’anteprima dei dati per verificare la correttezza della mappatura.
- La formattazione automatica correggerà il case dei campi Nome, Cognome, Città e Email.

### 5. Arricchimento dei Dati (Età)

- L'app calcolerà automaticamente l'età in numero intero e assegnerà un gruppo di appartenenza in base a questa.

### 6. Arricchimento dei Dati (Località)

- L'app integra informazioni aggiuntive sulla località, come provincia, regione e CAP, utilizzando il database dei comuni italiani.

### 7. Segmenta e Scarica i Dati

- Visializza i dati segmentati e scaricali singolarmente o come archivio ZIP tramite i pulsanti di download disponibili.

## Dipendenze

L'applicazione utilizza le seguenti librerie Python:

- Python 3.13
- Streamlit
- Pandas
- Plotly Express
- re
- datetime
- io
- zipfile

**Nota**: Come utente finale, non è necessario installare queste dipendenze. L'applicazione è già configurata e ospitata.

## Risoluzione dei Problemi

- **Problemi con le colonne del DataFrame**:
  
  - Assicurati che il file caricato contenga tutte le colonne necessarie (Nome, Cognome, Sesso, Data di Nascita, Città, Email).
  - Verifica che la mappatura delle colonne sia corretta nell'interfaccia di mappatura.

- **Errori durante l'upload del file**:
  
  - Controlla che il file sia in formato CSV o Excel e che non sia corrotto.
  - Verifica la presenza di eventuali errori di formattazione nel file.

## Contatti

Per ulteriori informazioni o assistenza, contatta:

- **Vivoadv**: [https://www.vivoadv.it](https://www.vivoadv.it)
- **Andrea Vaghi**: [https://andreavaghi.it](https://andreavaghi.it)