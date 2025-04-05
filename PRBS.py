# This is code to evaluate PRBS
import PySimpleGUI as sg
from typing import ClassVar
from typing import Dict

class PRBS:
    
    # class variable
    parameters_Dictionary : ClassVar[int] = {"7" : 1, "9" : 4, "11" : 2, "13": 1, "15" : 1, "20" : 17, "23" : 5}

    def __init__(self):
        
        self.main()
    
    def main(self):

        self.window = self.create_main_window()

        while True:
            
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation("SEED", values = values): continue
                if len(self.value) == 13:
                    self.PRBS13_Calculator(values)
                else:
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
        length_Array = len(binary_Array)
        x = self.get_Parameters(values)
        hold = []
        for i in range(2**(length_Array) - 1):
            if (binary_Array[0] + binary_Array[x]) % 2 == 1:
                binary_Array.insert(length_Array, 1)
                hold.append(binary_Array[0])
                binary_Array.pop(0)
            else:
                binary_Array.insert(length_Array, 0)
                hold.append(binary_Array[0])
                binary_Array.pop(0)
        print(hold)
        print(binary_Array)
        self.window["LE"].update(f"{len(hold) + 1}")

    def PRBS13_Calculator(self, values):

        binary_Array = self.value
        length_Array = len(binary_Array)
        hold = []
        for i in range(2**(length_Array) - 1):
            if (binary_Array[0] + binary_Array[1] + binary_Array[11] + binary_Array[12]) % 2 == 1:
                binary_Array.insert(length_Array, 1)
                hold.append(binary_Array[0])
                binary_Array.pop(0)
            else:
                binary_Array.insert(length_Array, 0)
                hold.append(binary_Array[0])
                binary_Array.pop(0)
        print(hold)
        print(binary_Array)
        self.window["LE"].update(f"{len(hold) + 1}")

    def get_Parameters(self, values):

        dict_Index = str(len(values["SEED"]))
        y = PRBS.parameters_Dictionary[dict_Index]
        return y
    
    def input_Validation(self, *args, values):

        self.value = []
        for test_Input in args:
            if values[test_Input] == '':
                sg.popup("Input cannot be blank")
                return True
            try:
                float(values[test_Input])
            except:
                sg.popup("Input must be a numeric")
                return True
            if str(len(values[test_Input])) not in PRBS.parameters_Dictionary:
                sg.popup("Bit number mismatch! 7, 9, 11, 15, 20, 23")
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