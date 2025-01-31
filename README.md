# Validazione, Modellazione e Arricchimento Dati

"Validazione, Modellazione e Arricchimento Dati" è un'applicazione, costruita con Streamlit, progettata per semplificare la gestione e l'analisi delle liste utente esportate dalle sedi tramite un'interfaccia intuitiva.

## Accesso all'Applicazione

L'applicazione è già ospitata e pronta all'uso. Per accedervi:

1. **Visita l'URL dedicato**.
2. **Inserisci la password**.

## Caratteristiche

- **Caricamento File**: Importa file in formato CSV o Excel direttamente dalla barra laterale.
- **Mappatura Campi**: Associa le colonne del tuo file ai campi richiesti (Nome, Cognome, Sesso, Data di Nascita, Città, Email).
- **Analisi del DataFrame**: Visualizza un'anteprima dei dati e identifica eventuali problemi.
- **Gestione dei Record Anomali**: Scarica i record senza email, con email non valide o duplicate.
- **Formattazione e Modellazione**: Formatizza correttamente i campi Nome, Cognome, Città ed Email.
- **Arricchimento dei Dati (Età)**: Aggiunge informazioni aggiuntive come età in numero intero e gruppo di età di appartenenza.
- **Arricchimento dei Dati (Località)**: Integra dati sulla località includendo provincia, regione e CAP utilizzando un database dei comuni italiani.
- **Segmentazione e Download**: Suddivide i dati in segmenti specifici e permette di scaricarli singolarmente o in un archivio ZIP.

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

- L'app calcolerà automaticamente l'età e assegnerà un gruppo di appartenenza in base a questa.

### 6. Arricchimento dei Dati (Località)

- Integra informazioni aggiuntive sulla località, come provincia, regione e CAP, utilizzando il database dei comuni italiani.

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