import tkinter as tk
from collections import OrderedDict

def automatic_spacer(name,email, spacing = 20):
    return f"{name.ljust(spacing)}{email.rjust(spacing)}"


top = tk.Tk()
stakeholders = OrderedDict()
stakeholders["Jay"] = "jay.zhong@monashtechschool.vic.edu.au"
stakeholders["Danny"] = "danny.tran@monashtechschool.vic.edu.au"
stakeholders["Josh"] = "josh.mclennan@monashtechschool.vic.edu.au"
stakeholders["Andrew"] = "andrew.gray@monashtechschool.vic.edu.au"
spacing = 25

Lb1 = tk.Listbox(top)
Lb1.insert(0, automatic_spacer("Name", "Email", spacing))
for name, email in stakeholders.items():
    Lb1.insert("end", automatic_spacer(name, email, spacing))

Lb1.pack(fill=tk.BOTH)


b = tk.Button(top, text="Delete Top", command = lambda: Lb1.delete(1))
b.pack()
top.mainloop()