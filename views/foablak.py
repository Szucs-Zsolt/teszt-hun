import wx
import wx.grid
from models.adatbazis import Adatbazis
from models.csv_kezelo import csv_kiiro

class Foablak(wx.Frame):
    """
    GUI létrehozása és megjelenítése: 
      - Az adatbázisok nevét tartalmazó ablak, azok kiváláasztását lehetővé tévő mező.
      - Konvertálást elindító gomb.
    Controller:
      - Ez a class controllerként is működik, mivel összekapcsolja az adatbázist
        (beolvassa belőle a táblák tartalmát) és a metódust, ami ez alapján kiírja
        csv formában. 
    """

    def __init__(self, title, db):
        """
        A GUI Megkapja az adatbázis eléréséhez szükséges objectet és lekérdezi a 
	táblák nevét.

        Paraméterek
            title:       ablak neve
            db:          kapcsolat az adatbázishoz 
        """
        super().__init__(parent=None, title=title, size=(800,600))

        # Az adatbázisból lekérdezzük a táblák nevét
        self.db = db
        tablak_neve = db.tablak_neve()
        if (tablak_neve is None):
            print("Nem sikerült a táblák nevét beolvasni")
            exit()

        # GUI elkészítése
        self.panel = wx.Panel(self)
        font = self.panel.GetFont()
        font.SetPointSize(18)
        self.panel.SetFont(font)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # 1. elem - fejléc felirata
        felirat = wx.StaticText(self.panel, label="Adatbázis tábláinak lementése CSV formában")

        # 2. elem - tábla (grid) létrehozása
        # Tábla általános kinézete
        self.tabla = wx.grid.Grid(self.panel)
        self.tabla.CreateGrid(len(tablak_neve) ,2)
        self.tabla.SetColLabelValue(0, "Lementés")
        self.tabla.SetColLabelValue(1, "Tábla neve")
        self.tabla.SetSelectionMode(wx.grid.Grid.GridSelectNone)
        self.tabla.SetColSize(1, 580)

        # Tábla első oszlop pipálható
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellBoolEditor())
        attr.SetRenderer(wx.grid.GridCellBoolRenderer())
        self.tabla.SetColAttr(0, attr)

        # Tábla feltöltése tartalommal
        for i in range(len(tablak_neve)):
            self.tabla.SetCellValue(i, 1, tablak_neve[i])
            self.tabla.SetReadOnly(i, 1, True)

        # 3. elem - gomb (a leírásban kifejezetten azt kérték, hogy a felirata 'Save' legyen)
        self.konvertalas_button = wx.Button(self.panel, label="Save")
        
        # Elrendezése: az üresen maradó helyet a tábla teljesen kitölti
        self.sizer.Add(felirat, proportion=0, flag=wx.ALIGN_CENTER | wx.BOTTOM | wx.TOP, border=20)
        self.sizer.Add(self.tabla, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border = 20)
        self.sizer.Add(self.konvertalas_button, proportion=0, flag= wx.EXPAND | wx.RIGHT | wx.BOTTOM, border=20)
        

        # Gomblenyomás esetén meghívjuk a konvertáló metódust
        self.panel.Bind(event=wx.EVT_BUTTON, source=self.konvertalas_button, handler=self.konvertalas_button_handler)
        # Panel cellára való kattintás azonnal kijelöli a check boxot
        self.tabla.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.tabla_kattintas_handler)

        self.panel.SetSizer(self.sizer)

        self.Center()
        self.Show()

    def konvertalas_button_handler(self, event):
        """
        Beolvassa bejelölt táblák a tartalmát és egyenként kiírja csv formában.
        """
        sikerult = True
        for i in range(self.tabla.GetNumberRows()):
            # A bejelölt sorokból kiolvassa a tábla nevét
            if (self.tabla.GetCellValue(i,0)=="1"):
                tabla_neve = self.tabla.GetCellValue(i,1)
                sorok =  self.db.tabla_tartalma(tabla_neve)
                if sorok is None:
                    self.uzenet_hiba("Nem sikerült beolvasni a kijelölt táblák tartalmát.", "Hiba")
                    return
                
                tabla_kiirva = csv_kiiro(file_neve=tabla_neve+".csv", sorok=sorok)
                if tabla_kiirva:
                    self.tabla.SetCellValue(i,0,"")

                sikerult = sikerult and tabla_kiirva

        if sikerult:
            self.uzenet_ok("A kijelölt táblák kiírva csv formában.", "Sikerült")
        else:                    
            self.uzenet_hiba("Nem sikerült a táblákat kiírni csv formában.", "Hiba")

    def tabla_kattintas_handler(self, event):
        """
        Checkboxok ki/bejelölése egyetlen kattintással lehetséges, nem
        kell kétszer kattintani (1. cella aktív legye, 2. kijelölje)
        """
        sor = event.GetRow()
        oszlop = event.GetCol()
        if oszlop == 0:
            self.tabla.SetGridCursor(sor, oszlop)
            if self.tabla.GetCellValue(sor, oszlop) == "1":
                self.tabla.SetCellValue(sor, oszlop, "")
            else:
                self.tabla.SetCellValue(sor, oszlop, "1")


    def uzenet_hiba(self, msg, title):
        """
        Hibaüzenet kiírása
        """
        wx.MessageBox(msg, title, wx.OK | wx.ICON_ERROR)


    def uzenet_ok(self, msg, title):
        """
        Tájékoztató üzenet kiírása
        """
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

        
