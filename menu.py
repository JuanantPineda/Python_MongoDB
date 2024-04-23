import funciones

banderaCRUD = True

while banderaCRUD == True:
    conexion = funciones.conexionMongodb()
    numero = funciones.menuCRUD()
    print()
    if numero == 1:
        funciones.insertar(conexion)
        print()
    elif numero == 2:
        funciones.eliminacion(conexion)
        print()
    elif numero == 3:
        funciones.actualizar(conexion)
        print()
    elif numero == 4:
        funciones.consultaSimple(conexion)
        print()
    elif numero == 5:
        funciones.consultaArray(conexion)
        print()
    elif numero == 6:
        funciones.consultaEmbebida(conexion)
        print()
    elif numero == 7:
        funciones.consultaAgrupacion(conexion)
        print()
    elif numero == 8:
        banderaCRUD = False