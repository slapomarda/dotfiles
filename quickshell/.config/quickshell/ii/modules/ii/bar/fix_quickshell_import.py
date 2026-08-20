path = "VolumePopup.qml"
with open(path, "r") as f:
    content = f.read()

# Fix 1: aggiungere l'import mancante
old_imports = """import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls"""

new_imports = """import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import Quickshell"""

count_1 = content.count(old_imports)
if count_1 != 1:
    print(f"ATTENZIONE fix import: blocco trovato {count_1} volte (atteso 1). Nessuna modifica applicata per gli import.")
else:
    content = content.replace(old_imports, new_imports)
    print("OK: import Quickshell aggiunto.")

# Fix 2: rimuovere il console.log di debug, tornare alla chiamata diretta
old_debug = '''            buttonText: Translation.tr("Sound settings")
            onClicked: {
                console.log("CLICK Sound settings ricevuto");
                Quickshell.execDetached(["pavucontrol-qt"]);
            }'''

new_clean = '''            buttonText: Translation.tr("Sound settings")
            onClicked: Quickshell.execDetached(["pavucontrol-qt"])'''

count_2 = content.count(old_debug)
if count_2 != 1:
    print(f"ATTENZIONE fix debug: blocco trovato {count_2} volte (atteso 1). Nessuna modifica applicata per la rimozione del debug.")
else:
    content = content.replace(old_debug, new_clean)
    print("OK: rimosso console.log di debug, ripristinata chiamata pulita.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
