import peewee as pw

db = pw.SqliteDatabase("kitaplik.db")

class Modelimiz(pw.Model):
    class Meta:
        database = db
        legacy_table_names = False

class Kitap(Modelimiz):
    isim = pw.CharField(max_length=250, null=False, unique=True)

class Okuyucu(Modelimiz):
    isim = pw.CharField(max_length=250, null=False, unique=True)
    kitaplar = pw.ManyToManyField(Kitap, backref="okuyucular")
    
OkunanKitap = Okuyucu.kitaplar.get_through_model()


db.create_tables([
    Kitap,
    Okuyucu,
    OkunanKitap
])
