import json

# Nombre del documento y archivo de salida
DOCUMENT_NAME = "License Plate Number 10.0"
OUTPUT_FILE = "License-Plate-Number-dataset.json"

titles = [
    "Generalidades",
    "Introducción",
    "Conceptos básicos",
    "Atributos",
    "Validaciones",
    "Tipos de LPN",
    "Template de etiquetas LPN",
    "Estados",
    "Plantillas de etiquetas de LPN",
    "Sustitución de etiquetas WIS",
    "Operaciones sobre LPNs",
    "Creación y consulta de LPNs",
    "Consulta de LPN",
    "Consulta de códigos de barra de un LPN",
    "Impresión de LPN",
    "API de LPN",
    "Creación de un LPN",
    "Obtención de un LPN",
    "Obtención de un LPN por Identificador Externo y Tipo",
    "Creación de LPNs mediante Excel",
    "Otras consultas sobre LPNs",
    "Consulta de Contenido de LPN",
    "Consulta de LPN por Atributos",
    "Consulta por atributos de cabezal",
    "Consulta por atributos del detalle",
    "Consulta de Logs LPN",
    "Logs de Cabezal",
    "Logs de Detalles",
    "Consulta de Productos por Atributos",
    "Edición de atributos de LPNs",
    "Recepción de LPNs",
    "Agendamiento de LPNs",
    "Planificación de LPNs",
    "Colector de Recepción",
    "Confirmación de Recepción",
    "Cross Docking sobre LPNs",
    "Controles de calidad sobre LPNs",
    "Consulta de Etiquetas",
    "Mesa de Clasificación",
    "Colector de Almacenamiento Agrupado",
    "Colector de Almacenamiento Fraccionado",
    "Manejo de Stock sobre LPNs",
    "Consulta de Stock",
    "Colector de Auditoría de LPN",
    "Auditoría en una fase",
    "Auditoria en dos fases",
    "Colector de Transferencia",
    "Colector de Inventario",
    "Colector de Ajustes de stock",
    "Colector de Cambio de lote",
    "Colector de Reabastecimiento por etapas",
    "Marcado de Averías sobre LPNs",
    "Pedidos sobre LPNs",
    "Creación de pedidos sobre LPNs",
    "Pedidos sobre LPNs por Panel Web",
    "Pedidos de LPNs completos",
    "Pedidos de mercadería contenida en LPNs específicos",
    "Pedidos de mercadería basados en atributos",
    "Pedidos sobre LPNs por API",
    "Pedidos de LPNs completos",
    "Pedidos de mercadería contenida en LPNs específicos",
    "Pedidos de mercadería basados en atributos",
    "Consultas de LPN en pedidos",
    "LPNs de detalle de pedido",
    "Atributos de detalle de pedido",
    "Detalle de atributos de detalle de pedido",
    "Anulación de pedidos pendientes sobre LPNs",
    "Eliminar pedidos pendientes",
    "Eliminar pedidos pendientes (LPN específico)",
    "Eliminar pedidos pendientes (LPN atributos)",
    "API de Pedidos Anulados",
    "Preparación de LPNs",
    "Ajustes en Liberación de Onda para manejo de LPN",
    "Análisis de rechazo para preparaciones sobre LPNs",
    "Anulación de preparaciones sobre LPNs",
    "Colector de Reabastecimiento de ubicaciones bajas",
    "Colector de Picking Normal",
    "Configuración colector de picking",
    "Modalidades de picking",
    "Modalidad de picking Tradicional",
    "Modalidad de picking LPN",
    "Sugerencia de LPNs candidatos",
    "Colector de Extracción",
    "Modalidad de picking Mixta",
    "Modalidades de picking LPN",
    "Pickear en LPN y dejar el remanente en un LPN nuevo",
    "Pickear en LPN y dejar el remanente suelto",
    "Pickear en un nuevo LPN y dejar el remanente en LPN original",
    "Pickear suelto y dejar el remanente en el LPN original",
    "Colector de Picking Manual",
    "Colector de Consolidación de Contenedores",
    "Colector de Devolución de picking",
    "Colector de Partición de Contenedores",
    "Colector de Separación de Picking",
    "Mesa de Empaque",
    "Colector de Control de contenedor",
    "Colector de Ensamblado de fórmulas",
    "Expedición de LPNs",
    "Panel de Egresos",
    "Pedidos de mostrador Panel Web",
    "Colector de Expedición",
    "Colector de Asignación de carga",
    "Colector de Carga de camión",
    "Colector de Descarga de contenedores",
    "Cierre de Camión"
]

# Función para crear el dataset con respuestas vacías
def create_dataset_with_empty_responses(titles, document_name, output_file):
    data = [
        {
            "role": "system",
            "content": "Eres un asistente virtual llamado Asistente WMS, enfocado en responder preguntas relacionadas al sistema WMS (Warehouse Management System), de forma concreta y precisa."
        }
    ]
    
    # Crear preguntas y respuestas vacías basadas en los títulos
    for title in titles:
        user_content = title
        assistant_content = f"Según el manual {document_name}: "
        
        # Añadir entrada de usuario y respuesta vacía
        data.append({"role": "user", "content": user_content})
        data.append({"role": "assistant", "content": assistant_content})
    
    # Guardar el archivo JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Generar el dataset
create_dataset_with_empty_responses(titles, DOCUMENT_NAME, OUTPUT_FILE)
