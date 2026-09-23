from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
ADAPTA_DIR = PROJECT_ROOT / "AdaptaBrasilAPIAccess"
API_DIR = PROJECT_ROOT / "API"


def run_script(script_path: Path, *args: str) -> None:
    command = [sys.executable, str(script_path), *args]
    print(f"\n=== Executando: {' '.join(command)} ===")

    result = subprocess.run(command, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        raise SystemExit(f"Falha ao executar {script_path.name} (código: {result.returncode})")


def main() -> None:
    print("Iniciando fluxo completo do projeto...")

    # 1) Gera a estrutura dos indicadores da API
    run_script(
        ADAPTA_DIR / "AdaptaBrasilAPIAccess.py",
        "--arquivo_saida",
        str(ADAPTA_DIR / "adaptaBrasilAPIEstrutura.csv"),
    )

    # 2) Filtra e organiza os dados em API/Data
    run_script(API_DIR / "coleta_dados.py")

    # 3) Consome a API e salva os CSVs em API/output
    run_script(API_DIR / "consumo_api.py")

    print("\nFluxo concluído com sucesso!")
    print(f"Arquivos gerados em: {API_DIR / 'Data'} e {API_DIR / 'output'}")


if __name__ == "__main__":
    main()
