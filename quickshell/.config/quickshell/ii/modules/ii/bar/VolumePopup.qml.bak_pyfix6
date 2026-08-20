import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import Quickshell

StyledPopup {
    id: root

    ColumnLayout {
        id: columnLayout
        anchors.centerIn: parent
        spacing: 8

        StyledPopupHeaderRow {
            icon: "volume_up"
            label: Translation.tr("Volume")
        }

        // --- 1. SLIDER VOLUME PRINCIPALE ---
        RowLayout {
            Layout.fillWidth: true
            Layout.minimumWidth: 240
            spacing: 8

            StyledSlider {
                id: volumeSlider
                Layout.fillWidth: true
                configuration: StyledSlider.Configuration.M
                stopIndicatorValues: []
                value: Audio.sink?.audio?.volume ?? 0
                onMoved: {
                    Audio.sink.audio.volume = value;
                }

                MaterialSymbol {
                    property bool nearFull: volumeSlider.value >= 0.9
                    anchors {
                        verticalCenter: volumeSlider.verticalCenter
                        right: nearFull ? volumeSlider.handle.right : volumeSlider.right
                        rightMargin: nearFull ? 14 : 8
                    }
                    iconSize: 20
                    color: nearFull ? Appearance.colors.colOnPrimary : Appearance.colors.colOnSecondaryContainer
                    text: (Audio.sink?.audio?.muted ?? false) ? "volume_off" : "volume_up"

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: Audio.toggleMute()
                    }
                }
            }

            StyledText {
                Layout.alignment: Qt.AlignVCenter
                text: `${Math.round(Audio.value * 100)}%`
            }
        }

        // --- SEPARATORE ---
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Appearance.colors.colLayer0Border
            Layout.topMargin: 4
            Layout.bottomMargin: 4
        }

        // --- 2. SWITCH MICROFONO ---
        RowLayout {
            visible: Audio.source !== null
            Layout.fillWidth: true
            spacing: 12

            MaterialSymbol {
                text: (Audio.source?.audio?.muted ?? false) ? "mic_off" : "mic"
                iconSize: 20
                color: Appearance.colors.colOnLayer1
            }

            StyledText {
                text: Translation.tr("Microfono")
                Layout.fillWidth: true
                color: Appearance.colors.colOnLayer1
            }

            Switch {
                checked: !(Audio.source?.audio?.muted ?? false)
                onClicked: {
                    Audio.toggleMicMute()
                }
            }
        }

        // --- SEPARATORE ---
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Appearance.colors.colLayer0Border
            Layout.topMargin: 4
            Layout.bottomMargin: 4
        }

        // --- 3. SELETTORE USCITE AUDIO ---
        StyledText {
            text: "Uscite Audio"
            font.pixelSize: 12
            color: Appearance.colors.colOnSecondaryContainer
        }

        // Usa la lista filtrata per gli output
        Repeater {
            model: Audio.outputDevices 
            delegate: Rectangle {
                Layout.fillWidth: true
                height: 36
                radius: Appearance.rounding.small
                
                // Evidenzia se è il dispositivo attualmente attivo
                color: (Audio.sink && Audio.sink.id === modelData.id) ? Appearance.colors.colLayer1 : "transparent"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 8

                    MaterialSymbol {
                        text: "speaker"
                        iconSize: 18
                        color: Appearance.colors.colOnLayer1
                    }

                    StyledText {
                        // Usa la funzione nativa del tema per mostrare il nome pulito
                        text: Audio.friendlyDeviceName(modelData)
                        Layout.fillWidth: true
                        elide: Text.ElideRight
                        color: Appearance.colors.colOnLayer1
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        // Usa la funzione nativa del tema per cambiare output
                        Audio.setDefaultSink(modelData)
                    }
                }
            }
        }

        // --- 4. PULSANTE IMPOSTAZIONI ---
        RippleButton {
            Layout.topMargin: 8
            Layout.fillWidth: true
            implicitHeight: 36
            buttonRadius: Appearance.rounding.normal
            buttonText: Translation.tr("Sound settings")
            onClicked: {
                Quickshell.execDetached(["pavucontrol-qt"]);
                GlobalFocusGrab.dismiss();
            }
        }
    }
}
