import json
import pickle
import numpy as np

__Locality = None
__Furnishing = None
__Type = None
__data_columns = None
__model = None

def get_estimated_price(Locality, Furnishing, Type, Area, BHK, Bathroom, Parking):
    try:
        loc_index = __data_columns.index(Locality.lower())
        fur_index = __data_columns.index(Furnishing.lower())
        type_index = __data_columns.index(Type.lower())
    except:
        loc_index = -1
        fur_index = -1
        type_index = -1

    x_input = np.zeros(len(__data_columns))
    x_input[0] = Area
    x_input[1] = BHK
    x_input[2] = Bathroom
    x_input[3] = Parking
    if loc_index >= 0:
        x_input[loc_index] = 1
    if fur_index >= 0:
        x_input[fur_index] = 1
    if type_index >= 0:
        x_input[type_index] = 1

    return round(__model.predict([x_input])[0], 2)

def get_Locality_names():
    return __Locality

def get_Furnishing():
    return __Furnishing

def get_Type():
    return __Type

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __Locality
    global __Furnishing
    global __Type
    global __model

    with open("./artifacts/dehli_data_columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __Locality = __data_columns[4:33]
        __Furnishing = __data_columns[33:36]
        __Type = __data_columns[36:]
    with open("./artifacts/Dehli_House_Data_Model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("Loading saved artifacts...done")

if __name__ == "__main__":
    load_saved_artifacts()
    print(get_Type())
    print(get_Furnishing())
    print(get_Locality_names())
    print(get_estimated_price('Alaknanda', 'Furnished', 'Apartment', 1500, 3, 3, 1))
