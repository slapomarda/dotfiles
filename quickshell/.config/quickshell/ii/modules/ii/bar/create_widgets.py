import os

files = {}

files["NetworkIndicator.qml"] = '''import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

MouseArea {
    id: root
    property bool borderless: Config.options.bar.borderless
    implicitWidth: networkIcon.implicitWidth + 8
    implicitHeight: Appearance.sizes.barHeight
    hoverEnabled: !Config.options.bar.tooltips.clickToShow

    MaterialSymbol {
        id: networkIcon
        anchors.centerIn: parent
        text: Network.materialSymbol
        iconSize: Appearance.font.pixelSize.larger
        color: Appearance.colors.colOnLayer1
    }

    NetworkPopup {
        id: networkPopup
        hoverTarget: root
    }
}
'''

files["NetworkPopup.qml"] = '''import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

StyledPopup {
    id: root

    ColumnLayout {
        id: columnLayout
        anchors.centerIn: parent
        spacing: 4

        StyledPopupHeaderRow {
            icon: Network.materialSymbol
            label: Translation.tr("Network")
        }

        StyledPopupValueRow {
            visible: Network.ethernet
            icon: "lan"
            label: Translation.tr("Ethernet:")
            value: Translation.tr("Connected")
        }

        StyledPopupValueRow {
            visible: !Network.ethernet
            icon: "wifi"
            label: Translation.tr("Wi-Fi:")
            value: Network.wifiEnabled ? Translation.tr("On") : Translation.tr("Off")
        }

        StyledPopupValueRow {
            visible: !Network.ethernet && Network.wifiEnabled && Network.active !== null
            icon: "router"
            label: Translation.tr("SSID:")
            value: Network.networkName
        }

        StyledPopupValueRow {
            visible: !Network.ethernet && Network.wifiEnabled && Network.active !== null
            icon: "signal_cellular_alt"
            label: Translation.tr("Signal:")
            value: `${Network.active?.strength ?? 0}%`
        }

        RowLayout {
            Layout.topMargin: 4
            Layout.fillWidth: true
            spacing: 8

            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                buttonText: Network.wifiEnabled ? Translation.tr("Turn Wi-Fi off") : Translation.tr("Turn Wi-Fi on")
                onClicked: Network.toggleWifi()
            }

            RippleButton {
                Layout.fillWidth: true
                implicitHeight: 36
                buttonRadius: Appearance.rounding.normal
                buttonText: Translation.tr("Wi-Fi settings")
                onClicked: GlobalStates.sidebarRightOpen = true
            }
        }
    }
}
'''

files["BluetoothIndicator.qml"] = '''import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

MouseArea {
    id: root
    property bool borderless: Config.options.bar.borderless
    visible: BluetoothStatus.available
    implicitWidth: bluetoothIcon.implicitWidth + 8
    implicitHeight: Appearance.sizes.barHeight
    hoverEnabled: !Config.options.bar.tooltips.clickToShow

    MaterialSymbol {
        id: bluetoothIcon
        anchors.centerIn: parent
        text: BluetoothStatus.connected ? "bluetooth_connected" : BluetoothStatus.enabled ? "bluetooth" : "bluetooth_disabled"
        iconSize: Appearance.font.pixelSize.larger
        color: Appearance.colors.colOnLayer1
    }

    BluetoothPopup {
        id: bluetoothPopup
        hoverTarget: root
    }
}
'''

files["BluetoothPopup.qml"] = '''import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import Quickshell.Bluetooth

StyledPopup {
    id: root

    ColumnLayout {
        id: columnLayout
        anchors.centerIn: parent
        spacing: 4

        StyledPopupHeaderRow {
            icon: BluetoothStatus.connected ? "bluetooth_connected" : "bluetooth"
            label: Translation.tr("Bluetooth")
        }

        StyledPopupValueRow {
            icon: "power_settings_new"
            label: Translation.tr("Status:")
            value: BluetoothStatus.enabled ? Translation.tr("On") : Translation.tr("Off")
        }

        StyledPopupValueRow {
            visible: BluetoothStatus.enabled && BluetoothStatus.activeDeviceCount > 0
            icon: "link"
            label: Translation.tr("Connected devices:")
            value: `${BluetoothStatus.activeDeviceCount}`
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.topMargin: 2
            spacing: 2
            visible: BluetoothStatus.connectedDevices.length > 0

            Repeater {
                model: BluetoothStatus.connectedDevices
                delegate: StyledPopupValueRow {
                    required property var modelData
                    icon: "headphones"
                    label: modelData.name
                    value: ""
                }
            }
        }

        RippleButton {
            Layout.topMargin: 4
            Layout.fillWidth: true
            implicitHeight: 36
            buttonRadius: Appearance.rounding.normal
            buttonText: Translation.tr("Bluetooth settings")
            onClicked: GlobalStates.sidebarRightOpen = true
        }
    }
}
'''

files["VolumeIndicator.qml"] = '''import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

MouseArea {
    id: root
    property bool borderless: Config.options.bar.borderless
    implicitWidth: volumeIcon.implicitWidth + 8
    implicitHeight: Appearance.sizes.barHeight
    hoverEnabled: !Config.options.bar.tooltips.clickToShow

    onWheel: event => {
        if (event.angleDelta.y > 0) Audio.incrementVolume();
        else Audio.decrementVolume();
    }

    MaterialSymbol {
        id: volumeIcon
        anchors.centerIn: parent
        text: {
            if (Audio.sink?.audio?.muted ?? false) return "volume_off";
            const v = Audio.value;
            if (v > 0.6) return "volume_up";
            if (v > 0) return "volume_down";
            return "volume_mute";
        }
        iconSize: Appearance.font.pixelSize.larger
        color: Appearance.colors.colOnLayer1
    }

    VolumePopup {
        id: volumePopup
        hoverTarget: root
    }
}
'''

files["VolumePopup.qml"] = '''import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

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

        StyledPopupValueRow {
            visible: Audio.source !== null
            icon: (Audio.source?.audio?.muted ?? false) ? "mic_off" : "mic"
            label: Translation.tr("Microphone:")
            value: (Audio.source?.audio?.muted ?? false) ? Translation.tr("Muted") : Translation.tr("Active")
        }

        RippleButton {
            Layout.topMargin: 4
            Layout.fillWidth: true
            implicitHeight: 36
            buttonRadius: Appearance.rounding.normal
            buttonText: Translation.tr("Sound settings")
            onClicked: GlobalStates.sidebarRightOpen = true
        }
    }
}
'''

created = []
skipped = []
for filename, content in files.items():
    if os.path.exists(filename):
        skipped.append(filename)
        continue
    with open(filename, "w") as f:
        f.write(content)
    created.append(filename)

print("Creati:", created)
if skipped:
    print("Saltati (esistevano già):", skipped)
