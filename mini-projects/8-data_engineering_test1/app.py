from __future__ import annotations

from pathlib import Path
import re
import unicodedata
from typing import Any

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "messy_energy_billing_data.csv"
CLEAN_FILE = BASE_DIR / "clean_energy_data.csv"


def remove_accents(value: Any) -> str | None:
    """Normalize text by trimming, title-casing, and removing accents."""
    if pd.isna(value):
        return None
    text = str(value).strip().title()
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def clean_currency(value: Any) -> float | None:
    """Convert mixed BRL currency formats into float values."""
    if pd.isna(value) or str(value).strip() == "":
        return None

    clean_str = re.sub(r"[^\d,\.]", "", str(value))
    if "," in clean_str and "." in clean_str:
        if clean_str.rfind(",") > clean_str.rfind("."):
            clean_str = clean_str.replace(".", "").replace(",", ".")
        else:
            clean_str = clean_str.replace(",", "")
    elif "," in clean_str:
        clean_str = clean_str.replace(",", ".")

    return float(clean_str) if clean_str else None


def clean_consumption(value: Any) -> float | None:
    """Extract numeric energy consumption values from mixed text formats."""
    if pd.isna(value) or str(value).strip().upper() in {"", "N/A", "NAN"}:
        return None

    clean_str = re.sub(r"[^\d\.]", "", str(value))
    try:
        return float(clean_str) if clean_str else None
    except ValueError:
        return None


def clean_categorical(value: Any) -> str | None:
    """Standardize text fields by trimming whitespace and applying title case."""
    if pd.isna(value):
        return None
    return str(value).strip().title()


def normalize_tariff_type(value: Any) -> str | None:
    """Map known tariff variants to a single business-friendly label."""
    cleaned = clean_categorical(value)
    if cleaned is None:
        return None

    mapping: dict[str, str] = {
        "Ind.": "Industrial",
        "Industrial": "Industrial",
        "Comercial": "Commercial",
        "Commercial": "Commercial",
        "Agro": "Agro",
    }
    return mapping.get(cleaned, cleaned)


def clean_status(value: Any) -> str | None:
    """Normalize invoice statuses while preserving unknown values."""
    cleaned = clean_categorical(value)
    if cleaned is None:
        return None

    mapping: dict[str, str] = {
        "Paid": "Paid",
        "Pending": "Pending",
        "Overdue": "Overdue",
        "Processing": "Processing",
    }
    return mapping.get(cleaned, cleaned)


def parse_billing_date(value: Any) -> pd.Timestamp | None:
    """Parse supported billing date formats and leave ambiguous values as NaT."""
    if pd.isna(value) or str(value).strip() == "":
        return None

    text = str(value).strip()
    supported_formats = [
        ("%d/%m/%Y", False),
        ("%d-%m-%Y", False),
        ("%Y/%m/%d", False),
        ("%Y-%m-%d", False),
        ("%m-%d-%Y", False),
        ("%d/%m/%y", False),
    ]

    for fmt, dayfirst in supported_formats:
        parsed = pd.to_datetime(text, format=fmt, errors="coerce", dayfirst=dayfirst)
        if not pd.isna(parsed):
            return parsed

    return None


def get_sites_dimension() -> pd.DataFrame:
    data = {
        "Site_Name": [
            "Uberlandia-Mg",
            "Sao Paulo-Sp",
            "Belo Horizonte-Mg",
            "Rio Verde-Go",
            "Camacari-Ba",
            "Campo Novo-Mt",
        ],
        "Estado": ["MG", "SP", "MG", "GO", "BA", "MT"],
        "Regiao": ["Sudeste", "Sudeste", "Sudeste", "Centro-Oeste", "Nordeste", "Centro-Oeste"],
    }
    return pd.DataFrame(data)


def process_billing_data(input_filepath: Path, output_filepath: Path) -> pd.DataFrame:
    print("Iniciando extracao e limpeza...")
    df = pd.read_csv(input_filepath, skiprows=4)
    df.dropna(how="all", inplace=True)

    # Remove exact duplicate exports, then keep the first occurrence of each invoice id.
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset=["Invoice_ID"], keep="first", inplace=True)

    df["Site_Name"] = df["Site_Name"].apply(remove_accents)
    df["Total_Amount"] = df["Total_Amount"].apply(clean_currency)
    df["Energy_Consumption"] = df["Energy_Consumption"].apply(clean_consumption)
    df["Tariff_Type"] = df["Tariff_Type"].apply(normalize_tariff_type)
    df["Status"] = df["Status"].apply(clean_status)
    df["Billing_Date"] = df["Billing_Date"].apply(parse_billing_date)

    print("Enriquecendo dados com informacoes geograficas...")
    df_sites = get_sites_dimension()
    df = pd.merge(df, df_sites, on="Site_Name", how="left")

    df.sort_values(by=["Billing_Date", "Invoice_ID"], inplace=True, na_position="last")
    df.to_csv(output_filepath, index=False, date_format="%Y-%m-%d")

    print(f"Sucesso! Arquivo enriquecido salvo em: {output_filepath}")
    print(
        "Resumo de qualidade: "
        f"{df['Billing_Date'].isna().sum()} datas invalidas, "
        f"{df['Energy_Consumption'].isna().sum()} consumos ausentes, "
        f"{df['Total_Amount'].isna().sum()} valores ausentes, "
        f"{df['Estado'].isna().sum()} sites sem correspondencia."
    )
    return df


if __name__ == "__main__":
    clean_df = process_billing_data(RAW_FILE, CLEAN_FILE)
