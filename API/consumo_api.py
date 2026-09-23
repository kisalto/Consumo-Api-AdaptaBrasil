import pandas as pd
import requests

STATE = "PR"

# Reestruturado com mapeamento explícito
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


def main():
    links_df = pd.read_csv("API/Data/adaptaBrasilAPIEstrutura.csv", sep="|")

    for desastre, indicadores in ID_STRUCTURE.items():
        all_data = []

        for tipo_indicador, indicator_id in indicadores.items():
            url_series = links_df.loc[
                links_df["id"] == indicator_id, "url_obtem_dados_indicador"
            ]

            if url_series.empty:
                continue

            url = url_series.values[0]

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                df = pd.DataFrame(data if isinstance(data, list) else [data])
                df = df.sort_values(by="name")
                file_name = f"API/output/{desastre}/{tipo_indicador}.csv"
                df.to_csv(file_name, index=False)
                print(f"Gerado: {file_name}")

            except requests.RequestException as e:
                print(f"Erro na requisição: {e}")

        # Salva todos os dados do desastre em um CSV
        if all_data:
            df = pd.DataFrame(all_data)
            df = df.sort_values(by="name")
            df.to_csv(f"API/output/{desastre}/{desastre}.csv", index=False)
            print(f"Arquivo 'API/output/{desastre}/{desastre}.csv' gerado com sucesso!")


if __name__ == "__main__":
    main()