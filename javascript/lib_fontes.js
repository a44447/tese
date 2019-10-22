var CLC = { floresta: { folhosas: 23, coniferas: 24 ,mista: 25 },
            mato: { prado: 26, charneca: 27, pasto: 28, arbusto: 29 }}
    ,CLC_MATO = [CLC.mato.prado, CLC.mato.charneca, CLC.mato.pasto, CLC.mato.arbusto]
    ,CLC_FLORESTA = [CLC.floresta.folhosas, CLC.floresta.coniferas, CLC.floresta.mista]
    ,CLC_VEGETACAO = CLC_MATO.concat(CLC_FLORESTA)
    ,PALETTE_NDVI = [ "FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", "99B718",
                      "74A901", "66A000", "529400", "3E8601", "207401", "056201",
                      "004C00", "023B01", "012E01", "011D01", "011301"]
    ,PALETTE_CLC =  [ "FFFFFF", "E6004D", "FF0000", "CC4DF2", "CC0000", "E6CCCC",
                      "E6CCE6", "A600CC", "A64DCC", "FF4DFF", "FFA6FF", "FFE6FF",
                      "FFFFA8", "FFFF00", "E6E600", "E68000", "F2A64D", "E6A600",
                      "E6E64D", "FFE6A6", "FFE64D", "E6CC4D", "F2CCA6", "80FF00",
                      "00A600", "4DFF00", "CCF24D", "A6FF80", "A6E64D", "A6F200",
                      "E6E6E6", "CCCCCC", "CCFFCC", "000000", "A6E6CC", "A6A6FF",
                      "4D4DFF", "CCCCFF", "E6E6FF", "A6A6E6", "00CCF2", "80F2E6",
                      "00FFA6", "A6FFE6", "E6F2FF"];

exports.PEDROGAO = "BL4171577";
exports.LEIRIA = "BL4172371";
exports.PALETTE_NDVI = PALETTE_NDVI;
exports.PALETTE_CLC =  PALETTE_CLC;
exports.VIS_CLC = { min:0, max: PALETTE_CLC.length-1, palette: PALETTE_CLC }
exports.CLC = CLC;
exports.CLC_MATO = CLC_MATO;
exports.CLC_FLORESTA = CLC_FLORESTA;
exports.CLC_VEGETACAO = CLC_VEGETACAO; 
/*
  |----------------------------------------------------------
  | Seleciona a área ardida
  |----------------------------------------------------------
  | identificador - Identificado na base de dados do ICN
  | tolerancia - Tolerância de simplificação (metros)
  |----------------------------------------------------------
*/
exports.geo_alvo = function(identificador, tolerancia)
{
  var area_ardida = ee.FeatureCollection("users/ruisreis/AreasArdidas-2017-031002018-ETRS89PTTM06")
    ,area_alvo = area_ardida.filter(
                  // Selecciona o incêndio
                  ee.Filter.eq("Cod_SGIF",identificador))
    // Obtém a geometria do incêndio, primeira ocorrência
    ,geo_alvo = area_alvo.first().geometry();

  if(tolerancia>0)
  {
    // Simplifica a geometria, dada uma tolerância
    geo_alvo = geo_alvo.simplify(tolerancia);
  }
  return { regiao: geo_alvo, data: ee.Date(area_alvo.first().get("DHInicio").getInfo().substr(0,10)), alvo: area_alvo };
}

/*
  |----------------------------------------------------------
  | Define uma área adjacente à geometria indicada
  |----------------------------------------------------------
  | area - Geometria da área alvo
  | distancia - Distância (metros)
  |----------------------------------------------------------
*/
exports.geo_adjacente = function(alvo, distancia)
{
    var geo_portugal = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
                        .filter(
                          ee.Filter.and(
                          ee.Filter.eq("country_co", "PO"),
                          ee.Filter.eq("country_na", "Portugal")))
        ,erro = ee.ErrorMargin(distancia,"meters");
    
    var total = alvo
                //.simplify(distancia)
                //.dissolve(erro) 
                // Alarga a geometria do incêndio, dada uma distância linear
                //.convexHull()
                .buffer(distancia, erro)
                // Vamos garantir que excluímos zonas de mar junto à costa
                .intersection(geo_portugal);
    var regiao = total
                // Queremos apenas a área adjacente, retirar a geometria indicada
                .difference(alvo.simplify(distancia));
    
    return {regiao: regiao, total: total};
}

/*
  |----------------------------------------------------------
  | Obtém a cobertura da área alvo
  |----------------------------------------------------------
  | alvo - Geometria da área alvo
  | categorias - Categorias de cobertura a considerar
  |----------------------------------------------------------
*/
exports.img_cobertura = function(alvo, categorias, valores)
{
  var img_clc2012 = ee.ImageCollection("COPERNICUS/CORINE/V18_5_1/100m")
                      // Vamos trabalhar com o CLC de 2012
                      .filter(ee.Filter.eq("system:index","2012"))
                      // Garantir a unicidade da imagem
                      .first()
                      // Recorta a área
                      .clip(alvo);

  if(categorias!==null && Array.isArray(categorias))
  {
    var buf_cat = "";
    for(var index=0;index<categorias.length;index++)
    {
      if(index!==0) { buf_cat += " || "; }
      buf_cat += 'clc==' + categorias[index];
    }
    
    // Seleciona as categorias indicadas
    var img_clc2012_mask = img_clc2012.expression(buf_cat, { clc:img_clc2012.select("landcover") });
  }
  
  // Apenas queremos saber se existe uma das categorias
  if(typeof(valores)!="undefined" && valores)
    return img_clc2012.select("landcover").mask(img_clc2012_mask);
  else
    return img_clc2012_mask
}

/*
  |----------------------------------------------------------
  | Colecção de imagens de Sentinel-2
  |----------------------------------------------------------
  | regiao - Geometria da área a considerar
  | incio - Data inicial
  | fim - Data final
  |----------------------------------------------------------
*/
exports.img_col = function(regiao, inicio, fim) { return s2_col(regiao, inicio, fim); }

/*
  |----------------------------------------------------------
  | Obtém os valores de NDVI para uma dada máscara e datas
  |----------------------------------------------------------
  | regiao - Geometria da área a considerar
  | mascara - Imagem com valores (0-Ignorar e 1-Seleccionar)
  | inicio - Data inicio
  | fim - Data fim
  |----------------------------------------------------------
*/
exports.img_ndvi = function(nome, regiao, mascara, inicio, fim)
{
  // Imagens do Sentinel 2
  return s2_col(regiao, inicio, fim)
          .map(s2_ndvi_map(nome, regiao, mascara));
}

exports.img_ndvi_add = function(nome, regiao, mascara)
{
  return function(imagem)
  {
    return imagem.addBands(s2_ndvi(nome, regiao, mascara,imagem))
  }
}

/*
  |----------------------------------------------------------
  | Map que adiciona a uma imagem uma série temporal base
  |----------------------------------------------------------
  | constante - termo constante
  | tempo - meses após a origem
  | origem - data origem para cálculo do tempo
  | imagem - imagem a tratar
  |----------------------------------------------------------
*/
exports.img_ts_base = function(constante, tempo, origem)
{
  return function(imagem)
  {
    var data = ee.Date(imagem.get("system:time_start"))
        ,ano = data.difference(origem, "month");
    return imagem.addBands(ee.Image.constant(ano).float().rename(tempo))
            .addBands(ee.Image.constant(1).rename(constante))
            .set(tempo,ano);
  }
}

/*
  |----------------------------------------------------------
  | Série temporal harmónica
  |----------------------------------------------------------
  | tempo - Nome da banda com informação de tempo
  | sufixo - Sufixo a aplicar às variáveis independentes
  | frequencia - Frequência do ciclo
  |----------------------------------------------------------
*/
exports.img_ts_harmonica = function(tempo, cos, sin, frequencia)
{
  return function(imagem)
  {
    var radianos = imagem.select(tempo).multiply(2 * Math.PI * frequencia);
    return imagem
            .addBands(radianos.cos().rename(cos))
            .addBands(radianos.sin().rename(sin));
  }
}

/*
  |----------------------------------------------------------
  | Map que adiciona a uma imagem as bandas auxiliares para o
  | cálculo logaritmico
  |----------------------------------------------------------
  | inicial - diferença entre o NDVI do alvo e o de referência na
  |           data do incêncio
  | referencia - valor NDVI de referência
  | nome - nome da banda com o NDVI de referência
  | imagem - imagem a tratar
  |----------------------------------------------------------
*/
exports.img_ts_ln = function(inicial, referencia)
{
  return function(imagem)
  {
    return imagem.addBands(ee.Image.constant(referencia).float().rename("NDVI_RE"))
            .addBands(imagem
              .expression("(O-R)/A", {
                O: imagem.select("NDVI_AO")
                ,R: imagem.select("NDVI_RO")
                ,A: inicial
              })
              .log()
              .rename("y"));
  }
}

/*
  |----------------------------------------------------------
  | Regressão linear
  |----------------------------------------------------------
  | coleccao - Colecção de imagens a considerar
  | dependente - Nome da variável dependente
  | independentes - Nome das variáveis inddependentes 
  |----------------------------------------------------------
*/
exports.img_reg_linear = function (colecao, dependente, independentes)
{
  var regressor = colecao.select(independentes.concat([dependente]))
                    .reduce(ee.Reducer.linearRegression(independentes.length, 1))
      ,coeficientes = regressor.select("coefficients")
                      .arrayProject([0])
                      .arrayFlatten([independentes]);
  return {regressor:regressor, coeficientes:coeficientes};
}

/*
  |----------------------------------------------------------
  | Estimador de regressão linear
  |----------------------------------------------------------
  | independentes - Nome das variáveis inddependentes 
  | coeficiente - Coeficientes da regressão
  | nome - Nome da banda
  |----------------------------------------------------------
*/
exports.img_est_linear = function(independentes, coeficientes, nome)
{
  return function(imagem)
  {
    return imagem.addBands(
              imagem.select(independentes)
                .multiply(coeficientes)
                .reduce(ee.Reducer.sum())
              .rename(nome));
  }
}

/*
  |----------------------------------------------------------
  | Estimador de regressão linear - logaritmica
  |----------------------------------------------------------
  | independentes - Nome das variáveis inddependentes 
  | coeficiente - Coeficientes da regressão
  | nome - Nome da banda
  |----------------------------------------------------------
*/
exports.img_est_ln = function(independentes, coeficientes, a)
{
  return function(imagem)
  {
    return imagem.addBands(
              imagem.select(independentes)
                .multiply(coeficientes)
                .reduce(ee.Reducer.sum())
                //.exp()
                //.multiply(ee.Image.constant(a).float())
                //.add(imagem.select("NDVI_RE"))
              .rename("NDVI_AE"));
  }
}

/*
  |----------------------------------------------------------
  | Colecção de imagens de Sentinel-2
  |----------------------------------------------------------
  | regiao - Geometria da área a considerar
  | incio - Data inicial
  | fim - Data final
  |----------------------------------------------------------
*/
function s2_col(regiao, inicio, fim)
{
  // Imagens do Sentinel 2
  return ee.ImageCollection('COPERNICUS/S2')
          .filter(ee.Filter.and(
            // Apenas as imagens com menos de 20% de nuvens
            ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)
            // Na região seleccionada
            ,ee.Filter.bounds(regiao)
            // Filtra as datas de inicio e fim
            ,ee.Filter.date(inicio, fim)));
}

function s2_ndvi_map(nome, regiao, mascara)
{
  return function(imagem)
  {
    return s2_ndvi(nome, regiao, mascara, imagem);
  }
}
/*
  |----------------------------------------------------------
  | Calcula NDVI a partir de uma imagem de Sentinel-2
  |----------------------------------------------------------
  | nome - Nome da banda calculada
  | regiao - Geometria da área a considerar
  | mascara - Imagem que define a área a filtrar
  | imagem - Imagem de Sentinel-2
  |----------------------------------------------------------
*/
function s2_ndvi(nome, regiao, mascara, imagem)
{
    return ee.Image(imagem
              // Selecciona a área de interesse
              //.clip(regiao)
              .updateMask(mascara)
              // Elimina as nuvens
              .updateMask(
                imagem.select('QA60').bitwiseAnd(1 << 10).eq(0)         // Nuvens
                .and(imagem.select('QA60').bitwiseAnd(1 << 11).eq(0)))  // Cirrus
              // Cálcula o NDVI (considera apenas valores positivos)
              .normalizedDifference(['B8', 'B4'])
              .float()
              //.clamp(0,1)
              .rename(nome))
            .copyProperties(imagem, ["system:time_start"]);
}
