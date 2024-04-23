from pymongo import MongoClient
import pprint
import sys
from bson.objectid import ObjectId

def menuCRUD():
    menu = '''Bien venido al menu CRUD
    1. Insertar un episodio de la serie
    2. Elimina un episodio de la serie
    3. Actualiza la puntacion de un episodio
    4. Mostrar todos los episodios que tenga mas de 8 de puntuacion
    5. Mostrar los generos que tiene la serie
    6. Mostrar los dias en los que se emite la serie
    7. Mostrar la media de puntacion total por temporadas
    8. Salir
    '''

    print(menu)

    while True:
        try:
            opcion = int(input("Elija un numero para probar la consulta: "))
            while opcion > 8:
                print("Tienes que elejir una opcion que este disponible")
                opcion = int(input("Elija un numero para probar la consulta: "))
            break
        except ValueError:
            print ("Debes introducir un número")

    return opcion

def conexionMongodb():
    try:
        client = MongoClient('localhost')
        db = client.westworld
        col = db.serie
    except :
        print("No puedo conectar a la base de datos:")
        sys.exit(1)
    print("Conexión correcta en MongoDB")
    
    return col


def prueba(col):
    documento = {"type": "regular"}
    result = col.find(documento)
    num_docs = 0
    for var in result:
        num_docs += 1
        pprint.pprint(var)
        print()
    print("Nº de documentos: " + str(num_docs))

def insertar(col):

    name = input("Ingrese el nombre de la serie: ")
    season = int(input("Ingrese el numero de la temporada: "))
    number = int(input("Ingrese el numero del episodio: "))
    type = input("Ingrese el tipo del episodio: ")
    airdate = input("Ingrese la fecha del episodio; ")
    average = float(input("Ingrese la puntuacion del episodio: "))

    documento = {
      "name": name,
      "season": season,
      "number": number,
      "type": type,
      "airdate": airdate,
      "airtime": "21:00",
      "runtime": 60,
      "rating": {"average": average}
    }

    resultado = col.insert_one(documento)

    print("Se ha ingresado con exito el episodio")

def eliminacion(col):

    id= input("Introduzca el id para su eliminacion: ")

    try:
        documento = {"_id": ObjectId(id)}

        print("Documento a eliminar")
        pprint.pprint(col.find_one(documento))

        resultado = col.delete_one(documento)
        print("Se ha eliminado el episodio")

    except:
        print("El episodio no existe no se puede eliminar")

def actualizar(col):

    id= input("Introduzca el id para su actualizacion: ")

    try:
        documento = {"_id": ObjectId(id)}

        puntuacion = float(input("Ingrese la puntuacion a cambiar: "))

        actualiza = {"$set": {"rating":{"average": puntuacion}}}

        print("Documento sin actualizar")
        pprint.pprint(col.find_one(documento))

        resultado = col.update_one(documento,actualiza)
        print("--------------------------------------------------")
        print("Documento actualizado")
        pprint.pprint(col.find_one(documento))
    except:
        print("El episodio no existe no se puede actualizar")

def consultaSimple(col):
    
    documento = {"rating.average": { "$gt": 8}}
    resultado = col.find(documento, {"_id": 0, "name": 1})

    cont = 0
    print("Los nombres de los episodios son:")
    for documento in resultado:
        nombre = documento.get("name")
        if nombre:
            print("-",nombre)
            cont += 1

    print("Hay", cont, "documentos")

def consultaArray(col):

    try:
        documento ={"genres":{"$all": ["Science-Fiction", "Western"]}}
        resultado = col.find_one(documento,{"_id":0,"genres":1})
        if resultado== "None":
            print("La serie no contiene esos generos")
        else:
            print("La serie contiene esos generos:")
            for valor in resultado["genres"]:
                print("-",valor)
    except:
        print("La serie no contiene esos genero")

def consultaEmbebida(col):

    resultado = col.distinct("schedule.days")

    print("Los dias que se emite la serie son:")
    for var in resultado:
        print(var)

def consultaAgrupacion(col):

    documento = [{"$group": {"_id": "$season", "averageRating": {"$avg": "$rating.average"}}},{"$sort": {"averageRating": -1}}]
    resultado = col.aggregate(documento)

    for var in resultado:
        if var["_id"] == "None" or var["averageRating"] == "None":
            print()
        else:
            print("Temporada",var["_id"]," media ",var["averageRating"])