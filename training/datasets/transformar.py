with open('inversion_dataset.csv', 'r') as file:
    # Leer cada línea del archivo
    for line in file:
        # Dividir la línea en la frase y el indicador, basado en la última coma encontrada
        sentence, indicator = line.strip().rsplit(',', 1)
        # Si el indicador es '0', imprimir la frase con 'inversion:' añadido al principio
        if indicator.strip() == '0':
            print("inversion:", sentence.strip())