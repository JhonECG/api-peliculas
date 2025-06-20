import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido",
                "evento": event
            }
        }))

        # Extracción de datos
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Generación de UUID y estructura de película
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        # Guardado en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de éxito
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada exitosamente",
                "pelicula": pelicula,
                "respuesta_dynamodb": response
            }
        }))

        # Respuesta
        return {
            'statusCode': 200,
            'pelicula': pelicula
        }

    except Exception as e:
        # Log de error
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear película",
                "error": str(e)
            }
        }))

        return {
            'statusCode': 500,
            'error': 'Error interno al crear película'
        }
