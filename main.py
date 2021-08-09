

from path import Path
import pandas as pd

testcases_dir = Path(__file__).dirname()

def calculate_atotal(dataframe):
    atotal_list = []
    for i in range(0,dataframe.shape[0]):
        atotal = dataframe[0][i] + dataframe[2][i]
        atotal_list.append(atotal)
    # dataframe.assign(atotal_list)
    dataframe['a total'] = atotal_list


if __name__ == '__main__':
    # Script para comprobar los datos obetidos por la librería joint1dISAMI.

    filename = 'grieta_F1802-3-lr_1.num'  # Nombre del archivo Excel con los datos de entrada.
    input_file = testcases_dir + "/" + filename

    with open(filename) as f:
        content = f.readlines()
        count = 0
        for line in content:
            new_list_2 = []
            new_list = line.split()
            for item in new_list:
                new_list_2.append(float(item))
            content[count] = new_list_2
            count = count + 1
    # you may also want to remove whitespace characters like `\n` at the end of each line
    # content = [x.strip() for x in content]
    df = pd.DataFrame(content)
    calculate_atotal(df)
    print("H")
