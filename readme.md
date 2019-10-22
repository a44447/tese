# Modelo preditivo de recupera��o da vegeta��o afetada por inc�ndios florestais
Este reposit�rio cont�m os artefactos que fazem parte da biblioteca desenvolvida no �mbito da disserta��o de mestrado intitulada "Modelo preditivo de recupera��o da vegeta��o afetada por inc�ndios florestais", do Mestrado em Engenharia Inform�tica de de Computadores do Instituto Superior de Engenharia de Lisboa.
Este c�digo � publicado sob a licen�a Creative Commons CC BY-NC:
>Esta licen�a permite que outros remisturem, adaptem e criem a partir do seu trabalho para fins n�o comerciais, e embora os novos trabalhos tenham de lhe atribuir o devido cr�dito e n�o possam ser usados para fins comerciais, eles n�o t�m de licenciar esses trabalhos derivados ao abrigo dos mesmos termos.

# recveg.cobertura

Cobertura - Corine Land Cover

@author: Rui Reis

## Cobertura
```python
Cobertura(self, /, *args, **kwargs)
```

Classe que encapsula a funcionalidade de caracteriza��o da cobertura da
superf�cie terrestre tendo em conta a utiliza��o do Corinne Land Cover
(CLC) publicado pela plataforma Copernicus

### Floresta
```python
Cobertura.Floresta(self, /, *args, **kwargs)
```
Categorias de CLC para tipos de floresta
### Mato
```python
Cobertura.Mato(self, /, *args, **kwargs)
```
Lista das categorias CLC para tipos de mato
### palette
```python
Cobertura.palette()
```
Palette de cores para visualiza��o de classes CLC
### lista
```python
Cobertura.lista()
```
Lista das categorias CLC para tipos de vegeta��o
### gera
```python
Cobertura.gera(regiao, categorias=None)
```

Gera uma representa��o da imagem correspondente ao Corine Land
Cover  de 2012 para a regi�o indicada

# recveg.composito

Comp�sito MVC de NDVI

@author: Rui Reis

## Composito
```python
Composito(self, data, modelo, dias=10)
```
Comp�sito MVC de NDVI
### alvo
Cobertura da �rea alvo
### escala
Escala da cobertura de superf�cie
### fim
### fim_intervalo
Data fim do intervalo
### caracteristicas
Lista das carecter�sticas do registo posicional do composto
### imagens
N�mero de imagens no comp�sito
### inicio
Data inicio do comp�sito
### inicio_intervalo
Data inicio do intervalo
### metricas
Obtem as metricas para este comp�sito
### perimetro
Perimetro da �rea total
### processamento
Obtem a tempo de processamento para este comp�sito
### referencia
Cobertura da �rea de refer�ncia
### registo
Obtem o registo posicional deste composto

### Constantes posicionais dos campos do evento
#### DATA_FIM
#### DATA_INICIO
#### IMAGENS
#### NDVI_MEDIA_FLORESTA_ALVO
#### NDVI_MEDIA_FLORESTA_REFERENCIA
#### NDVI_MEDIA_MATO_ALVO
#### NDVI_MEDIA_MATO_REFERENCIA
#### NDVI_MEDIA_VEGETACAO_ALVO
#### NDVI_MEDIA_VEGETACAO_REFERENCIA
#### NDVI_MEDIANA_FLORESTA_ALVO
#### NDVI_MEDIANA_FLORESTA_REFERENCIA
#### NDVI_MEDIANA_MATO_ALVO
#### NDVI_MEDIANA_MATO_REFERENCIA
#### NDVI_MEDIANA_VEGETACAO_ALVO
#### NDVI_MEDIANA_VEGETACAO_REFERENCIA
#### NDVI_PONTOS_FLORESTA_ALVO
#### NDVI_PONTOS_FLORESTA_REFERENCIA
#### NDVI_PONTOS_MATO_ALVO
#### NDVI_PONTOS_MATO_REFERENCIA
#### NDVI_PONTOS_VEGETACAO_ALVO
#### NDVI_PONTOS_VEGETACAO_REFERENCIA
#### TEMPO_PROCESSAMENTO

### palette
```python
Composito.palette()
```
Palette de cores para visualiza��o de NDVI
### avalia
```python
Composito.avalia(self)
```
Avalia o comp�sito de MVC

# recveg.evento

Caracteriza��o de uma zona ardida na base de dados do ICNF

## Evento
```python
Evento(self, dados)
```
Encapsula a informa��o de um evento
### concelho
Concelho onde pertence a Freguesia
### data_fim
Data de extin��o do fogo
### data_inicio
Data inicio do fogo
### distrito
Distrito onde pertence o Concelho
### freguesia
Freguesia onde pertence o local
### identificador
Identificador do evento
### local
Nome do local onde ocorreu o fogo
### campos
```python
Evento.campos()
```
Devolve a lista dos nomes dos campos correspondentes ao evento
# recveg.gee

Constantes GEE e das suas fontes de dados

## GEE
```python
GEE(self, /, *args, **kwargs)
```
Constantes do GEE
### BANDA_NIR
Nome da banda NIR na miss�o Sentinel 2
### BANDA_QUALIDADE
Nome da banda de qualidade referente � presen�a de nuvens na miss�o Sentinel 2
### BANDA_RED
Nome da banda RED na miss�o Sentinel 2
### CLC_ANO
Ano de publica��o do Corine Land Cover
### CLC_BANDA
Nome da banda do CLC
### CLC_COLECCAO
Nome da colec��o de imagens do CLC no GEE
### ICNF_CAMPO_CONCELHO
Nome do campo relativo ao concelho na base de dados do ICNF
### ICNF_CAMPO_DISTRITO
Nome do campo relativo ao distrito na base de dados do ICNF
### ICNF_CAMPO_FIM
Nome do campo que reflete a data de extin��o do inc�ndio na base de dados do ICNF
### ICNF_CAMPO_FREGUESIA
Nome do campo relativo � freguesia na base de dados do ICNF
### ICNF_CAMPO_IDENTIFICADOR
Nome do campo com o identificador �nico do evento de inc�ndio na base de dados do ICNF
### ICNF_CAMPO_INICIO
Nome do campo que regista a data de in�cio do epis�dio de inc�ndio
### ICNF_CAMPO_LOCAL
Nome do campo relativo ao nome da localidade na base de dados do ICNF
### ICNF_CAMPOS
Lista de Python com os nomes dos campos do evento de inc�ndio na base de dados do ICNF
### ICNF_COLECCAO
Nome da cole��o que cont�m a base de dados do ICNF no GEE
### IMAGEM_DATA
Nome do campo que regista a imagem da data no GEE
### IMAGEM_INDICE
Nome do campo que regista o indice da imagem, numa cole��o de imagens, no reposit�rio do GEE
### LT_CODIGO
Nome do campo com o c�digo de pais na base de dados de limites territoriais do Departamento de Estado dos EUA
### LT_COLECCAO
Nome da cole��o com a base de dados de limites territoriais do Departamento de Estado dos EUA no GEE
### LT_NOME
Nome do campo com o c�digo da zona do pais na base de dados de limites territoriais do Departamento de Estado dos EUA
### SENTINEL_COLECCAO
Nome da cole��o de dados recolhidos pela miss�o Sentinel 2 no reposit�rio do GEE
### SENTINEL_PERCENTAGEM_NUVENS
Nome do campo das propriedades de uma imagem Sentinel 2 no reposit�rio do GEE que regista a cobertura de nuvens
### UNIDADES_METROS
Nome da unidade metro
# recveg.geometria

Geometria

## Geometria
```python
Geometria(self, identificador, tolerancia, distancia)
```
Encapsula a funcionalidade de avalia��o da geometria dos fogos ocorridos
### alvo
Geometria alvo do inc�ndio
### distancia
Dist�ncia correspondente � largura da faixa de refer�ncia
### evento
Decri��o do evento
### referencia
Geometria de refer�ncia adjacente ao inc�ndio
### tolerancia
Toler�ncia, em metros, a aplicar na simplifica��o da geometria
### total
Geometria total (alvo e refer�ncia)
### extrai
```python
Geometria.extrai(self)
```
Extrai informa��o do evento
# recveg.modelo

Modelo de extra��o, agrega��o e armazenamento de dados

## ModeloNotificacao
```python
ModeloNotificacao(self, evento=None)
```
Classe que suporta as notifica��es ao processo do utilizador e o fluxo
### fluxo
Estado do fluxo de execu��o
### INICIO
Evento de inicio de processamento de um comp�sito
### SUCESSO
Evento de sucesso na obten��o de um comp�sito
### TERMINA
Evento de pedido do utilizador para que ocorra a interrup��o do processamento.
### VAZIO
Evento relativo a um comp�sito vazio
### inicio
```python
ModeloNotificacao.inicio(self, dados=None)
```
Notifica o processo do utilizador que iniciou a avalia��o de um MVC
### sucesso
```python
ModeloNotificacao.sucesso(self, dados=None)
```
Notifica o processo do utilizador que foi avaliado um MVC v�lido
### vazio
```python
ModeloNotificacao.vazio(self, dados=None)
```
Notifica o processo do utilizador que n�o existe MVC na data
### termina
```python
ModeloNotificacao.termina(self)
```
O fluxo foi terminado, modifica o estado
## Modelo
```python
Modelo(self, local, tolerancia=100, distancia=300, ciclo=10)
```
Modelo de explora��o, agrega��o e persist�ncia dos dados de GEE

#### Constantes com as chaves usadas no dicion�rio que � estruturado no ficheiro de dados
#### ADJACENTE_FF
#### ALVO_FF
#### ALVO_FL
#### COMUM_FF
#### COMUM_FL
#### DATA_INCENDIO_FF
#### DATA_PRIMEIRA_IMAGEM_FF
#### ESCALA_FF
#### FLORESTA_FF
#### LOCAL_FF
#### MATO_FF
#### METADADOS_FF
#### REFERENCIA_FF
#### REFERENCIA_FL
#### TABELA_FF
#### TOLERANCIA_FF
#### VEGETACAO_FF
#### VERSAO_FF

### alvo
Informa��o da cobertura na zona do inc�ndio

### data_primeira_imagem
Data da primeira imagem ap�s o inc�ndio

### distancia
Dist�ncia correspondente � largura da faixa de refer�ncia
### escala
Escala da informa��o de NDVI em metros
### evento
Identificador do inc�ndio
### geometria
Geometria da �rea ardida (alvo e refer�ncia)
### referencia
Informa��o da cobertura na zona adjacente ao inc�ndio
### tabela
Tabela com os registos j� avaliados
### tolerancia
Toler�ncia, em metros, a aplicar na simplifica��o da geometria
### versao
Vers�o do modelo
### inicializa
```python
Modelo.inicializa(self)
```
Inicializa o modelo
### avalia
```python
Modelo.avalia(self, data_inicio=None, maximo=100, evento=None)
```

Avalia os compostos de NDVI, num m�ximo de compostos e
reporta cada passo a evento

### guarda
```python
Modelo.guarda(self, nome, esmaga=False)
```
Guarda o modelo num ficheiro
### carrega
```python
Modelo.carrega(self, nome)
```
Carrega os dados de modelo a partir de um ficheiro
# recveg.modelocobertura

Modelo de cobertura

## ModeloCobertura
```python
ModeloCobertura(self, geometria)
```
Modela a cobertura de uma dada �rea definida pela geometria
### escala
Escala da informa��o da cobertura, usa a floresta como refer�ncia (*)
### floresta
Modelo da cobertura de floresta
### geometria
Geometria da zona
### mato
Modelo da cobertura de mato
### vegetacao
Modelo da cobertura de vegeta��o
### avalia
```python
ModeloCobertura.avalia(self)
```
Obtem a dimens�o, em pontos, de cada m�scara (*)
### imprime
```python
ModeloCobertura.imprime(self, titulo=None)
```
Envia para a consola um resumo do modelo de cobertura
# recveg.modelotipocobertura

Modelo de um tipo de cobertura

## ModeloTipoCobertura
```python
ModeloTipoCobertura(self, imagem, dimensao=0)
```
Classe que encapsula a funcionalidade de um tipo de cobertura
### dimensao
Dimens�o, em pontos, da imagem
### imagem
Imagem da cobertura
# recveg.sentinel

Dados multi-espectrais da miss�o Sentinel 2

## Sentinel
```python
Sentinel(self, /, *args, **kwargs)
```
Obten��o de dados do Sentinel 2
### coleccao
```python
Sentinel.coleccao(regiao, inicio, fim)
```

Obt�m uma colec��o de imagens do Sentinel 2 incluindo apenas as
imagens com menos de 20% de nuvens na regi�o seleccionada para o
intervalo entre as datas de inicio e fim

### mapa_ndvi
```python
Sentinel.mapa_ndvi(nome, cobertura)
```

Fun��o de mapeamento para gera��o das bandas de NDVI com exclus�o
das zonas afetadas por nuvens

### mapa_validacao
```python
Sentinel.mapa_validacao(nome)
```
Map que adiciona uma banda com o sufixo _B que representa os pixeis v�lidos
# recveg.utilidades

Classe com m�todos de utlidades

## Utilidades
```python
Utilidades(self, /, *args, **kwargs)
```
Classe que encapsula um conjunto de m�todos utilit�rios
### DIA
Constante que representa um dia em milisegundos

### agora
```python
Utilidades.agora()
```
A data e hora atuais como um timestap de unix em milisegundos
### dia_seguinte
```python
Utilidades.dia_seguinte(data)
```
Dia seguinte � data indicada como um timestamp de unix em milisegundos
### dia_apos
```python
Utilidades.dia_apos(data, dias)
```
Dia correspondete � data indicada acrescida de um dado n�mero de dias
### apenas_data
```python
Utilidades.apenas_data(data)
```
Eliminar do timestamp de unix em milisegundos a hora do dia
### formata_data
```python
Utilidades.formata_data(data, formato='%d-%m-%Y')
```
Formata umtimestamp unix em milisegundos
### formata_data_hora
```python
Utilidades.formata_data_hora(data)
```
Formata umtimestamp unix em milisegundos
# recveg.zonasardidas

Encapsula a base de dados de zonas ardidas da base de dados do ICNF

## ZonasArdidas
```python
ZonasArdidas(self)
```
Extrai informa��o descritiva das zonas ardidas
### eventos
Lista das zonas ardidas sob a forma de uma lista de objectos Evento
### lista
Lista de descri��es de zonas ardidas em bruto
### distritos
```python
ZonasArdidas.distritos(self)
```
Obt�m uma lista de Distritos com a indica��o do n�mero de eventos associado a cada um
### extrai
```python
ZonasArdidas.extrai(self, distrito=None, concelho=None, freguesia=None, local=None)
```
Extrai os eventos de acordo com o crit�rio apresentado
