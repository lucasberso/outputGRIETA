

from path import Path
import pandas as pd
from matplotlib import pyplot as plt
from GRIETA_Lengths import GRIETA_Critical_Lengths

testcases_dir = Path(__file__).dirname()

def calculate_atotal(dataframe, hole_diam, Total_crack_length_option, input_hole_steps):
    atotal_list = []
    for i in range(0,dataframe.shape[0]):
        if dataframe["Input Steps"][i] <= input_hole_steps:
            if Total_crack_length_option == "A":
                atotal = dataframe["Crack a"][i] + hole_diam
                atotal_list.append(atotal)
            elif Total_crack_length_option == "c":
                atotal = dataframe["Crack c"][i] + hole_diam
                atotal_list.append(atotal)
            elif Total_crack_length_option == "A+C":
                atotal = dataframe["Crack a"][i] + dataframe["Crack c"][i] + hole_diam
                atotal_list.append(atotal)
        else:
            if Total_crack_length_option == "A":
                atotal = dataframe["Crack a"][i]
                atotal_list.append(atotal)
            elif Total_crack_length_option == "c":
                atotal = dataframe["Crack c"][i]
                atotal_list.append(atotal)
            elif Total_crack_length_option == "A+C":
                atotal = dataframe["Crack a"][i] + dataframe["Crack c"][i]
                atotal_list.append(atotal)
    # dataframe.assign(atotal_list)
    dataframe['a total'] = atotal_list




if __name__ == '__main__':
    # Input data needed
    # hole_diam = 6.8
    # Files_per_mission = 3
    # Total_crack_length_option = "A+C" # Options: A, C and A+C
    # input_hole_steps = 1



    # Script para comprobar los datos obetidos por la librería joint1dISAMI.
    Input_Excel = r"C:\Users\javier.vela\Documents\Automatización\GRIETA\Plantilla_PRUEBA.xlsx"
    Data_Folder = r"C:\Users\javier.vela\Documents\Automatización\GRIETA\Ejemplo"
    out_folder = r"C:\Users\javier.vela\Documents\Automatización\GRIETA"
    out_name = "TXT_OUTPUT"
    Coding = GRIETA_Critical_Lengths(Input_Excel, Data_Folder)
    df_all = Coding.Read_files()
    df_all = Coding.Obtain_Crack_Length(df_all)
    # Coding.Plot_Crack_Length(df_all)
    Coding.Compute_Critical_Crack_Lengths(df_all, out_folder, out_name)

#    filename = 'grieta_F1802-3-lr_1.num'  # Nombre del archivo Excel con los datos de entrada.
#    input_file = testcases_dir + "/" + filename
#
#    with open(filename) as f:
#        content = f.readlines()
#        count = 0
#        content_mat = []
#        input_steps = 0
#        for line in content:
#            new_list_2 = []
#            new_list = line.split()
#            for item in new_list:
#                new_list_2.append(float(item))
#
#            All_zeros = "Yes"
#            for i in range(0, len(new_list_2)):
#                if new_list_2[i]!= 0:
#                    All_zeros = "No"
#
#            if All_zeros == "No":
#                new_list_2.append(input_steps)
#                content_mat.append(new_list_2)
#                # content[count] = new_list_2
#                # count = count + 1
#            else:
#                input_steps = input_steps + 1
#    content = content_mat
#    # Reroder content list
#    content_order = []
#    for j in range(0, len(content[0])):
#        content_order.append([])
#        for i in range(0, len(content)):
#            content_order[j].append(content[i][j])
#
#    # you may also want to remove whitespace characters like `\n` at the end of each line
#    # content = [x.strip() for x in content]
#    name_list = ["Crack a","Crack b", "Crack c", "Crack d", "Cycles", "Flights", "Beta a", "Beta b", "Beta c", "Beta d", "Klim ab", "Klim cd", "Input Steps"]
#    df = pd.DataFrame()
#    for i in range(0, len(name_list)):
#        df[name_list[i]] = content_order[i]
#
#    calculate_atotal(df, hole_diam, Total_crack_length_option, input_hole_steps)
#
#    plt.plot(df["Flights"], df['a total'])
#    plt.show()
#    print("H")


