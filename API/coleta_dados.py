import pandas as pd

dados = pd.read_csv('AdaptaBrasilAPIAccess/adaptaBrasilAPIEstrutura.csv', sep='|')
dados = dados[["id", "nome", "url_obtem_dados_indicador", "setor_estrategico"]].copy()
dados = dados.sort_values(by="id")

# Indices de riscos setoriais
sectoral_risk = dados[dados['setor_estrategico'] == 'Recursos Hídricos'].copy()
sectoral_risk = sectoral_risk.sort_values(by="id")

# Desastres Geo-hidrologicos
GeoHydrological_Disasters = dados[dados['setor_estrategico'] == 'Desastres Geo-hidrológicos'].copy()
GeoHydrological_Disasters = GeoHydrological_Disasters.sort_values(by="id")

dados.to_csv('API/Data/adaptaBrasilAPIEstrutura.csv', sep='|', index=False)
sectoral_risk.to_csv('API/Data/sectoral_risk.csv', sep='|', index=False)
GeoHydrological_Disasters.to_csv('API/Data/GeoHydrological_Disasters.csv', sep='|', index=False)