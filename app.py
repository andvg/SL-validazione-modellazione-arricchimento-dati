# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import re
from datetime import datetime
import io
import zipfile
import hmac

# Configurazione della pagina
st.set_page_config(page_title="Validazione, Modellazione e Arricchimento Dati", layout="wide")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["PW_SECRET"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Non memorizzare la password.
        else:
            st.session_state["password_correct"] = False

    # Restituisce True se la password è validata.
    if st.session_state.get("password_correct", False):
        return True

    # Mostra input per la password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password errata")
    return False

if not check_password():
    st.stop()  # Non continuare se check_password non è True.

# Funzione per caricare il file dei comuni e memorizzarlo nella cache
@st.cache_data
def carica_comuni_db(file_path):
    try:
        comuni_db_data = pd.read_csv(file_path, sep=";")
        comuni_db_data = comuni_db_data.drop_duplicates(subset=['denominazione_ita'])
        # Converti le denominazioni a lowercase per facilitare il matching
        comuni_db_data['denominazione_ita_lower'] = comuni_db_data['denominazione_ita'].str.lower().str.strip()
        return comuni_db_data
    except Exception as e:
        st.error(f"Errore nel caricamento del database comuni: {e}")
        return pd.DataFrame()

# Funzione per caricare il file di dati
def carica_file():
    uploaded_file = st.sidebar.file_uploader("Carica un file (CSV o Excel)", type=['csv', 'xls', 'xlsx', 'xlsm'])
    return uploaded_file

# Funzione per leggere il file caricato
@st.cache_data
def leggi_file(uploaded_file, header_option):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, header=header_option)
        else:
            df = pd.read_excel(uploaded_file, header=header_option)
        # Assicurati che i nomi delle colonne siano tutti stringhe
        df.columns = df.columns.map(str)
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")
        return None

# Funzione per mappare le colonne
def mappatura_colonne(df):
    st.sidebar.subheader("Mapping Columns")
    columns = df.columns.tolist()
    try:
        nome = st.sidebar.selectbox("Seleziona la colonna per 'Nome':", columns, index=columns.index('Nome') if 'Nome' in columns else 0)
        cognome = st.sidebar.selectbox("Seleziona la colonna per 'Cognome':", columns, index=columns.index('Cognome') if 'Cognome' in columns else 1)
        sesso = st.sidebar.selectbox("Seleziona la colonna per 'Sesso':", columns, index=columns.index('Sesso') if 'Sesso' in columns else 2)
        data_nascita = st.sidebar.selectbox("Seleziona la colonna per 'Data di Nascita':", columns, index=columns.index('Data_Nascita') if 'Data_Nascita' in columns else 3)
        citta = st.sidebar.selectbox("Seleziona la colonna per 'Città':", columns, index=columns.index('Città') if 'Città' in columns else 4)
        email = st.sidebar.selectbox("Seleziona la colonna per 'Email':", columns, index=columns.index('Email') if 'Email' in columns else 5)
    except ValueError:
        st.error("Assicurati che le colonne 'Nome', 'Cognome', 'Sesso', 'Data_Nascita', 'Città' e 'Email' esistano nel file caricato.")
        return None
    
    df_mappato = df[[nome, cognome, sesso, data_nascita, citta, email]].copy()
    df_mappato.columns = ['Nome', 'Cognome', 'Sesso', 'Data_Nascita', 'Città', 'Email']
    return df_mappato

# Funzione per formattare i dati dopo la mappatura
def formatta_dati(df):
    st.subheader("Formattazione dei dati")
    
    # Identifica le colonne di tipo stringa
    str_cols = df.select_dtypes(include=['object', 'string']).columns
    
    # Rimuovi spazi superflui nelle colonne di tipo stringa
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
    
    # Formatta Nome, Cognome e Città in Titlecase
    for col in ['Nome', 'Cognome', 'Città']:
        if col in df.columns:
            df[col] = df[col].str.title()
    
    # Formatta Email in lowercase
    if 'Email' in df.columns:
        df['Email'] = df['Email'].str.lower()
    
    # Formatta la Data di Nascita
    df['Data_Nascita'] = pd.to_datetime(df['Data_Nascita'], dayfirst=True, errors='coerce')
    df['Data_Nascita_Formatta'] = df['Data_Nascita'].dt.strftime('%d/%m/%Y')
    
    st.success("Formattazione dati completata!")
    st.dataframe(df.head())
    return df

# Funzione per validare l'email
def valida_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, str(email)))

# Funzione per calcolare l'età
def calcola_eta(data_nascita):
    if pd.isna(data_nascita):
        return None
    try:
        oggi = datetime.today()
        eta = oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))
        return eta
    except:
        return None

# Funzione per calcolare la fascia d'età
def calcola_fascia_eta(eta):
    if pd.isna(eta) or eta is None:
        return 'Sconosciuto'
    elif eta < 18:
        return 'Minorenni'
    elif 18 <= eta < 25:
        return 'Ragazzi'
    elif 25 <= eta < 40:
        return 'Giovani adulti'
    elif 40 <= eta < 60:
        return 'Adulti'
    else:
        return 'Senior'

# Funzione per aggiungere età e gruppo d'età
def aggiungi_eta_e_gruppo(df):
    st.subheader("Calcolo dell'età e gruppo di appartenenza")
    df.loc[:, 'eta'] = df['Data_Nascita'].apply(calcola_eta)
    df.loc[:, 'gruppo_eta'] = df['eta'].apply(calcola_fascia_eta)
    return df

# Funzione per validare i dati
def validazione_dati(df):
    st.subheader("Validazione dei dati")
    
    email_vuote = df['Email'].isna().sum()
    email_non_valide = df['Email'].apply(lambda x: not valida_email(x) if pd.notna(x) else False).sum()
    duplicati_email = df[df['Email'].notna()]['Email'].duplicated(keep=False).sum()
    duplicati_email_nome_cognome = df.dropna(subset=['Email', 'Nome', 'Cognome']).duplicated(subset=['Email', 'Nome', 'Cognome'], keep=False).sum()
    
    invalid_data_nascita = df['Data_Nascita'].isna().sum()
    
    condizione_scaricabili_email = (
        df['Email'].notna() & (
            df['Email'].apply(lambda x: not valida_email(x)) |
            df['Email'].duplicated(keep=False)
        )
    )
    scaricabili_data_email = df[condizione_scaricabili_email].copy()
    numero_scaricabili_email = scaricabili_data_email.shape[0]
    
    condizione_scaricabili_no_email = df['Email'].isna()
    scaricabili_data_no_email = df[condizione_scaricabili_no_email].copy()
    numero_scaricabili_no_email = scaricabili_data_no_email.shape[0]
    
    condizione_lavorabili = ~condizione_scaricabili_email & ~condizione_scaricabili_no_email
    lavorabili_data = df[condizione_lavorabili].copy()
    numero_lavorabili = lavorabili_data.shape[0]
    
    # Presentazione dei risultati in una tabella senza indici
    validation_results = pd.DataFrame({
        "Categoria": [
            "Email vuote",
            "Email non valide",
            "Duplicati Email",
            "Duplicati Email, Nome, Cognome",
            "Data di nascita non valida",
            "Record lavorabili",
            "Record scaricabili (con Email)",
            "Record scaricabili (senza Email)"
        ],
        "Numero di record": [
            email_vuote,
            email_non_valide,
            duplicati_email,
            duplicati_email_nome_cognome,
            invalid_data_nascita,
            numero_lavorabili,
            numero_scaricabili_email,
            numero_scaricabili_no_email
        ]
    })
    
    st.table(validation_results.style.hide(axis="index"))
    
    # Creazione dei grafici in colonne
    col1, col2 = st.columns(2)
    
    with col1:
        crea_grafico_analisi_dettagliata({
            'Email vuota': email_vuote,
            'Email non valida': email_non_valide,
            'Duplicati Email': duplicati_email,
            'Data nascita non valida': invalid_data_nascita
        })
    
    with col2:
        crea_grafico_gestione_manuale({
            'Lavorabili': numero_lavorabili,
            'Scaricabili con Email': numero_scaricabili_email,
            'Scaricabili senza Email': numero_scaricabili_no_email
        })
    
    # Download dei file
    with st.expander("Scarica i record per la gestione manuale"):
        if not scaricabili_data_email.empty:
            st.download_button(
                label='Scarica data_manuale_email.csv',
                data=scaricabili_data_email.to_csv(index=False).encode('utf-8'),
                file_name='data_manuale_email.csv',
                mime='text/csv'
            )
        
        if not scaricabili_data_no_email.empty:
            st.download_button(
                label='Scarica data_manuale_no_email.csv',
                data=scaricabili_data_no_email.to_csv(index=False).encode('utf-8'),
                file_name='data_manuale_no_email.csv',
                mime='text/csv'
            )
    
    return lavorabili_data

# Funzione per creare grafici di analisi dettagliata
def crea_grafico_analisi_dettagliata(analisi_dettagliata):
    fig = px.bar(
        x=list(analisi_dettagliata.keys()),
        y=list(analisi_dettagliata.values()),
        labels={'x': 'Tipo di record', 'y': 'Numero di record'},
        title='Problemi nei record',
        text=list(analisi_dettagliata.values())
    )
    fig.update_traces(marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Funzione per creare grafici di gestione manuale
def crea_grafico_gestione_manuale(gestione_manuale):
    fig = px.bar(
        x=list(gestione_manuale.keys()),
        y=list(gestione_manuale.values()),
        labels={'x': 'Tipo di record', 'y': 'Numero di record'},
        title='Lavorabili e gestione manuale',
        text=list(gestione_manuale.values())
    )
    fig.update_traces(marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'], textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Funzione per mappare le informazioni dei comuni
@st.cache_data
def map_comune_info(lavorabili_data, comuni_db_data):
    # Creazione mappe per provincia e regione
    lavorabili_data.loc[:, 'citta_lower'] = lavorabili_data['Città'].str.lower().str.strip()
    
    # Creazione dei dizionari per mappare le informazioni
    mappa_provincia = dict(zip(comuni_db_data['denominazione_ita_lower'], comuni_db_data['denominazione_provincia']))
    mappa_regione = dict(zip(comuni_db_data['denominazione_ita_lower'], comuni_db_data['denominazione_regione']))
    mappa_cap = dict(zip(comuni_db_data['denominazione_ita_lower'], comuni_db_data['cap']))
    
    # Aggiunta delle nuove colonne utilizzando le mappe con .loc
    lavorabili_data.loc[:, 'provincia'] = lavorabili_data['citta_lower'].map(mappa_provincia)
    lavorabili_data.loc[:, 'regione'] = lavorabili_data['citta_lower'].map(mappa_regione)
    
    # Assegna il CAP e convertilo esplicitamente a stringa
    lavorabili_data.loc[:, 'cap'] = lavorabili_data['citta_lower'].map(mappa_cap).apply(
        lambda x: str(int(x)) if pd.notna(x) else None
    )
    
    # Rimuoviamo la colonna ausiliaria 'citta_lower'
    lavorabili_data = lavorabili_data.drop(columns=['citta_lower'])
    
    # Aggiungi la colonna 'residente_citta' usando .loc
    lavorabili_data.loc[:, 'residente_citta'] = lavorabili_data['Città'].str.lower().str.strip() == lavorabili_data['provincia'].str.lower().str.strip()
    
    # Identifica le città non trovate
    citta_non_trovate = lavorabili_data[lavorabili_data['provincia'].isna()]['Città'].unique()
    if len(citta_non_trovate) > 0:
        st.warning("Le seguenti città non sono state trovate nel database dei comuni e non hanno informazioni su Provincia, Regione e CAP:")
        st.write(citta_non_trovate)
    
    return lavorabili_data

# Funzione per creare grafici di distribuzione delle province
def crea_grafico_distribuzione_province(lavorabili_data):
    # Definire le province di interesse
    provincie_interessate = ['Genova', 'Savona', 'La Spezia', 'Imperia']
    altra_provincia = lavorabili_data[~lavorabili_data['provincia'].isin(provincie_interessate)]
    
    # Funzione per calcolare i conteggi
    def calcola_conteggi(data, column, values):
        return {value: data[data[column] == value].shape[0] for value in values}
    
    # Calcolare il numero di record per ciascuna provincia
    provincie = ['Altra provincia'] + provincie_interessate
    conteggi_province = {
        'Altra provincia': altra_provincia.shape[0],
        **calcola_conteggi(lavorabili_data, 'provincia', provincie_interessate)
    }
    
    # Creare il grafico per le province
    fig = px.bar(
        x=list(conteggi_province.keys()),
        y=list(conteggi_province.values()),
        labels={'x': 'Provincia', 'y': 'Numero di record'},
        title='Distribuzione dei record per Provincia',
        text=list(conteggi_province.values()),
        color=list(conteggi_province.keys()),
        color_discrete_sequence=['#9467bd', '#1f77b4', '#2ca02c', '#d62728', '#ff7f0e']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Funzione per creare grafici di distribuzione residente_citta
def crea_grafico_distribuzione_residente(lavorabili_data):
    # Definire le province di interesse
    provincie_interessate = ['Genova', 'Savona', 'La Spezia', 'Imperia']
    combinazioni_residente = {
        'Genova Città': ('Genova', True),
        'Genova Prov': ('Genova', False),
        'Savona Città': ('Savona', True),
        'Savona Prov': ('Savona', False),
        'La Spezia Città': ('La Spezia', True),
        'La Spezia Prov': ('La Spezia', False),
        'Imperia Città': ('Imperia', True),
        'Imperia Prov': ('Imperia', False)
    }
    
    # Calcolare i conteggi
    conteggi_residente = {
        label: lavorabili_data[
            (lavorabili_data['provincia'] == provincia) & 
            (lavorabili_data['residente_citta'] == residente)
        ].shape[0]
        for label, (provincia, residente) in combinazioni_residente.items()
    }
    
    # Creare il grafico per provincia e residente_citta
    fig = px.bar(
        x=list(conteggi_residente.keys()),
        y=list(conteggi_residente.values()),
        labels={'x': 'Provincia e Residente Città', 'y': 'Numero di record'},
        title='Distribuzione dei record per Provincia e Residente_Citta',
        text=list(conteggi_residente.values()),
        color=list(conteggi_residente.keys()),
        color_discrete_sequence=['#1f77b4', '#1f77b4', '#2ca02c', '#2ca02c', '#d62728', '#d62728', '#ff7f0e', '#ff7f0e']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Funzione per creare i bottoni di download
def crea_bottoni_download(lavorabili_data):
    st.subheader("Download dei segmenti di dati")
    
    # Definisci le province di interesse
    provincie_interessate = ['Genova', 'Savona', 'La Spezia', 'Imperia']
    
    # Segmento: fuori Liguria
    data_fuori_liguria = lavorabili_data[~lavorabili_data['provincia'].isin(provincie_interessate)]
    if not data_fuori_liguria.empty:
        csv_fuori_liguria = data_fuori_liguria.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Scarica data_fuori_liguria.csv',
            data=csv_fuori_liguria,
            file_name='data_fuori_liguria.csv',
            mime='text/csv'
        )
    
    # Definisci le combinazioni per le province e residente_citta
    combinazioni = {
        'data_ge_citta.csv': ('Genova', True),
        'data_ge_prov.csv': ('Genova', False),
        'data_sv_citta.csv': ('Savona', True),
        'data_sv_prov.csv': ('Savona', False),
        'data_sp_citta.csv': ('La Spezia', True),
        'data_sp_prov.csv': ('La Spezia', False),
        'data_im_citta.csv': ('Imperia', True),
        'data_im_prov.csv': ('Imperia', False)
    }
    
    # Crea un dizionario per raccogliere le coppie nome file e dati
    segmenti = {}
    for file_name, (provincia, residente) in combinazioni.items():
        segmento = lavorabili_data[
            (lavorabili_data['provincia'] == provincia) & 
            (lavorabili_data['residente_citta'] == residente)
        ]
        if not segmento.empty:
            segmenti[file_name] = segmento
    
    # Organizza i bottoni di download in un accordion
    with st.expander("Scarica segmenti specifici"):
        for file_name, segmento in segmenti.items():
            csv_data = segmento.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f'Scarica {file_name}',
                data=csv_data,
                file_name=file_name,
                mime='text/csv'
            )
    
    # Bottone "Scarica Tutto" fuori dall'accordion
    if len(segmenti) > 0:
        with st.spinner('Preparazione del file ZIP...'):
            # Crea un buffer BytesIO per il file ZIP
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_name, segmento in segmenti.items():
                    zipf.writestr(file_name, segmento.to_csv(index=False))
            # Resetta il puntatore del buffer
            buffer.seek(0)
            st.download_button(
                label='Scarica tutto',
                data=buffer,
                file_name='segmenti_dati.zip',
                mime='application/zip'
            )
    else:
        st.info("Non ci sono segmenti di dati disponibili per il download.")

# Funzione principale
def main():
    # Carica il file
    uploaded_file = carica_file()
    if uploaded_file is not None:
        # Chiedi se il file ha l'intestazione
        has_header = st.sidebar.radio("Il file caricato ha una riga di intestazione?", ('Sì', 'No'))
        header_option = 0 if has_header == 'Sì' else None
        
        with st.spinner('Caricamento del file...'):
            df = leggi_file(uploaded_file, header_option)
        
        if df is not None:
            if has_header == 'No':
                df.columns = [f'Colonna_{i}' for i in range(1, len(df.columns) + 1)]
            
            st.header("Anteprima dei dati")
            st.dataframe(df.head())
            
            with st.spinner('Mappatura delle colonne...'):
                df_mappato = mappatura_colonne(df)
                if df_mappato is None:
                    st.error("Errore durante la mappatura delle colonne. Assicurati di selezionare correttamente tutte le colonne richieste.")
                    return
            
            with st.spinner('Formattazione dei dati...'):
                df_mappato = formatta_dati(df_mappato)
            
            with st.spinner('Calcolo dell\'Età e del gruppo di appartenenza...'):
                df_mappato = aggiungi_eta_e_gruppo(df_mappato)
                st.header("Dataframe con Età e Gruppo di Età")
                st.dataframe(df_mappato.head())
            
            with st.spinner('Validazione dei dati...'):
                lavorabili_data = validazione_dati(df_mappato)
            
            # --- Inizio Arricchimento Dati ---
            st.header("Arricchimento dei dati con informazioni dei comuni")
            
            # Carica il database dei comuni
            comuni_db_file_path = 'service/gi_comuni_cap.csv'  # Aggiorna il percorso se necessario
            comuni_db_data = carica_comuni_db(comuni_db_file_path)
            
            if not comuni_db_data.empty:
                with st.spinner('Arricchimento dei dati con provincia e regione...'):
                    lavorabili_data = map_comune_info(lavorabili_data, comuni_db_data)
                    st.success("Arricchimento dati completato!")
                    st.header("Dataframe arricchito")
                    st.dataframe(lavorabili_data.head())
                
                # Creazione dei grafici di distribuzione
                with st.spinner('Creazione dei grafici di distribuzione...'):
                    col1, col2 = st.columns(2)
                    with col1:
                        crea_grafico_distribuzione_province(lavorabili_data)
                    with col2:
                        crea_grafico_distribuzione_residente(lavorabili_data)
                
                # --- Inizio Creazione dei Bottoni di Download ---
                with st.spinner('Preparazione dei bottoni di download...'):
                    crea_bottoni_download(lavorabili_data)
            else:
                st.error("Il database dei comuni non è stato caricato correttamente.")
        
        else:
            st.error("Impossibile caricare il file. Per favore verifica il formato e riprova.")
    else:
        # Mostra le informazioni guidate quando nessun file è caricato
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                readme_content = f.read()
            st.markdown(readme_content)
        except FileNotFoundError:
            st.error("README.md non trovato. Per favore assicurati che il file README.md sia presente nella directory dell'app.")
        except Exception as e:
            st.error(f"Errore nella lettura di README.md: {e}")

if __name__ == "__main__":
    main()
