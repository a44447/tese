var fontes=require("users/ruisreis/Tese:lib/lib_fontes");

var par_zona = fontes.PEDROGAO
    ,par_tolerancia = 100
    ,par_adjacente = 300
    ,par_categorias = fontes.CLC_VEGETACAO;

// Seleciona a zona ardida
var geo_alvo = fontes.geo_alvo(par_zona, par_tolerancia)
    ,geo_adjacente = fontes.geo_adjacente(geo_alvo.regiao, par_adjacente);

// Cobertura da superfície
var map_alvo = fontes.img_cobertura(geo_alvo.regiao, par_categorias, true)
    ,map_adjacente = fontes.img_cobertura(geo_adjacente.regiao, par_categorias, true);

Map.centerObject(geo_adjacente.total);
Map.addLayer(map_alvo, fontes.VIS_CLC, "CLC1", true);
Map.addLayer(map_adjacente, fontes.VIS_CLC, "CLC2", false);