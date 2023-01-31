import peewee as pw
from models import Kitap, Okuyucu

def create():
    k1 = Kitap(isim="Martin Eden")
    k1.save()

    o1 = Okuyucu.create(isim="Abdullah")
    o1.kitaplar.add(k1)

    kitap_id = Kitap.insert(isim="Cinayet Alfabesi").execute()

    k2 = Kitap.get(Kitap.id == kitap_id)
    k2.okuyucular.add(o1)

def read():
    print("KİTAP LİSTESİ")
    
    kitaplar = Kitap.select()
    # kitaplar.count | len(kitaplar)
    # Kitaplar.sql()

    for kitap in kitaplar:
        
        print(kitap.id, kitap.isim)
        
        print("Kitabı okuyanlar:")
        
        for okuyucu in kitap.okuyucular:
            print(okuyucu.isim)
        
        print("----------------")

    print("OKUYUCU LİSTESİ")
    for okuyucu in Okuyucu.select():
        print(okuyucu.isim,
              "| Kitap sayısı:", okuyucu.kitaplar.count())
    
def update():
    martin_eden = Kitap.get(Kitap.isim == "Martin Eden")
    
    martin_eden.isim = "Martin Ede"
    martin_eden.save()
    print(martin_eden.isim)

    Kitap.update(isim="Martin Eden").where(Kitap.id == martin_eden.id).execute()
    
    martin_eden = Kitap.get(Kitap.id == martin_eden.id)
    print(martin_eden.isim)
    
def multi_create():
    veriler = [("Musullu Süleyman",),
               ("İsimsiz",),
               ("İnsanları Okumak",),
               ("Bilim Ne değildir?",)]
    Kitap.insert_many(veriler, fields=[Kitap.isim]).execute()

    veriler = [{"isim": "İsimsiz"},
               {"isim": "Sefa"}]
    Okuyucu.insert_many(veriler).execute()

    isimsiz = Okuyucu.get(Okuyucu.isim.contains("siz"))
    abdullah = Okuyucu.get(Okuyucu.isim.startswith("A"))
    sefa = Okuyucu.get(Okuyucu.isim.endswith("fa"))
    # between(), in_(), not_in(), ...

    aranacaklar = ["siz", "mus", "oku", "bil"]
    okuyucular = [isimsiz, [abdullah, sefa], abdullah, [abdullah, sefa]]

    index = 0
    for aranan in aranacaklar:
        kitap = Kitap.get(Kitap.isim.contains(aranan))
        okuyucu = okuyucular[index]
        
        if type(okuyucu) == list:
            for _okuyucu in okuyucu:
                kitap.okuyucular.add(_okuyucu)
        else:
            kitap.okuyucular.add(okuyucu)
        
        index += 1
    
def delete():
    kitap = Kitap.get(Kitap.isim == "İsimsiz")
    okuyucu = Okuyucu.get(Okuyucu.isim == "İsimsiz")
    
    okuyucu.kitaplar.remove(kitap)
    # kitap.okuyucular.remove(okuyucu)
    # .clear()

    kitap.delete_instance()
    Okuyucu.delete().where(Okuyucu.id == okuyucu.id).execute()


#create()
read()
#update()
#multi_create()
#delete()