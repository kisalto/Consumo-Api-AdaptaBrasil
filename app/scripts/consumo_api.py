from pathlib import Path
import pandas as pd
import requests

STATE = "PR"

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
    links_df = pd.read_csv("./input/adaptaBrasilAPIEstrutura.csv", sep="|")

    for desastre, indicadores in ID_STRUCTURE.items():
        all_data = []

        # 1. Cria o repositório/diretório para o desastre atual
        output_dir = Path(f"./output/{desastre}")
        output_dir.mkdir(parents=True, exist_ok=True)

        for tipo_indicador, indicator_id in indicadores.items():
            url_series = links_df.loc[
                links_df["id"] == indicator_id, "url_obtem_dados_indicador"
            ]

            if url_series.empty:
                print(f"URL não encontrada para o ID {indicator_id}")
                continue

            url = url_series.values[0]

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                raw_data = data if isinstance(data, list) else [data]

                # Salva o CSV individual do indicador
                df = pd.DataFrame(raw_data)
                if "name" in df.columns:
                    df = df.sort_values(by="name")

                file_name = output_dir / f"{tipo_indicador}.csv"
                df.to_csv(file_name, index=False)
                print(f"Gerado: {file_name}")

                # 2. Adiciona os dados e a tag da dimensão para a consolidação final
                for item in raw_data:
                    item_copy = item.copy()
                    item_copy["tipo_indicador"] = tipo_indicador
                    all_data.append(item_copy)

            except requests.RequestException as e:
                print(f"Erro na requisição para {tipo_indicador} ({url}): {e}")

        # 3. Salva a consolidação com todos os dados do desastre
        if all_data:
            df_consolidado = pd.DataFrame(all_data)
            if "name" in df_consolidado.columns:
                df_consolidado = df_consolidado.sort_values(by="name")

            consolidado_file = output_dir / f"{desastre}.csv"
            df_consolidado.to_csv(consolidado_file, index=False)
            print(f"Arquivo consolidado gerado: {consolidado_file}\n")


if __name__ == "__main__":
    main()