path = "VolumePopup.qml"
with open(path, "r") as f:
    content = f.read()

old_line = '''            buttonText: Translation.tr("Sound settings")
            onClicked: Quickshell.execDetached(["pavucontrol-qt"])'''

new_line = '''            buttonText: Translation.tr("Sound settings")
            onClicked: {
                console.log("CLICK Sound settings ricevuto");
                Quickshell.execDetached(["pavucontrol-qt"]);
            }'''

count = content.count(old_line)
if count != 1:
    print(f"ATTENZIONE: blocco trovato {count} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_line, new_line)
    with open(path, "w") as f:
        f.write(content)
    print("OK: aggiunto console.log di debug. Ricordati di rilanciare 'qs -c ii' da terminale (non in background) per vedere l'output.")
