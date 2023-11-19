import wx
from models.adatbazis import Adatbazis
from models.csv_kezelo import csv_kiiro
from views.foablak import Foablak

# Az adatbáziskezelő a konfigurációs fájlból betölti a kapcsolat adatait
db = Adatbazis(config_file=".\\config\\mysql_connection.cfg")

app = wx.App()
foablak = Foablak("MySQL - CSV lementés", db)
app.MainLoop()