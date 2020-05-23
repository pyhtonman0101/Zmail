import smtplib
from string import Template
from email.mime.base import MIMEBase
from email import encoders

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import filedialog


PASSWORD="*********"              #write you email Id password
file_path=''
def printing():
    global MY_ADDRESS
    y=MY_ADDRESS.get()
    print(y)


def get_contacts(filename):
    """
        Return two lists names, emails containing names and email addresses
        read from a file specified by filename.
    """

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
        return names, emails

def file_dialogue():
    global filedialogue,MY_ADDRESS
    filedialogue = filedialog.askopenfilename(initialdir='/',title='select the file',filetype=(('jpeg','*.jpg'),('All Files','*.*')))
    file=(filedialogue.split('/'))[-1]
    file_name = Label(frame1, text=file, font=('arial', 10), fg='cyan', bg='black').grid(row=2, column=1,sticky=E)

def file_dialogue_attachemnts():
    global file_path,attachement_path
    attachement_path = filedialog.askopenfilename(initialdir='/', title='select the file',
                                              filetype=(('jpeg', '*.jpg'), ('All Files', '*.*')))
    file_path = (attachement_path.split('/'))[-1]
    path_lable = Label(frame1, text=file_path, font=('arial', 10), fg='cyan', bg='black').grid(row=5, column=1, sticky=W)

def Body_atachements():
    global body_path
    body_path = filedialog.askopenfilename(initialdir='/', title='select the file',
                                              filetype=(('jpeg', '*.jpg'), ('All Files', '*.*')))
    body = (body_path.split('/'))[-1]
    body_lable = Label(frame1, text=body, font=('arial', 10), fg='cyan', bg='black').grid(row=4, column=1, sticky=E)


def read_template(filename):
    """
        Returns a Template object comprising the contents of the
        file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content=template_file.read()
        return Template(template_file_content)


def main():
    names, emails =get_contacts(str(filedialogue)) # read contacts
    message_template=read_template(str(body_path))

    print(MY_ADDRESS.get())
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(str(MY_ADDRESS.get()), PASSWORD)


    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg=MIMEMultipart()       # create a message


        # add in the actual person name to the message template
        message =message_template.substitute(PERSON_NAME=name.title())


        # Prints out the message body for our sake
        print(message)


        # setup the parameters of the message
        msg['From']=MY_ADDRESS.get()
        msg['To']=email
        msg['Subject']= subject.get()

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))


        file_location=str(attachement_path)

        file_name=file_path
        if str(file_path) != "":

            #file_location = "C:\\Users\AMD\PycharmProjects\zahidkvy\\bulkemailsend\\" + file_name  # file_location example: D:\pythonman\pythonimage.png
            # example: pyhonimage.png

            attachment = open(file_location, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
            msg.attach(p)  # attached file into msg



        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

        # Terminate the SMTP session and close the connection
    s.quit()
#--------------------------x---------------------------------x----------------------------------
# Now let's write the GUI programming for design the software
win=Tk()
win.config(bg='black')
win.title('Zmail')
label=Label(win)
label.pack()
inputvar=StringVar()
frame1=Frame(label,relief=SUNKEN,bg="gray15",bd=10)
frame1.pack()

sender=Label(frame1,text='Sender:',font=('arial',15,'bold'),fg='cyan',bg='gray14').grid(row=1,sticky=W)

recievers= Label(frame1,text='Recipients File',font=('arial',15,'bold'),fg='cyan',bg='gray14').grid(row=2,sticky=W)
browse_receivers= Button(frame1,text='Select file',bd=5,fg='white',bg='black',font=('arial',15,'bold'),relief=SUNKEN,padx=8,pady=8,command=lambda:file_dialogue())
browse_receivers.grid(row=2,column=1,sticky=W)

MY_ADDRESS = Entry(frame1,bg='black',fg='cyan',font=('arial',15,'bold'),relief=SUNKEN,bd=10)
MY_ADDRESS.grid(row=1,column=1)

Subjectlable= Label(frame1,text='Subject: ',font=('arial',15,'bold'),fg='cyan',bg='gray14').grid(row=3,sticky=W)
subject = Entry(frame1,bg='black',fg='cyan',font=('arial',15,'bold'),textvariable=inputvar,relief=SUNKEN,bd=10)
subject.grid(row=3,column=1)

Body= Label(frame1,text='Body: ',font=('arial',15,'bold'),fg='cyan',bg='gray14').grid(row=4,sticky=W)
attached_attachements=Button(frame1,text='Attachements',bd=5,font=('arial',15,'bold'),fg='white',bg='black',relief=SUNKEN,padx=8,pady=8,command=lambda:file_dialogue_attachemnts()).grid(row=5,sticky=W)
Body_btn=Button(frame1,text='Body',bd=5,fg='white',font=('arial',15,'bold'),bg='black',relief=SUNKEN,padx=8,pady=8,command=lambda:Body_atachements()).grid(row=4,column=1,sticky=W)

sendbut= Button(frame1,text='send',bd=5,fg='white',bg='green2',font=('arial',15,'bold'),relief=SUNKEN,padx=8,pady=8,command=lambda:main()).grid(row=5,column=1,sticky=E)


win.mainloop()