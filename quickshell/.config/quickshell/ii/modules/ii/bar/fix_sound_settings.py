path = "VolumePopup.qml"
with open(path, "r") as f:
    content = f.read()

old_line = 'onClicked: Quickshell.execDetached(["pavucontrol"])'
new_line = 'onClicked: Quickshell.execDetached(["pavucontrol-qt"])'

count = content.count(old_line)
if count != 1:
    print(f"ATTENZIONE: riga trovata {count} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_line, new_line)
    with open(path, "w") as f:
        f.write(content)
    print("OK: comando corretto in pavucontrol-qt.")
