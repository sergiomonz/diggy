import json
import boto3
from decimal import Decimal
import uuid

AWS_REGION = "us-east-1"
KEY_ERROR_MESSAGE = {
    "category_id": "La categoría no existe o no fue seleccionada",
    "user_id" : "No se indicó el usuario al cual le pertenece el evento",
    "name": "Debe escribir el nombre del evento",
    "coordinates": "Es necesaria la ubicación del evento",
   #"images": "El evento debe tener imagenes",
    "description": "El evento debe tener una descripción",
    "range_age": "El rango de edad debe ser selecionado",
    "price": "Debe indicar el precio del evento",
    "slots": "Debe indicar los cupos disponibles actuales del evento",
    "max": "Debe ingresar la cantidad máxima de personas al evento",
    "date_start": "Debe ingresar la hora y fecha de inicio del evento",
    "date_end": "Debe ingresar la hora y fecha en la cual termina el evento"
}

client = boto3.resource('dynamodb',region_name=AWS_REGION)
events_table = client.Table("events")
categories_table = client.Table("categories")
sns = boto3.resource('sns')
topic = sns.Topic('arn:aws:sns:us-east-1:605550406178:push-get-tokens')

def create_id():    
    return "E" + str(uuid.uuid4())

def get_category_name(category_id):
    response = categories_table.get_item(
        Key = { 'id' : category_id}
    )
    if 'Item' not in response:
        raise KeyError("category_id")
        
    return response['Item']['name']

def send(message):
    response = topic.publish(
        Message = message
    )
    validate_sns_response(response)
    return response
    
def validate_sns_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error al intentar usar el servicio de push-notification")
    
def create_event(event):
    category = get_category_name(event['category_id'])
    response = events_table.put_item(
        Item= {
        "event_id": create_id(),
        "user_id": event['user_id'],
        "category_id":event['category_id'],
        "category_name":category,
        "name": event['name'],
        "coordinates": event['coordinates'],
        #"images": event['images'],
        "description": event['description'],
        "range_age": event['range_age'],
        "price": event['price'],
        "slots": event['slots'],
        "max": event['max'],
        "date_start": event['date_start'],
        "date_end": event['date_end'],
        "score" : 0,
        "total_comments" : 0,
        "comments":[]
    })
    validate_dynamodb_response(response)
    return response

def validate(data):
    for key in KEY_ERROR_MESSAGE.keys():
        if key not in data or not data[key]:
            print(key," missing")
            raise KeyError(key)
            
def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno en la base de datos")
            
def lambda_handler(event, context):
    message = {
        "error" : False,
        "message": "El evento fue creado exitosamente",
        
    }
    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(message)
    }
    
    try:
        
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        event_data = json.loads(event["body"], parse_float=Decimal)
        event_data['user_id'] = user_id
        validate(event_data)
        create_event(event_data)
        body = {
            "event_name" : event_data['name'],
            "category_id" : event_data['category_id']
        }
        send(json.dumps(body))
            
    except KeyError as e:
        print(e)
        message['error']  = True
        message['message'] = KEY_ERROR_MESSAGE[e.args[0]]
        response['statusCode'] = 400
        
    except Exception as e:
        print(e)
        message['error']  = True
        message['message'] = str(e)
        response['statusCode'] = 500
        
    
    response['body'] = json.dumps(message,ensure_ascii=False)
    return response
        
    
    
