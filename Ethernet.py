# This code is designed to simulate the basic functionality of Ethernet
# Have to keep in mind the specific formatting scheme of JSON -> 'JavaScript Object Notation'

import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict
import json

class ethernet:

    code_T : ClassVar[Dict] = {"K": 1, "D": 0}
    hex_Decoder : ClassVar[Dict] = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000',
                                    '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
    def __init__(self):

        self.Disparity_tX = -1
        self.Disparity_rX = -1
        self.tx = 0
        self.rx = 0
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
                if self.rx == self.tx:
                    sg.popup("No new word to decode")
                    continue
                self.get_Running_Disparity_Rx(values)
            elif event == "SEND":
                self.read_Ethernet_Frame(values)
            elif event == "RESET":
                self.Reset()
        self.window.close()

    def create_main_window(self):

       Transceiver_Frame = sg.Frame("Ethernet", 
            [
                [sg.Text("Please enter the binary-value you would like to send:"), sg.Input("", key = 'BINARY_INPUT'), 
                sg.Text("Please select code Type (Control (K) / Data (D))"), sg.Combo(list(ethernet.code_T),default_value = "D", key = "CODE_TYPE")],
                [sg.Text("8b/10-Representation"), sg.Input('', key = "ENCODED_OUTPUTtx")],
                [sg.Text("Running-Disparity"), sg.Input('-1 (Default)', key = "DISPARITYTX")],
                [sg.Text("Send Ethernet _Frame"), sg.Button("Send", key = "SEND")]

            ])
       Receiver_Frame = sg.Frame("Ethernet", 
            [
                [sg.Text("Recieved bits"), sg.Input("", key = 'RECEIVED_W'), sg.Text("Received Code"), sg.Input("", key = "RECEIVED_CODE")],
                [sg.Text("Decoded bits"), sg.Input('', key = "DECODED_OUTPUTrx")],
                [sg.Text("Running-Disparity"), sg.Input('-1 (Default)', key = "DISPARITYRX")],
                [sg.Button("Decoded Bye", key = "DECODE")]
            ])
       submission_Frame = sg.Frame("Submi",
            [
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Reset", key = "RESET"), sg.Button("Exit", key = "EXIT")]
            ])
       layout = [[Transceiver_Frame, Receiver_Frame], [submission_Frame]]
       window = sg.Window("Ethernet", layout, resizable = True)
       return window
    
    def read_Ethernet_Frame(self, values):

        with open("ethernet_Frame.json", "r") as h:

            self.ethernet_Frame = json.load(h)

        self.hex_Deco(values)
        
    def hex_Deco(self, values):

        for key in self.ethernet_Frame:
            length = len(self.ethernet_Frame[key])
            for i in range(length):
                self.hold = ''
                hold_second = ''
                for j in self.ethernet_Frame[key][i]:
                    self.hold = self.hold + ethernet.hex_Decoder[j]
                    hold_second = hold_second + j
                print(f"{hold_second}-Hex translates to {self.hold}-bin.")
                self.get_Running_Disparity_Tx(values)

    def get_Running_Disparity_Tx(self, values):

        Flag = self.Code(values)
        try:
            if self.Disparity_tX < 0 and Flag == 0:
                Ten_B = self.Transceiver_Negative(values)
                self.update_Disparity_Tx(Ten_B)
            elif self.Disparity_tX and Flag == 0:
                Ten_B = self.Transceiver_Positive(values)
                self.update_Disparity_Tx(Ten_B)
            elif Flag == 1:
                Ten_B = self.K_tx(values)
                self.update_Disparity_Tx(Ten_B)
        except ValueError as e:
            sg.popup(str(e))
            return
        self.window["ENCODED_OUTPUTtx"].update(f"{Ten_B}")
        self.window["RECEIVED_W"].update(f"{Ten_B}")
        self.window["RECEIVED_CODE"].update(f"{values["CODE_TYPE"]}")
        self.window["DISPARITYTX"].update(f"{self.Disparity_tX}")
        self.tx = self.tx + 1

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
        ten_B = six_b + four_b
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

    def K_tx(self, values):

        five_b, three_b = self.partition_Pattern_Tx(values)
        if five_b not in self.loaded_data['K_Lookup_5b_6b'] or three_b not in self.loaded_data['K_Lookup_3b_4b']: 
            raise ValueError("K-code not found!")
        print("Hi")
        six_b = self.loaded_data['K_Lookup_5b_6b'][five_b]
        four_b = self.loaded_data['K_Lookup_3b_4b'][three_b]
        ten_B = six_b + four_b
        return ten_B
    
    def get_Running_Disparity_Rx(self, values):

        N65 = self.loaded_data['Negative_Lookup_6b_5b']
        N43 = self.loaded_data['Negative_Lookup_4b_3b']
        P65 = self.loaded_data['Positive_Lookup_6b_5b']
        P43 = self.loaded_data['Positive_Lookup_4b_3b']
        
        six_b, four_b = self.partition_Pattern_Rx(values)
        Flag = self.Code(values)

        if six_b in self.loaded_data['K_Lookup_6b_5b'] and \
            four_b in self.loaded_data['K_Lookup_4b_3b'] and \
                Flag == 1:
                    Eight_Bit = self.K_rx(values)

        elif (six_b in N65 and four_b in N43) and \
            (six_b in P65 and four_b in P43):
            if self.Disparity_rX < 0:
                Eight_Bit = self.Receiver_Negative(values)
            elif self.Disparity_rX > 0:
                Eight_Bit = self.Receiver_Positive(values)

        elif six_b in N65 and four_b in N43:
            Eight_Bit = self.Receiver_Negative(values)
        elif six_b in P65 and four_b in P43:
            Eight_Bit = self.Receiver_Positive(values)

        else:
            sg.popup("Value not found!")
            return

        self.update_Disparity_Rx(values["RECEIVED_W"])
        self.window["DECODED_OUTPUTrx"].update(f"{Eight_Bit}")
        self.window["DISPARITYRX"].update(f"{self.Disparity_rX}")
        self.rx = self.rx + 1

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
        eight_B = five_b + three_b
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

    def K_rx(self, values):

        five_b, three_b = self.partition_Pattern_Rx(values)
        six_b = self.loaded_data['K_Lookup_6b_5b'][five_b]
        four_b = self.loaded_data['K_Lookup_4b_3b'][three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def Code(self, values):
        
        return ethernet.code_T[values["CODE_TYPE"]]

    def Reset(self):

        self.tx = 0
        self.rx = 0

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
