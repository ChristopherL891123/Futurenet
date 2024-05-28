
import tkinter

AdminGUI_MLModels = tkinter.Tk()  
AdminGUI_MLModels.geometry("1920x1080")
AdminGUI_MLModels.configure(bg = "#233861")
AdminGUI_MLModels.title("ADMIN - FUTURENET - CHRISTOPHER LAMA")

label1 = tkinter.Label(AdminGUI_MLModels, text="ML models by Client",
                       font=("Lekton Bold", -24))
label1.place(x=550, y=25)


UpdateHistoryTextbox = tkinter.Text(AdminGUI_MLModels, height=40, width=200)
UpdateHistoryTextbox.place(x=50, y=100)

AdminGUI_MLModels.mainloop()
