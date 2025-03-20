# This is code that calculates the "Josephus-Problem"
# TODO: code more generalized-solution to the Josephus Problem
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
            elif event == "SUBMIT":
                m, l = self.Josephus_Calculation(values)
                Winning_Position = 2*l + 1
                sg.popup(f"Winning position is: {Winning_Position}", title = "Winning Number")

        self.window.close()

    def create_Main_Window(self):

        k_2 = sg.Frame("Step-size = 2", 
            [
                [sg.Text("k is defaulted to two")],
                [sg.Text("Please enter the number of players"), sg.Input("", key = "NUM_OF_PLAYERS")],
                [sg.Button("Submit", key = "SUBMIT")]
                ],
            size = (400, 100))
        layout = [[k_2]]
        return sg.Window("Josephus Problem", layout, resizable = True)
    
    def Josephus_Calculation(self, values):
        # look for l, m such that l + 2^m = Number_of_Players and that 0 <= l < 2^m
        M = 0
        Number_of_Players = float(values["NUM_OF_PLAYERS"])
        while 2**M <= Number_of_Players: # TEST_0, I_1. TEST_1, I_2. TEST_2, I_3.
            M = M + 1
            print(M)
        l = Number_of_Players - 2**(M - 1)
        return M, l
        
if __name__ == "__main__":
    Executable = Josephus()

