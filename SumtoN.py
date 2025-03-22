# code to calculate sum of integers up to N
import PySimpleGUI as sg

class Sum_of_Integers:
    def __init__(self):
        self.main()
    def main(self):
        self.window = self.create_main_window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT":
                if self.input_Validation(values): continue # break out of current iteration, and begin anew
                sg.popup(f"The sum of integers 1 to N is: {self.Sum(values)}", title = "Sum")
        self.window.close()

    def create_main_window(self):
        sum_Frame = sg.Frame("Sum of Integers up to N", 
            [
                [sg.Text("Please enter your N:"), sg.Input("", key = 'N')],
                [sg.Button("Submit", key = "SUBMIT"), sg.Button("Exit", key = "EXIT")]
            ])
        layout = [[sum_Frame]]
        window = sg.Window("Sum up to N", layout, resizable = True)
        return window
    def Sum(self, values):
        N = int(values["N"]) + 1
        running_Sum = 0
        for i in range(1, N):
            running_Sum = running_Sum + i 
        return running_Sum
    def input_Validation(self, values):
        if values["N"] == '':
            sg.popup("Input cannot be blank", size = (50, 50), title = "Blank Input")
            return True
        try:
            int(values["N"])
            return False
        except:
            sg.popup("Input must be a integer", title = "Integer Input Error", size = (50, 50))
            return True
        
if __name__ == "__main__":
    Executable = Sum_of_Integers()

