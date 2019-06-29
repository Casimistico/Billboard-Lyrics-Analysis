"""This module is used to perform an initial exploration of a dataframe generated using pandas"""

def explorar_dataframe(dataframe):
    """This function finds key information about the Dataframe and shows it to the user"""
    dim = dataframe.shape
    print("Data frame has ", dim[0], " rows y ", dim[1], " column")
    missing_val_count_by_column = (dataframe.isnull().sum())
    if dataframe.empty:
        print("There are not missing values")
    else:
        print("Missing values in ", len(missing_val_count_by_column), " columns")
        print(missing_val_count_by_column[missing_val_count_by_column > 0])
