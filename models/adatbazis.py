import mysql.connector

class Adatbazis:
    def __init__(self, config_file):
        """
        Megnyitja és beolvassa a konfigurációs fájlból a MySQL/MariaDB
        szerveren lévő adatbázis eléréséhez szükséges adatokat. 
        Ha nem sikerül, akkor kilép.

        Paraméter
            config_file: ebből olvassa be a kapcsolódáshoz szükséges
                         összes adatot
        """

        # Adatbázis megnyitása (open_connection()) során kapnak értéket
        self.connection = None
        self.cursor = None

        # Adatbázis eléréséhez szükséges adatok. Egy sor = egy adat.
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                self.host = f.readline().replace("\n", "")
                self.database = f.readline().replace("\n", "")
                self.user = f.readline().replace("\n", "")
                self.password = f.readline().replace("\n", "")
        except FileNotFoundError:
            print(f"Hiányzó konfigurációs fájl: {config_file}")
            exit()
        except Exception as e:
            print("Hiba: ", e)    
            exit()

    def kapcsolat_megnyitasa(self):
        """
        A már beolvasott adatok alapján kapcsolódik az adatbázishoz.
        A self.cursor ezután már használható.
        
        Visszaadott érték:
            True:  sikerült a kapcsolódás
            False: nem sikerült kapcsolódni az adatbázishoz
        """
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )
            self.cursor = self.connection.cursor()
            return True
        except mysql.connector.errors.ProgrammingError:
            print(f"Hiba: Az adatbázisnév - felhasználónév - jelszó kombinácó hibás. (host: {self.host}, adatbázis: {self.database})")
        except mysql.connector.errors.DatabaseError:
            print(f"Hiba: Nem sikerült kapcsolódni a szerverhez: host: {self.host}")
        except Exception as e:
            print("Hiba:", e)

        return False

    def kapcsolat_bezarasa(self):
        """
        Amennyiben az adatbázishoz a kapcsolat nyitva van, bezárja.
        """
        if self.connection:
            self.connection.close()

    def tablak_neve(self):
        """
        Beolvassa és visszaadja az adatbázisból a benne lévő táblák nevét.
        A táblák neve stringeket tartalmazó listában van.
        None, ha nem sikerült a beolvasás.
        """
        table_name_list = None
        try:
            if not self.kapcsolat_megnyitasa():
                return None

            self.cursor.execute("SHOW TABLES;")
            # list of tuples formában adja vissza
            table_names = self.cursor.fetchall()
            table_name_list = []
            for name in table_names:
                table_name_list.append(list(name)[0])    
        except Exception as e:
            print("Hiba:", e)
        finally:
            self.kapcsolat_bezarasa()

        return table_name_list


    def tabla_tartalma(self, tabla_neve):
        """
        A már megnyitott adatbázisból beolvassa a tábla összes sorát, 
        és visszaadja lista formában.
        A lista egy eleme = a tábla egy sora.

        Paraméterek:
            tabla_neve: ennek a táblának a tartalmát adja vissza
        """
        beolvasott_sorok = None
        try:
            if not self.kapcsolat_megnyitasa():
                return None

            self.cursor.execute(f"SELECT * FROM {tabla_neve}")
            beolvasott_sorok = self.cursor.fetchall()
        except Exception as e:
            print("Hiba:", e)
        finally:
            self.kapcsolat_bezarasa()
        return beolvasott_sorok