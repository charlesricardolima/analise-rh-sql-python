from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"

QUERY_01 = DATA_DIR / "query_01.csv"
QUERY_02 = DATA_DIR / "query_02.csv"


def carregar_dados() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega os CSVs exportados das consultas SQL."""
    df_salarios = pd.read_csv(QUERY_01)
    df_regioes = pd.read_csv(QUERY_02)
    return df_salarios, df_regioes


def diagnostico(nome: str, df: pd.DataFrame) -> None:
    """Exibe informações básicas para a análise exploratória."""
    print(f"\n{'=' * 72}")
    print(f"DIAGNÓSTICO - {nome}")
    print("=" * 72)
    print(f"Linhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}")
    print(f"Duplicados: {df.duplicated().sum()}")

    print("\nTipos de dados:")
    print(df.dtypes)

    print("\nValores ausentes:")
    nulos = pd.DataFrame(
        {
            "quantidade": df.isna().sum(),
            "percentual": (df.isna().mean() * 100).round(2),
        }
    )
    print(nulos)

    print("\nEstatísticas descritivas:")
    print(df.describe(include="all").transpose())


def estatisticas_salariais(df: pd.DataFrame) -> pd.Series:
    """Calcula média, mediana, mínimo e máximo dos salários."""
    salarios = df["SALARY"]

    resumo = pd.Series(
        {
            "media": salarios.mean(),
            "mediana": salarios.median(),
            "minimo": salarios.min(),
            "maximo": salarios.max(),
        }
    )

    print(f"\n{'=' * 72}")
    print("ESTATÍSTICAS SALARIAIS")
    print("=" * 72)
    print(f"Média:   {resumo['media']:.2f}")
    print(f"Mediana: {resumo['mediana']:.2f}")
    print(f"Mínimo:  {resumo['minimo']:.2f}")
    print(f"Máximo:  {resumo['maximo']:.2f}")

    return resumo


def analise_por_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa salários por departamento."""
    resumo = (
        df.dropna(subset=["DEPARTMENT_NAME"])
        .groupby("DEPARTMENT_NAME")["SALARY"]
        .agg(["count", "mean", "median", "min", "max"])
        .sort_values("mean", ascending=False)
        .round(2)
    )

    print(f"\n{'=' * 72}")
    print("SALÁRIOS POR DEPARTAMENTO")
    print("=" * 72)
    print(resumo)
    print(
        f"\nFuncionários sem departamento informado: "
        f"{df['DEPARTMENT_NAME'].isna().sum()}"
    )

    return resumo


def analise_por_cargo(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa salários por cargo."""
    resumo = (
        df.groupby("JOB_TITLE")["SALARY"]
        .agg(["count", "mean", "median", "min", "max"])
        .sort_values("mean", ascending=False)
        .round(2)
    )

    print(f"\n{'=' * 72}")
    print("SALÁRIOS POR CARGO")
    print("=" * 72)
    print(resumo)

    return resumo


def analise_por_regiao(df: pd.DataFrame) -> pd.DataFrame:
    """Resume funcionários e salários por região."""
    resumo = (
        df.groupby("REGION_NAME")
        .agg(
            funcionarios=("EMPLOYEE_ID", "count"),
            salario_medio=("SALARY", "mean"),
            salario_mediano=("SALARY", "median"),
            salario_minimo=("SALARY", "min"),
            salario_maximo=("SALARY", "max"),
        )
        .sort_values("funcionarios", ascending=False)
        .round(2)
    )

    print(f"\n{'=' * 72}")
    print("FUNCIONÁRIOS E SALÁRIOS POR REGIÃO")
    print("=" * 72)
    print(resumo)

    return resumo


def gerar_graficos(
    df_salarios: pd.DataFrame,
    resumo_departamentos: pd.DataFrame,
    resumo_regioes: pd.DataFrame,
) -> None:
    """Gera e salva os gráficos do projeto."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    sns.histplot(df_salarios["SALARY"], bins=12, kde=True)
    plt.title("Distribuição dos salários")
    plt.xlabel("Salário")
    plt.ylabel("Quantidade de funcionários")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "distribuicao_salarial.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 4))
    sns.boxplot(x=df_salarios["SALARY"])
    plt.title("Boxplot dos salários")
    plt.xlabel("Salário")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "boxplot_salarios.png", dpi=160)
    plt.close()

    salarios_departamento = resumo_departamentos["mean"].sort_values()
    plt.figure(figsize=(10, 7))
    plt.barh(salarios_departamento.index, salarios_departamento.values)
    plt.title("Salário médio por departamento")
    plt.xlabel("Salário médio")
    plt.ylabel("Departamento")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "salario_medio_departamento.png", dpi=160)
    plt.close()

    funcionarios_regiao = resumo_regioes["funcionarios"].sort_values()
    plt.figure(figsize=(8, 5))
    plt.barh(funcionarios_regiao.index, funcionarios_regiao.values)
    plt.title("Quantidade de funcionários por região")
    plt.xlabel("Quantidade de funcionários")
    plt.ylabel("Região")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "funcionarios_regiao.png", dpi=160)
    plt.close()

    salario_regiao = resumo_regioes["salario_medio"].sort_values()
    plt.figure(figsize=(8, 5))
    plt.barh(salario_regiao.index, salario_regiao.values)
    plt.title("Salário médio por região")
    plt.xlabel("Salário médio")
    plt.ylabel("Região")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "salario_medio_regiao.png", dpi=160)
    plt.close()

    print(f"\nGráficos salvos em: {IMAGES_DIR}")


def main() -> None:
    df_salarios, df_regioes = carregar_dados()

    print("Arquivos carregados com sucesso.")
    print(f"Query 1: {len(df_salarios)} registros")
    print(f"Query 2: {len(df_regioes)} registros")

    diagnostico("QUERY 1 - SALÁRIOS", df_salarios)
    diagnostico("QUERY 2 - REGIÕES", df_regioes)

    estatisticas_salariais(df_salarios)
    resumo_departamentos = analise_por_departamento(df_salarios)
    analise_por_cargo(df_salarios)
    resumo_regioes = analise_por_regiao(df_regioes)

    gerar_graficos(df_salarios, resumo_departamentos, resumo_regioes)


if __name__ == "__main__":
    main()
