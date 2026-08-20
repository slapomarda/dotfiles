path = "NetworkPopup.qml"
with open(path, "r") as f:
    content = f.read()

changes = []

# 1) Icona header: ora dipende dal primario, non dal radio wifi on/off
old1 = '''        StyledPopupHeaderRow {
            icon: Network.wifiEnabled ? Network.materialSymbol : "lan"
            label: Translation.tr("Network")
        }'''
new1 = '''        StyledPopupHeaderRow {
            icon: Network.primaryConnection === "ethernet" ? "lan" : Network.materialSymbol
            label: Translation.tr("Network")
        }'''
changes.append((old1, new1, "icona header"))

# 2) Bottone Wi-Fi
old2 = '''            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                toggled: Network.wifiEnabled
                buttonText: Translation.tr("Wi-Fi")
                onClicked: {
                    if (!Network.wifiEnabled) Network.enableWifi(true);
                }
            }'''
new2 = '''            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                toggled: Network.primaryConnection === "wifi"
                buttonText: Translation.tr("Wi-Fi")
                onClicked: {
                    Network.setPrimaryConnection("wifi");
                }
            }'''
changes.append((old2, new2, "bottone Wi-Fi"))

# 3) Bottone Ethernet
old3 = '''            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                toggled: !Network.wifiEnabled
                buttonText: Translation.tr("Ethernet")
                onClicked: {
                    if (Network.wifiEnabled) Network.enableWifi(false);
                }
            }'''
new3 = '''            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                toggled: Network.primaryConnection === "ethernet"
                buttonText: Translation.tr("Ethernet")
                onClicked: {
                    Network.setPrimaryConnection("ethernet");
                }
            }'''
changes.append((old3, new3, "bottone Ethernet"))

# 4) Riga di stato ethernet: visibile solo quando ethernet e' il primario (il wifi resta sempre acceso ora)
old4 = '''        StyledPopupValueRow {
            visible: !Network.wifiEnabled
            icon: "lan"
            label: Translation.tr("Status:")
            value: Network.ethernet ? Translation.tr("Connected") : Translation.tr("Cable not detected")
        }'''
new4 = '''        StyledPopupValueRow {
            visible: Network.primaryConnection === "ethernet"
            icon: "lan"
            label: Translation.tr("Status:")
            value: Network.ethernet ? Translation.tr("Connected") : Translation.tr("Cable not detected")
        }'''
changes.append((old4, new4, "riga stato ethernet"))

# 5) Separatore e lista reti: ora sempre visibili se il wifi e' fisicamente acceso (radio), non legati al "primario"
old5 = '''        Rectangle {
            visible: Network.wifiEnabled
            Layout.fillWidth: true
            height: 1
            color: Appearance.colors.colLayer0Border
            Layout.topMargin: 4
            Layout.bottomMargin: 4
        }'''
new5 = '''        Rectangle {
            visible: true
            Layout.fillWidth: true
            height: 1
            color: Appearance.colors.colLayer0Border
            Layout.topMargin: 4
            Layout.bottomMargin: 4
        }'''
changes.append((old5, new5, "separatore lista reti"))

old6 = '''        StyledText {
            visible: Network.wifiEnabled
            text: Translation.tr("Networks")
            font.pixelSize: 12
            color: Appearance.colors.colOnSecondaryContainer
        }

        ColumnLayout {
            visible: Network.wifiEnabled'''
new6 = '''        StyledText {
            visible: true
            text: Translation.tr("Networks")
            font.pixelSize: 12
            color: Appearance.colors.colOnSecondaryContainer
        }

        ColumnLayout {
            visible: true'''
changes.append((old6, new6, "visibilita' lista reti"))

ok = True
for old, new, label in changes:
    count = content.count(old)
    if count != 1:
        print(f"ATTENZIONE: blocco '{label}' trovato {count} volte (atteso 1). Nessuna modifica per questo blocco.")
        ok = False
        continue
    content = content.replace(old, new)
    print(f"OK: applicato '{label}'.")

with open(path, "w") as f:
    f.write(content)

if ok:
    print("Tutte le modifiche applicate correttamente.")
else:
    print("Alcune modifiche NON sono state applicate, controlla i messaggi sopra prima di committare.")
