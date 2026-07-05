"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import zipfile
import os
import pandas as pd
import glob
def procesar_un_zip(ruta_zip, carpeta_salida):
    '''with archivo_zip.open(ruta_interna) as f:
        texto_completo = f.read().decode('utf-8').strip()
    registro = {
        "phrase": texto_completo,  # Tu requerimiento: el texto va aquí
        "sentiment": hijo          # ¡Aquí usas el nombre de la carpeta hijo! (e.g., 'positive')
    }
                            
    # 5. CLASIFICACIÓN: Dependiendo del padre, lo mandas a una lista o a la otra
    if padre == 'train':
        datos_train.append(registro)
    elif padre == 'test':
        datos_test.append(registro)

    if not os.path.exists(carpeta_donde_guardar):
        os.makedirs(carpeta_donde_guardar)
        
    # Convertimos la lista de TRAIN en su CSV correspondiente
    if datos_train:
        df_train = pd.DataFrame(datos_train)
        ruta_train_csv = os.path.join(carpeta_donde_guardar, "train_dataset.csv")
        df_train.to_csv(ruta_train_csv, index=False, encoding='utf-8')
        print(f"¡Creado!: {ruta_train_csv} con {len(df_train)} filas.")
        
    # Convertimos la lista de TEST en su CSV correspondiente
    if datos_test:
        df_test = pd.DataFrame(datos_test)
        ruta_test_csv = os.path.join(carpeta_donde_guardar, "test_dataset.csv")
        df_test.to_csv(ruta_test_csv, index=False, encoding='utf-8')
        print(f"¡Creado!: {ruta_test_csv} con {len(df_test)} filas.")'''


def clean_campaign_data():
    output_dir = os.path.join("files", "output")
    os.makedirs(output_dir, exist_ok=True)

    client_frames = []
    campaign_frames = []
    economics_frames = []

    lista_zips = glob.glob(os.path.join("files", "input", "*.zip"))
    for ruta_zip in lista_zips:
        with zipfile.ZipFile(ruta_zip) as archivo_zip:
            miembros = archivo_zip.namelist()
            if not miembros:
                continue
            with archivo_zip.open(miembros[0]) as archivo_csv:
                df = pd.read_csv(archivo_csv, encoding="utf-8")

        df_client = df[
            [
                "client_id",
                "age",
                "job",
                "marital",
                "education",
                "credit_default",
                "mortgage",
            ]
        ].copy()
        df_campaign = df[
            [
                "client_id",
                "number_contacts",
                "contact_duration",
                "previous_campaign_contacts",
                "previous_outcome",
                "campaign_outcome",
                "month",
                "day",
            ]
        ].copy()
        df_economics = df[
            ["client_id", "cons_price_idx", "euribor_three_months"]
        ].copy()

        df_client["job"] = (
            df_client["job"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace("-", "_", regex=False)
        )
        df_client["education"] = (
            df_client["education"]
            .astype(str)
            .str.replace(".", "_", regex=False)
            .replace("unknown", pd.NA)
        )
        df_client["credit_default"] = df_client["credit_default"].apply(
            lambda x: 1 if str(x).strip().lower() == "yes" else 0
        )
        df_client["mortgage"] = df_client["mortgage"].apply(
            lambda x: 1 if str(x).strip().lower() == "yes" else 0
        )

        df_campaign["previous_outcome"] = df_campaign["previous_outcome"].apply(
            lambda x: 1 if str(x).strip().lower() == "success" else 0
        )
        df_campaign["campaign_outcome"] = df_campaign["campaign_outcome"].apply(
            lambda x: 1 if str(x).strip().lower() == "yes" else 0
        )
        month_mapping = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }
        df_campaign["month"] = (
            df_campaign["month"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(month_mapping)
        )
        df_campaign["last_contact_date"] = pd.to_datetime(
            {
                "year": 2022,
                "month": df_campaign["month"],
                "day": df_campaign["day"],
            }
        ).dt.strftime("%Y-%m-%d")
        df_campaign = df_campaign[
            [
                "client_id",
                "number_contacts",
                "contact_duration",
                "previous_campaign_contacts",
                "previous_outcome",
                "campaign_outcome",
                "last_contact_date",
            ]
        ]

        client_frames.append(df_client)
        campaign_frames.append(df_campaign)
        economics_frames.append(df_economics)

    if client_frames:
        pd.concat(client_frames, ignore_index=True).to_csv(
            os.path.join(output_dir, "client.csv"), index=False, encoding="utf-8"
        )
    if campaign_frames:
        pd.concat(campaign_frames, ignore_index=True).to_csv(
            os.path.join(output_dir, "campaign.csv"), index=False, encoding="utf-8"
        )
    if economics_frames:
        pd.concat(economics_frames, ignore_index=True).to_csv(
            os.path.join(output_dir, "economics.csv"), index=False, encoding="utf-8"
        )

    return

"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    


if __name__ == "__main__":
    clean_campaign_data()
