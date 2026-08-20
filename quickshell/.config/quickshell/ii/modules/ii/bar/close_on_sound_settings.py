path = "VolumePopup.qml"
with open(path, "r") as f:
    content = f.read()

old_line = '''            buttonText: Translation.tr("Sound settings")
            onClicked: Quickshell.execDetached(["pavucontrol-qt"])'''

new_line = '''            buttonText: Translation.tr("Sound settings")
            onClicked: {
                Quickshell.execDetached(["pavucontrol-qt"]);
                GlobalFocusGrab.dismiss();
            }'''

count = content.count(old_line)
if count != 1:
    print(f"ATTENZIONE: blocco trovato {count} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_line, new_line)
    print("OK: bottone Sound settings ora chiude anche il popup.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
