
import tkinter

clientGUI_MLModels = tkinter.Tk()  
clientGUI_MLModels.geometry("1920x1080")
clientGUI_MLModels.configure(bg = "#233861")
clientGUI_MLModels.title("CLIENT - FUTURENET - CHRISTOPHER LAMA")

label1 = tkinter.Label(clientGUI_MLModels, text="Available updates",
                       font=("Lekton Bold", -24))
label1.place(x=550, y=25)

UpdateHistoryTextbox = tkinter.Text(clientGUI_MLModels, height=40, width=200)
UpdateHistoryTextbox.place(x=50, y=100)

clientGUI_MLModels.mainloop()
