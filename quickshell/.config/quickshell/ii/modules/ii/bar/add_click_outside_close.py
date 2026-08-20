path = "VolumeIndicator.qml"
with open(path, "r") as f:
    content = f.read()

# Aggiungere import qs.services se manca (per GlobalFocusGrab)
if "import qs.services" not in content:
    content = content.replace(
        "import qs.modules.common\n",
        "import qs.modules.common\nimport qs.services\n",
        1
    )
    print("OK: import qs.services aggiunto.")
else:
    print("import qs.services già presente, nessuna modifica agli import.")

old_block = """    // Toggle al click
    onClicked: {
        isPopupOpen = !isPopupOpen
    }"""

new_block = """    // Toggle al click
    onClicked: {
        isPopupOpen = !isPopupOpen
    }

    onIsPopupOpenChanged: {
        if (isPopupOpen) {
            GlobalFocusGrab.addDismissable(root);
        } else {
            GlobalFocusGrab.removeDismissable(root);
        }
    }

    Connections {
        target: GlobalFocusGrab
        function onDismissed() {
            root.isPopupOpen = false;
        }
    }"""

count = content.count(old_block)
if count != 1:
    print(f"ATTENZIONE: blocco trovato {count} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_block, new_block)
    print("OK: aggiunta logica di chiusura al click esterno (GlobalFocusGrab).")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
