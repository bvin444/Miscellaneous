# This code is designed to simulate the basic functionality of Ethernet
# Have to keep in mind the specific formatting scheme of JSON -> 'JavaScript Object Notation'

import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict
import json

class ethernet:

    def __init__(self):

        self.Disparity = -1
        self.main()
        
    def main(self):

        with open("Encoding_Tables.json", "r") as f:

            self.loaded_data = json.load(f)

        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation(values): continue
                self.get_Running_Disparity(values)
        self.window.close()

    def create_main_window(self):

        sum_Frame = sg.Frame("Ethernet", 
            [
                [sg.Text("Please enter the binary-value you would like to send:"), sg.Input("", key = 'BINARY_INPUT')],
                [sg.Text("8b/10-Representation"), sg.Input('', key = "ENCODED_OUTPUT")],
                [sg.Text("Running-Disparity"), sg.Input('-1 (Default)', key = "DISPARITY")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ])
        layout = [[sum_Frame]]
        window = sg.Window("Ethernet", layout, resizable = True)
        return window
    
    def get_Running_Disparity(self, values):

        if self.Disparity < 0:
            Ten_B = self.Negative(values)
            self.update_Disparity(Ten_B)
        else:
            Ten_B = self.Positive(values)
            self.update_Disparity(Ten_B)
        self.window["ENCODED_OUTPUT"].update(f"{Ten_B}")
        self.window["DISPARITY"].update(f"{self.Disparity}")

    def Positive(self, values):

        five_b, three_b = self.partition_Pattern(values)
        six_b = self.loaded_data['Positive_Lookup_5b_6b'][five_b]
        four_b = self.loaded_data['Positive_Lookup_3b_4b'][three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def Negative(self, values):

        five_b, three_b = self.partition_Pattern(values)
        six_b = self.loaded_data['Negative_Lookup_5b_6b'][five_b]
        four_b = self.loaded_data['Negative_Lookup_3b_4b'][three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def partition_Pattern(self, values):

        five_b = ''
        three_b = ''
        for i in values["BINARY_INPUT"][:5]:
            five_b = five_b + i
        for J in values["BINARY_INPUT"][5:]:
            three_b = three_b + J
        return five_b, three_b
    
    def update_Disparity(self, Ten_B):
        
        for i in Ten_B:
            if i == '1':
                self.Disparity = 1 + self.Disparity
            elif i == '0':
                self.Disparity = -1 + self.Disparity

    def input_Validation(self, values):

        if values["BINARY_INPUT"] == '':
            sg.popup("Input cannot be blank", title = "Blank Input")
            return True
        if len(values["BINARY_INPUT"]) != 8:
            sg.popup("Please enter a byte (8-bits)", title = "Binary Input Error. Cuc")
            return True
        for x in values["BINARY_INPUT"]:
            if x != '1' and x != '0':
                sg.popup("Please enter a binary number!!")
                return True
        
if __name__ == "__main__":
    Executable = ethernet()