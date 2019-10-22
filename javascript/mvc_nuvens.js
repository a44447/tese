var fontes=require("users/ruisreis/Tese:lib/lib_fontes");

var par_zona = fontes.PEDROGAO
    ,par_tolerancia = 100
    ,par_adjacente = 300    ,par_categorias = fontes.CLC_VEGETACAO;

// Seleciona a zona ardida
var geo_alvo = fontes.geo_alvo(par_zona, par_tolerancia)
    ,geo_adjacente = fontes.geo_adjacente(geo_alvo.regiao, par_adjacente)
    ,par_inicio = ee.Date(geo_alvo.data)
    ,par_fim = ee.Date(new Date());

// Cobertura da superfície
var map_alvo = fontes.img_cobertura(geo_alvo.regiao, par_categorias)
    ,map_adjacente = fontes.img_cobertura(geo_adjacente.regiao, par_categorias);

// Compósitos
var c1=fontes.img_ndvi("NDVI", geo_alvo.regiao, map_alvo, ee.Date.fromYMD(2017,9,24), ee.Date.fromYMD(2017,10,4))
        .max()
        .visualize({ bands:["NDVI"], min:0, max:1, palette: fontes.PALETTE_NDVI, forceRgbOutput:true}),
    c2=fontes.img_ndvi("NDVI", geo_adjacente.regiao, map_adjacente, ee.Date.fromYMD(2017,9,24), ee.Date.fromYMD(2017,10,4))
        .max()
        .visualize({ bands:["NDVI"], min:0, max:1, palette: fontes.PALETTE_NDVI, forceRgbOutput:true});

Map.centerObject(geo_adjacente.total);
Map.addLayer(c1, null, "MVC1", true);
Map.addLayer(c2, null, "MVC2", false);