# This is code that calculates the "Josephus-Problem"
# might be interesting to code up a way to calculate who the final two are. That way, you can save one other person.
import PySimpleGUI as sg

class Josephus:
    def __init__(self):
        self.main()
        # TODO: code more generalized-solution to the Josephus Problem

    def main(self):

        self.window = self.create_Main_Window()
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "EXIT"): break
            elif event == "SUBMIT_0":
                if self.input_Validation(values["NUM_OF_PLAYERS_FIXED"]): continue
                l = self.Josephus_Calculation_fixed_step(values)
                Winning_Position = 2*l + 1
                sg.popup(f"Winning position is: {Winning_Position}", title = "Winning Number")
            elif event == "SUBMIT_1":
                if self.input_Validation(values["NUM_OF_PLAYERS_GENERAL"], values["STEP_SIZE"]): continue
                sg.popup(f"Winning position is: {(self.Josephus_Calculation_General_Solution(values))}")

        self.window.close()

    def create_Main_Window(self):

        k_2 = sg.Frame("Step-size = 2", 
            [
                [sg.Text("k is defaulted to two")],
                [sg.Text("Please enter the number of players"), sg.Input("", key = "NUM_OF_PLAYERS_FIXED")],
                [sg.Button("Submit", key = "SUBMIT_0")]
                ],
            size = (400, 100))
        general_Solution = sg.Frame("General Solution", [
            [sg.Text("Please enter your step size: "), sg.Input("", key = "STEP_SIZE")],
            [sg.Text("Please enter the number of players "), sg.Input("", key = "NUM_OF_PLAYERS_GENERAL")],
            [sg.Button("Submit", key = "SUBMIT_1")]
        ])
        layout = [[k_2, general_Solution]]
        return sg.Window("Josephus Problem", layout, resizable = True)
    
    def Josephus_Calculation_fixed_step(self, values):
        # look for l, m such that l + 2^m = Number_of_Players and that 0 <= l < 2^m
        M = 0
        Number_of_Players = float(values["NUM_OF_PLAYERS_FIXED"])
        while 2**M < Number_of_Players: # Say, N = 8. True. Set M = 1. True. Set M = 2. True. Set M = 3. # Ahh. M gets 1-more increment than we want. 
            M = M + 1
        l = Number_of_Players - 2**(M - 1) # this should work. Standard Equation, though, is l = n - 2^m.
        return l
    def Josephus_Calculation_General_Solution(self, values): # J(i,k)=(J(i−1,k)+k) modi
        n = int(values["NUM_OF_PLAYERS_GENERAL"])
        k = int(values["STEP_SIZE"])
        J = 0 # zero-based answer for 1-player
        for i in range(2, n + 1):
            J = (J + k) % i 
        return J + 1
    def input_Validation(self, *args):
        for test_Input in args:
            if test_Input == '' or test_Input == '0':
                sg.popup("Invalid Input", title = "Invalid input: error - Emp")
                return True
            try: #try-excepts are useful
                int(test_Input)
            except:
                sg.popup("Input must be an integer.", title = "Invalid input: error - Int")
                return True
        return False

if __name__ == "__main__":
    Executable = Josephus()