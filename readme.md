# Modelo preditivo de recuperação da vegetação afetada por incêndios florestais 
Este repositório contém os artefactos que fazem parte da biblioteca **recveg** desenvolvida no âmbito da dissertação de mestrado intitulada "Modelo preditivo de recuperação da vegetação afetada por incêndios florestais", do Mestrado em Engenharia Informática de de Computadores do Instituto Superior de Engenharia de Lisboa.
Este código é publicado sob a licença Creative Commons CC BY-NC:
>Esta licença permite que outros remisturem, adaptem e criem a partir do seu trabalho para fins não comerciais, e embora os novos trabalhos tenham de lhe atribuir o devido crédito e não possam ser usados para fins comerciais, eles não têm de licenciar esses trabalhos derivados ao abrigo dos mesmos termos.

# Classes
## Cobertura
```python
Cobertura (Estático)
```
Classe que encapsula a funcionalidade de caracterização da cobertura da
superfície terrestre tendo em conta a utilização do Corinne Land Cover
(CLC) publicado pela plataforma Copernicus

### Floresta
```python
Cobertura.Floresta (Estático)
```
Categorias de CLC para tipos de floresta
### Mato
```python
Cobertura.Mato (Estático)
```
Lista das categorias CLC para tipos de mato
### palette
```python
Cobertura.palette()
```
Palette de cores para visualização de classes CLC
### lista
```python
Cobertura.lista()
```
Lista das categorias CLC para tipos de vegetação
### gera
```python
Cobertura.gera(regiao, categorias=None)
```
Gera a representação de um objecto GEE dos dados de cobertura de superfície para a regiao indicada

## Composito
```python
Composito(self, data, modelo, dias=10)
```
Compósito MVC de NDVI
### alvo
Cobertura da área alvo
### escala
Escala da cobertura de superfície
### fim
### fim_intervalo
Data fim do intervalo
### caracteristicas
Lista das carecterísticas do registo posicional do composto
### imagens
Número de imagens no compósito
### inicio
Data inicio do compósito
### inicio_intervalo
Data inicio do intervalo
### metricas
Obtem as metricas para este compósito
### perimetro
Perimetro da área total
### processamento
Obtem a tempo de processamento para este compósito
### referencia
Cobertura da área de referência
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
Palette de cores para visualização de NDVI
### avalia
```python
Composito.avalia(self)
```
Avalia o compósito de MVC

## Evento
```python
Evento(self, dados)
```
Encapsula a informação de um evento de incêndio na base de dados do ICNF
### concelho
Concelho onde pertence a Freguesia
### data_fim
Data de extinção do fogo
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

## GEE
```python
GEE (Estático)
```
Constantes do GEE
### BANDA_NIR
Nome da banda NIR na missão Sentinel 2
### BANDA_QUALIDADE
Nome da banda de qualidade referente à presença de nuvens na missão Sentinel 2
### BANDA_RED
Nome da banda RED na missão Sentinel 2
### CLC_ANO
Ano de publicação do Corine Land Cover
### CLC_BANDA
Nome da banda do CLC
### CLC_COLECCAO
Nome da colecção de imagens do CLC no GEE
### ICNF_CAMPO_CONCELHO
Nome do campo relativo ao concelho na base de dados do ICNF
### ICNF_CAMPO_DISTRITO
Nome do campo relativo ao distrito na base de dados do ICNF
### ICNF_CAMPO_FIM
Nome do campo que reflete a data de extinção do incêndio na base de dados do ICNF
### ICNF_CAMPO_FREGUESIA
Nome do campo relativo à freguesia na base de dados do ICNF
### ICNF_CAMPO_IDENTIFICADOR
Nome do campo com o identificador único do evento de incêndio na base de dados do ICNF
### ICNF_CAMPO_INICIO
Nome do campo que regista a data de início do episódio de incêndio
### ICNF_CAMPO_LOCAL
Nome do campo relativo ao nome da localidade na base de dados do ICNF
### ICNF_CAMPOS
Lista de Python com os nomes dos campos do evento de incêndio na base de dados do ICNF
### ICNF_COLECCAO
Nome da coleção que contém a base de dados do ICNF no GEE
### IMAGEM_DATA
Nome do campo que regista a imagem da data no GEE
### IMAGEM_INDICE
Nome do campo que regista o indice da imagem, numa coleção de imagens, no repositório do GEE
### LT_CODIGO
Nome do campo com o código de pais na base de dados de limites territoriais do Departamento de Estado dos EUA
### LT_COLECCAO
Nome da coleção com a base de dados de limites territoriais do Departamento de Estado dos EUA no GEE
### LT_NOME
Nome do campo com o código da zona do pais na base de dados de limites territoriais do Departamento de Estado dos EUA
### SENTINEL_COLECCAO
Nome da coleção de dados recolhidos pela missão Sentinel 2 no repositório do GEE
### SENTINEL_PERCENTAGEM_NUVENS
Nome do campo das propriedades de uma imagem Sentinel 2 no repositório do GEE que regista a cobertura de nuvens
### UNIDADES_METROS
Nome da unidade metro

## Geometria
```python
Geometria(self, identificador, tolerancia, distancia)
```
Encapsula a funcionalidade de avaliação da geometria dos fogos ocorridos
### alvo
Geometria alvo do incêndio
### distancia
Distância correspondente à largura da faixa de referência
### evento
Decrição do evento
### referencia
Geometria de referência adjacente ao incêndio
### tolerancia
Tolerância, em metros, a aplicar na simplificação da geometria
### total
Geometria total (alvo e referência)
### extrai
```python
Geometria.extrai(self)
```
Extrai informação do evento

## ModeloNotificacao
```python
ModeloNotificacao(self, evento=None)
```
Classe que suporta as notificações ao processo do utilizador e o fluxo
### fluxo
Estado do fluxo de execução
### INICIO
Evento de inicio de processamento de um compósito
### SUCESSO
Evento de sucesso na obtenção de um compósito
### TERMINA
Evento de pedido do utilizador para que ocorra a interrupção do processamento.
### VAZIO
Evento relativo a um compósito vazio
### inicio
```python
ModeloNotificacao.inicio(self, dados=None)
```
Notifica o processo do utilizador que iniciou a avaliação de um MVC
### sucesso
```python
ModeloNotificacao.sucesso(self, dados=None)
```
Notifica o processo do utilizador que foi avaliado um MVC válido
### vazio
```python
ModeloNotificacao.vazio(self, dados=None)
```
Notifica o processo do utilizador que não existe MVC na data
### termina
```python
ModeloNotificacao.termina(self)
```
O fluxo foi terminado, modifica o estado
## Modelo
```python
Modelo(self, local, tolerancia=100, distancia=300, ciclo=10)
```
Modelo de exploração, agregação e persistência dos dados de GEE

#### Constantes com as chaves usadas no dicionário que é estruturado no ficheiro de dados
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
Informação da cobertura na zona do incêndio

### data_primeira_imagem
Data da primeira imagem após o incêndio

### distancia
Distância correspondente à largura da faixa de referência
### escala
Escala da informação de NDVI em metros
### evento
Identificador do incêndio
### geometria
Geometria da área ardida (alvo e referência)
### referencia
Informação da cobertura na zona adjacente ao incêndio
### tabela
Tabela com os registos já avaliados
### tolerancia
Tolerância, em metros, a aplicar na simplificação da geometria
### versao
Versão do modelo
### inicializa
```python
Modelo.inicializa(self)
```
Inicializa o modelo
### avalia
```python
Modelo.avalia(self, data_inicio=None, maximo=100, evento=None)
```

Avalia os compostos de NDVI, num máximo de compostos e
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

## ModeloCobertura
```python
ModeloCobertura(self, geometria)
```
Modela a cobertura de uma dada área definida pela geometria
### escala
Escala da informação da cobertura, usa a floresta como referência (*)
### floresta
Modelo da cobertura de floresta
### geometria
Geometria da zona
### mato
Modelo da cobertura de mato
### vegetacao
Modelo da cobertura de vegetação
### avalia
```python
ModeloCobertura.avalia(self)
```
Obtem a dimensão, em pontos, de cada máscara (*)
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
Dimensão, em pontos, da imagem
### imagem
Imagem da cobertura

## Sentinel
```python
Sentinel(self, /, *args, **kwargs)
```
Obtenção de dados do Sentinel 2
### coleccao
```python
Sentinel.coleccao(regiao, inicio, fim)
```

Obtém uma colecção de imagens do Sentinel 2 incluindo apenas as
imagens com menos de 20% de nuvens na região seleccionada para o
intervalo entre as datas de inicio e fim

### mapa_ndvi
```python
Sentinel.mapa_ndvi(nome, cobertura)
```

Função de mapeamento para geração das bandas de NDVI com exclusão
das zonas afetadas por nuvens

### mapa_validacao
```python
Sentinel.mapa_validacao(nome)
```
Map que adiciona uma banda com o sufixo _B que representa os pixeis válidos

## Utilidades
```python
Utilidades (Estático)
```
Classe que encapsula um conjunto de métodos utilitários
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
Dia seguinte à data indicada como um timestamp de unix em milisegundos
### dia_apos
```python
Utilidades.dia_apos(data, dias)
```
Dia correspondente à data indicada acrescida de um dado número de dias
### apenas_data
```python
Utilidades.apenas_data(data)
```
Eliminar do timestamp de unix em milisegundos a hora do dia
### formata_data
```python
Utilidades.formata_data(data, formato='%d-%m-%Y')
```
Formata um timestamp unix em milisegundos
### formata_data_hora
```python
Utilidades.formata_data_hora(data)
```
Formata um timestamp unix em milisegundos

## ZonasArdidas
```python
ZonasArdidas(self)
```
Extrai informação descritiva das zonas ardidas
### eventos
Lista das zonas ardidas sob a forma de uma lista de objectos Evento
### lista
Lista de descrições de zonas ardidas em bruto
### distritos
```python
ZonasArdidas.distritos(self)
```
Obtém uma lista de Distritos com a indicação do número de eventos associado a cada um
### extrai
```python
ZonasArdidas.extrai(self, distrito=None, concelho=None, freguesia=None, local=None)
```
Extrai os eventos de acordo com o critério apresentado
