def cargar_indice_invertido(nombre_archivo):
    """
    Carga un índice invertido desde un archivo de texto.
    
    El índice invertido es un diccionario que, para cada palabra,
    almacena el conjunto de IDs de documentos en los que aparece.
    
    Parámetros:
        nombre_archivo (str): El nombre del archivo que contiene el índice invertido.
    
    Retorna:
        dict: Un diccionario donde las claves son palabras (str) y 
              los valores son conjuntos de IDs de documentos (set(int)).
    """
    indice_invertido = {}
    with open(nombre_archivo, 'r') as file:
        for linea in file:
            # Dividir la línea en palabras: la primera será la palabra base,
            # el resto serán los IDs de documentos.
            palabras = linea.strip().split()
            palabra = palabras[0]
            documentos = palabras[1:]
            
            # Convertir cada ID de documento en entero y remover la coma al final si existe.
            documentos_limpios = set(map(int, (doc_id.rstrip(',') for doc_id in documentos)))
            
            # Guardar en el índice la palabra (en minúsculas) asociada al conjunto de documentos.
            indice_invertido[palabra.lower()] = documentos_limpios

    return indice_invertido


def buscar_recursivo(palabras, indice_invertido, resultados_parciales=None, index=0):
    """
    Busca recursivamente documentos que contengan todas las palabras indicadas.
    
    Esta función se llama a sí misma para ir refinando el conjunto de resultados
    a medida que se procesan las palabras.
    
    Parámetros:
        palabras (list[str]): Lista de palabras a buscar.
        indice_invertido (dict): El índice invertido cargado.
        resultados_parciales (list[set[int]]): Lista de conjuntos de IDs de documento 
                                               donde cada posición corresponde a los
                                               resultados para una palabra específica.
        index (int): Índice actual de la palabra a procesar.
    
    Retorna:
        set[int] o None: Un conjunto con los IDs de los documentos que contienen 
                         todas las palabras, o None si no hay resultados.
    """
    # Si es la primera llamada, inicializar resultados_parciales con el conjunto de documentos
    # para cada palabra.
    if resultados_parciales is None:
        resultados_parciales = [set(indice_invertido.get(p, [])) for p in palabras]

    # Mientras no se hayan procesado todas las palabras
    if index < len(palabras):
        # Actualizar los resultados parciales para la palabra actual
        resultados_parciales[index] = set(indice_invertido.get(palabras[index], []))
        # Llamada recursiva para la siguiente palabra
        return buscar_recursivo(palabras, indice_invertido, resultados_parciales, index + 1)
    else:
        # Una vez procesadas todas las palabras, intersectar todos los conjuntos
        # para obtener los documentos que contienen TODAS las palabras.
        return set.intersection(*resultados_parciales) if resultados_parciales else None


def buscar(query, indice_invertido):
    """
    Busca documentos que coincidan con una consulta (query) dada.
    
    Parámetros:
        query (str): La consulta, que puede contener una o varias palabras.
        indice_invertido (dict): El índice invertido con los documentos.
    
    Retorna:
        set[int] o None: Un conjunto con los IDs de los documentos que contienen
                         todas las palabras de la consulta, o None si no hay resultados.
    """
    # Convertir la consulta a minúsculas y separar en palabras individuales.
    palabras = query.lower().split()
    # Usar la función recursiva para obtener el conjunto de documentos resultantes.
    return buscar_recursivo(palabras, indice_invertido)


def main():
    """
    Función principal del programa.
    
    1. Carga el índice invertido desde un archivo 'resultados.txt'.
    2. Pide al usuario que ingrese una consulta por consola.
    3. Realiza la búsqueda en el índice invertido.
    4. Escribe los resultados en el archivo 'resultados_consultas.txt'.
    5. Informa al usuario que el proceso ha finalizado.
    """
    # Cargar el índice invertido desde el archivo
    indice_invertido = cargar_indice_invertido('resultados.txt')
    
    # Pedir la consulta al usuario (por ejemplo, puede ser una frase con varias palabras)
    consulta = input("Ingrese su consulta: ")

    # Abrir el archivo de resultados para escritura
    with open('resultados_consultas.txt', 'w') as resultados_file:
        # Realizar la búsqueda
        resultados = buscar(consulta, indice_invertido)
        
        # Escribir un encabezado con la consulta
        resultados_file.write(f"Resultados para la consulta '{consulta}':\n")
        
        # Verificar si hubo resultados
        if resultados:
            # Listar cada documento encontrado
            for doc_id in resultados:
                resultados_file.write(f"- Documento {doc_id}\n")
        else:
            # Indicar que no se encontraron resultados
            resultados_file.write(f"No se encontraron resultados para la consulta '{consulta}'.\n")

    # Informar al usuario que se han guardado los resultados
    print("Proceso completado. Los resultados de la consulta se han guardado en 'resultados_consultas.txt'.")


if __name__ == "__main__":
    main()
