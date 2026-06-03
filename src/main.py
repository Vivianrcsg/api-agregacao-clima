from fastapi import FastAPI, HTTPException
from datetime import datetime
import requests

app = FastAPI()

# --------------------
# HEALTH CHECK
# --------------------
@app.get("/api/v1/health")
def health():

    return {
        "status": "healthy",
        "versao": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# --------------------
# CLIMA POR CIDADE
# --------------------
@app.get("/api/v1/clima/{nome_cidade}")
def obter_clima(nome_cidade: str):

    if len(nome_cidade.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail={
                "erro": True,
                "codigo": "NOME_INVALIDO",
                "mensagem": "O nome da cidade deve conter pelo menos 2 caracteres",
                "nome_informado": nome_cidade
            }
        )

    try:

        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={nome_cidade}&count=1&language=pt&format=json"
        )

        geo_resp = requests.get(geo_url)

        if geo_resp.status_code != 200:
            raise HTTPException(
                status_code=503,
                detail={
                    "erro": True,
                    "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                    "mensagem": "Erro ao consultar geolocalização"
                }
            )

        dados_geo = geo_resp.json()

        if "results" not in dados_geo:
            raise HTTPException(
                status_code=404,
                detail={
                    "erro": True,
                    "codigo": "CIDADE_NAO_ENCONTRADA",
                    "mensagem": "Nenhuma cidade encontrada com o nome informado",
                    "nome_informado": nome_cidade
                }
            )

        cidade = dados_geo["results"][0]

        latitude = cidade["latitude"]
        longitude = cidade["longitude"]

        clima_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&current_weather=true"
        )

        clima_resp = requests.get(clima_url)

        if clima_resp.status_code != 200:
            raise HTTPException(
                status_code=503,
                detail={
                    "erro": True,
                    "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
                    "mensagem": "Erro ao consultar clima"
                }
            )

        clima = clima_resp.json()

        return {
            "nome": cidade["name"],
            "estado": cidade.get("admin1", ""),
            "clima": {
                "temperatura": clima["current_weather"]["temperature"],
                "velocidade_vento": clima["current_weather"]["windspeed"]
            },
            "consultado_em": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "erro": True,
                "codigo": "SERVICO_EXTERNO_INDISPONIVEL"
            }
        )


# --------------------
# CIDADES POR ESTADO
# --------------------
@app.get("/api/v1/cidades/{sigla_uf}")
def listar_cidades(sigla_uf: str, limite: int = 10):

    if len(sigla_uf) != 2:
        raise HTTPException(
            status_code=400,
            detail={
                "erro": True,
                "codigo": "SIGLA_UF_INVALIDA",
                "mensagem": "A sigla do estado deve conter exatamente 2 letras",
                "sigla_uf_informada": sigla_uf
            }
        )

    url = (
        f"https://servicodados.ibge.gov.br/api/v1/"
        f"localidades/estados/{sigla_uf.upper()}/municipios"
    )

    resposta = requests.get(url)

    if resposta.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail={
                "erro": True,
                "codigo": "UF_NAO_ENCONTRADA",
                "mensagem": "Estado com a sigla informada não foi encontrado",
                "sigla_uf_informada": sigla_uf
            }
        )

    cidades = resposta.json()

    return {
        "uf": sigla_uf.upper(),
        "quantidade_retornada": min(limite, len(cidades)),
        "cidades": [
            {"nome": c["nome"]}
            for c in cidades[:limite]
        ],
        "consultado_em": datetime.utcnow().isoformat()
    }
