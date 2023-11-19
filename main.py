"""
A program csatlakozik egy adatbázishoz. Az ehhez szükséges
adatokat a konfigurációs fájljából veszi.
Ezután kiírja a táblák nevét, amik kijelölhetők.
A kijelölt táblák tartalmát csv fájlokba menti.
"""

import wx
from models.adatbazis import Adatbazis
from models.csv_kezelo import csv_kiiro
from views.foablak import Foablak

if __name__=="__main__":
    # Az adatbáziskezelő a konfigurációs fájlból betölti a kapcsolat adatait
    db = Adatbazis(config_file=".\\config\\mysql_connection.cfg")

    app = wx.App()
    foablak = Foablak("MySQL - CSV lementés", db)
    app.MainLoop()