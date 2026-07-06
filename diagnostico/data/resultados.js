const DIAGNOSTIC_CONFIG={course:"Estadistica 10",period:"2026-2",totalQuestions:15,secondsPerQuestion:60,teacherPassword:"est10-docente-2026",groups:["10A","10B","10C"]};
const QUESTIONS=[
{id:1,topic:"Lectura de tablas",answer:"B",skill:"Extraer informacion de una tabla"},
{id:2,topic:"Graficas de barras",answer:"C",skill:"Interpretar frecuencias"},
{id:3,topic:"Graficas circulares",answer:"A",skill:"Relacionar porcentajes y sectores"},
{id:4,topic:"Porcentajes",answer:"D",skill:"Calcular proporciones simples"},
{id:5,topic:"Media aritmetica",answer:"B",skill:"Calcular promedio"},
{id:6,topic:"Mediana",answer:"A",skill:"Ordenar datos e identificar valor central"},
{id:7,topic:"Moda",answer:"C",skill:"Identificar el dato mas frecuente"},
{id:8,topic:"Rango",answer:"D",skill:"Comparar valor maximo y minimo"},
{id:9,topic:"Variables",answer:"B",skill:"Diferenciar variable cualitativa y cuantitativa"},
{id:10,topic:"Frecuencia absoluta",answer:"A",skill:"Contar ocurrencias"},
{id:11,topic:"Frecuencia relativa",answer:"C",skill:"Relacionar parte y total"},
{id:12,topic:"Probabilidad basica",answer:"B",skill:"Evaluar casos favorables sobre posibles"},
{id:13,topic:"Muestreo",answer:"D",skill:"Reconocer muestra y poblacion"},
{id:14,topic:"Interpretacion de datos",answer:"A",skill:"Tomar conclusiones a partir de datos"},
{id:15,topic:"Resolucion de problemas",answer:"C",skill:"Seleccionar procedimiento estadistico"}
];
const GROUP_RESULTS={"10A":{students:0,average:null,questions:QUESTIONS.map(q=>({id:q.id,correctPercent:null,dominantError:"Pendiente por cargar resultados"}))},"10B":{students:0,average:null,questions:QUESTIONS.map(q=>({id:q.id,correctPercent:null,dominantError:"Pendiente por cargar resultados"}))},"10C":{students:0,average:null,questions:QUESTIONS.map(q=>({id:q.id,correctPercent:null,dominantError:"Pendiente por cargar resultados"}))}};
const INDIVIDUAL_RESULTS={"10A":{},"10B":{},"10C":{}};