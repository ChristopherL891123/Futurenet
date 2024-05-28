
import tkinter

clientGUI = tkinter.Tk()  
clientGUI.geometry("1920x1080")
clientGUI.configure(bg = "#233861")
clientGUI.title("CLIENT - FUTURENET - CHRISTOPHER LAMA")

label1 = tkinter.Label(clientGUI, text="FUTURENET\nCLIENT VERSION\nBy Christopher Lama\nAdvisors: Dr. Carlos Monroy and Dr. Charles Thangaraj",
                       font=("Lekton Bold", -34))
label1.place(x=550, y=25)

updateHistoryButton = tkinter.Button(clientGUI, text="Available Compatible Updates")
updateHistoryButton.place(x=850, y=250, height=100, width=300)

rollOutUpdatesButton = tkinter.Button(clientGUI, text="Updates History")
rollOutUpdatesButton.place(x=850, y=450, height=100, width=300)

checkClientStatusButton = tkinter.Button(clientGUI, text="ML Models")
checkClientStatusButton.place(x=850, y=650, height=100, width=300)

clientGUI.mainloop()