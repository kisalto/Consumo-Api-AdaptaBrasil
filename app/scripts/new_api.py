from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.painelcidades.adaptabrasil.mcti.gov.br/public/v1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:155.0) Gecko/20100101"
        " Firefox/155.0"
    ),
    "Accept": "application/json",
    "Origin": "https://painelcidades.adaptabrasil.mcti.gov.br",
    "Referer": "https://painelcidades.adaptabrasil.mcti.gov.br/",
}

ID_STRUCTURE = {
    "Deslizamento de terra": {
        "Geral": 60001,
        "Vulnerabilidade": 60002,
        "Exposição": 60003,
        "Ameaça": 60004,
    },
    "Inundações, enxurradas e alagamentos": {
        "Geral": 60041,
        "Vulnerabilidade": 60042,
        "Exposição": 60043,
        "Ameaça": 60044,
    },
    "Risco de estresse hídrico": {
        "Geral": 2,
        "Vulnerabilidade": 3,
        "Exposição": 4,
        "Ameaça": 5,
    },
}


def create_session(max_workers: int = 20) -> requests.Session:
    """Cria e configura uma Session com Retry automático e Pool de conexões ajustado."""
    session = requests.Session()
    session.headers.update(HEADERS)

    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False,
    )

    adapter = HTTPAdapter(
        max_retries=retries,
        pool_connections=max_workers,
        pool_maxsize=max_workers,
    )

    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def sanitize_folder_name(name: str) -> str:
    """Normaliza o nome da pasta removendo acentos/caracteres especiais."""
    replacements = {
        " ": "_",
        ",": "",
        "ã": "a",
        "õ": "o",
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ç": "c",
    }
    name_clean = name.lower()
    for key, val in replacements.items():
        name_clean = name_clean.replace(key, val)
    return name_clean


def get_counties_by_state(
    session: requests.Session, state_code: int = 41
) -> list[dict]:
    """Obtém a lista de municípios do Paraná usando a sessão configurada."""
    url = f"{BASE_URL}/locations/counties/{state_code}"
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_indicator_task(
    session: requests.Session,
    county: dict,
    ameaca: str,
    dimensao: str,
    indicator_id: int,
) -> tuple[str, str, list[dict]]:
    """Busca os dados de um único indicador usando a sessão compartilhada."""
    municipio_id = county["id"]
    municipio_nome = county["name"]
    url = f"{BASE_URL}/indicators/{municipio_id}/value"
    params = {"id": indicator_id}

    records = []
    try:
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        indicators_data = response.json()

        for item in indicators_data:
            legend = next(
                (
                    l
                    for l in item.get("legends", [])
                    if l.get("id") == item.get("legendItemId")
                ),
                None,
            )

            records.append({
                "municipio_id": municipio_id,
                "municipio_nome": municipio_nome,
                "estado_id": county["state"],
                "indicador_id": indicator_id,
                "indicador_nome": item.get("indicatorName"),
                "ano": item.get("year"),
                "valor": item.get("value"),
                "classificacao": legend.get("label") if legend else None,
            })

    except requests.exceptions.RequestException as e:
        print(
            f"Erro ao buscar ID {indicator_id} no município"
            f" {municipio_nome}: {e}"
        )

    return ameaca, dimensao, records


def process_and_save_by_folders(state_code: int = 41, max_workers: int = 20):
    session = create_session(max_workers=max_workers)

    counties = get_counties_by_state(session=session, state_code=state_code)
    print(
        f"Iniciando extração paralela para {len(counties)} municípios (UF"
        f" {state_code})...\n"
    )

    data_store = {}
    for ameaca, dim_dict in ID_STRUCTURE.items():
        for dimensao in dim_dict:
            data_store[(ameaca, dimensao)] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for county in counties:
            for ameaca, dim_dict in ID_STRUCTURE.items():
                for dimensao, indicator_id in dim_dict.items():
                    futures.append(
                        executor.submit(
                            fetch_indicator_task,
                            session,
                            county,
                            ameaca,
                            dimensao,
                            indicator_id,
                        )
                    )

        total_tasks = len(futures)
        print(
            f"Disparadas {total_tasks} requisições com {max_workers} threads"
            " simultâneas e Retry automático habilitado...\n"
        )

        completed = 0
        for future in as_completed(futures):
            ameaca, dimensao, records = future.result()
            data_store[(ameaca, dimensao)].extend(records)
            completed += 1

            if completed % 200 == 0 or completed == total_tasks:
                print(
                    f"Progresso: {completed}/{total_tasks} requisições"
                    " concluídas."
                )

    print("\nSalvando os arquivos CSV organizados...")
    for (ameaca, dimensao), records in data_store.items():
        #folder_name = sanitize_folder_name(ameaca)
        folder_name = ameaca
        output_dir = Path("API/output") / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / f"{dimensao}.csv"
        df = pd.DataFrame(records)
        df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"Arquivo gerado: {file_path}")


if __name__ == "__main__":
    process_and_save_by_folders(state_code=41, max_workers=50)
    print("\nProcesso finalizado com sucesso!")