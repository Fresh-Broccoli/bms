import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from collections import defaultdict


class BioreactorGmailBot:
    def __init__(self, email, password):
        """ Initialises the bioreactor email bot
        The bot will first make sure that email is a valid Gmail account before logging onto Gmail with the valid email
        address and password.
        An empty stakeholder dictionary along with a tuple detailing the bot's email address and password
            will be created.

        Parameters
        ----------
        email (String): the email address of the bot (must be a Gmail address).
        password (String): password to the bot's Gmail account.
        """
        try:
            self.validate_gmail(email)
            self.sender_account_info = (email, password)
            self.stakeholders = defaultdict(lambda: "Value not found")
            self.server = smtplib.SMTP("smtp.gmail.com", 587)
            # For Outlook: smtplib.SMTP('smtp.office365.com', 587)
            self.server.starttls()
            self.server.login(email, password)

        except NotGmailError:
            print(f"{email} is not a valid gmail email. Try again.")

    def send_message(self, to, subject, message, attach_file=None):
        """ Sends a basic email to a particular email address

        Parameters
        ----------
        to (String): the email address of the person receiving this email.
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        attach_file (String , optional): the directory of the file we're interested in sending (absolute/relative).
        """
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.sender_account_info[0]
        msg["To"] = to
        msg.attach(MIMEText(message))

        if attach_file:
            msg.attach(self.mime_attachment(attach_file))

        try:
            self.server.sendmail(self.sender_account_info[0], to, msg.as_string().encode('utf-8'))
            print(f"Email sent to {to} successfully!")
        except:
            print(f"Failed to send email to {to}...")

    def send_to_all(self, subject="", message="", auto_heading=False, attach_file=None):
        """ Sends an email all email addresses within self.stakeholders.

        Parameters
        ----------
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        auto_heading (Bool, optional): If True, message will be appended to "Hello {name},\n\n".
        attach_file (String , optional): the directory of the file we're interested in sending (absolute/relative).
        """
        if auto_heading:
            def m(n):
                return f"Hello {n},\n\n" + message
        else:
            def m(n):
                return message
        for name, email in self.stakeholders.items():
            self.send_message(email, subject, m(name), attach_file=attach_file)

    def conditional_send(self, to, subject, message, condition, *args, auto_parse=False, attach_file=None):
        """ Sends an email to a particular email address only if the condition is fulfilled.
        Also supports sending variable values via string parsing (look into auto_parse).

        Parameters
        ----------
        to (String): the email address of the person receiving this email.
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        condition (Bool || Function): A condition that needs to be fulfilled in order for the email to be sent.
        *args (List): Elements will be used by condition to check whether it has been fulfilled. Contents are
            also used to parse message.
        auto_parse (Bool, optional): If True, contents of *args will be used to parse {} of message.
        attach_file (String , optional): the directory of the file we're interested in sending (absolute/relative).
        """
        message = self.parse_message(message, *args) if auto_parse else message
        if callable(condition):
            self.conditional_send(to, subject, message, condition(args), attach_file=attach_file)
        else:
            if condition:
                self.send_message(to, subject, message, attach_file=attach_file)

    def conditional_send_to_all(self, subject, message, condition, *args, auto_heading=False, auto_parse=False,
                                attach_file=None):
        """ Sends an email all email addresses within self.stakeholders only if the condition is fulfilled and the
            locally stored list of stakeholders is not empty.
        Also supports sending variable values via string parsing (look into auto_parse).

        Parameters
        ----------
        subject (String): the subject of the email.
        message (String): the body of the email. Can be parsed to have variables.
        condition (Bool || Function): A condition that needs to be fulfilled in order for the email to be sent.
        *args (List): Elements will be used by condition to check whether it has been fulfilled. Contents are
            also used to parse message.
        auto_heading (Bool, optional): If True, message will be appended to "Hello {name},\n\n".
        auto_parse (Bool, optional): If True, contents of *args will be used to parse {} of message.
        attach_file (String , optional): the directory of the file we're interested in sending (absolute/relative).
        """
        if len(self.stakeholders) > 0:
            message = self.parse_message(message, *args) if auto_parse else message
            if callable(condition):
                self.conditional_send_to_all(subject, message, condition(args), auto_heading=auto_heading,
                                             auto_parse=auto_parse, attach_file=attach_file)
            else:
                if condition:
                    self.send_to_all(subject, message, auto_heading, attach_file=attach_file)
        else:
            print("You don't have any stakeholders to direct this email to!")

    def mime_attachment(self, file):
        """ Prepares attachment for the email.
        Currently only works for text-based files.
        Parameters
        ----------
        file (String): the directory of the file that we want to send via e-mail.

        Returns
        ------
        MIMEText
        """
        # For now, it can only read text-based files.
        with open(file) as f:
            attachment = MIMEText(f.read())
            attachment.add_header("Content-Disposition", "attachment", filename=file[5:])
        return attachment
        """
        # Copied from:
        # https://stackoverflow.com/questions/23171140/how-do-i-send-an-email-with-a-csv-attachment-using-python
        attachment = None
        ctype, encoding = mimetypes.guess_type(file)
        print("ctype: ", ctype, "\nencoding: ", encoding)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)
        print("Maintype: " + maintype)
        if maintype == "text":
            with open(file) as fp:
                attachment = MIMEText(fp.read(), _subtype=subtype)

        elif maintype == "image":
            with open(file) as fp:
                attachment = MIMEImage(fp.read(), _subtype=subtype)
        else:
            fp = open(file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)

        attachment.add_header("Content-Disposition", "attachment", filename=file[5:])
        return attachment
        """

    def add_stakeholder(self, name, email):
        """ Adds a stakeholder to the system so they'll receive e-mail notifications.

        Parameters
        ----------
        name (String): the name of the stakeholder.
        email (String): the email of the stakeholder.
        """
        self.stakeholders[name] = email

    def remove_stakeholder(self, name):
        """ Removes a specific stakeholder from the system by name.

        Parameter
        ---------
        name (String): the name of the stakeholder.
        """
        self.stakeholders.pop(name)

    def clear_stakeholders(self):
        """ Removes all stakeholders from the system.

        Parameter
        ---------
        name (String): the name of the stakeholder.
        """
        self.stakeholders.clear()

    def parse_message(self, message, *args):
        """ Formats message with *args elements

        Parameters
        ----------
        message (String): A String containing {} that'll be formatted.
        *args (List): A list of strings that will be inserted into {} from message.

        Return
        ------
        Returns the formatted message.
        """
        return message.format(*args)

    def validate_gmail(self, email):
        """ Checks to see if the inserted email is a Gmail account.
        *It doesn't check whether the email is a VALID Gmail address.
        Parameter
        ---------
        email (String): the e-mail address that we want to check to see if it's a Gmail account.
        :param email:
        :return:
        """
        if email[-10:] != "@gmail.com":
            raise NotGmailError


class NotGmailError(Exception):
    pass


if __name__ == "__main__":
    application = BioreactorGmailBot("bioreactor.bot@gmail.com", "75q3@*NyiVDKmr_k")

    # application.send_message("jay.zhong@monashtechschool.vic.edu.au", "Test", "Testing, testing, one, two three...")
