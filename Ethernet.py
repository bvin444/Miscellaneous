# This code is designed to simulate the basic functionality of Ethernet
import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict

class ethernet:
    
    Negative_Lookup_5b_6b : ClassVar[Dict] = {
    '00000': '100111', '00001': '011101', '00010': '101101', '00011': '110001',
    '00100': '110101', '00101': '101001', '00110': '011001', '00111': '111000',
    '01000': '111001', '01001': '100101', '01010': '010101', '01011': '110100',
    '01100': '001101', '01101': '101100', '01110': '011100', '01111': '010111',
    '10000': '011011', '10001': '100011', '10010': '010011', '10011': '110010',
    '10100': '001011', '10101': '101010', '10110': '011010', '10111': '111010',
    '11000': '110011', '11001': '100110', '11010': '010110', '11011': '110110',
    '11100': '001110', '11101': '101110', '11110': '011110', '11111': '101011',
    }
    Positive_Lookup_5b_6b : ClassVar[Dict] = {
    '00000': '011000', '00001': '100010', '00010': '010010', '00011': '110001',
    '00100': '001010', '00101': '010001', '00110': '100001', '00111': '000111',
    '01000': '000110', '01001': '100101', '01010': '101001', '01011': '001100',
    '01100': '110100', '01101': '010110', '01110': '100110', '01111': '101000',
    '10000': '100100', '10001': '011100', '10010': '101100', '10011': '001001',
    '10100': '110100', '10101': '010100', '10110': '100100', '10111': '000101',
    '11000': '001100', '11001': '011001', '11010': '101001', '11011': '001101',
    '11100': '110001', '11101': '011001', '11110': '101001', '11111': '010100',
    }
    Negative_Lookup_3b_4b : ClassVar[Dict] = {
    '000': '1011', '001': '1001', '010': '0101', '011': '1100',
    '100': '1101', '101': '1010', '110': '0110', '111': '1110',
    }
    Positive_Lookup_3b_4b : ClassVar[Dict] = {
    '000': '0100', '001': '0110', '010': '1010', '011': '0011',
    '100': '0010', '101': '0101', '110': '1001', '111': '0001',
    }

    def __init__(self):

        self.Disparity = -1
        self.main()

    def main(self):

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
        six_b = ethernet.Positive_Lookup_5b_6b[five_b]
        four_b = ethernet.Positive_Lookup_3b_4b[three_b]
        ten_B = six_b+ four_b
        return ten_B
    
    def Negative(self, values):

        five_b, three_b = self.partition_Pattern(values)
        six_b = ethernet.Negative_Lookup_5b_6b[five_b]
        four_b = ethernet.Negative_Lookup_3b_4b[three_b]
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
            sg.popup("Input cannot be blank", size = (50, 50), title = "Blank Input")
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