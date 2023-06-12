"""
-----------------------------------------------------

    Autoren:
        Tobias Sarmiento
        Jannat Farooqi
        Selcan Yaman

-----------------------------------------------------

    DermoPEL Projekt Sommersemester 2023

-----------------------------------------------------

    in Auftrag von: HTLBuVA 1050 Spengergasse,
    Professor Nassler, PRE Unterricht 3AHBGM.

-----------------------------------------------------

    Kurze Beschreibung:

    DermoPEL ist eine in Python mithilfe von der
    Kivy Library programmierte App, welche an eine
    MySQL Datenbank angebunden ist. Die App dient zur
    zentralen und einfachen Protokollierung von
    Dermatologischen Beschwerden und anderen
    medizinisch relevanten Daten.

-----------------------------------------------------

    Versionen:

    DermoPEL Version 0:
        Vorlage für zukünftige Versionen
        Alle Interpreter und Librarys installiert
        Tobias Sarmiento

    DermoPEL Version 1:
        Layouts testen
        Tobias Sarmiento

    DermoPEL Version 2:
        Experimentieren mit Labels, Screenmanager,
        Images und Transitions
        Tobias Sarmiento

    DermoPEL Version 3:
        Näher an echter Version dran,
        Basic Klassen, Layouts und ScreenManager definiert
        Tobias Sarmiento

    DermoPEL Version 4:
        Top- und Bottom-Bar eingefügt
        Icons auf Mainscreen eingefügt
        Tobias Sarmiento

    DermoPEL Version 5:
        Button behaviour eingefügt
        Tobias Sarmiento

    DermoPEL Version 6:
        Design verändert
        Tobias Sarmiento

    DermoPEL Version 7:
        basic Settingscreen definiert
        Screentransitions eingefügt
        Tobias Sarmiento

    DermoPEL Version 8:
        Auf neuen Aufbau von V2 angepasst
        Datenbank Connection Klasse aufgebaut
        und Basic Funktionen als Kommentare eingefügt
        (siehe DermoPELApp)
        Tobias Sarmiento

    DermoPEL Version 9:
        Kommentar für Camera eingefügt
        PopUp für neues Protokoll eingefügt
        Tobias Sarmiento

    DermoPEL Version 10:
        Startscreen eingefügt
        Login und Signup screen definiert
        Tobias Sarmiento

    DermoPEL Version 11:
        Login- und Signup-Screen code-behind
        Testversionen zu Versionen geändert
        Tobias Sarmiento

    DermoPEL Version 12:
        HASHing-Algorithmus eingefügt
        Entrys und Camera-behaviour
        Tobias Sarmiento

    DermoPEl Version 12.1:
        Kamera Popup verbessert
        Tobias Sarmiento

    DermoPEl Version 12.2:
        Kamera Bug gefixt
        Tobias Sarmiento

    DermoPEl Version 13:
        Image mit BLOB in db gespeichert
        Tobias Sarmiento

    DermoPEL Version 14:
        Datepicker, Tabs und Buttons eingefügt
        Mivy App => KivyMD App
        Tobias Sarmiento

    DermoPEL Version 15:
        NoteTabs fertiggestellt und Colorpicker
        Farben auf globale Variablen gestellt
        Tobias Sarmiento

    DermoPEL Version 16:
        StateTab fertiggestellt
        Tobias Sarmiento

    DermoPEL Verion 17:
        Doctorscreen fertiggestellt
        Tobias Sarmiento

    DermoPEL Version 18:
        Profilescreen fertiggestellt
        Tobias Sarmiento

    DermoPEL Version 19:
        Stammdaten und Doctoransicht fertig
        Blob decoding repariert
        Sarmiento Tobias

    DermoPEL Version 20:
        Alle ziele erfüllt, BaseApp fertig
        Sarmiento Tobias

    DermoPEL Version 21:
        git repo initialized
        tempfile-struktur geändert
        Sarmiento Tobias

    DermoPEL Version 21.1:
        Settingsscreen zu Doctorsearch geändert
        Sarmiento Tobias

    DermoPEL Version 21.2:
        Counter und Liste für Fotos hinzugefügt,
        FEHLERHAFT! Fotos werden weiß angezeigt
        Sarmiento tobias

    DermoPEL Version 21.3:
        Bilder behoben, funktionieren nun.
        Sarmiento Tobias

    DermoPEL Version 21.4:
        Tutorial angefangen
        Sarmiento Tobias

    DermoPEL Version 22:
        Tutorial und Kamera fertiggestellt,
        alle Ziele erreicht
        erste fertige Version
        Sarmiento Tobias

    DermoPEL Version 23:
        Bugfixes
        Sarmiento Tobias

-----------------------------------------------------
"""
# Bug: bei erstmaligem einloggen werden protokolle nicht angezeigt! fixed!!!
import codecs
# from android.permissions import request_permissions, Permission
# from android.storage import primary_external_storage_path
from kivy import utils
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, ColorProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, NoTransition, CardTransition
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex, platform
from kivy.uix.camera import Camera
from kivy.config import Config
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from datetime import datetime, timedelta
from PIL import Image
import mysql.connector
import hashlib
import base64
import os
import io

# KIVY_DPI=320 KIVY_METRICS_DENSITY=2 python main.py --size 1280x720

# Window Size
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.pickers import MDDatePicker, MDColorPicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.tab import MDTabsBase

"""Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')"""

# -----------------------------------------------------
# Variables
# -----------------------------------------------------

# Hier mysql connection und cursor als Globale Variablen definiert, suboptimal
"""#Connection
dermoconn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="dermopel_testdb"
)

#Cursor
dermocurser = dermoconn.cursor()"""

# Hier bessere lösung: Klasse mit Konstruktor
"""class Database:
    def __init__(self, host, user, passwd, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Example usage:
db = Database(host="localhost", user="root", passwd="", database="dermopel_testdb")
db.cursor.execute("SELECT * FROM my_table")
results = db.cursor.fetchall()
db.close()"""

# Global Variables
curruserid = 0
currprotocol = 0
currentry = 0
currimg = 0
# currentryimg = 0
currpatient = 0
currdoc = 0
currdir = 0
userprotocol = 0
isprinted = False
# entrycounter wird für die imgs benötigt.
entrycounter = {}

# JSON File for Login-storage (muss zu store = JsonStore(App.get_running_app().user_data_dir + '/login.json') geändert werden vor der kompilierung wegen android.)
store = JsonStore('login.json')


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="e121967-mysql.services.easyname.eu",
            user="u187500db1",
            passwd="Dermo123",
            database="u187500db1"
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()


def convertdata(filename):
    # Convert images or files data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
    binary_data = codecs.encode(binary_data, 'base64')
    return binary_data


def createimgs(b):
    global currdir, entrycounter
    entrycounter[currprotocol][currentry] = entrycounter[currprotocol][currentry] + 1
    # Konvertiert blob = > png
    os.mkdir(f'Temp/TempEntry{currentry}')
    file = open(f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png', "wb")
    file.write(base64.b64decode(b))
    # print(blob)
    # pad = len(blob) % 4
    # blob += b"="*pad
    # lenmax = len(blob) - len(blob) % 4
    # file.write(codecs.decode(blob[0:lenmax], 'base64'))
    # print(codecs.decode(blob, 'base64'))
    # file.write(codecs.decode(blob, 'base64'))
    file.close()
    # Erschafft zweites dünkleres Foto
    img = Image.open(f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png')
    img = img.point(lambda p: p * 0.5)
    img.save(f'Temp/TempEntry{currentry}/tempimgdb_down{entrycounter[currprotocol][currentry]}.png')
    currdir = currdir + 1
    # hier ist mit currentry statt currdir schlauer!!!


# -----------------------------------------------------
# Classes
# -----------------------------------------------------


class Display(BoxLayout):
    directs = ''


# class ProfileScreen(Screen):
#    pass


class LoginScreen(Screen):
    pass


class Top_PatientAndDoctorScreen(BoxLayout):
    def easter_egg(self, widget):
        App.get_running_app().darkblue = [.25, .04, .24, 1]
        App.get_running_app().lightblue = [1, 1, 1, 1]
        App.get_running_app().greyblue = [1, .09, .97, 1]

    def on_release_profile(self, widget):
        if not App.get_running_app().isdoctor or App.get_running_app().istreating:
            App.get_running_app().root.ids.DermoScreens.transition = CardTransition()
            App.get_running_app().root.ids.DermoScreens.transition.direction = 'left'
            App.get_running_app().root.ids.DermoScreens.current = 'profilescreen'
        else:
            global curruserid, currprotocol, currentry, currdoc, currpatient, isprinted, userprotocol, entrycounter
            curruserid = 0
            currprotocol = 0
            userprotocol = 0
            currentry = 0
            currdoc = 0
            currpatient = 0
            entrycounter = {}
            App.get_running_app().isdoctor = False
            App.get_running_app().istreating = False
            App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
            App.get_running_app().root.ids.DermoScreens.current = 'startscreen'
            store.delete("curruserjson")
            isprinted = False


class Login(BoxLayout):
    def on_login(self, widget):
        global curruserid, currdoc
        db = Database()
        db.cursor.execute("SELECT p_id, p_loginname, p_password FROM Patient")
        precords = db.cursor.fetchall()
        db.cursor.execute("SELECT d_id, d_loginname, d_password FROM Doctor")
        drecords = db.cursor.fetchall()
        # Error Popups
        missingloginerror = Factory.LoginOrSignUpError()
        wrongloginerror = Factory.LoginOrSignUpError()
        wrongpasserror = Factory.LoginOrSignUpError()
        # Passwort und User überprüfung
        if self.ids.login_namebox.text != "" and self.ids.login_passbox.text != "":
            # Variablen für überprüfung ob user oder passwort falsch ist
            login = False
            error = True
            patient = False
            for i in range(0, len(precords)):
                if self.ids.login_namebox.text == precords[i][1]:
                    login = True
                    patient = True
                    if hashlib.md5(self.ids.login_passbox.text.encode()).hexdigest() == precords[i][2]:
                        # switch screens
                        self.parent.parent.manager.transition = RiseInTransition()
                        self.parent.parent.manager.current = "patientscreen"
                        curruserid = precords[i][0]
                        # speichert user in json
                        store.put('curruserjson', curruser=curruserid, type="patient",
                                  expires=(datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S.%f'))
                        error = False
                        currdoc = 0
                        App.get_running_app().isdoctor = False
                        App.get_running_app().istreating = False
                        # patscreen = App.get_running_app().root.ids.DermoScreens.get_screen('patientscreen')
                        # patscreen.children[0].children[1].children[0].draw_protocol()
                        db.close()
            if not patient:
                for i in range(0, len(drecords)):
                    if self.ids.login_namebox.text == drecords[i][1]:
                        login = True
                        if hashlib.md5(self.ids.login_passbox.text.encode()).hexdigest() == drecords[i][2]:
                            # switch screens
                            self.parent.parent.manager.transition = RiseInTransition()
                            self.parent.parent.manager.current = "doctorscreen"
                            curruserid = drecords[i][0]
                            App.get_running_app().isdoctor = True
                            store.put('curruserjson', curruser=curruserid, type="doctor",
                                      expires=(datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S.%f'))
                            error = False
                            db.close()
            if login and error:
                wrongpasserror.loginorsignuperrormsg = "wrong password"
                wrongpasserror.open()
            elif error:
                wrongloginerror.loginorsignuperrormsg = "username was not found"
                wrongloginerror.open()
        else:
            missingloginerror.loginorsignuperrormsg = "missing username or password"
            missingloginerror.open()


class SignUp(BoxLayout):
    def on_signup(self, widget):
        global curruserid
        db = Database()
        db.cursor.execute("SELECT p_id, p_loginname, p_password FROM Patient")
        precords = db.cursor.fetchall()
        db.cursor.execute("SELECT d_id, d_loginname, d_password FROM Doctor")
        drecords = db.cursor.fetchall()
        missingsigninerror = Factory.LoginOrSignUpError()
        duplicateusernameerror = Factory.LoginOrSignUpError()
        weakpassworderror = Factory.LoginOrSignUpError()
        if self.ids.signup_namebox.text != "" and self.ids.signup_passbox.text != "":
            useravailable = True
            if self.ids.patientcheckbox.active:
                for i in range(0, len(precords)):
                    if self.ids.signup_namebox.text == precords[i][1]:
                        useravailable = False
                        duplicateusernameerror.loginorsignuperrormsg = "Username already exists, please choose another one."
                        duplicateusernameerror.open()
            elif self.ids.doctorcheckbox.active:
                for i in range(0, len(drecords)):
                    if self.ids.signup_namebox.text == drecords[i][1]:
                        useravailable = False
                        duplicateusernameerror.loginorsignuperrormsg = "Username already exists, please choose another one."
                        duplicateusernameerror.open()
            if useravailable:
                if len(self.ids.signup_passbox.text) >= 4:
                    if self.ids.patientcheckbox.active:
                        # MD5-Hash Algorithmus
                        hashpass = hashlib.md5(self.ids.signup_passbox.text.encode()).hexdigest()
                        db.cursor.execute("INSERT INTO Patient (p_loginname, p_password) VALUES (%s, %s)",
                                          (self.ids.signup_namebox.text, hashpass))
                        db.conn.commit()
                        db.cursor.execute("SELECT p_id FROM Patient WHERE p_loginname = %s",
                                          (self.ids.signup_namebox.text,))
                        curruserid = db.cursor.fetchone()[0]
                        store.put('curruserjson', curruser=curruserid, type="patient",
                                  expires=(datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S.%f'))
                        self.parent.parent.manager.transition = RiseInTransition()
                        self.parent.parent.manager.current = "patientscreen"
                        App.get_running_app().isdoctor = False
                        App.get_running_app().istreating = False
                    elif self.ids.doctorcheckbox.active:
                        hashpass = hashlib.md5(self.ids.signup_passbox.text.encode()).hexdigest()
                        db.cursor.execute("INSERT INTO Doctor (d_loginname, d_password) VALUES (%s, %s)",
                                          (self.ids.signup_namebox.text, hashpass))
                        db.conn.commit()
                        db.cursor.execute("SELECT d_id FROM Doctor WHERE d_loginname = %s",
                                          (self.ids.signup_namebox.text,))
                        curruserid = db.cursor.fetchone()[0]
                        store.put('curruserjson', curruser=curruserid, type="doctor",
                                  expires=(datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S.%f'))
                        self.parent.parent.manager.transition = RiseInTransition()
                        self.parent.parent.manager.current = "doctorscreen"
                        App.get_running_app().isdoctor = True
                    db.close()
                else:
                    weakpassworderror.loginorsignuperrormsg = "Password too weak. Must have at least 4 Characters."
                    weakpassworderror.open()
        else:
            missingsigninerror.loginorsignuperrormsg = "missing username or password"
            missingsigninerror.open()


class PatientSwipeItem(MDSwiperItem):
    firstn = StringProperty("")
    lastn = StringProperty("")
    svnr = StringProperty("")
    currpat = NumericProperty(0)

    # currpattemp = NumericProperty(0)

    def __init__(self, currpat, firstn, lastn, svnr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currpat = currpat
        self.firstn = firstn
        self.lastn = lastn
        self.svnr = svnr


class DoctorScreen(MDScreen):
    def on_enter(self, *args):
        global isprinted
        App.get_running_app().istreating = False
        if not isprinted:
            App.get_running_app().isdoctor = True
            db = Database()
            db.cursor.execute(
                f"SELECT p_id, p_firstname, p_name, p_svnr FROM Patient WHERE p_d_treatingdoctor = {curruserid}")
            patients = db.cursor.fetchall()
            if not patients:
                print(self.children[0].children[1].children)
                self.children[0].children[1].clear_widgets()
                msg = Factory.NoPatientsMsg()
                self.children[0].children[1].add_widget(msg)
            # clears widgets
            else:
                widgets = []
                for widget in self.children[0].children[1].children[0].children[0].children:
                    widgets.append(widget)
                for wid in widgets:
                    self.children[0].children[1].children[0].children[0].remove_widget(wid)
                for patient in patients:
                    pat = PatientSwipeItem(
                        currpat=int(patient[0]),
                        firstn=str(patient[1]),
                        lastn=str(patient[2]),
                        svnr=str(patient[3]),
                        # on_touch_down=self.on_click_patient(self)
                    )
                    self.children[0].children[1].children[0].add_widget(pat)
            isprinted = True

    def on_click_patient(self, widget):
        global currpatient, currdoc, curruserid
        currpatient = widget.parent.parent.currpat
        currdoc = curruserid
        curruserid = currpatient
        App.get_running_app().root.ids.DermoScreens.transition = CardTransition()
        App.get_running_app().root.ids.DermoScreens.transition.direction = 'left'
        App.get_running_app().root.ids.DermoScreens.current = 'patientscreen'


class PatientScreen(Screen):
    def on_enter(self, *args):
        # ruft children [0] (Screenmanager) children[1] (middlescreen) children[0] (protocol)
        self.children[0].children[1].children[0].children[1].draw_protocol()
        # Damit Protocolle in der mitte des screens erscheinen.
        # height = Window.height
        width = Window.width
        # print(f"Window height: {height}, Window width: {width}")
        ratio = width / dp(110)
        integ = int(str(ratio)[0])
        ratio = ratio - integ
        if width < 1100:
            self.children[0].children[1].children[0].children[2].width = dp((ratio * 110) // 2)
            self.children[0].children[1].children[0].children[0].width = dp((ratio * 110) // 2)
        else:
            self.children[0].children[1].children[0].children[2].width = 0
            self.children[0].children[1].children[0].children[0].width = 0
        if App.get_running_app().isdoctor:
            App.get_running_app().istreating = True


class Protocol(StackLayout):
    # def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    # Funktion wird in on_pre_enter von screen gerufen.
    def draw_protocol(self):
        global curruserid, entrycounter
        db = Database()
        db.cursor.execute(f"SELECT pr_id, pr_name FROM Protocol WHERE pr_p_id = {curruserid}")
        prrecords = db.cursor.fetchall()
        self.clear_widgets()
        for i, p in enumerate(prrecords):
            protocolfolder = Button(
                # padding=("20dp", "20dp", "20dp", "20dp"),
                size_hint=(None, None),
                size=("110dp", "110dp"),
                border=(0, 0, 0, 0),
                background_normal="Images/Folder_DermoPEL.png",
                background_down="Images/Folder_Down_DermoPEL.png",
                text="",
                bold=True,
                halign="center",
                color=(0, 0, 0, 1),
                on_release=self.on_protocol_release
            )
            protocolfolder.text_size = (
                protocolfolder.width, protocolfolder.height)  # Set text_size to the size of the button
            protocolfolder.text = prrecords[i][1]  # Set the text of the button after setting the text_size
            self.add_widget(protocolfolder)
            if len(prrecords) - len(entrycounter) > 0:
                entrycounter.update({p[0]: {}})
            #elif len(prrecords) - len(entrycounter) == 1:
            #    entrycounter.update({p[-1]: []})
            # protocolname = Label(
            #    size_hint=(None, None),
            #    size=("110dp", "110dp"),
            #    text="test"
            # text=prrecords[i][1]
            # )

            # fixes clocking errors with kivy
            # Clock.schedule_once(
            #    lambda dt, pf=protocolfolder, pn=protocolname: self.add_widget(pf) and self.add_widget(pn))

            db.close()

    def on_protocol_release(self, widget):
        global currprotocol
        # hiermit wird die id vom gerade angeclickten protocol an die Entrys weitergegeben.
        db = Database()
        db.cursor.execute("SELECT pr_id FROM Protocol WHERE pr_name = %s AND pr_p_id = %s;", (widget.text, curruserid))
        currprotocol = db.cursor.fetchall()[0][0]
        Factory.Entrys().open()
        db.close()

    """with newbuttontest.canvas.before:
        Color(rgb=get_color_from_hex('#d8d8d8'))
        RoundedRectangle(size=newbuttontest.size, pos=newbuttontest.pos, radius=[10, 10, 10, 10])"""
    """for i in range(0, 100):
        # size = dp(100) + i*10
        size = dp(100)
        b = Button(text=str(i+1), size_hint=(None, None), size=(dp(size), dp(size)))  # size_hint(.2, .2)
        self.add_widget(b)"""


# DermoScreens = ScreenManager()
# DermoScreens.add_widget(ProfileScreen(name='profilescreen'))


class ProfileScreen(Screen):
    def on_enter(self, *args):
        db = Database()
        db.cursor.execute(
            f"SELECT p_firstname, p_name, p_svnr, p_birthdate, p_allergies, p_preconditions, p_medications, p_d_treatingdoctor FROM Patient WHERE p_id = {curruserid}")
        currpat = db.cursor.fetchone()
        screen = self.children[0].children[1].children[0]
        if App.get_running_app().isdoctor or App.get_running_app().istreating:
            self.children[0].remove_widget(self.children[0].children[2])
            logo = Factory.LogoTopBar()
            self.children[0].add_widget(logo, index=2)
            #logo = Factory.LogoTopBar()
            #self.children[0].children[0] = logo
        #print(self.children[0].children)
        # for value, box in zip(currpat, screen.ids):
        #    if value is not None:
        #        screen.ids.box.text = str(value)
        if currpat[0] is not None:
            screen.ids.firstnamebox.text = currpat[0]
        if currpat[1] is not None:
            screen.ids.surnamebox.text = currpat[1]
        if currpat[2] is not None:
            screen.ids.svnrbox.text = str(currpat[2])
        if currpat[3] is not None:
            screen.ids.birthdatebox.text = str(datetime.strptime(
                str(currpat[3]), '%Y-%m-%d').strftime('%#d. %#m. %Y'))
        if currpat[4] is not None:
            screen.ids.allergiescheckbox.active = True
            screen.ids.allergybox.text = currpat[4]
        if currpat[5] is not None:
            screen.ids.conditionscheckbox.active = True
            screen.ids.conditionbox.text = currpat[5]
        if currpat[6] is not None:
            screen.ids.medicationscheckbox.active = True
            screen.ids.medicationbox.text = currpat[6]
        if currpat[7] is not None:
            db.cursor.execute(f"SELECT d_loginname FROM Doctor WHERE d_id = {currpat[7]}")
            screen.ids.treatingdocbox.text = str(db.cursor.fetchone()[0])
        # print(self.ids)
    # db.cursor.execute(f"SELECT ")

    # def on_leave(self, *args):
    # checkt, ob alle Felder ausgefüllt wurden
    # db = Database()
    # db.cursor.execute(
    #    f"SELECT p_firstname, p_name, p_svnr, p_birthdate FROM Patient WHERE p_id = {curruserid}")
    # currpat = db.cursor.fetchone()
    # temp = True
    # for val in currpat:
    #    if val is None:
    #        temp = False
    #        App.get_running_app().canupdate = False
    # if temp:
    #    App.get_running_app().canupdate = True

    # screen = self.children[0].children[1].children[0]
    ##texts = []
    # for box in screen.children:
    #    for inputs in box.children:
    #        if isinstance(inputs, TextInput):
    #            texts.append(inputs.text)
    #        else:
    #            for lowinputs in inputs.children:
    #                if isinstance(lowinputs, TextInput):
    #                    if not lowinputs.multiline:
    #                        texts.append(lowinputs.text)
    # print(texts)


class PatientData(BoxLayout):
    def on_date_release(self, widget):
        # DatePicker
        if self.ids.birthdatebox.text != '':
            dateof = datetime.strptime(self.ids.birthdatebox.text, '%d. %m. %Y')
        else:
            dateof = datetime.today()
        date_dialog = MDDatePicker(
            year=dateof.year,
            month=dateof.month,
            day=dateof.day,
            primary_color=(App.get_running_app().darkblue),
            accent_color=(App.get_running_app().lightblue),
            text_color=(App.get_running_app().darkblue),
            text_toolbar_color=(App.get_running_app().lightblue),
            text_button_color=(App.get_running_app().darkblue),
            text_weekday_color=(.01, .06, .5, 1)
        )
        date_dialog.on_save = self.on_datepicker
        date_dialog.open()
        self.datepicker = date_dialog

    def on_datepicker(self, selecteddate, datelist):
        self.ids.birthdatebox.text = selecteddate.strftime('%#d. %#m. %Y')
        self.datepicker.dismiss()

    def on_search_doctor(self, widget):
        db = Database()
        db.cursor.execute(f"SELECT d_id FROM Doctor WHERE d_loginname = '{self.ids.treatingdocbox.text}'")
        doc = db.cursor.fetchone()
        if self.ids.treatingdocbox.text == '':
            db.cursor.execute(f"UPDATE Patient SET p_d_treatingdoctor = null WHERE p_id = {curruserid}")
            db.conn.commit()
            Snackbar(
                text="[color=#0824AA]no doctor selected.[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=App.get_running_app().lightblue,
                font_size="20dp",
                radius=(20, 20, 20, 20),
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        if doc is None:
            Snackbar(
                text="[color=#0824AA]no doctor was found.[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=App.get_running_app().lightblue,
                font_size="20dp",
                radius=(20, 20, 20, 20),
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        else:
            # db = Database()
            db.cursor.execute(f"UPDATE Patient SET p_d_treatingdoctor = {doc[0]} WHERE p_id = {curruserid}")
            db.conn.commit()
            Snackbar(
                text="[color=#0824AA]doctor was saved![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=App.get_running_app().lightblue,
                font_size="20dp",
                radius=(20, 20, 20, 20),
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()


class EntryScreen(Screen):
    def on_pre_enter(self, *args):
        db = Database()
        db.cursor.execute(f"SELECT * FROM Entry WHERE e_id = {currentry} AND e_pr_p_id = {curruserid}")
        entry = db.cursor.fetchone()
        # gibt eine Liste mit allen Tabs zurück 0 = pic 1 = pain 2 = notes
        tablist = self.children[0].children[1].get_slides()
        # setzt Datum
        tablist[0].children[0].children[1].text = str(datetime.strptime(
            str(entry[6]), '%Y-%m-%d').strftime('%#d. %#m. %Y'))
        print(entrycounter)
        # setzt foto
        if entry[3] is not None:
            #print(f'Temp/TempEntry{currentry}')
            if os.path.exists(f'Temp/TempEntry{currentry}'):
                for f in os.listdir(f'Temp/TempEntry{currentry}'):
                    os.remove(os.path.join(f'Temp/TempEntry{currentry}', f))
                os.rmdir(f'Temp/TempEntry{currentry}')
            createimgs(entry[3])
            #with Image.open(f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png') as img:
            #    width, height = img.size
            #tablist[0].children[1].width = width
            #tablist[0].children[1].height = height
            tablist[0].children[1].background_normal = f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png'
            tablist[0].children[1].background_down = f'Temp/TempEntry{currentry}/tempimgdb_down{entrycounter[currprotocol][currentry]}.png'
            tablist[0].children[1].background_disabled_normal = f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png'
            tablist[0].children[1].background_disabled_down = f'Temp/TempEntry{currentry}/tempimgdb_down{entrycounter[currprotocol][currentry]}.png'
            # self.children[0].children[0].children[0].children[2].background_normal = f'Temp/TempEntry{currentry}/tempimgdb.png'
        else:
            if os.path.exists(f'Temp/TempEntry{currentry}'):
                for f in os.listdir(f'Temp/TempEntry{currentry}'):
                    os.remove(os.path.join(f'Temp/TempEntry{currentry}', f))
                os.rmdir(f'Temp/TempEntry{currentry}')
            os.mkdir(f'Temp/TempEntry{currentry}')
            tablist[0].children[
                1].background_normal = 'Images/new_pic_DermoPEL.png'
            tablist[0].children[
                1].background_down = 'Images/New_Pic_Down_DermoPEL.png'
            tablist[0].children[
                1].background_disabled_normal = 'Images/new_pic_DermoPEL.png'
            tablist[0].children[
                1].background_disabled_down = 'Images/New_Pic_Down_DermoPEL.png'
        # setzt schmerz
        if entry[4] is not None:
            tablist[1].children[3].value = entry[4]
        else:
            tablist[1].children[3].value = 0
        # setzt farbe
        if entry[5] is not None:
            # tablist[1].children[0].children[1].currcolor = entry[5]
            tablist[1].currcolor = entry[5]
        else:
            tablist[1].currcolor = '#a6c8e0'
        # setzt durchmesser
        if entry[7] is not None:
            tablist[1].children[0].children[1].children[1].text = str(entry[7]) + " cm"
        else:
            tablist[1].children[0].children[1].children[1].text = '0 cm'
        # setzt anomalien
        if entry[8] is not None:
            if entry[8] == 0:
                tablist[1].children[0].children[0].children[1].color = (1, 1, 1, .5)
                tablist[1].children[0].children[0].children[1].text = "yes"
                tablist[1].children[0].children[0].children[1].state = "normal"
            else:
                tablist[1].children[0].children[0].children[1].color = (.8, .95, 1, .5)
                tablist[1].children[0].children[0].children[1].text = "no"
                tablist[1].children[0].children[0].children[1].state = "down"
        else:
            tablist[1].children[0].children[0].children[1].color = (.8, .95, 1, .5)
            tablist[1].children[0].children[0].children[1].text = "no"
            tablist[1].children[0].children[0].children[1].state = "down"
        # setzt Notizen
        if entry[9] is not None:
            tablist[2].children[2].text = entry[9]
        else:
            tablist[2].children[2].text = ''
        # setzt ArztNotizen
        if entry[10] is not None:
            tablist[2].children[0].text = entry[10]
        else:
            tablist[2].children[0].text = ''
        db = Database()
        db.cursor.execute(
            f"SELECT p_firstname, p_name, p_svnr, p_birthdate FROM Patient WHERE p_id = {curruserid}")
        currpat = db.cursor.fetchone()
        temp = True
        for val in currpat:
            if val == '' or val is None:
                temp = False
        # textinput für Arzt zugänglich machen
        if App.get_running_app().isdoctor or not temp:
            # diasabled alle widgets für arzt
            for i in tablist[0:2]:
                for j in i.children:
                    j.disabled = True
            if App.get_running_app().isdoctor:
                tablist[2].children[0].readonly = False
                tablist[2].children[2].readonly = True
            else:
                tablist[2].children[0].readonly = True
                tablist[2].children[2].readonly = True
        else:
            for i in tablist[0:2]:
                for j in i.children:
                    j.disabled = False
            tablist[2].children[0].readonly = True
            tablist[2].children[2].readonly = False

        # Titel!
        # self.children[0].children[1].children[1].children[0].children[0].children[0].children[0].children[1].text = str(datetime.strptime(
        #    str(entry[6]), '%Y-%m-%d').strftime('%#d. %#m. %Y'))
        #                                                       tab
        # self.children[0].children[1].children[1].children[0].children[1]
        # print(self.children[0].children[1].children[1].children[0].children[1].children)
        """self.children[0].children[0].children[0].children[-1].text = "Entry from the\n" + datetime.strptime(
            str(entry[6]), '%Y-%m-%d').strftime('%#d. %#m. %Y')
        # Foto!
        if entry[3] is not None and not os.path.exists(f'Temp/TempEntry{currentry}/tempimgdb.png'):
            #print(entry[3].decode())
            #image_data = io.BytesIO(base64.b64decode(entry[3]))
            #image_data = base64.b64decode(entry[3])
            #print(image_data)
            #print(image_data)
            # binary_data = base64.b64decode(image)
            #with open(f"selfie{currimg}.png", "wb") as f:
            #    f.write(image_data)
            #imagetexture = CoreImage(image_data, ext="png").texture
            #image = Image(source="")
            #image.texture = CoreImage(image_data, ext="png").texture
            #image.reload()
            #cim = CoreImage(image_data, ext="png")
            #image = Image(texture=cim.texture)
            #self.children[0].children[0].children[0].children[2].background_normal = image
            #print(self.children[0].children[0].children[0].children)
            #self.children[0].children[0].children[0].remove_widget(self.children[0].children[0].children[0].children[2])
            #self.children[0].children[0].children[0].add_widget(image, 2)
            #self.children[0].children[0].children[0].children[2].background_normal = image
            # Konvertiert blob => png
            file = open(f'Temp/TempEntry{currentry}/tempimgdb.png', "wb")
            file.write(base64.b64decode(entry[3]))
            file.close()
            # Erschafft zweites dünkleres Foto
            img = Image.open(f'Temp/TempEntry{currentry}/tempimgdb.png')
            img = img.point(lambda p: p * 0.5)
            img.save(f'Temp/TempEntry{currentry}/tempimgdb_down.png')
            #with Image(filename=f'Temp/TempEntry{currentry}/tempimgdb.png') as img:
            #    # tinted image using tint() function
            #    img.tint(color="green", alpha="rgb(10 %, 20 %, 40 %)")
            #    img.save(filename=f'Temp/TempEntry{currentry}/tempimgdb_down.png')
            self.children[0].children[0].children[0].children[2].background_normal = f'Temp/TempEntry{currentry}/tempimgdb.png'
            self.children[0].children[0].children[0].children[2].background_down = f'Temp/TempEntry{currentry}/tempimgdb_down.png'
        # diameter!
        if entry[7] is not None:
            self.children[0].children[0].children[1].children[0].text = str(entry[7])"""

    # def on_pre_leave(self, *args):
    #    os.remove(f'Temp/TempEntry{currentry}/tempimgdb.png')


class Entry(BoxLayout):
    def on_currentryprint(self, widget):
        global curruserid, currprotocol, currentry
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        App.get_running_app().root.ids.DermoScreens.current = 'camerascreen'
        Factory.ConfirmPicture().open()
        """
        db = Database(host="localhost", user="root", passwd="", database="dermopel_db")
        print(currentry)
        file = open('Images/Settings_DermoPEL.png', 'rb').read()
        file = base64.b64encode(file)
        db.cursor.execute("INSERT INTO Entry (e_id, e_picture) VALUES ({curruserid}, %s)",
                              (self.ids.new_protocol_namebox.text,))"""


class LimitInput(TextInput):
    limit = 0

    def keyboard_on_key_up(self, keycode, text):
        if text[0] == 'backspace':
            self.do_backspace()

    def on_text(self, instance, value):
        if len(self.text) >= self.limit:
            self.text = self.text[0:self.limit]


class CameraScreen(Screen):
    def on_pre_enter(self, *args):
        self.children[0].children[1].play = True

    def on_leave(self, *args):
        self.children[0].children[1].play = False
    pass


class EntryCamera(BoxLayout):
    def on_takepicture(self, widget):
        global entrycounter
        entrycounter[currprotocol][currentry] = entrycounter[currprotocol][currentry] + 1
        self.ids.entrycam.export_to_png(f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png')
        Factory.ConfirmPicture().open()


class ProfileBar(BoxLayout):
    def on_logout(self, widget):
        global curruserid, currprotocol, currentry, currdoc, currpatient, userprotocol, entrycounter
        curruserid = 0
        currprotocol = 0
        currentry = 0
        currdoc = 0
        currpatient = 0
        userprotocol = 0
        entrycounter = {}
        App.get_running_app().isdoctor = False
        App.get_running_app().istreating = False
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        App.get_running_app().root.ids.DermoScreens.current = 'startscreen'
        store.delete("curruserjson")

    def on_save_profile(self, widget):
        db = Database()
        screen = self.parent.children[1].children[0]
        db.cursor.execute(
            f"UPDATE Patient SET p_firstname = '{screen.ids.firstnamebox.text}' WHERE p_id = {curruserid}")
        db.cursor.execute(f"UPDATE Patient SET p_name = '{screen.ids.surnamebox.text}' WHERE p_id = {curruserid}")
        if screen.ids.svnrbox.text != '':
            db.cursor.execute(f"UPDATE Patient SET p_svnr = {int(screen.ids.svnrbox.text)} WHERE p_id = {curruserid}")
        else:
            db.cursor.execute(f"UPDATE Patient SET p_svnr = null WHERE p_id = {curruserid}")
        if screen.ids.birthdatebox.text != '':
            db.cursor.execute(
                f"UPDATE Patient SET p_birthdate = '{datetime.strptime(screen.ids.birthdatebox.text, '%d. %m. %Y')}' WHERE p_id = {curruserid}")
        else:
            db.cursor.execute(f"UPDATE Patient SET p_birthdate = null WHERE p_id = {curruserid}")
        if screen.ids.allergiescheckbox.active:
            db.cursor.execute(
                f"UPDATE Patient SET p_allergies = '{screen.ids.allergybox.text}' WHERE p_id = {curruserid}")
        else:
            db.cursor.execute(f"UPDATE Patient SET p_allergies = null WHERE p_id = {curruserid}")
        if screen.ids.conditionscheckbox.active:
            db.cursor.execute(
                f"UPDATE Patient SET p_preconditions = '{screen.ids.conditionbox.text}' WHERE p_id = {curruserid}")
        else:
            db.cursor.execute(f"UPDATE Patient SET p_preconditions = null WHERE p_id = {curruserid}")
        if screen.ids.medicationscheckbox.active:
            db.cursor.execute(
                f"UPDATE Patient SET p_medications = '{screen.ids.medicationbox.text}' WHERE p_id = {curruserid}")
        else:
            db.cursor.execute(f"UPDATE Patient SET p_medications = null WHERE p_id = {curruserid}")
        db.conn.commit()
        db.close()

    def on_patient_delete(self, widget):
        confirmdelete = Factory.ConfirmAction(caller=self)
        confirmdelete.msg = "Are you sure you want to delete your Account?"
        # confirmdelete.bind(on_confirm=self.on_confirm_delete)
        confirmdelete.open()

    def on_confirm(self):
        global curruserid, currprotocol, currentry, currdoc, currpatient, userprotocol, entrycounter
        db = Database()
        db.cursor.execute(f"DELETE FROM Patient WHERE p_id = {curruserid}")
        db.conn.commit()
        db.close()
        curruserid = 0
        currprotocol = 0
        currentry = 0
        currdoc = 0
        currpatient = 0
        userprotocol = 0
        entrycounter = {}
        App.get_running_app().isdoctor = False
        App.get_running_app().istreating = False
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        App.get_running_app().root.ids.DermoScreens.current = 'startscreen'
        store.delete("curruserjson")


class EntryBar(BoxLayout):
    def on_save_release(self, widget):
        # parent => parent => BoxLayout => EntryBottom => TabsMain => TabsCarousel => Tab1 => PictureTab => BoxLayout => Textinput
        #   self.parent.parent.children[0].children[1].children[1].children[0].children[0].children[0].children[0].children[1]
        #self.parent.parent.children[0].children[1].children[1].children[0].children[0].children[0]
        tabs = self.parent.parent.children[0].children[1].get_slides()
        tabs[0].on_picture_update()
        tabs[1].on_state_update()
        tabs[2].on_notes_update()
        # Ueberprueft, ob currtab eine instanz von einem Tab ist.
        #if isinstance(currtab, PictureTab):
        #    currtab.on_picture_update()
        #elif isinstance(currtab, PainTab):
        #    currtab.on_state_update()
        #elif isinstance(currtab, NotesTab):
        #    currtab.on_notes_update()


class PictureTab(BoxLayout, MDTabsBase):
    datepicker = MDDatePicker

    def on_date_release(self, widget):
        # DatePicker
        dateof = datetime.strptime(self.ids.datebox.text, '%d. %m. %Y')
        date_dialog = MDDatePicker(
            year=dateof.year,
            month=dateof.month,
            day=dateof.day,
            primary_color=(App.get_running_app().darkblue),
            accent_color=(App.get_running_app().lightblue),
            text_color=(App.get_running_app().darkblue),
            text_toolbar_color=(App.get_running_app().lightblue),
            text_button_color=(App.get_running_app().darkblue),
            text_weekday_color=(.01, .06, .5, 1)
        )
        date_dialog.on_save = self.on_datepicker
        date_dialog.open()
        self.datepicker = date_dialog

    def on_datepicker(self, selecteddate, datelist):
        self.children[0].children[1].text = selecteddate.strftime('%#d. %#m. %Y')
        self.datepicker.dismiss()
        # self.children[0].children[1].text

    def on_new_picture(self, widget):
        Factory.ChoosePicture().open()

    def on_picture_update(self):
        try:
            currdate = datetime.strptime(self.ids.datebox.text, '%d. %m. %Y')
        except:
            print("wrong date format")
        else:
            db = Database()
            db.cursor.execute(
                f"UPDATE Entry SET e_date = '{currdate.date()}' WHERE e_id = {currentry} AND e_pr_id = {currprotocol} AND e_pr_p_id = {curruserid}")
            db.conn.commit()


class PainTab(BoxLayout, MDTabsBase):
    currcolor = StringProperty('#a6c8e0')
    colorpicker = MDColorPicker
    diameterlist = DropDown

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diameterlist = DropDown(
            size_hint=(.5, 1)
        )
        i = .25
        while i <= 7:
            if i % 1 == 0:
                i = int(i)
            item = Button(
                text=f'{i} cm',
                size_hint_x=.5,
                size_hint_y=None,
                height="40dp",
                border=(20, 20, 20, 20),
                background='',
                background_color=App.get_running_app().darkblue,
                color=App.get_running_app().lightblue,
                bold=True,
                font_size="20dp"
            )
            """with item.canvas.before:
                Color(App.get_running_app().lightblue)
                item.rect = RoundedRectangle(
                    pos=item.pos,
                    size=item.size,
                    radius=[(20, 20)]
                )"""
            item.bind(on_release=lambda x, button=item: self.diameterlist.select(button.text))
            self.diameterlist.add_widget(item)
            self.diameterlist.bind(on_select=lambda instance, x: setattr(self.ids.diameterbutton, 'text', x))
            i += .25

    def on_diameter_release(self, widget):
        self.diameterlist.open(widget)

    def on_pain_change(self, widget):
        # Updatet Pain Value zum Slider
        if (len(self.ids.painmeter.text) == 7):
            self.ids.painmeter.text = self.ids.painmeter.text.rstrip(self.ids.painmeter.text[-1])
            self.ids.painmeter.text += str(int(widget.value))
        else:
            temptxt = self.ids.painmeter.text.rstrip(self.ids.painmeter.text[-1])
            self.ids.painmeter.text = temptxt.rstrip(self.ids.painmeter.text[-2])
            self.ids.painmeter.text += str(int(widget.value))

    def on_new_color(self, widget):
        colorpicker = MDColorPicker(
            size_hint=(0.45, 0.85),
            type_color='HEX'
            # default_color=self.currcolor
        )
        colorpicker.bind(on_release=self.on_new_color_clicked)
        colorpicker.open()
        # self.ids.colorbox

    def on_new_color_clicked(self, widget, type, rgba):
        rgb = tuple(widget.get_rgb(rgba))
        hexcode = '#' + ('%02x%02x%02x' % rgb)
        self.currcolor = hexcode
        widget.dismiss()

    def on_anomaly(self, widget):
        if widget.state == "normal":
            widget.color = (1, 1, 1, .5)
            widget.text = "yes"
        else:
            widget.color = (.8, .95, 1, .5)
            widget.text = "no"

    def on_state_update(self):
        db = Database()
        if len(self.ids.painmeter.text) == 7:
            pain = self.ids.painmeter.text[-1]
        else:
            pain = 10
        if self.ids.anomalybtn.state == "normal":
            anomaly = 0
        else:
            anomaly = 1
        if self.ids.diameterbutton.text != '':
            diameter = float(self.ids.diameterbutton.text[:-3])
        db.cursor.execute(
            f"UPDATE Entry SET e_color = '{self.currcolor}' WHERE e_id = {currentry} AND e_pr_id = {currprotocol} AND e_pr_p_id = {curruserid}")
        db.cursor.execute(
            f"UPDATE Entry SET e_pain = '{pain}' WHERE e_id = {currentry} AND e_pr_id = {currprotocol} AND e_pr_p_id = {curruserid}")
        db.cursor.execute(
            f"UPDATE Entry SET e_diameter = '{diameter}' WHERE e_id = {currentry} AND e_pr_id = {currprotocol} AND e_pr_p_id = {curruserid}")
        db.cursor.execute(
            f"UPDATE Entry SET e_anomaly = '{anomaly}' WHERE e_id = {currentry} AND e_pr_id = {currprotocol} AND e_pr_p_id = {curruserid}")
        db.conn.commit()
        db.close()


class NotesTab(BoxLayout, MDTabsBase):
    def on_notes_update(self):
        db = Database()
        if App.get_running_app().isdoctor:
            pass
            # notesfromdoctor muss hinzugefügt werden
            db.cursor.execute(
                f"UPDATE Entry SET e_notesfromdoctor = '{self.children[0].text}' WHERE e_id = {currentry}")
        else:
            db.cursor.execute(
                f"UPDATE Entry SET e_notes = '{self.children[2].text}' WHERE e_id = {currentry} AND e_pr_id = {currprotocol} AND e_pr_p_id = {curruserid}")
        db.conn.commit()
        db.close()


class Entrys(Popup):
    def on_open(self):
        global curruserid, currprotocol, entrycounter
        db = Database()
        db.cursor.execute(f"SELECT e_date, e_id FROM Entry WHERE e_pr_id = {currprotocol}")
        entrys = db.cursor.fetchall()
        for i, entry in enumerate(entrys):
            # print(entry[0].strftime("%d %m %Y"))
            #list(entry).sort()
            date = datetime.strptime(str(entry[0]), '%Y-%m-%d').strftime('%#d. %#m. %Y')
            entrybtn = Button(
                size_hint=(1, None),
                height="60dp",
                background_normal='',
                # background_color=(App.get_running_app().greyblue),
                background_color=(App.get_running_app().darkblue),
                # text=str(entry[0]),
                text=date,
                bold=True,
                halign="center",
                font_size="22.5dp",
                # color=(0, 0, 0, 1),
                on_release=self.on_entry_release
            )
            entrybtn.index = i
            self.ids.entrylayout.add_widget(entrybtn, 0)
            if len(entrycounter[currprotocol]) < len(entrys):
                #print(entry)
                entrycounter[currprotocol].update({entry[1]:0})
            #print(entrycounter)
        #if entrys is not [()]:
            #if len(entrycounter[currprotocol]) < len(entrys):
            #    entrycounter[currprotocol].append(0)
        newentrybtn = Button(
            size_hint=(1, None),
            height="60dp",
            background_normal='',
            background_color=(.23, .34, .45, 1),
            # background_color=(App.get_running_app().lightblue),
            text="+",
            font_size="45dp",
            on_release=self.on_new_entry_release
        )
        if App.get_running_app().isdoctor:
            newentrybtn.disabled = True
        self.ids.entrylayout.add_widget(newentrybtn, len(entrys))
        db.close()

    def on_entry_release(self, widget):
        global currentry, currprotocol
        # setzt zu entryscreen und übergibt current entry.
        db = Database()
        # entryscreen = App.get_running_app().root.ids.DermoScreens.get_screen('entryscreen')
        db.cursor.execute(f"SELECT e_id FROM Entry WHERE e_pr_id = {currprotocol}")
        # hier error, muss sich anpassen an widget.
        currentry = db.cursor.fetchall()[widget.index][0]
        # entryscreen = App.get_running_app().root.ids.DermoScreens.get_screen('entryscreen').add_widget(entry)
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        # App.get_running_app().root.ids.DermoScreens.current_screen = entryscreen
        App.get_running_app().root.ids.DermoScreens.current = 'entryscreen'
        db.close()
        self.dismiss()

    def on_new_entry_release(self, widget):
        global currentry, entrycounter
        tempid = 0
        db = Database()
        db.cursor.execute(
            f"INSERT INTO Entry(e_pr_id, e_pr_p_id, e_date) VALUES({currprotocol}, {curruserid}, '{datetime.today().strftime('%Y-%m-%d')}')")
        db.conn.commit()
        db.cursor.execute(f"SELECT e_id FROM Entry WHERE e_pr_id = {currprotocol}")
        # kriegt jetziges entry id
        for entrys in db.cursor.fetchall():
            if entrys[0] > tempid:
                tempid = entrys[0]
        currentry = tempid
        entrycounter[currprotocol].update({tempid: 0})
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        App.get_running_app().root.ids.DermoScreens.current = 'entryscreen'
        db.close()
        self.dismiss()

    def on_protocol_delete(self, widget):
        db = Database()
        db.cursor.execute(f"DELETE FROM Protocol WHERE pr_id = {currprotocol}")
        db.conn.commit()
        cscreen = App.get_running_app().root.ids.DermoScreens.get_screen('patientscreen')
        cscreen.on_enter()
        db.close
        self.dismiss()

    # db.cursor.execute(f"SELECT * FROM Entry WHERE ")


class NewProtocoll(Popup):
    def on_new_protocol_release(self, widget):
        global curruserid, currprotocol, entrycounter
        db = Database()
        if len(self.ids.new_protocol_namebox.text) <= 13:
            db.cursor.execute(f"INSERT INTO Protocol (pr_p_id, pr_name) VALUES ({curruserid}, %s)",
                              (self.ids.new_protocol_namebox.text,))
            db.cursor.execute("SELECT pr_id FROM Protocol WHERE pr_name = %s;", (self.ids.new_protocol_namebox.text,))
            currprotocol = db.cursor.fetchall()[0][0]
            db.conn.commit()
            entrycounter
            db.close()
        else:
            protocollenerror = Factory.LoginOrSignUpError()
            protocollenerror.loginorsignuperrormsg = "Name too long, can't have more than 13 characters."
            protocollenerror.open()
            self.dismiss()

    def on_dismiss(self):
        # muss zuerst screen instanzieren, um dessen draw_protocol funktion aufzurufen. dient dazu, upyudaten nach neuem protocol.
        patscreen = App.get_running_app().root.ids.DermoScreens.get_screen('patientscreen')
        patscreen.children[0].children[1].children[0].children[1].draw_protocol()
        # patscreen.children[0].children[1].children[0].draw_protocol()
        # print(PatientScreen.children.get(0))
        # .children[1].children[0].draw_protocol()
        # newprotocol = Protocol()
        # newprotocol.draw_protocol()


class ChoosePicture(Popup):
    file_manager = MDFileManager

    def on_fromfolder(self, widget):
        # request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        path = os.path.expanduser("~")  # path to the directory that will be opened in the file manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
            select_path=self.select_path,  # function called when selecting a file/directory
            preview=True,
            # icon_folder="Images/User_DermoPEL.png"
        )
        self.file_manager.show(path)

    def select_path(self, path: str):
        db = Database()
        self.exit_manager()
        for f in os.listdir(f'Temp/TempEntry{currentry}'):
            os.remove(os.path.join(f'Temp/TempEntry{currentry}', f))
        os.rmdir(f'Temp/TempEntry{currentry}')
        imgblob = bytearray(convertdata((path)))
        query = f"UPDATE Entry SET e_picture = %s WHERE e_id = {currentry}"
        values = (imgblob,)
        db.cursor.execute(query, values)
        db.conn.commit()
        toast(path)
        tab = self.parent.children[3].children[0].children[0].children[0].children[1].get_slides()[0]
        # print(self.parent.children)
        createimgs(imgblob)
        tab.children[1].background_normal = f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png'
        tab.children[1].background_down = f'Temp/TempEntry{currentry}/tempimgdb_down{entrycounter[currprotocol][currentry]}.png'
        tab.children[1].background_disabled_normal = f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png'
        tab.children[1].background_disabled_down = f'Temp/TempEntry{currentry}/tempimgdb_down{entrycounter[currprotocol][currentry]}.png'

    def exit_manager(self, *args):
        tab = self.parent.children[2].children[0].children[0].children[0].children[1].get_slides()[0]
        print(tab.children[1].background_normal)
        self.file_manager.manager_open = False
        self.file_manager.close()

    def on_takepic(self, widget):
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        App.get_running_app().root.ids.DermoScreens.current = 'camerascreen'

class ConfirmPicture(Popup):
    def on_open(self):
        self.ids.entryimg.source = f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png'

    def on_confirm_release(self, widget):
        # DB behaviour!
        db = Database()
        #        imgblob = convertdata(f'Temp/selfie{currimg}.png')
        imgblob = bytearray(convertdata(f'Temp/TempEntry{currentry}/tempimgdb{entrycounter[currprotocol][currentry]}.png'))
        # query = "UPDATE entry SET e_picture = %s WHERE e_id = %s"
        # values = (imgblob, currentry)
        # db.cursor.execute(query, values)
        query = f"UPDATE Entry SET e_picture = %s WHERE e_id = {currentry}"
        values = (imgblob,)
        db.cursor.execute(query, values)
        db.conn.commit()
        App.get_running_app().root.ids.DermoScreens.transition = RiseInTransition()
        App.get_running_app().root.ids.DermoScreens.current = 'entryscreen'
        self.dismiss()

    #def on_dismiss(self):
        #global currimg
        # os.remove(f'Temp/selfie{currimg}.png')
        #currimg = currimg + 1


class LoginOrSignUpError(Popup):
    loginorsignuperrormsg = StringProperty()


class ConfirmAction(Popup):
    msg = StringProperty()

    def __init__(self, caller, **kwargs):
        super().__init__(**kwargs)
        self.caller = caller

    def on_confirm(self, widget):
        self.caller.on_confirm()
        self.dismiss()


class ChooseDoctor(Popup):
    doclist = []
    docdropdown = DropDown

    def on_open(self):
        db = Database()
        db.cursor.execute(f"SELECT * FROM Doctor")
        self.doclist = db.cursor.fetchall()
        self.docdropdown = DropDown(
            size_hint=(.5, 1)
        )
        """for doc in self.doclist:
            item = Button(
                text=doc[1],
                size_hint_x=.5,
                size_hint_y=None,
                height="40dp",
                border=(20, 20, 20, 20),
                background='',
                background_color=App.get_running_app().darkblue,
                color=App.get_running_app().lightblue,
                bold=True,
                font_size="20dp"
            )
            item.bind(on_release=lambda x, button=item: self.docdropdown.select(button.text))
            self.docdropdown.add_widget(item)
            self.docdropdown.bind(on_select=lambda instance, x: setattr(self.ids.search_docbox, 'text', x))"""

    def on_search_doc(self, widget):
        # print(widget.text)
        if widget.text != '':
            searchresult = []
            self.docdropdown.clear_widgets()
            # for x in self.docdropdown.children[0].children:
            #    self.docdropdown.remove_widget(x)
            # self.docdropdown.clear_widgets(self)
            for i in self.doclist:
                if i[1][:len(widget.text)] == widget.text or i[1][:len(widget.text)] == widget.text.title():
                    """item = Button(
                        text=i[1],
                        size_hint_x=.5,
                        size_hint_y=None,
                        height="40dp",
                        border=(20, 20, 20, 20),
                        background='',
                        background_color=App.get_running_app().darkblue,
                        color=App.get_running_app().lightblue,
                        bold=True,
                        font_size="20dp"
                    )
                    #item.bind(on_release=lambda x, button=item: self.docdropdown.select(button.text))
                    self.docdropdown.add_widget(item)
                    #self.docdropdown.bind(on_select=lambda instance, x: setattr(self.ids.search_docbox, 'text', x))"""
                    searchresult.append(i[1])
                # print(i[1][:len(widget.text)])
            # print(searchresult)
            # print(set(searchresult))
            try:
                for j in set(searchresult):
                    item = Button(
                        text=j,
                        size_hint_x=.5,
                        size_hint_y=None,
                        height="40dp",
                        border=(20, 20, 20, 20),
                        background='',
                        background_color=App.get_running_app().darkblue,
                        color=App.get_running_app().lightblue,
                        bold=True,
                        font_size="20dp"
                    )
                    item.bind(on_release=lambda x, button=item: self.docdropdown.select(button.text))
                    #item.bind(on_release=lambda x, button=item: self.ids.search_docbox.text)
                    self.docdropdown.add_widget(item)
                    self.docdropdown.bind(
                        on_select=lambda instance, x: setattr(self.ids.search_docbox, 'text', x))
            except:
                print("recursion error")
            # for t in self.docdropdown.children[0].children:
            #    print(t.text)
            # self.on_open_dropdown(widget)
            # self.docdropdown.open(self.ids.search_docbox)

    def on_open_dropdown(self, widget):
        self.docdropdown.open(widget)

    def on_save_doc(self, widget):
        db = Database()
        #db.cursor.execute(f"UPDATE Patient SET WHERE p_id = {curruserid}")
        #if self.ids.search_docbox.text in self.doclist:
        #    print("works")
        t = False
        for doc in self.doclist:
            if self.ids.search_docbox.text == doc[1] or self.ids.search_docbox.text.title() == doc[1]:
                db.cursor.execute(f"UPDATE Patient SET p_d_treatingdoctor = {doc[0]} WHERE p_id = {curruserid}")
                db.conn.commit()
                Snackbar(
                    text="[color=#0824AA]doctor was saved![/color]",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    bg_color=App.get_running_app().lightblue,
                    font_size="20dp",
                    radius=(20, 20, 20, 20),
                    size_hint_x=(
                                        Window.width - (dp(10) * 2)
                                ) / Window.width
                ).open()
                t = True
        if not t:
            Snackbar(
                text="[color=#0824AA]this doctor does not exist.[/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                bg_color=App.get_running_app().lightblue,
                font_size="20dp",
                radius=(20, 20, 20, 20),
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()



# -----------------------------------------------------
# App
# -----------------------------------------------------


class DermoPELApp(MDApp):
    # Farben
    isdoctor = BooleanProperty(False)
    istreating = BooleanProperty(False)
    # canupdate = BooleanProperty(False)
    darkbluehx = StringProperty('#0824aa')
    lightbluehx = StringProperty('#ccf2ff')
    greybluehx = StringProperty('#a6c8e0')
    greyhx = StringProperty('#eaeaea')
    darkblue = ColorProperty([.03, .14, .67, 1])
    lightblue = ColorProperty([.8, .95, 1, 1])
    greyblue = ColorProperty([.65, .78, .88, 1])
    grey = ColorProperty([.92, .92, .92, 1])
    platform = StringProperty(platform)

    def on_resize(self, win, width, height):
        # print(str(width) + ' ' + str(height))
        patscreen = App.get_running_app().root.ids.DermoScreens.get_screen('patientscreen')
        patscreen.on_enter()

    def build(self):
        self.icon = 'Images/Logokreis_DermoPEL.png'
        Window.bind(on_resize=self.on_resize)
        if platform == 'win':
            Config.set('input', 'mouse', 'mouse,disable_multitouch')
        if (platform == 'android' or platform == 'ios'):
            Window.maximize()
        else:
            pass
            # Window sizes Samsung A12
            # Window.size = (650, 600)
            # Window.size = (360, 800)
        # patscreen = App.get_running_app().root.ids.DermoScreens.get_screen('patientscreen')
        # patscreen.children[0].children[1].children[0].children[0].width = dp(100)
        global curruserid
        db = Database()
        db.cursor.execute("SELECT * FROM Patient")
        pdebug = db.cursor.fetchall()
        db.cursor.execute("SELECT * FROM Doctor")
        ddebug = db.cursor.fetchall()
        db.cursor.execute("SELECT * FROM Protocol")
        prdebug = db.cursor.fetchall()
        # db.cursor.execute("SELECT * FROM Entry")
        # edebug = db.cursor.fetchall()
        print("Patients: " + str(pdebug) + "\nDoctors: " + str(ddebug) + "\nProtocols: " + str(
            prdebug))  # + "\nEntrys: " + str(edebug))

        self.root = Display()
        if store.exists('curruserjson'):
            if datetime.now() < datetime.strptime(store.get('curruserjson')['expires'], '%Y-%m-%d %H:%M:%S.%f'):
                if store.get('curruserjson')['type'] == "patient":
                    self.root.ids.DermoScreens.current = 'patientscreen'
                    curruserid = store.get('curruserjson')['curruser']
                    App.get_running_app().isdoctor = False
                elif store.get('curruserjson')['type'] == "doctor":
                    self.root.ids.DermoScreens.current = 'doctorscreen'
                    curruserid = store.get('curruserjson')['curruser']
                    App.get_running_app().isdoctor = True
            else:
                store.delete('curruserjson')

        # Connection zur DB
        # Kann ohne DB initiallisiert werden
        """dermoconn = mysql.connector.connect(
            # bei online DB muss Host eine IP sein.
            host="localhost",
            user="root",
            passwd="",
            database="dermopel_testdb"
        )"""

        # Curser, welche unsere Queries executed
        # dermocurser = dermoconn.cursor()

        # zeigt description der db an
        """dermocurser.execute("SELECT * FROM Patient")
        print(dermocurser.description)"""

        # zeigt alle DBs an
        """dermocurser.execute("SHOW DATABASES")
        for db in dermocurser:
            print(db)"""

        # neue row hinzufügen
        """mysql_command = "INSERT INTO Patient (p_id) VALUES (%s)"
        values = (self.root.ids.Doctor_switch.state,)
        dermocurser.execute(mysql_command, values)"""

        # alle rows anzeigen
        """dermocurser.execute("SELECT * FROM Patient")
        records = dermocurser.fetchall()
        print(records)"""

        # eine row anzeigen
        """dermocurser.execute("SELECT * FROM Patient")
        records2 = dermocurser.fetchone()
        print(records2)"""

        # anzahl an rows anzeigen
        """dermocurser.execute("SELECT * FROM Patient")
        records3 = dermocurser.fetchmany(2)
        print(records3)"""

        # für Debugging: gibt anzahl an veränderten oder Selecteten Rows zurück
        """dermocurser.execute("SELECT * FROM Patient")
        print(dermocurser.rowcount)"""

        # für Debugging: gibt das letzte Statement zurück
        """dermocurser.execute("SELECT * FROM Patient")
        print(dermocurser.statement)"""

        # Änderungen commiten
        # dermoconn.commit()

        # conn schließen
        # dermoconn.close()

        # Beispiel für Benutzung der Database Klasse
        """testdb = Database(host="localhost", user="root", passwd="", database="dermopel_testdb")
        testdb.cursor.execute("SELECT p_id FROM Patient WHERE p_id = 1")
        record = testdb.cursor.fetchone()
        if record[0] == 1:
            print(record[0])"""
        # müssen hier record[0] nehmen, da fetchone einen tuple (ähnlich wie array) zurückgibt
        # (fetchall gibt eine liste an tuples zurück)

        # Camera Play
        # self.testcam = Camera()

        # setzt Resolution, nimmt Tuple
        # self.testcam.resolution(800, 800)

        # Button, welcher Foto aufnimmt
        """testbut = Button(text="Foto aufnehmen")
        testbut.bind(on_press=self.take_selfie)"""
        return self.root

    # funktion für kamera export
    """def take_selfie(self, *args):
        print("taking pic")
        self.testcam.export_to_png("./pic.png")"""


if __name__ == '__main__':
    if os.path.exists('Temp'):
        for f in os.listdir('Temp'):
            for d in os.listdir('Temp/' + f):
                os.remove(os.path.join('Temp', f, d))
            os.rmdir(os.path.join('Temp', f))
        os.rmdir('Temp')
    os.mkdir('Temp')
    DermoPELApp().run()
    for f in os.listdir('Temp'):
        for d in os.listdir('Temp/' + f):
            os.remove(os.path.join('Temp', f, d))
        os.rmdir(os.path.join('Temp', f))
