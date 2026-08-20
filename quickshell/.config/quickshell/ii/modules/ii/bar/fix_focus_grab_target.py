path = "VolumeIndicator.qml"
with open(path, "r") as f:
    content = f.read()

old_block = """    onIsPopupOpenChanged: {
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

new_block = """    onIsPopupOpenChanged: {
        if (isPopupOpen) {
            // Aspettiamo che il LazyLoader abbia istanziato il PanelWindow
            Qt.callLater(() => {
                if (volumePopup.item) {
                    GlobalFocusGrab.addDismissable(volumePopup.item);
                }
            });
        } else {
            if (volumePopup.item) {
                GlobalFocusGrab.removeDismissable(volumePopup.item);
            }
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
    print("OK: ora registriamo volumePopup.item (la finestra reale) come dismissable, non l'icona.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
