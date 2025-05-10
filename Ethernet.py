# This code is designed to simulate the basic functionality of Ethernet
# Have to keep in mind the specific formatting scheme of JSON -> 'JavaScript Object Notation'

import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict
import json

class ethernet:

    code_T : ClassVar[Dict] = {"K": 1, "D": 0}
    def __init__(self):

        self.Disparity_tX = -1
        self.Disparity_rX = -1
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
                self.get_Running_Disparity_Tx(values)
            elif event == "DECODE":
                self.get_Running_Disparity_Rx(values)
        self.window.close()

    def create_main_window(self):

       Transceiver_Frame = sg.Frame("Ethernet", 
            [
                [sg.Text("Please enter the binary-value you would like to send:"), sg.Input("", key = 'BINARY_INPUT'), 
                sg.Text("Please select code Type"), sg.Combo(list(ethernet.code_T),default_value = "D", key = "CODE_TYPE")],
                [sg.Text("8b/10-Representation"), sg.Input('', key = "ENCODED_OUTPUTtx")],
                [sg.Text("Running-Disparity"), sg.Input('-1 (Default)', key = "DISPARITYTX")],

            ])
       Receiver_Frame = sg.Frame("Ethernet", 
            [
                [sg.Text("Recieved bits"), sg.Input("", key = 'RECEIVED_W')],
                [sg.Text("Decoded bits"), sg.Input('', key = "DECODED_OUTPUTrx")],
                [sg.Text("Running-Disparity"), sg.Input('-1 (Default)', key = "DISPARITYRX")],
                [sg.Button("Decoded Bye", key = "DECODE")]
            ])
       submission_Frame = sg.Frame("Submi",
            [
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ])
       layout = [[Transceiver_Frame, Receiver_Frame], [submission_Frame]]
       window = sg.Window("Ethernet", layout, resizable = True)
       return window
    
    def get_Running_Disparity_Tx(self, values):

        Flag = self.Code()
        if self.Disparity_tX < 0 and Flag == 1:
            Ten_B = self.Transceiver_Negative(values)
            self.update_Disparity_Tx(Ten_B)
        elif self.Disparity_tX and Flag == 1:
            Ten_B = self.Transceiver_Positive(values)
            self.update_Disparity_Tx(Ten_B)
        else:
            Ten_B = self.K_tx(values)
            self.update_Disparity_Tx(Ten_B)
        self.window["ENCODED_OUTPUTtx"].update(f"{Ten_B}")
        self.window["RECEIVED_W"].update(f"{Ten_B}")
        self.window["DISPARITYTX"].update(f"{self.Disparity_tX}")

    def Transceiver_Positive(self, values):

        five_b, three_b = self.partition_Pattern_Tx(values)
        six_b = self.loaded_data['Positive_Lookup_5b_6b'][five_b]
        four_b = self.loaded_data['Positive_Lookup_3b_4b'][three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def Transceiver_Negative(self, values):

        five_b, three_b = self.partition_Pattern_Tx(values)
        six_b = self.loaded_data['Negative_Lookup_5b_6b'][five_b]
        four_b = self.loaded_data['Negative_Lookup_3b_4b'][three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def partition_Pattern_Tx(self, values):

        five_b = ''
        three_b = ''
        for i in values["BINARY_INPUT"][:5]:
            five_b = five_b + i
        for J in values["BINARY_INPUT"][5:]:
            three_b = three_b + J
        return five_b, three_b
    
    def update_Disparity_Tx(self, Ten_B):
        
        for i in Ten_B:
            if i == '1':
                self.Disparity_tX = 1 + self.Disparity_tX
            elif i == '0':
                self.Disparity_tX = -1 + self.Disparity_tX
    
    def get_Running_Disparity_Rx(self, values):

        six_b, four_b = self.partition_Pattern_Rx(values)
        if six_b in self.loaded_data['K_Lookup_6b_5b'] and four_b in self.loaded_data['K_Lookup_4b_3b']: Eight_Bit = self.K_rx(values)
        elif six_b in self.loaded_data['Negative_Lookup_6b_5b'] and four_b in self.loaded_data['Negative_Lookup_4b_3b']: Eight_Bit = self.Receiver_Negative(values)
        elif six_b in self.loaded_data['Positive_Lookup_6b_5b'] and four_b in self.loaded_data['Positive_Lookup_4b_3b']: Eight_Bit = self.Receiver_Positive(values)
        else:
            sg.popup("Value not found!")
            return 
        self.update_Disparity_Rx(values["RECEIVED_W"])
        self.window["DECODED_OUTPUTrx"].update(f"{Eight_Bit}")
        self.window["DISPARITYRX"].update(f"{self.Disparity_rX}")

    def Receiver_Positive(self, values):

        six_b, four_b = self.partition_Pattern_Rx(values)
        five_b = self.loaded_data['Positive_Lookup_6b_5b'][six_b]
        three_b = self.loaded_data['Positive_Lookup_4b_3b'][four_b]
        eight_B = five_b+ three_b
        return eight_B
    
    def Receiver_Negative(self, values):

        six_b, four_b = self.partition_Pattern_Rx(values)
        five_b = self.loaded_data['Negative_Lookup_6b_5b'][six_b]
        three_b = self.loaded_data['Negative_Lookup_4b_3b'][four_b]
        eight_B = five_b+ three_b
        return eight_B
    
    def partition_Pattern_Rx(self, values):

        six_b = ''
        four_b = ''
        for i in values["RECEIVED_W"][:6]:
            six_b = six_b + i
        for J in values["RECEIVED_W"][6:]:
            four_b = four_b + J
        return six_b, four_b
    
    def update_Disparity_Rx(self, Ten_B):
        
        for i in Ten_B:
            if i == '1':
                self.Disparity_rX = 1 + self.Disparity_rX
            elif i == '0':
                self.Disparity_rX = -1 + self.Disparity_rX
    
    def K_tx(self, values):

        five_b, three_b = self.partition_Pattern_Tx(values)
        six_b = self.loaded_data['K_Lookup_5b_6b'][five_b]
        four_b = self.loaded_data['K_Lookup_3b_4b'][three_b]
        ten_B = six_b+ four_b
        return ten_B

    def K_rx(self, values):

        five_b, three_b = self.partition_Pattern_Rx(values)
        six_b = self.loaded_data['K_Lookup_6b_5b'][five_b]
        four_b = self.loaded_data['K_Lookup_4b_3b'][three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def Code(self, values):
        
        return ethernet.code_T[self.window["CODE_TYPE"]]

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
