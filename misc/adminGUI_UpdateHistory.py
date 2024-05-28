
import tkinter

AdminGUI_UpdateHistory = tkinter.Tk()  
AdminGUI_UpdateHistory.geometry("1920x1080")
AdminGUI_UpdateHistory.configure(bg = "#233861")
AdminGUI_UpdateHistory.title("ADMIN - FUTURENET - CHRISTOPHER LAMA")

label1 = tkinter.Label(AdminGUI_UpdateHistory, text="Enter update number: ", font=("Times", "12", "bold"))
label1.place(x=300, y=60)

Textbox = tkinter.Text(AdminGUI_UpdateHistory, height=1, width=10)
Textbox.place(x=470, y=60)

UpdateHistoryTextbox = tkinter.Text(AdminGUI_UpdateHistory, height=40, width=200)
UpdateHistoryTextbox.place(x=50, y=100)

# the buttons below read the input present in the label1
sendNotificationButton = tkinter.Button(AdminGUI_UpdateHistory, text="Send notification to client")
sendNotificationButton.place(x=300, y=850, height=100, width=300)

viewChangelogButton = tkinter.Button(AdminGUI_UpdateHistory, text="View changelog")
viewChangelogButton.place(x=800, y=850, height=100, width=300)

AdminGUI_UpdateHistory.mainloop()
