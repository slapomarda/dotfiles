path = "BarContent.qml"
with open(path, "r") as f:
    content = f.read()

old_block = """            NetworkIndicator {
                Layout.alignment: Qt.AlignVCenter
            }

            BluetoothIndicator {
                visible: BluetoothStatus.available
                Layout.alignment: Qt.AlignVCenter
            }

            VolumeIndicator {
                Layout.alignment: Qt.AlignVCenter
            }

            RippleButton { // Right sidebar button"""

new_block = """            Item {
                // Spacer to keep the indicators away from the screen edge
                implicitWidth: Appearance.rounding.screenRounding
            }

            NetworkIndicator {
                Layout.alignment: Qt.AlignVCenter
            }

            BluetoothIndicator {
                visible: BluetoothStatus.available
                Layout.alignment: Qt.AlignVCenter
            }

            VolumeIndicator {
                Layout.alignment: Qt.AlignVCenter
            }

            RippleButton { // Right sidebar button"""

count = content.count(old_block)
if count != 1:
    print(f"ATTENZIONE: blocco trovato {count} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_block, new_block)
    print("OK: aggiunto spacer/padding a destra degli indicator.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
