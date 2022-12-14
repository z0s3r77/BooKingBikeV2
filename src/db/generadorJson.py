from schema import Schema, And, Use
import os
import json



#Con esta función convertimos la RESPONSE de la API en un objeto Python
def convertResponseStringIntoObjtect(response):

    #Damos el valor de la coleccion de bicicletas a response
    #Comprobamos que sea de tipo str

    try:
        assert isinstance(response,str)
    except:
        return False

    #Json.loads detecta en el string un formato JSON y lo convierte en un objeto Dict
    try:
        response = json.loads(response)
    except:
        return False


    return response




#Con esta funcion comprobamos que cada documento de la colección siga el esquema correcto

def checkSchemaDocument(response):


    if isinstance(response, dict):
        pass
    else:
        return False


    conf_schema = Schema({

        "_id": And(Use(str)),
        "Brand":  And(Use(str)),
        "Model": {
            "Name":  And(Use(str)),
            "Style": And(Use(str)),
            "Suspension":  And(Use(str)),
            "Material":  And(Use(str)),
            "Fork brand":  And(Use(str)),
            "Fork length": {
                "$numberInt":  And(Use(str))
            },
            "Developments":  And(Use(str)),
            "Group":  And(Use(str)),
            "Type":  And(Use(str)),
            "Wheel size": {
                "$numberDouble":  And(Use(str))
            },
            "Weight": {
                "$numberDouble":  And(Use(str))
            }
        },
        "Price": {
            "$numberInt":  And(Use(str))
        },
        "Status": And(Use(str)),
        "Location":  And(Use(str)),
        "img":  And(Use(str))
    })


    for document in response["documents"]:
        try:
            conf_schema.validate(document)
        except:
            return False

    return True        
    



def generateJsonFileFromResponse(response, file):
    
    #Comprobamos si la respuesta es object Dict
    try:
        assert isinstance(response, dict)
    except:
        return False

    try:
        #Comprobamos si existe el directorio json , sino, lo crea
        if not os.path.exists('json/'):
            os.makedirs('json/')

        if isinstance(file, str):
        #Abrimos el archivo bikes.json con el fin de escribir en este "w"
            outFile = open(f"json/{file}.json", "w")
        else:
            return False

    except OSError:
        print("No se puede abrir el archivo")
        quit()
        
    else: 
            #json.dump nos permite convertir el diccionario en un objeto JSON
        json.dump(response["documents"], outFile, indent=4)
            
        outFile.close()

        return True


#Volcamos la respuesta de requestToMongoApi del modulo conexionApiMongo

def GeneradorJsonFile(response, newjsonfile):

    response = convertResponseStringIntoObjtect(response)
    checkSchemaDocument(response)
    if generateJsonFileFromResponse(response, newjsonfile) == False:
        return False
    else:
        return True