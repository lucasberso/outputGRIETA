import os

import numpy as np
from path import Path
import pandas as pd
from matplotlib import pyplot as plt
from openpyxl import load_workbook
from wrappers import read_table_horiz

class Read_Input_Excel():
    """
    Clase creada para leer el input del archivo Excel
    """
    def __init__(self, Excel_file, folder_data):
        self.folder_data = folder_data
        self.Excel_file = Excel_file
        self.book = load_workbook(self.Excel_file, data_only = True)
        self.files_missions = []
        for row in range(7,12):
            self.files_missions.append(self.book["INPUTS"].cell(row,2).value)
        self.Crack_Length_Calc_Method = self.book["INPUTS"].cell(14,2).value
        self.hole_diameter = self.book["INPUTS"].cell(17,2).value
        self.limit_stress = self.book["INPUTS"].cell(21,2).value
        self.load_case = self.book["INPUTS"].cell(22,2).value


    def Read_files(self):
        list_files = os.listdir(self.folder_data)
        SR_files = []
        MR_files = []
        LR_files = []
        ULR_files = []
        MIX_files = []
        for file in list_files:
            for mission_file in self.files_missions:
                if mission_file != None:
                    if file[:len(mission_file)] == mission_file and file[-5:] == "num.1":
                        if mission_file[-2:] == "sr":
                            SR_files.append(file)
                        elif mission_file[-2:] == "mr":
                            MR_files.append(file)
                        elif mission_file[-2:] == "lr":
                            LR_files.append(file)
                        elif mission_file[-3:] == "ulr":
                            ULR_files.append(file)
                        elif mission_file[-3:] == "mix":
                            MIX_files.append(file)
        All_missions = []
        All_missions.append(SR_files)
        All_missions.append(MR_files)
        All_missions.append(LR_files)
        All_missions.append(ULR_files)
        All_missions.append(MIX_files)

        content_mat = []
        for i in range(0, len(All_missions)):
            content_mat.append([])
            input_steps = 0
            for j in range(0, len(All_missions[i])):
                filename = self.folder_data + "/" + All_missions[i][j]
                with open(filename) as f:
                    content = f.readlines()
                    for line in content:
                        new_list_2 = []
                        new_list = line.split()
                        for item in new_list:
                            new_list_2.append(float(item))

                        All_zeros = "Yes"
                        for t in range(0, len(new_list_2)):
                            if new_list_2[t] != 0:
                                All_zeros = "No"

                        if All_zeros == "No":
                            new_list_2.append(input_steps)
                            content_mat[i].append(new_list_2)
                        else:
                            input_steps = input_steps + 1
        content = content_mat
        # Reroder content list
        content_order = []
        for k in range(0, len(content)):
            content_order.append([])
            if len(content[k]) > 0:
                for j in range(0, len(content[k][0])):
                    content_order[k].append([])
                    for i in range(0, len(content[k])):
                        content_order[k][j].append(content[k][i][j])

        name_list = ["Crack a", "Crack b", "Crack c", "Crack d", "Cycles", "Flights", "Beta a", "Beta b", "Beta c",
                     "Beta d", "Klim ab", "Klim cd", "Input Steps"]
        df_all = []
        for k in range(0, len(content_order)):
            df_all.append([])
            df_all[k] = pd.DataFrame()
            if len(content_order[k]) > 0:
                for i in range(0, len(name_list)):
                    df_all[k][name_list[i]] = content_order[k][i]

        return(df_all)

    def Obtain_Crack_Length(self, dataframe_all):
        for k in range(0, len(dataframe_all)):
            atotal_list = []
            for i in range(0, dataframe_all[k].shape[0]):
                if dataframe_all[k]["Crack b"][i] != 0 or dataframe_all[k]["Crack d"][i] != 0:
                    if self.Crack_Length_Calc_Method == "A":
                        atotal = dataframe_all[k]["Crack a"][i] + self.hole_diameter
                        atotal_list.append(atotal)
                    elif self.Crack_Length_Calc_Method == "c":
                        atotal = dataframe_all[k]["Crack c"][i] + self.hole_diameter
                        atotal_list.append(atotal)
                    elif self.Crack_Length_Calc_Method == "A+C":
                        atotal = dataframe_all[k]["Crack a"][i] + dataframe_all[k]["Crack c"][i] + self.hole_diameter
                        atotal_list.append(atotal)
                else:
                    if self.Crack_Length_Calc_Method == "A":
                        atotal = dataframe_all[k]["Crack a"][i]
                        atotal_list.append(atotal)
                    elif self.Crack_Length_Calc_Method == "c":
                        atotal = dataframe_all[k]["Crack c"][i]
                        atotal_list.append(atotal)
                    elif self.Crack_Length_Calc_Method == "A+C":
                        atotal = dataframe_all[k]["Crack a"][i] + dataframe_all[k]["Crack c"][i]
                        atotal_list.append(atotal)
            # dataframe.assign(atotal_list)
            dataframe_all[k]['a total'] = atotal_list
        return(dataframe_all)

    def Plot_Crack_Length(self, dataframe_all):
        missions_list = ["SR", "MR", "LR", "ULR", "MIX"]
        legend_mat = []
        for k in range(0, len(dataframe_all)):
            if len(dataframe_all[k]) > 0:
                plt.plot(dataframe_all[k]["Flights"], dataframe_all[k]['a total'])
                legend_mat.append(missions_list[k])
        plt.legend(legend_mat)
        plt.xlabel("Number of Flights")
        plt.ylabel("Crack length (mm)")
        plt.show()


    def Compute_Critical_Crack_Lengths(self, df_all):
        Fracture_Mechs_criterion = self.book["INPUTS"].cell(24,2).value
        Net_sect_yield_criterion = self.book["INPUTS"].cell(25, 2).value
        Fast_crack_growth_criterion = self.book["INPUTS"].cell(26, 2).value
        Crit_crack_length_cons = self.book["INPUTS"].cell(27, 2).value

        # Obtain the critical lengths on each of the methods
        if Fracture_Mechs_criterion == "KR curve":
            # Read KR curve
            row = 35
            col = 1
            KR_curve_list = []
            cont = 0
            while self.book["INPUTS"].cell(row, col).value != None:
                KR_curve_list.append([])
                KR_curve_list[cont].append(self.book["INPUTS"].cell(row, col).value)
                KR_curve_list[cont].append(self.book["INPUTS"].cell(row, col + 1).value * 0.3)
                row = row + 1
                cont = cont + 1

            KR_curve = np.array(KR_curve_list)

            plt.plot(KR_curve[:, 0], KR_curve[:, 1])
            plt.plot(df_all[0]["Crack a"], df_all[0]["Klim ab"])
            plt.plot(df_all[1]["Crack a"], df_all[1]["Klim ab"])
            plt.plot(df_all[2]["Crack a"], df_all[2]["Klim ab"])
            plt.plot(df_all[4]["Crack a"], df_all[4]["Klim ab"])
            plt.show()

            Crit_Lengths_FM = self.KR_curve_calc(df_all, KR_curve)
            plt.plot(KR_curve[:, 0], KR_curve[:, 1])
            plt.plot(df_all[0]["Crack a"], df_all[0]["Klim ab"])
            plt.plot(df_all[1]["Crack a"], df_all[1]["Klim ab"])
            plt.plot(df_all[2]["Crack a"], df_all[2]["Klim ab"])
            plt.plot(df_all[4]["Crack a"], df_all[4]["Klim ab"])
            plt.show()
            print("hola")

        # elif Fracture_Mechs_criterion == "Residual strength":
        #     Crit_Lengths_FM = self.Residual_Strength_calc()
#
        # if Net_sect_yield_criterion == "Yes":
        #     Crit_Lengths_NSY = self.Net_Sec_Yield_calc()
#
        # if Fast_crack_growth_criterion != "No":
        #     Crit_Lengths_CWC = self.Fast_Growth_Crack_calc(Fast_crack_growth_criterion)

        # Plot the critical crack lengths for each segment and in total with the conservatism method


    def KR_curve_calc(self, df_all, KR_curve):
        perc_tol = 0.05
        tang_mat = []
        for k in range(0, len(df_all)):
            a_0 = 0
            tang_point = ""
            Tangent_Point = "No"
            Limit_Reach = "No"
            if len(df_all[k] > 0):
                while Tangent_Point == "No" and Limit_Reach == "No":
                    for i in range(1, KR_curve.shape[0]):
                        K_curve = KR_curve[i,1]
                        a_curve = KR_curve[i,0] + a_0
                        K_actual = 0
                        for j in range(0, len(df_all[k]["Crack a"]) - 1):
                            if a_curve > df_all[k]["Crack a"][j] and a_curve < df_all[k]["Crack a"][j + 1]:
                                K_actual = df_all[k]["Klim ab"][j] + (df_all[k]["Klim ab"][j + 1] - df_all[k]["Klim ab"][j])/(df_all[k]["Crack a"][j + 1] - df_all[k]["Crack a"][j]) *(a_curve - df_all[k]["Crack a"][j])
                                break

                        if K_actual > K_curve * (1 - perc_tol) and K_actual < K_curve * (1 + perc_tol):
                            if Tangent_Point == "Yes": # THIS MEANS THAT TWO TANGENT POINTS HAS BEEN FOUNDED WHICH CAN BE AN ERROR DUE TO THE TOLERANCE
                                Tangent_Point = "No"
                            else:
                                tang_point = a_curve
                                Tangent_Point = "Yes"

                        elif K_curve > K_actual:
                            Tangent_Point = "No"
                            break

                    a_0 = a_0 + 1
                    if a_0 == 104:
                        Tangent_Point = "No"
                    if a_0 > df_all[0]["Crack a"][len(df_all[0]["Crack a"]) - 1]:
                        Limit_Reach = "Yes"
                if Tangent_Point == "No":
                    tang_point = df_all[0]["Crack a"][len(df_all[0]["Crack a"]) - 1]
                tang_mat.append(tang_point)
            else:
                tang_mat.append("")
        return(tang_mat)


"""
    def Residual_Strength_calc(self):

    def Net_Sec_Yield_calc(self):

    def Fast_Growth_Crack_calc(self, Method):
    
"""