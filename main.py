from tkinter import *
import pandas as pd
import os

screen = Tk()
screen.config(bg="#DB8A74")
screen.title("Soru")


class SorgulayiciGenclik():
    def __init__(self):
        self.username = StringVar
        self.pswd = StringVar
        self.user_frame = Frame(screen)
        self.user_frame.pack()
        self.userdata = pd.read_csv("userdata.csv").to_dict()
        self.username_entry = Entry(self.user_frame, width=76)
        self.username_entry.insert(END, "Kullanici adi")
        self.username_entry.pack(pady=200)

        self.pswd_entry = Entry(self.user_frame, width=76)
        self.pswd_entry.insert(END, "Sifre")
        self.pswd_entry.pack()

        submit = Button(self.user_frame, text="submit", command=self.logged_in)
        submit.pack()

    def logged_in(self):
        name = str(self.username_entry.get())
        pswd = str(self.pswd_entry.get())
        self.userdata[name] = pswd
        self.userdata = pd.DataFrame(self.userdata).to_csv("userdata.csv")
        self.user_frame.destroy()
        qm = QuestionManager()
        qm.startup(name)


class QuestionManager():
    def __init__(self):
        self.path_to_q = pd.read_csv("path_q.csv")
        self.choice_screen = Tk()
        self.choice_screen.config(bg="#DB8A74")
        self.choice_screen_frame = Frame(self.choice_screen)
        self.question_number = 0
        self.suanki_zorluk = "kolay"
        self.questions_answered = []
        self.answer_key = pd.read_csv("path.csv")
        self.yanlis_sayi = 0
        self.cozulen_soru = 0

    def startup(self, name):
        def increaseqn():
            if len(self.questions_answered) > self.question_number:
                self.question_number += 1

        self.choice_screen.title(name)

        self.A = Button(text="A", master=self.choice_screen_frame, width=30, height=10, command=lambda: self.check("a"))
        self.A.pack(side=LEFT)
        self.B = Button(text="B", master=self.choice_screen_frame, width=30, height=10, command=lambda: self.check("b"))
        self.B.pack(side=LEFT)
        self.C = Button(text="C", master=self.choice_screen_frame, width=30, height=10, command=lambda: self.check("c"))
        self.C.pack(side=LEFT)
        self.D = Button(text="D", master=self.choice_screen_frame, width=30, height=10, command=lambda: self.check("d"))
        self.D.pack(side=LEFT)
        self.next = Button(text="siradaki", master=self.choice_screen_frame, width=40, height=10, command=increaseqn)
        self.next.pack(side=BOTTOM)
        self.ui_setup()

    def ui_setup(self):
        self.choice_screen_frame.pack()
        self.soru_getir()

    def soru_getir(self):
        if self.suanki_zorluk == "kolay":
            self.suanki_soru = self.path_to_q.kolay.to_list()[self.question_number]
            self.answer_key1 = self.answer_key.kolay.to_list()
        elif self.suanki_zorluk == "orta":
            self.suanki_soru = self.path_to_q.orta.to_list()[self.question_number]
            self.answer_key1 = self.answer_key.orta.to_list()
        elif self.suanki_zorluk == "zor":
            self.suanki_soru = self.path_to_q.zor.to_list()[self.question_number]
            self.answer_key1 = self.answer_key.zor.to_list()
        elif self.suanki_zorluk == "bitti":
            self.choice_screen_frame.destroy()
            sonuc = Label()
            sonuc.config(
                text=f"Sonucunuz: {self.cozulen_soru - self.yanlis_sayi}/{self.cozulen_soru}\n Doğru oranınız: {(self.cozulen_soru - self.yanlis_sayi) / self.yanlis_sayi * 100}",
                width=50, height=50)
            sonuc.pack()
            self.cozulen_soru = 0
            self.yanlis_sayi = 0

        self.question_link = "127.0.0.1:80/" + self.suanki_soru + ".pdf"
        print(self.question_link)
        os.system(f"start chrome {self.question_link}")

    def check(self, opt):
        self.cevap = False
        while len(self.questions_answered) < len(self.answer_key1) and self.cevap == False and len(
                self.questions_answered) == self.question_number:
            self.cozulen_soru += 1
            if opt != self.answer_key1[self.question_number]:
                print("!!!")
                self.yanlis_sayi += 1
            self.questions_answered.append(opt)
            print(self.question_number, " ", self.questions_answered)
            self.cevap = True
        if len(self.questions_answered) == len(self.answer_key1):
            self.questions_answered = []
            self.question_number = 0
            if self.suanki_zorluk == "kolay":
                self.suanki_zorluk = "orta"
            elif self.suanki_zorluk == "orta":
                self.suanki_zorluk = "zor"
            elif self.suanki_zorluk == "zor":
                self.suanki_zorluk = "bitti"
            self.soru_getir()


genc = SorgulayiciGenclik()

screen.mainloop()
