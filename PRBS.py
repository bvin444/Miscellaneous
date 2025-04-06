# This is code to evaluate PRBS
import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict

class PRBS:
    
    # class variable
    parameters_Dictionary : ClassVar[Dict] = {"7" : 1, "9" : 4, "11" : 2, "13": 1, "15" : 1, "20" : 17, "23" : 5}
    primitive_taps_2 : ClassVar[Dict[int, list[int]]] = {1: [1], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [0, 3], 6: [0, 5], 7: [0, 1], 9: [0, 4], 10: [0, 3], 11: [0, 2], 15: [0, 1], 17: [0, 14], 18: [0, 11],
                                    20: [0, 3], 21: [0, 19], 22: [0, 21], 23: [0, 5], 8: [0, 2, 3, 4], 12: [0, 6, 8, 11], 13: [0, 1, 11, 12], 14: [0, 1, 2, 12], 16: [0, 2, 3, 5], 19: [0, 14, 17, 18]}

    def __init__(self):
        
        self.main()
    
    def main(self):

        self.window = self.create_main_window()

        while True:
            
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation("SEED", values = values): continue
                self.PRBS_Calculator(values)

    def create_main_window(self):

        PRBS_Frame = sg.Frame("PRBS",
            [
                [sg.Text("This code allows you to specify seeds for PRBS7, PRBS9, PRBS11, PRBS15, PRBS20, and PRBS23")],
                [sg.Text("Please enter your seed:"), sg.Input("", key = "SEED")],
                [sg.Text("The length of sequence is: "), sg.Input("", key = "LE")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Text("Note: Your PRBS can be found in the terminal after pressing submit.")],
                [sg.Button("Exit", key = "EXIT")]
            ])
        
        layout = [[PRBS_Frame]]

        return sg.Window("PRBS Analysis", layout, resizable = True)

    def PRBS_Calculator(self, values):

        binary_Array = self.value
        length_Array = len(binary_Array) # length of input array
        hold = []
        for i in range(2**(length_Array) - 1):
            sum = self.get_Sum(length_Array, binary_Array)
            if sum % 2 == 1:
                binary_Array.insert(length_Array, 1)
                hold.append(binary_Array[0])
                binary_Array.pop(0)
            else:
                binary_Array.insert(length_Array, 0)
                hold.append(binary_Array[0])
                binary_Array.pop(0)
        print(hold)
        print(binary_Array)
        self.window["LE"].update(f"{len(hold)}")
    
    def get_Sum(self, Length, binary_Array):

        iteration_N = len(PRBS.primitive_taps_2[Length]) # number of taps
        sum = 0
        index = 0
        for i in range(1, iteration_N + 1):
            sum = sum + binary_Array[PRBS.primitive_taps_2[Length][index]]
            index = index + 1
        return sum
    
    def input_Validation(self, *args, values):

        self.value = []
        for test_Input in args:
            if values[test_Input] == '':
                sg.popup("Input cannot be blank")
                return True
            if len(values[test_Input]) > 23:
                sg.popup("Please enter no more than 23-bits!")
                return True
            for i in values[test_Input]:
                if i != '1' and i != '0':
                    sg.popup("Input must be a binary value (eg. 0001000)")
                    return True
                else:
                    self.value.append(int(i))
                
        self.numerical_Dictionary = {key: float(values[key]) for key in args}
        return False

if __name__ == "__main__":

    Executable = PRBS()