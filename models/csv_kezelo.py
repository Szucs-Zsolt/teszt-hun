import csv

def csv_kiiro(file_neve, sorok):
    """
    Kiírja a kapott sorok tartalmát fájlba, csv formában.
    True: ha sikerült a kiírás
    False: ha hiba volt

    Paraméterek:
        file_neve: ebbe a fájlba írja ki
        sorok: ezeket a sorokat (stringeket tartalmazó list)
    """
    try:
        with open(file_neve, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for sor in sorok:
                writer.writerow(sor)
            return True    
    except Exception as e:
        return False