
import tkinter

AdminGUI = tkinter.Tk()  
AdminGUI.geometry("1920x1080")
AdminGUI.configure(bg = "#233861")
AdminGUI.title("ADMIN - FUTURENET - CHRISTOPHER LAMA")

label1 = tkinter.Label(AdminGUI, text="FUTURENET\nADMIN VERSION\nBy Christopher Lama\nAdvisors: Dr. Carlos Monroy and Dr. Charles Thangaraj",
                       font=("Lekton Bold", -34))
label1.place(x=550, y=25)

updateHistoryButton = tkinter.Button(AdminGUI, text="View Update History")
updateHistoryButton.place(x=850, y=250, height=100, width=300)

rollOutUpdatesButton = tkinter.Button(AdminGUI, text="Roll Out Updates")
rollOutUpdatesButton.place(x=850, y=450, height=100, width=300)

checkClientStatusButton = tkinter.Button(AdminGUI, text="Check Client Status")
checkClientStatusButton.place(x=850, y=650, height=100, width=300)

MlModelsButton = tkinter.Button(AdminGUI, text="ML Models by Client")
MlModelsButton.place(x=850, y=850, height=100, width=300)

AdminGUI.mainloop()
