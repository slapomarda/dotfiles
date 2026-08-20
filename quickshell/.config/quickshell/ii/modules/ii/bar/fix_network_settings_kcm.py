path = "NetworkPopup.qml"
with open(path, "r") as f:
    content = f.read()

old_block = '''            onClicked: {
                Quickshell.execDetached(["kitty", "nmtui"]);
                GlobalFocusGrab.dismiss();
            }'''

new_block = '''            onClicked: {
                Quickshell.execDetached(["kcmshell6", "kcm_networkmanagement"]);
                GlobalFocusGrab.dismiss();
            }'''

count = content.count(old_block)
if count != 1:
    print(f"ATTENZIONE: blocco trovato {count} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_block, new_block)
    print("OK: Network settings ora apre kcmshell6 kcm_networkmanagement.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
