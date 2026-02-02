RECURSOS_DISPONIBLES = [
    {
        "nombre":"Sala Central",
        "requiere":[],
        "excluye":["Sala pequeña","Area abierta"]
    },
    {
        "nombre":"Sala pequeña",
        "requiere":[],
        "excluye":["Sala Central","Area Abierta"]
    },
    {
        "nombre":"Area Abierta",
        "requiere":[],
        "excluye":["Sala Central","Sala pequeña"]
    },
    {
        "nombre":"Sistema de sonido",
        "requiere":["Sala Central"],
        "excluye":[]
    },
    {
        "nombre":"Proyector",
        "requiere":["Sala Central"],
        "excluye":["Area Abierta"]
    },
    {
        "nombre":"Pizarra",
        "requiere":[],
        "excluye":[]
    },
    {
        "nombre":"Moderador",
        "requiere":[],
        "excluye":[]
    },
    {
        "nombre":"Tecnico de Sonido",
        "requiere":["Sistema de Sonido"],
        "excluye":[]
    },
    {
        "nombre":"Camara de Grabacion",
        "requiere":["Sala Central","Sistema de Sonido"],
        "excluye":[]
    }
]