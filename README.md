# CityAdvisor

## En este repositorio vamos comparar codigos postales mediante la creación de una api que automatize el proceso de obtención, guardado y visualización de datos.


### 1. Creación de la api: 
#### He creado una webapi mediante streamlit en la que recibiremos un input del usuario que nos dará pié a crear nuestra base de datos y después le damos una visualización de su selección.

### 2. Estructura de la base de datos:
#### La estructura será de una colección para cada codigo postal, que va a contener 1 documento identificador en el que incluiremos algunos parámetros comunes a toda la colección, y luego el resto de documentos serán todos los elementos que nos encontremos, englobados a través de sus fields por categorías y subcategorías. Incluimos aquí también latitud, longitud y nombre para las visualizaciones.

### 2. Obtención de datos:
#### Cuando recibimos el input del usuario, mediante la api de Google Places obtenemos su geolozalización y creamos el documento identificador de la colección, después le pasamos las coordenadas a fourscuare para encontrar una serie de elementos definidos por mi en config.dic_categorias y creamos el resto de documentos de nuestra colección con los resultados. Por otra parte, hemos scrapeado una página web con selenium de la que hemos obtenido las rentas para cada código postal, agregándoselas al documento identificador.

### 3. Visualización:
#### Utilizando los charts de streamlit le daremos algunas comparaciones al usuario


