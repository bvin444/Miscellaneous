# This is code to evaluate PRBS
import PySimpleGUI as sg


class PRBS:
    
    def __init__(self):
        
        self.main()
    
    def main(self):

        self.window = self.create_main_window()

        while True:
            
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation("SEED", values = values): continue
                self.PRBS_Calculator()

    def create_main_window(self):

        PRBS_Frame = sg.Frame("PRBS",
            [
                [sg.Text("Please enter your seed:"), sg.Input("", key = "SEED")],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ])
        
        layout = [[PRBS_Frame]]

        return sg.Window("PRBS Analysis", layout, resizable = True)

    def PRBS_Calculator(self):
        self.create_Array()
    def create_Array(self):

        hold = self.numerical_Dictionary["SEED"]
        Array = []
        while hold != 0:
            Array.append(int(hold % 10))
            print(hold)
            hold = hold // 10 
            print(hold)
        print(Array)
    
    def input_Validation(self, *args, values):

        for test_Input in args:
            if test_Input == '':
                sg.popup("Input cannot be blank")
                return True
            try:
                float(values[test_Input])
            except:
                sg.popup("Input must be a numeric")
                return True
        self.numerical_Dictionary = {key: float(values[key]) for key in args}

if __name__ == "__main__":

    Executable = PRBS()

