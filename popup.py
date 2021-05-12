from collections import OrderedDict
import tkinter

""" 
Taken from: https://www.semicolonworld.com/question/54647/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
Modified by Jay Zhong to have multiple input fields.
"""

class PopupTwoFields(object):

    root = None

    def __init__(self, receiver, msg, entry_names):
        """
        msg = [<str>] the message to be displayed at each entry point
        entry_names [<str>] = a list of keys that we'll use for our input fields
        """
        tki = tkinter
        self.top = tki.Toplevel(PopupTwoFields.root)
        self.data= None
        self.receiver = receiver
        frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        self.entry_fields = OrderedDict()
        for i in range(len(msg)):
            tki.Label(frm, text=msg[i]).pack(padx=4, pady=4)
            self.entry_fields[entry_names[i]] = tki.Entry(frm)
            self.entry_fields[entry_names[i]].pack(pady=4)

        b_submit = tki.Button(frm, text='Submit')
        b_submit['command'] = lambda: self.get_data(self.entry_fields)
        b_submit.pack()

        b_cancel = tki.Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)


    def get_data(self, dict_key):
        data = OrderedDict()
        for key, entry in dict_key.items():
            data[key] = entry.get()
        self.top.destroy()
        self.receiver.receive(data)

if __name__ == "__main__":
    root = tkinter.Tk()

    Mbox = PopupTwoFields
    Mbox.root = root

    D = {'user':'Bob'}

    b_login = tkinter.Button(root, text='Log in')
    b_login['command'] = lambda: Mbox(['Name?', "Password?"], ["Name", "Password"])
    b_login.pack()

    b_loggedin = tkinter.Button(root, text='Current User')
    b_loggedin['command'] = lambda: Mbox(D['Name'])
    b_loggedin.pack()

    root.mainloop()