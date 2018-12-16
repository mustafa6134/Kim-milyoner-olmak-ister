from tkinter import *
from tkinter import messagebox
from time import *
import sqlite3
import random
import copy

def soru_listele():
    #Bu fonksiyon dışarıdan txt dosyası okuyup ,soruları karıştırıp zorluk derecesine göre ayırıyor.

    soru_Listesi = open('Sorular.txt', 'r')
    soru_Listesi = soru_Listesi.read()
    soru_Listesi = list(soru_Listesi.split("\n"))

    for dizi, i in enumerate(soru_Listesi):
        a = i.split("/")
        soru_Listesi[dizi] = a
    kolay_s=[]
    zor_s=[]
    soru_ll=[]
    while len(soru_Listesi)!=0:
        sec=random.choice(soru_Listesi)
        soru_ll.append(sec)
        soru_Listesi.pop(soru_Listesi.index(sec))

    for i in soru_ll:

        if i.pop(0)=="1":
            kolay_s.append(i)
        else:
            zor_s.append(i)

    return zor_s , kolay_s

def giris():

    global giris_Ekran
    global kullanici_G
    global sifre

    giris_Ekran=Tk()
    giris_Ekran.geometry("300x150+800+350")
    giris_Ekran.resizable(width=False, height=False)
    Label(text="Kullanıcı Adı:",font="Arial 15",fg="SteelBlue1",bg="gray19").place(x=20,y=10)
    Label(text="Şifre :",font="Arial 15",fg="SteelBlue1",bg="gray19").place(x=80, y=40)
    giris_Ekran.configure(background="gray19")
    kullanici_G=Entry(fg="SteelBlue1",bg="gray30")
    kullanici_G.place(y=14,x=145)

    sifre=Entry(show="*",fg="SteelBlue1",bg="gray30")
    sifre.place(x=145,y=48)

    gir=Button(text="Giriş",width=10,command=giris_kotrol,font="Arial 10",fg="SteelBlue1",bg="gray19")
    gir.place(x=180,y=90)

    kayit=Button(text="Kayıt Olun",command=kayıt_ol,font="Arial 10",fg="SteelBlue1",bg="gray19")
    kayit.place(x=40,y=90)

    giris_Ekran.mainloop()
def kayıt_ol():
    giris_Ekran.destroy()
    global kayit_Ekran
    global isim,soyad,kullanici_K,sifre,tekrar,posta
    kayit_Ekran=Tk()
    kayit_Ekran.geometry("300x400+700+100")
    kayit_Ekran.configure(background="gray19")

    Label(text="Kayıt Sayfası",font="Arial 15",fg="SteelBlue1",bg="gray19").pack()

    Label(text="İsim :",fg="SteelBlue1",bg="gray19").place(x=60,y=40)
    isim=Entry(fg="SteelBlue1",bg="gray30")
    isim.place(x=110,y=40)

    Label(text="Soyad :",fg="SteelBlue1",bg="gray19").place(x=50,y=90)
    soyad=Entry(fg="SteelBlue1",bg="gray30")
    soyad.place(x=110,y=90)

    Label(text="Kullanıcı Adı :",fg="SteelBlue1",bg="gray19").place(x=20,y=140)
    kullanici_K=Entry(fg="SteelBlue1",bg="gray30")
    kullanici_K.place(x=110,y=140)

    Label(text="Şifre :",fg="SteelBlue1",bg="gray19").place(x=60,y=190)
    sifre=Entry(show="*",fg="SteelBlue1",bg="gray30")
    sifre.place(x=110,y=190)

    Label(text="Tekrar Şifre :",fg="SteelBlue1",bg="gray19").place(x=28, y=240)
    tekrar=Entry(show="*",fg="SteelBlue1",bg="gray30")
    tekrar.place(x=110 , y=240)

    Label(text="E-posta:",fg="SteelBlue1",bg="gray19").place(x=50,y=290)
    posta=Entry(width=26,fg="SteelBlue1",bg="gray30")
    posta.place(x=110,y=290)

    bitir=Button(text="Kayıt",font="Arial 12",fg="SteelBlue1",bg="gray19",command=kayit_kontrol)
    bitir.place(x=130,y=340)

    con=sqlite3.connect("Kim milyoner olmak ister.db")
    cursor=con.cursor()
    cursor.execute("create table if not exists Kullanici ('İsim' text , 'Soyad' text , 'Kullanici_Adi' text , 'Sifre' text , 'Eposta' text, 'Para' text NOT NULL,'Puan' int NOT NULL)")
    con.commit()
    con.close()
    kayit_Ekran.mainloop()

def kayit_kontrol():
    con = sqlite3.connect("Kim milyoner olmak ister.db")
    cursor = con.cursor()
    cursor.execute("select Eposta,Kullanici_Adi from Kullanici")
    liste = list(cursor.fetchall())
    e_posta=[]
    ad=[]

    buyuk_harf=[]
    kucuk_harf=[]

    for i in liste:
        e_posta.append(i[0])
        ad.append(i[1])
        #Şifrede büyük ve küçük harf olup olamadığını   kontrol ediyor
    for i in sifre.get():
        if i in "qazxswedcvfrtgbnhyujmökıolçşpğiü":
            kucuk_harf.append(i)
        elif i in "qazxswedcvfrtgbnhyujmökıolçşpğiü".upper():
            buyuk_harf.append(i)

        #Boş satır kontrolü
    if isim.get()=="" or  soyad.get()=="" or kullanici_K.get()=="" or sifre.get()=="" or tekrar.get()=="" or posta.get()=="":
        messagebox.showwarning("Kayıt","Eksik Bilgi Girdiniz.Bilgilerinizi kontrol ediniz.")

        #Şifre kontrolü
    elif sifre.get()!=tekrar.get():
            messagebox.showwarning("Kayıt","Şifre Eşleşmedi.")
    elif 8 >len(sifre.get()):
        messagebox.showwarning("Kayıt","Sifre 8 Karakterden Fazla Olmalı")
    elif len(kucuk_harf)==0:
        messagebox.showwarning("Kayıt","En az 1 küçük harf olamsı gerekiyor.")
    elif len(buyuk_harf)==0:
        messagebox.showwarning("Kayıt", "En az 1 büyük harf olamsı gerekiyor.")

        #E-posta kontrolü
    elif posta.get() in e_posta:
        messagebox.showwarning("Kayıt","Bu E-postanın Zaten Var.Farklı bir E-posta Deneyiniz.")
    elif not ("@" in posta.get() and ".com" in posta.get()):
        messagebox.showwarning("Kullanici","E posta adresinizi kontrol ediniz ")

        #Kullanıcı adı kontrolü
    elif kullanici_K.get() in ad:
        messagebox.showwarning("Kayıt","Böyle Bir Kullanıcı Zaten Var.Başka Bİr Kullanıcı Adı Giriniz.")

    else:
        cursor.execute("insert into Kullanici values (?,?,?,?,?,?,?)",(isim.get(),soyad.get(),kullanici_K.get(),sifre.get(),posta.get(),"",0))
        con.commit()
        con.close()
        messagebox.showwarning("Kayıt","Kayıt Yapıldı")
        kayit_Ekran.destroy()
        giris()

def giris_kotrol():

    global kullanici_E
    con=sqlite3.connect("Kim milyoner olmak ister.db")
    cursor=con.cursor()
    cursor.execute("select Sifre from Kullanici where Kullanici_Adi=?",(kullanici_G.get(),))
    sif=cursor.fetchall()
    kullanici_E=kullanici_G.get()
    con.close()
    if len(sif)!=0:
        if  sifre.get() == sif[0][0]:
            con.close()
            giris_Ekran.destroy()
            ana()
        else:
            messagebox.showwarning( "Kullanıcı Girişi","Şifre yanlış girildi.")
    elif kullanici_G.get() == "" and sifre.get() == "":
         messagebox.showwarning("Kuulanıcı Girişi", "Hiç Bir Bilgi Girişi Yapılmadı.")
    elif sifre.get() == "":
        messagebox.showwarning("Kullanını Girişi", "Şifre girişi yapılmadı.")
    elif kullanici_G.get() == "":
        messagebox.showwarning("Kullanıcı Girişi", "Kullanıcı ismi girilmedi.")
    else:
        messagebox.showwarning("Kullanıcı Girişi", "Böyle Bir  Kullanıcı Adı Yok")

def ana():
        global kolay,zor,ana_Ekran,para_İmlec,cift
        global soru_No,yarı,seyir,puan
        soru_No = [-1]
        yarı=[1]
        seyir=[1]
        puan=[0]
        cift=[1]
        para_İmlec=[558]

        zor, kolay = soru_listele() #fonksiyonunu çagırıp zor ve kolay soruları karışık bir şekilde alıyor ana menüde kullanıyorum çünkü basla fonksiyonun altında kullansam aynı her soru sonrasında sorular tekrar karıştırılacak.

        ana_Ekran = Tk()
        ana_Ekran.geometry("1000x700+500+200")
        ana_Ekran.resizable(width=False, height=False)
        ana_Ekran.configure(background="gray30")
        ana_Ekran.title("Kim Milyoner Olamak İster?")
        Label(text="KİM MİLYONER OLAK İSTER?",font="Arial 30",fg="SteelBlue1",bg="gray30").place(x=300,y=70)
        con=sqlite3.connect("Kim milyoner olmak ister.db")
        cursor=con.cursor()
        cursor.execute("select İsim,Soyad from Kullanici where Kullanici_Adi=?",(kullanici_E,))
        login=cursor.fetchall()
        login=" ".join(login[0])

        Label(text="Hoşgeldiniz   "+login.upper(),font="Arial 13", width=40, bg="green3",fg="black").place(x=1,y=1)

        cursor.execute("select Kullanici_Adi,Puan,Para from Kullanici where Puan!=?",(0,))
        para_Tablosu=list(cursor.fetchall())
        con.close()

        if len(para_Tablosu):
            sira=[]
            for i in para_Tablosu:
                sira.append(i[1])
            sira.sort(reverse=True)

            yeni_Liste=[]
            for i in sira:
                for  j in para_Tablosu:
                    if i==j[1]:
                        yeni_Liste.append(j)

            satir=200
            Label(text="KULLANICI ADI" + "                    " + "PUAN" + "                " + "SON KAZANILAN PARA", font="Arial 14", bg="gray30",fg="tomato2").place(x=280, y=170)
            for i in yeni_Liste:
                Label(text=i[0],font="Arial 16",bg="gray30",fg="gold").place(x=280,y=satir)
                Label(text=i[1], font="Arial 16", bg="gray30", fg="SteelBlue1").place(x=520, y=satir)
                Label(text=i[2]+" TL", font="Arial 16", bg="gray30", fg="orange").place(x=720, y=satir)
                satir+=30

        oturum_b=Button(text="Oturum Çıkış",font="Arial 10",width=14,command=oturum,bg="gray19",fg="SteelBlue1")
        oturum_b.place(x=400,y=2)

        basla_b=Button(text="BAŞLA",font="Arial 16",width=14,command=baslat,bg="gray19",fg="SteelBlue1")
        basla_b.place(x=50,y=100)

        hakkinda_b = Button(text="HAKKINDA", font="Arial 13", width=14, command=hakkinda,bg="gray19",fg="SteelBlue1")
        hakkinda_b.place(x=50, y=200)

        cikis_b=Button(text="Oyundan Çık",font="Arial 10",width=14,bg="gray19",fg="SteelBlue1",command=cikis)
        cikis_b.place(y=600,x=800)

        ana_Ekran.mainloop()
def oturum():
    ana_Ekran.destroy()
    giris()
def baslat():
    ana_Ekran.destroy()
    basla()
def basla():
    global a_B, b_B, c_B, d_B,ss,seyirci_b,cekil_b,yari_b,cift_b
    global oyun_Ekran,sabit_Soru_Listesi,cevap,para_liste

    ss=[0]
    soru_No[0]= soru_No[0] + 1 #Her soruda 1 artıyor kaçıncı soruda oldugumuzu ogrenebiliyoruz.

    oyun_Ekran=Tk()
    oyun_Ekran.geometry("1000x700+500+200")
    oyun_Ekran.resizable(width=False, height=False)
    oyun_Ekran.title("Kim Milyoner Olamak İster?")
    oyun_Ekran.configure(background="gray19")

    if soru_No[0]==12:

        con = sqlite3.connect("Kim milyoner olmak ister.db")
        cursor = con.cursor()
        cursor.execute("update Kullanici set Para=? where Kullanici_Adi=?", ("1.000.000", kullanici_E))
        con.commit()
        con.close()
        Label(text="1.000.000" + " Kazandınız Tebrikler", font="Arial 20", bg="green3", fg="black").place(x=250, y=300)
        oyun_Ekran.update()
        sleep(3)
        oyun_Ekran.destroy()
        ana()

    else:
        if soru_No[0]>6:
            if cift[0]:
                cift_b = Button(text="Çift Cevap", width=14, fg="SteelBlue1", bg="gray30", command=cift_fonk)
                cift_b.place(x=350, y=50)
            else:
                cift_b = Button(text="Çift Cevap", width=14, fg="black", bg="red4").place(x=350, y=50)
        if soru_No[0]:
            cekil_b=Button(text="Çekimek İstiyorum",font="Arial 10",width=14,command=cekil,fg="cyan",bg="gray30")
            cekil_b.place(x=195, y=120)

        ana_b=Button(text="Ana Menü", font="Arial 10", width=14, command=geri, fg="SteelBlue1", bg="gray30")
        ana_b.place(x=840, y=640)

        if seyir[0]:
            seyirci_b=Button(text="Seyirci",width=14,fg="cyan",bg="gray30",command=seyirci)
            seyirci_b.place(x=50,y=50)
        else:
            seyirci_b = Button(text="Seyirci",  width=14, fg="black", bg="red4")
            seyirci_b.place(x=50, y=50)
        if yarı[0]:
            yari_b=Button(text="Yarı Yarıya",width=14,fg="cyan",bg="gray30",command=yarıyarıya)
            yari_b.place(x=200,y=50)
        else:
            yari_b = Button(text="Yarı Yarıya", width=14, fg="black", bg="red4")
            yari_b.place(x=200, y=50)
            ss[0]=1

        sabit_Soru_Listesi= soru_Sec()#kolay ve zor soru listelerinden soru_No suna göre soru alıyor
        soru_1=copy.deepcopy(sabit_Soru_Listesi)

        soru_text=Text(font="Arial 15",bg="gray30",fg="SteelBlue1",width=60,height=5)
        soru_text.insert(INSERT, str(soru_No[0] + 1) + ") " + soru_1.pop(0))
        soru_text.place(x=50,y=200)

        para_liste=["500","1.000","2.000","3.000","5.000","7.000","15.000","30.000","60.000","125.000","250.000","1.000.000"]
        y=560

        cevap=[]

        for i in range(len(soru_1)):
            a=random.choice(soru_1)
            soru_1.remove(a)
            cevap.append(a)

        #para İmleç
        Label(text="<<<",font="Arial 18", bg="gray19", fg="snow").place(x=950,y=para_İmlec[0])
        para_İmlec[0]=para_İmlec[0]-45

        for a,i in enumerate(para_liste):
            a+=1
            if a==7 or a==2:
                para_Taplo = Label(text=str(a) + "   " + i + " TL", width=15, font="Arial 15", bg="gray30", fg="green2")
                para_Taplo.place(x=780, y=y)

            else:
                para_Taplo=Label(text=str(a)+"   "+i+" TL",width=15,font="Arial 15",bg="gray30",fg="SteelBlue1")
                para_Taplo.place(x=780,y=y)

            if  a<soru_No[0]+1:
                para_Taplo = Label(text=str(a) + "   " + i + " TL", width=15, font="Arial 15", bg="green4", fg="snow")
                para_Taplo.place(x=780, y=y)
            y-=45

        a_B=Button(text="A)  "+cevap[0],font="Arial 13",width=40,bg="gray30",fg="SteelBlue1",command=lambda :dogrumu("A"))
        a_B.place(x=10,y=500)

        b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="gray30", fg="SteelBlue1",command=lambda :dogrumu("B"))
        b_B.place(x=400, y=500)

        c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="gray30", fg="SteelBlue1",command=lambda :dogrumu("C"))
        c_B.place(x=10, y=600)

        d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="gray30", fg="SteelBlue1",command=lambda :dogrumu("D"))
        d_B.place(x=400, y=600)
        if soru_No[0]<7:
            saniye =60

            nokta = ["O" for i in range(31)]
            nokta_ekran = Label(oyun_Ekran, text=nokta, font="Arial 17", fg="snow3", bg="gray19")
            nokta_ekran.place(x=10, y=450)
            nokta2 = []
            try:
                for i in nokta * 2:

                    if saniye==-1:
                        Label(text="Zaman Doldu Kaybettiniz.",font="Arial 20",bg="red",fg="snow").place(x=250,y=300)
                        oyun_Ekran.update()
                        sleep(2)
                        oyun_Ekran.destroy()
                        ana()

                    if saniye % 2 == 0 and saniye >10:
                        nokta2.append(i)
                        nokta_ekran2 = Label(oyun_Ekran, text=nokta2, font="Arial 17", fg="dark green", bg="gray19")
                        nokta_ekran2.place(x=10, y=450)
                    elif saniye <= 10 and saniye % 2 == 0:
                        nokta2.append(i)
                        nokta_ekran2 = Label(oyun_Ekran, text=nokta2, font="Arial 17", fg="red", bg="gray19")
                        nokta_ekran2.place(x=10, y=450)

                    aa = Label(oyun_Ekran, text=str(saniye) + "    ", font="Arial 60", bg="gray19", fg="snow")
                    aa.place(x=400, y=350)
                    oyun_Ekran.update()
                    sleep(1)
                    saniye -= 1
            except:
                pass

        oyun_Ekran.mainloop()

def dogrumu(K_cevap):

    karar=messagebox.askyesno("Kim milyoner olamak ister?","Son kararınız mı?")
    secenek=K_cevap

    if karar:

        cevaplar={"A":cevap[0],"B":cevap[1],"C":cevap[2],"D":cevap[3]}
        K_cevap=cevaplar[K_cevap]

        if K_cevap==sabit_Soru_Listesi[4]:  #Seçilen cevap doğruysa o butonu bulmak için altındaki koşullardan geçecek.
                                #Ve o butonun rengini değiştirecek.
            if secenek == "A":
                a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="gold", fg="black")
                a_B.place(x=10, y=500)
                oyun_Ekran.update()
                a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="green3", fg="black")
                a_B.place(x=10, y=500)
            elif secenek=="B":
                b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="gold", fg="black")
                b_B.place(x=400, y=500)
                oyun_Ekran.update()
                b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="green3", fg="black")
                b_B.place(x=400, y=500)
            elif secenek=="C":
                c_B = Button(text="B)  " + cevap[2], font="Arial 13", width=40, bg="gold", fg="black")
                c_B.place(x=10, y=600)
                oyun_Ekran.update()
                c_B = Button(text="B)  " + cevap[2], font="Arial 13", width=40, bg="green3", fg="black")
                c_B.place(x=10, y=600)
            else:
                d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="gold", fg="black")
                d_B.place(x=400, y=600)
                oyun_Ekran.update()
                d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="green3", fg="black")
                d_B.place(x=400, y=600)

            puan[0] = (soru_No[0] + 1) * 10
            con=sqlite3.connect("Kim milyoner olmak ister.db")
            cursor=con.cursor()
            cursor.execute("select puan from Kullanici where Kullanici_Adi=?",(kullanici_E,))
            eski_Puan=cursor.fetchall()
            eski_Puan=eski_Puan[0][0]

            yeni_Puan=eski_Puan+puan[0]
            cursor.execute("update Kullanici set Puan=? where Kullanici_Adi=?",(yeni_Puan,kullanici_E))
            con.commit()
            con.close()

            #Doğru cevabı rengini değiştirdikten sonra ekranın üst taravına " Doğru Cevep Tebrikler :) " yazısını yazdırıyor.
            sleep(3)
            dogru = Label(oyun_Ekran, text="Doğru Cevep Tebrikler :)", font="Arial 13", width=40, bg="green3", fg="black").place(x=1, y=1)
            oyun_Ekran.update()
            sleep(3)

            #Yeni soru için pencereyi kapatıp basla fonksiyonunu yeniden çalıştırıyor.
            oyun_Ekran.destroy()
            basla()

        else:   #Seçilen cevap yanlışsaa o butonu bulmak için altındaki koşullardan geçecek.
                #Ve o butonun rengini değiştirecek.
            if secenek == "A":
                a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="gold", fg="black")
                a_B.place(x=10, y=500)
                oyun_Ekran.update()
                a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="red3", fg="snow")
                a_B.place(x=10, y=500)
            elif secenek=="B":
                b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="gold", fg="black")
                b_B.place(x=400, y=500)
                oyun_Ekran.update()
                b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="red3", fg="snow")
                b_B.place(x=400, y=500)
            elif secenek=="C":
                c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="gold", fg="black")
                c_B.place(x=10, y=600)
                oyun_Ekran.update()
                c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="red3", fg="snow")
                c_B.place(x=10, y=600)
            else:
                d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="gold", fg="black")
                d_B.place(x=400, y=600)
                oyun_Ekran.update()
                d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="red3",fg="snow")
                d_B.place(x=400, y=600)

                    #Doğru cevabın ne olduğunu göstermek için altdaki dönğü de doğru cevabı arayıp rengini değiştirecek.
            for sayac,i in enumerate(cevaplar.values()):
                if i==sabit_Soru_Listesi[4]:
                    if sayac==0:
                        a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="green3", fg="black")
                        a_B.place(x=10, y=500)
                    elif sayac==1:

                        b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="green3", fg="snow")
                        b_B.place(x=400, y=500)
                    elif sayac==2:
                        c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="green3", fg="black")
                        c_B.place(x=10, y=600)
                    else:
                        d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="green3", fg="black")
                        d_B.place(x=400, y=600)

            sleep(3)
            dogru = Label(oyun_Ekran, text="Yanlış Cevap :(", font="Arial 13", width=40, bg="red3", fg="snow")
            dogru.place(x=1, y=1)
            oyun_Ekran.update()
            sleep(3)

            if 1<soru_No[0]<7:

                con = sqlite3.connect("Kim milyoner olmak ister.db")
                cursor = con.cursor()
                cursor.execute("update Kullanici set Para=? where Kullanici_Adi=?",("1.000", kullanici_E))
                con.commit()
                con.close()
                Label(text="1.000" + " Kazandınız Tebrikler", font="Arial 20", bg="maroon",fg="black").place(x=250, y=300)
                oyun_Ekran.update()
                sleep(3)

            elif 6<soru_No[0]<13:

                con = sqlite3.connect("Kim milyoner olmak ister.db")
                cursor = con.cursor()
                cursor.execute("update Kullanici set Para=? where Kullanici_Adi=?",("15.000", kullanici_E))
                con.commit()
                con.close()
                Label(text="15.000" + " Kazandınız Tebrikler", font="Arial 20", bg="maroon", fg="black").place(x=250,y=300)
                oyun_Ekran.update()
                sleep(3)

            oyun_Ekran.destroy()
            ana()
def cekil():

    con=sqlite3.connect("Kim milyoner olmak ister.db")
    cursor=con.cursor()
    cursor.execute("update Kullanici set Para=? where Kullanici_Adi=?", (para_liste[soru_No[0] - 1], kullanici_E))
    con.commit()
    con.close()
    Label(text=para_liste[soru_No[0] - 1] + " Kazandınız Tebrikler", font="Arial 20", bg="green3", fg="black").place(x=250, y=300)
    oyun_Ekran.update()
    sleep(2)
    oyun_Ekran.destroy()
    ana()

def soru_Sec():

    if soru_No[0]<7:
        return kolay[soru_No[0]]
    else:
        return zor[soru_No[0] - 7]

def cift_fonk():
    cift[0]=0
    global toplam_secim
    toplam_secim=[0]

    if yarı[0]==1:

        a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("A"))
        a_B.place(x=10, y=500)

        b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("B"))
        b_B.place(x=400, y=500)

        c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("C"))
        c_B.place(x=10, y=600)

        d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("D"))
        d_B.place(x=400, y=600)

    else:
        yeni = [i for i in cevap if not i in rasgele]
        if cevap[0] in yeni:
            a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("A"))
            a_B.place(x=10, y=500)
        if cevap[1] in yeni:
            b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("B"))
            b_B.place(x=400, y=500)
        if cevap[2] in yeni:
            c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("C"))
            c_B.place(x=10, y=600)
        if cevap[3] in yeni:
            d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="cyan3", fg="black",command=lambda :cift_dogrumu("D"))
            d_B.place(x=400, y=600)
    seyirci_b.destroy()
    cekil_b.destroy()
    yari_b.destroy()
    cift_b = Button(text="Çift Cevap", width=14, fg="black", bg="red4").place(x=350, y=50)

    oyun_Ekran.update()

def cift_dogrumu(yanit):
    if toplam_secim[0]==1:
        if 1 < soru_No[0] < 7:

            con = sqlite3.connect("Kim milyoner olmak ister.db")
            cursor = con.cursor()
            cursor.execute("update Kullanici set Para=? where Kullanici_Adi=?", ("1.000", kullanici_E))
            con.commit()
            con.close()
            Label(text="1.000" + " Kazandınız Tebrikler", font="Arial 20", bg="maroon", fg="black").place(x=250, y=300)
            oyun_Ekran.update()
            sleep(3)

        elif 6 < soru_No[0] < 13:

            con = sqlite3.connect("Kim milyoner olmak ister.db")
            cursor = con.cursor()
            cursor.execute("update Kullanici set Para=? where Kullanici_Adi=?", ("15.000", kullanici_E))
            con.commit()
            con.close()
            Label(text="15.000" + " Kazandınız Tebrikler", font="Arial 20", bg="maroon", fg="snow").place(x=250, y=300)
            oyun_Ekran.update()
            sleep(3)
        oyun_Ekran.destroy()
        ana()
    else:
        cevaplar = {"A": cevap[0], "B": cevap[1], "C": cevap[2], "D": cevap[3]}
        yanit_Harf=yanit
        yanit = cevaplar[yanit]
        if yanit ==sabit_Soru_Listesi[4]:
            if yanit==cevap[0]:
                a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="gray30", fg="green3").place(x=10,y=500)
            elif yanit==cevap[1]:
                b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="gray30", fg="green3").place(x=400,y=500)
            elif yanit==cevap[2]:
                c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="gray30", fg="green3").place(x=10,y=600)
            elif yanit==cevap[3]:
                d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="gray30", fg="green3").place(x=400,y=600)
            oyun_Ekran.destroy()
            basla()
        else:
            if yanit_Harf=="A":
                a_B = Button(text="A)  " + cevap[0], font="Arial 13", width=40, bg="red3", fg="snow").place(x=10,y=500)
            elif yanit_Harf=="B":
                b_B = Button(text="B)  " + cevap[1], font="Arial 13", width=40, bg="red3", fg="snow").place(x=400,y=500)
            elif yanit_Harf=="C":
                c_B = Button(text="C)  " + cevap[2], font="Arial 13", width=40, bg="red3", fg="snow").place(x=10,y=600)
            elif yanit_Harf=="D":
                d_B = Button(text="D)  " + cevap[3], font="Arial 13", width=40, bg="red3", fg="snow").place(x=400,y=600)
        toplam_secim[0]=toplam_secim[0]+1

def seyirci():


    seyir[0] = 0#fonksiyonun kullanıldığını belirlemek için true olan degeri false yapıyoruz ve basla fonksiyonunda if ile kontrol edilecek.
    kullanici_cevap = copy.deepcopy(cevap)
    kullanici_cevap.remove(sabit_Soru_Listesi[4])

    if ss[0]==0 and yarı[0]==0:

        kullanici_cevap.remove(rasgele[0])
        kullanici_cevap.remove(rasgele[1])
    seyirci_sectikleri = []

    for i in range((soru_No[0] + 1) * 6):
        seyirci_sectikleri.append(*random.choices(kullanici_cevap))

    for j in range(100 - ((soru_No[0] + 1) * 6)):
        seyirci_sectikleri.append(sabit_Soru_Listesi[4])

    A = seyirci_sectikleri.count(cevap[0])
    B = seyirci_sectikleri.count(cevap[1])
    C = seyirci_sectikleri.count(cevap[2])
    D = seyirci_sectikleri.count(cevap[3])

    Label(oyun_Ekran, text="A)  " + str(A) + "%", font="Arial 15", width=14, fg="SteelBlue1", bg="gray30").place(x=600, y=20)
    Label(oyun_Ekran, text="B)  " + str(B) + "%", font="Arial 15", width=14, fg="SteelBlue1", bg="gray30").place(x=600, y=60)
    Label(oyun_Ekran, text="C)  " + str(C) + "%", font="Arial 15", width=14, fg="SteelBlue1", bg="gray30").place(x=600, y=100)
    Label(oyun_Ekran, text="D)  " + str(D) + "%", font="Arial 15", width=14, fg="SteelBlue1", bg="gray30").place(x=600, y=140)
    seyirci_b = Button(text="Seyirci", width=14, fg="black", bg="red4")
    seyirci_b.place(x=50, y=50)
    oyun_Ekran.update()


def yarıyarıya():

    #oyun ekranındaki yarıyarıya butonuna tıkladığında doğru cevap hariç diger 3 secenekten 2sini rasgele ekrandan siliyor.
    #Sonra buton tekrar aynı soruda kullanılmasın diye butonu command siz olarak güncelleyip rengini değişririyor.
    global rasgele
    yarı[0]=0#fonksiyonun kullanıldığını belirlemek için true olan degeri false yapıyoruz ve basla fonksiyonunda if ile kontrol edilecek.
    liste=[i for i in cevap if i != sabit_Soru_Listesi[4]]
    liste_2=copy.deepcopy(liste)

    rasgele=[]
    for i in range(2):
        secilen=random.choice(liste)
        liste.remove(secilen)
        rasgele.append(secilen)

    for i in liste_2:
        if i in rasgele:

            if i==cevap[0]:
                a_B.destroy()
            if i==cevap[1]:
                b_B.destroy()
            if i==cevap[2]:
                c_B.destroy()
            if i==cevap[3]:
                d_B.destroy()
    yari_b = Button(text="Yarı Yarıya", width=14, fg="black", bg="red4")
    yari_b.place(x=200, y=50)
    oyun_Ekran.update()

def hakkinda():
    #ana Ekrandaki Hakkinda butonuna tıklandığında ana ekran kapatıp Hakkinda ekranını açıyor.
    ana_Ekran.destroy()
    global hakkinda_Ekran

    hakkinda_Ekran=Tk()
    hakkinda_Ekran.geometry("1000x700+500+200")
    hakkinda_Ekran.resizable(width=False, height=False)
    hakkinda_Ekran.title("Kim Milyoner Olamak İster? Hakkında")

    Label(text="HAKKINDA",font="Arial 25",bg="gray30",fg="SteelBlue1").place(x=300,y=10)

    hakkinda_Ekran.configure(background="gray30")

    geri_b=Button(text="GERİ",bg="gray19",fg="SteelBlue1",font="Arial 13",width=15,command=hakkindageri)
    geri_b.place(x=830,y=630)

    dosya=open("Hakkında.txt")
    dosya=dosya.read()

    text=Text(width=89,font="Arial 15",bg="gray19",fg="SteelBlue1")
    text.insert(INSERT,dosya)
    text.place(x=10,y=60)

def hakkindageri():

    hakkinda_Ekran.destroy()
    ana()

def geri():
    #Oyun ekranındaki Ana menü butonuna tıklandıgında Oyun ekranı kapatıp Ana menü ekranını açıyor.
    cevap=messagebox.askyesno("Kim mMilyoner Olmak İste?","Oyunu Bitirmek İstiyormusunuz?")
    if cevap:
        oyun_Ekran.destroy()
        ana()

def cikis():
    #Ana Ekrandaki Çıkış butonuna tıklandığında programdan komple çıkıyor.
    cevap=messagebox.askyesno("kim Milyoner Olamask İster","Oyundan çıkmak istiyormusunuz?")
    if cevap:
        ana_Ekran.destroy()

if __name__ == '__main__':

    giris()

