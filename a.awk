BEGIN {
  # Cargar stopwords en un array
  stopwords_file = ARGV[ARGC - 1] # Ruta de los stopwords
  while ((getline < stopwords_file) > 0) {
    stopwords[$1] = 1
  }
  close(stopwords_file)
}

{
  # Procesamos cada palabra y número en la línea
  for (i = 1; i <= NF; i++) {
    elemento = tolower($i) # Conversión de cada elemento a minúsculas

    # Verificar si el elemento actual NO está en la lista de stopwords y contiene solo caracteres alfabéticos y/o dígitos
    if (!(elemento in stopwords) && elemento ~ /^[a-zA-Z0-9]+$/) {
      # Agregar el elemento a la lista_invertida si no existe
      if (!(elemento in lista_invertida)) {
        lista_invertida[elemento] = ""
      }

      # Agregar el número de línea al elemento en lista_invertida si no existe
      if (index(lista_invertida[elemento], NR) == 0) {
        lista_invertida[elemento] = (lista_invertida[elemento] != "") ? lista_invertida[elemento] ", " : ""
        lista_invertida[elemento] = lista_invertida[elemento] NR
      }
    }
    else{
      printf "Palabra eliminada: %s\n", elemento
    }
  }
}

END {
  # Exportar resultados a un archivo de texto
  for (elemento in lista_invertida) {
    printf "%s %s\n", elemento, lista_invertida[elemento] > "resultados.txt"
  }
}
