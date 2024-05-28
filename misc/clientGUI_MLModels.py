
import tkinter

clientGUI_MLModels = tkinter.Tk()  
clientGUI_MLModels.geometry("1920x1080")
clientGUI_MLModels.configure(bg = "#233861")
clientGUI_MLModels.title("CLIENT - FUTURENET - CHRISTOPHER LAMA")

label1 = tkinter.Label(clientGUI_MLModels, text="ML models on client",
                       font=("Lekton Bold", -24))
label1.place(x=550, y=25)

label1 = tkinter.Label(clientGUI_MLModels, text="Model number: ", font=("Times", "12", "bold"))
label1.place(x=300, y=60)

Textbox = tkinter.Text(clientGUI_MLModels, height=1, width=10)
Textbox.place(x=470, y=60)

MLModelsTextbox = tkinter.Text(clientGUI_MLModels, height=40, width=200)
MLModelsTextbox.place(x=50, y=100)

# the buttons below read the input present in the label1
removeModelButton = tkinter.Button(clientGUI_MLModels, text="Remove Model from Client")
removeModelButton.place(x=300, y=850, height=100, width=300)

downloadModelButton = tkinter.Button(clientGUI_MLModels, text="Download Model")
downloadModelButton.place(x=800, y=850, height=100, width=300)

clientGUI_MLModels.mainloop()
