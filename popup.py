import tkinter

""" 
Taken from: https://www.semicolonworld.com/question/54647/correct-way-to-implement-a-custom-popup-tkinter-dialog-box
Modified by Jay Zhong to have two input fields.
"""

class PopupTwoFields(object):

    root = None

    def __init__(self, msg, dict_key=None):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        tki = tkinter
        self.top = tki.Toplevel(PopupTwoFields.root)

        frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)

        label = tki.Label(frm, text=msg)
        label.pack(padx=4, pady=4)

        caller_wants_an_entry = dict_key is not None

        if caller_wants_an_entry:
            self.entry = tki.Entry(frm)
            self.entry.pack(pady=4)

            b_submit = tki.Button(frm, text='Submit')
            b_submit['command'] = lambda: self.entry_to_dict(dict_key)
            b_submit.pack()

        b_cancel = tki.Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)

    def entry_to_dict(self, dict_key):
        data = self.entry.get()
        if data:
            d, key = dict_key
            d[key] = data
            self.top.destroy()

if __name__ == "__main__":
    root = tkinter.Tk()

    Mbox = PopupTwoFields
    Mbox.root = root

    D = {'user':'Bob'}

    b_login = tkinter.Button(root, text='Log in')
    b_login['command'] = lambda: Mbox('Name?', (D, 'user'))
    b_login.pack()

    b_loggedin = tkinter.Button(root, text='Current User')
    b_loggedin['command'] = lambda: Mbox(D['user'])
    b_loggedin.pack()

    root.mainloop()