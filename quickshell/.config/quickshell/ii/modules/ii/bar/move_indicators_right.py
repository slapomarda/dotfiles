path = "BarContent.qml"
with open(path, "r") as f:
    content = f.read()

# --- STEP 1: rimuovere i 3 indicator dal centro (rightCenterGroupContent) ---
old_center_block = """                NetworkIndicator {
                    visible: root.useShortenedForm < 2
                    Layout.alignment: Qt.AlignVCenter
                }

                BluetoothIndicator {
                    visible: (root.useShortenedForm < 2 && BluetoothStatus.available)
                    Layout.alignment: Qt.AlignVCenter
                }

                VolumeIndicator {
                    visible: root.useShortenedForm < 2
                    Layout.alignment: Qt.AlignVCenter
                }

                BatteryIndicator {"""

new_center_block = """                BatteryIndicator {"""

count_1 = content.count(old_center_block)
if count_1 != 1:
    print(f"ATTENZIONE STEP 1: blocco trovato {count_1} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_center_block, new_center_block)
    print("STEP 1 ok: indicator rimossi dal centro.")

# --- STEP 2: aggiungere i 3 indicator dopo il blocco Weather, in fondo a destra ---
old_right_block = """            // Weather
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

new_right_block = """            // Weather
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

count_2 = content.count(old_right_block)
if count_2 != 1:
    print(f"ATTENZIONE STEP 2: blocco trovato {count_2} volte (atteso 1). Nessuna modifica applicata.")
else:
    content = content.replace(old_right_block, new_right_block)
    print("STEP 2 ok: indicator aggiunti dopo Weather, in fondo a destra.")

with open(path, "w") as f:
    f.write(content)

print("File salvato.")
