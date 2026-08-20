import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import Quickshell

StyledPopup {
    id: root

    ColumnLayout {
        id: columnLayout
        anchors.centerIn: parent
        spacing: 8

        StyledPopupHeaderRow {
            icon: Network.wifiEnabled ? Network.materialSymbol : "lan"
            label: Translation.tr("Network")
        }

        // --- TOGGLE WIFI / ETHERNET ---
        RowLayout {
            Layout.fillWidth: true
            Layout.minimumWidth: 260
            spacing: 8

            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                toggled: Network.wifiEnabled
                buttonText: Translation.tr("Wi-Fi")
                onClicked: {
                    if (!Network.wifiEnabled) Network.enableWifi(true);
                }
            }

            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                toggled: !Network.wifiEnabled
                buttonText: Translation.tr("Ethernet")
                onClicked: {
                    if (Network.wifiEnabled) Network.enableWifi(false);
                }
            }
        }

        StyledPopupValueRow {
            visible: !Network.wifiEnabled
            icon: "lan"
            label: Translation.tr("Status:")
            value: Network.ethernet ? Translation.tr("Connected") : Translation.tr("Cable not detected")
        }

        // --- SEPARATORE ---
        Rectangle {
            visible: Network.wifiEnabled
            Layout.fillWidth: true
            height: 1
            color: Appearance.colors.colLayer0Border
            Layout.topMargin: 4
            Layout.bottomMargin: 4
        }

        // --- LISTA RETI WIFI ---
        StyledText {
            visible: Network.wifiEnabled
            text: Translation.tr("Networks")
            font.pixelSize: 12
            color: Appearance.colors.colOnSecondaryContainer
        }

        ColumnLayout {
            visible: Network.wifiEnabled
            Layout.fillWidth: true
            spacing: 2

            Repeater {
                model: Network.friendlyWifiNetworks
                delegate: Rectangle {
                    id: networkEntry
                    required property var modelData
                    Layout.fillWidth: true
                    implicitHeight: 40
                    radius: Appearance.rounding.small
                    color: modelData.active ? Appearance.colors.colLayer1 : "transparent"

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 8
                        anchors.rightMargin: 8
                        spacing: 8

                        MaterialSymbol {
                            text: modelData.active ? Network.materialSymbol : (
                                modelData.strength > 83 ? "signal_wifi_4_bar" :
                                modelData.strength > 50 ? "network_wifi_3_bar" :
                                modelData.strength > 17 ? "network_wifi_1_bar" :
                                "signal_wifi_0_bar"
                            )
                            iconSize: 18
                            color: Appearance.colors.colOnLayer1
                        }

                        StyledText {
                            Layout.fillWidth: true
                            text: modelData.ssid
                            elide: Text.ElideRight
                            color: Appearance.colors.colOnLayer1
                        }

                        MaterialSymbol {
                            visible: modelData.security && modelData.security.length > 0
                            text: "lock"
                            iconSize: 14
                            color: Appearance.colors.colOnLayer1
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            if (!modelData.active) {
                                Network.connectToWifiNetwork(modelData);
                            }
                        }
                    }
                }
            }

            StyledText {
                visible: Network.friendlyWifiNetworks.length === 0
                text: Translation.tr("No networks found")
                font.pixelSize: 12
                color: Appearance.colors.colOnLayer1
                Layout.topMargin: 4
                Layout.bottomMargin: 4
            }
        }

        // --- PULSANTE IMPOSTAZIONI ---
        RippleButton {
            Layout.topMargin: 8
            Layout.fillWidth: true
            implicitHeight: 36
            buttonRadius: Appearance.rounding.normal
            buttonText: Translation.tr("Network settings")
            onClicked: {
                Quickshell.execDetached(["kcmshell6", "kcm_networkmanagement"]);
                GlobalFocusGrab.dismiss();
            }
        }
    }
}
