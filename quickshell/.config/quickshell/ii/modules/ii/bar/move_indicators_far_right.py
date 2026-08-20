path = "BarContent.qml"
with open(path, "r") as f:
    content = f.read()

# --- STEP 1: rimuovere il blocco BarGroup con i 3 indicator da dopo Weather ---
old_block_after_weather = """            // Weather
            Loader {
                Layout.leftMargin: 4
                active: Config.options.bar.weather.enable

                sourceComponent: BarGroup {
                    WeatherBar {}
                }
            }

            BarGroup {
                Layout.leftMargin: 4

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
            }
        }
    }
}"""

new_block_after_weather = """            // Weather
            Loader {
                Layout.leftMargin: 4
                active: Config.options.bar.weather.enable

                sourceComponent: BarGroup {
                    WeatherBar {}
                }
            }
        }
    }
}"""

count_1 = content.count(old_block_after_weather)
if count_1 != 1:
    print(f"ATTENZIONE STEP 1: blocco trovato {count_1} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_block_after_weather, new_block_after_weather)
    print("STEP 1 ok: rimosso il BarGroup con gli indicator da dopo Weather.")

# --- STEP 2: aggiungere i 3 indicator nudi come PRIMO elemento di rightSectionRowLayout ---
# layoutDirection è RightToLeft quindi il primo elemento scritto = più a destra visivamente
old_rowlayout_start = """        RowLayout {
            id: rightSectionRowLayout
            anchors.fill: parent
            spacing: 5
            layoutDirection: Qt.RightToLeft

            RippleButton { // Right sidebar button"""

new_rowlayout_start = """        RowLayout {
            id: rightSectionRowLayout
            anchors.fill: parent
            spacing: 5
            layoutDirection: Qt.RightToLeft

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

count_2 = content.count(old_rowlayout_start)
if count_2 != 1:
    print(f"ATTENZIONE STEP 2: blocco trovato {count_2} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_rowlayout_start, new_rowlayout_start)
    print("STEP 2 ok: indicator nudi aggiunti all'estremo destro reale dello schermo.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
