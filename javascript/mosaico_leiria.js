var fontes=require("users/ruisreis/Tese:lib/lib_fontes");

var par_zona = fontes.LEIRIA
    ,par_tolerancia = 100                   // Tolerância de simplificação da geometria (em metros)
    ,par_adjacente = 300                    // Largura da zona adjacente à zona de estudo
    ,par_visualizacao = {
      min: 0.0,
      max: 0.3*10000,
      bands: ['B4', 'B3', 'B2'],
      opacity: 0.5
    };

// Seleciona a zona ardida
var geo_alvo = fontes.geo_alvo(par_zona, par_tolerancia)
    ,geo_adjacente = fontes.geo_adjacente(geo_alvo.regiao, par_adjacente);

// Varrimentos de dia 03-05-2019
var i1=ee.Image("COPERNICUS/S2/20190503T113329_20190503T113326_T29SMD")
    ,i2=ee.Image("COPERNICUS/S2/20190503T113329_20190503T113326_T29SND")
    ,i3=ee.Image("COPERNICUS/S2/20190503T113329_20190503T113326_T29TME")
    ,i4=ee.Image("COPERNICUS/S2/20190503T113329_20190503T113326_T29TNE");

Map.centerObject(geo_adjacente.total);
Map.addLayer(geo_adjacente.total,{color:"red"},"Zona",true);
Map.addLayer(i1, par_visualizacao, "I1", true);
Map.addLayer(i2, par_visualizacao, "I2", false);
Map.addLayer(i3, par_visualizacao, "I3", false);
Map.addLayer(i4, par_visualizacao, "I4", false);