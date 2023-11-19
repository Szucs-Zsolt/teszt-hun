## MySQL adatbázisban lévő táblák tartalmának lementése csv formában

A program miután kapcsolódott az adatbázishoz megjeleníti az abban lévő táblákat.
Ki lehet választani, hogy ezekből melyikeket írja ki csv formában.
Minden kiválaszott táblát azonos nevű csv fájlként ír ki a munkakönyvtárba.

# A telepítés lépései
1. A helyi gépre tükrözzük a repository-t.
```
git clone https://github.com/Szucs-Zsolt/teszt-hun.git
```

2. Kialakítjuk a futtatásához szükséges virtuális környezetet. 
- a program Python 3.9 verzióját használja 
- a telepítendő modulok a requirements.txt fájlban vannak.
(mysql-connector-python==8.2.0, numpy==1.26.2, Pillow==10.1.0, protobuf==4.21.12, six==1.16.0, wxPython==4.2.1)
```
    cd teszt-hun
    py -3.9 -m venv venv
    .\venv\Scripts\activate
    python -m pip install -r requirements.txt	
```

3. Az adatbázishoz való kapcsolódáshoz szükséges adatok a .\config\mysql_connection.cfg fájlba kerülnek. A szükséges adatok:
- Első sor    : szerver IP címe
- Második sor : az adatbázis neve, amihez kapcsolódni szeretnénk
- Harmadik sor: a felhasználó neve
- Negyedik sor: a felhasználó jelszava

Példa a .\config\mysql_connection.cfg fájl tartalmára
```
192.168.0.120
adatbazis_neve
user_neve
jelszo
```
4. A program elindítása után azonnal csatlakozik az adatbázishoz, megjeleníti az elérhető táblákat.
```
    python main.py
```
- Az első oszlop pipálható, itt lehet kiválasztani, hogy melyik táblát kívánjuk lementeni csv formában.
- A második oszlopban látható a tábla neve.
- A lementéshez szükséges gomb az ablak alján van, és a megrendelő írásbeli kérésének megfelelően a 'Save' felirattal rendelkezik.
- A lementett csv fájlok a program munkakönyvtárába kerülnek. Egy tábla tartalma egy CSV fájlba kerül, a fájl neve a tábla neve, CSV kiterjesztéssel.


## A program fejlesztése során használt szerver jellemzői: 
----------------------------------------------------------
- Debian: debian 6.1.0-12-amd64
- MySQL/MariaDB: mariadb  Ver 15.1 Distrib 10.11.4-MariaDB

5) Az adatbázis létrehozása során használt parancsok
----------------------------------------------------
```
    sudo apt update
    sudo apt install mariadb-server

    sudo mysql -u root -p
	
    CREATE DATABASE teszt;
    SHOW DATABASES;
    CREATE TABLE teszt.alkalmazott (
        alkalmazott_id  INTEGER  PRIMARY KEY  AUTO_INCREMENT,
 	nev VARCHAR(80),
	kor INTEGER
    );
    USE teszt;
    SHOW TABLES;
    DESC teszt.alkalmazott;
	
    INSERT INTO teszt.alkalmazott (nev, kor) VALUES ("Kovács János", 30);
    INSERT INTO teszt.alkalmazott (nev, kor) VALUES ("Gipsz Jakab", 31);
    SELECT * FROM teszt.alkalmazott;

    CREATE TABLE teszt.gyumolcs (
        gyumolcs_id INTEGER  PRIMARY KEY  AUTO_INCREMENT,
	nev VARCHAR(60),
	mennyiseg INTEGER);
    INSERT INTO teszt.gyumolcs (nev, mennyiseg) values ("alma", 1);
    INSERT INTO teszt.gyumolcs (nev, mennyiseg) values ("barack", 2);
    INSERT INTO teszt.gyumolcs (nev, mennyiseg) values ("citrom", 3);
    INSERT INTO teszt.gyumolcs (nev, mennyiseg) values ("dió", 4);
    INSERT INTO teszt.gyumolcs (nev, mennyiseg) values ("eper", 5);
    SELECT *  FROM teszt.gyumolcs;
```
6) Felhasználó létrehozása (csak olvasási jogot kap a teszt adatbázis összes táblájára)
---------------------------------------------------------------------------------------

    CREATE USER 'teszt_user'@'%'   IDENTIFIED BY 'teszt_jelszó';

    SELECT user,host FROM mysql.user;

    GRANT SELECT ON teszt.*   TO 'teszt_user'@'%'
    SHOW GRANTS FOR 'teszt_user'@'%';

    EXIT;	


7) A szerver konfigurációját megváltoztattuk (Alapesetben csak localhost-ról engedne belépni.)
----------------------------------------------------------------------------------------------
```
    sudo vim /etc/mysql/my.cnf
        [mysqld]
            bind-address = 0.0.0.0
```

Szerver újraindítása:
```
    sudo systemctl restart mariadb
```

Mivel ez a konfiguráció ezután mindenhonnan engedélyezi az adatbázis elérését, ezért feltételezzük, hogy a bejövő kapcsolatokat más módon már szűrtük IP címre / MAC addressre.