import pandas as pd

def explorar_dataframe(Dataframe):
    dim= Dataframe.shape
    print(" El Dataframe tiene ",dim[0], " filas y ",dim[1], " columnas")
    missing_val_count_by_column = (Dataframe.isnull().sum())
    print("Faltan valores en las siguientes columnas")
    print(missing_val_count_by_column[missing_val_count_by_column > 0])
    return
