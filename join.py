import peewee as pw
import datetime
from models import Modelimiz, Kitap, Okuyucu, OkunanKitap

class Yazar(Modelimiz):
    isim = pw.CharField(unique=True)
    yas = pw.IntegerField(default=None, null=True)

class KitapDetay(Modelimiz):
    kitap = pw.ForeignKeyField(Kitap, backref="kitaplar", primary_key=True)
    yazar = pw.ForeignKeyField(Yazar, backref="yazarlar")
    tarih = pw.DateField(default=datetime.datetime.now())
    fiyat = pw.FloatField(default=0.0)


def tablolari_olustur():
    import models
    models.db.create_tables([
        Yazar,
        KitapDetay
    ])

def create():
    yazarlar = [("Ahmet Mithat", 68),
                ("Jack London", 40),
                ("Alper Bilgili,", 50),
                ("Agatha Christie", 85),
                ("Jo-Ellan Dimitrius", None)]
    Yazar.insert_many(yazarlar, fields=[Yazar.isim, Yazar.yas]).execute()

    kitaplar = ['Mu','Ma','Bi','Cin','İn']
    yazarlar = ['Ahm','Ja','Al','Ag','Jo']
    tarihler = [datetime.date(2022,1,1), '2022-10-01', '2002-01-25', '2008-10-17', '2022-11-11']
    fiyatlar = [30.00, 50.00, 39.60, 25.00, 54.90]

    veriler = []
    index = 0
    for kitap in kitaplar:
        kitap = Kitap.get(Kitap.isim.contains(kitap))
        
        yazar = yazarlar[index]
        yazar = Yazar.select().where(Yazar.isim.contains(yazar)).get()
        
        tarih = tarihler[index]
        fiyat = fiyatlar[index]

        veriler.append({"kitap": kitap, "yazar": yazar, "tarih": tarih, "fiyat": fiyat})
        
        index += 1
    
    KitapDetay.insert_many(veriler).execute()

def read():
    kitaplar = (KitapDetay
                .select(Kitap.isim,
                        Yazar.isim.alias("yazar"),
                        KitapDetay.tarih,
                        KitapDetay.fiyat)
                .join(Kitap)
                .switch(KitapDetay)
                .join(Yazar)
                # .where().where().or_where()
                .order_by(KitapDetay.tarih.desc())) # limit() | distinct()
                
    for kitap in kitaplar.dicts(): # tuples() | namedtuples()
        print(kitap)
        # tarih.day | tarih.month | tarih.year

    miktar = pw.fn.COUNT(OkunanKitap.kitap_id).alias("okunan_miktar")
    birlesik = Okuyucu.isim.concat("+").concat(Kitap.isim).alias("birlesik")
    # model_name = Model.alias("")
    
    okuyucular = (Okuyucu
                  .select(Okuyucu.isim, miktar, birlesik)
                  .join(OkunanKitap, pw.JOIN.LEFT_OUTER,
                        on=(Okuyucu.id == OkunanKitap.okuyucu_id))
                  .join(Kitap, pw.JOIN.LEFT_OUTER,
                        on=(Kitap.id == OkunanKitap.kitap_id))
                  .group_by(Okuyucu.id)
                  .order_by(Okuyucu.isim, miktar))

    for okuyucu in okuyucular.objects():
        print("Okuyucu:", okuyucu.isim,
              "\n| Okuduğu miktar:", okuyucu.okunan_miktar,
              "\n| Birleşik kolon:", okuyucu.birlesik)

#tablolari_olustur()
#create()
read()
