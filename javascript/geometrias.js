var fontes=require("users/ruisreis/Tese:lib/lib_fontes");

var par_zona = fontes.PEDROGAO
    ,par_tolerancia = 100
    ,par_adjacente = 300;

// Seleciona a zona ardida
var geo_alvo = fontes.geo_alvo(par_zona, par_tolerancia)
    ,geo_adjacente = fontes.geo_adjacente(geo_alvo.regiao, par_adjacente);


Map.centerObject(geo_adjacente.total);
Map.addLayer(geo_alvo.regiao, {color:"red"}, "Alvo", true);
Map.addLayer(geo_adjacente.total, {color:"blue"}, "Alvo expandido",false);
Map.addLayer(geo_adjacente.regiao, {color:"green"}, "Referência",false);