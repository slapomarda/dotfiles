import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
MouseArea {
    id: root
    property bool borderless: Config.options.bar.borderless
    visible: BluetoothStatus.available

    implicitWidth: layout.implicitWidth + 16
    implicitHeight: Appearance.sizes.barHeight

    hoverEnabled: false
    cursorShape: Qt.PointingHandCursor

    readonly property bool isPopupOpen: BarPopupState.openPopup === "bluetooth"

    onClicked: {
        BarPopupState.toggle("bluetooth")
    }
    onIsPopupOpenChanged: {
        if (isPopupOpen) {
            Qt.callLater(() => {
                if (bluetoothPopup.item) {
                    GlobalFocusGrab.addDismissable(bluetoothPopup.item);
                }
            });
        } else {
            if (bluetoothPopup.item) {
                GlobalFocusGrab.removeDismissable(bluetoothPopup.item);
            }
        }
    }
    Connections {
        target: GlobalFocusGrab
        function onDismissed() {
            BarPopupState.close("bluetooth");
        }
    }
    RowLayout {
        id: layout
        anchors.centerIn: parent
        spacing: 6
        MaterialSymbol {
            id: bluetoothIcon
            text: BluetoothStatus.connected ? "bluetooth_connected" : BluetoothStatus.enabled ? "bluetooth" : "bluetooth_disabled"
            iconSize: Appearance.font.pixelSize.larger
            color: Appearance.colors.colOnLayer1
        }

        StyledText {
            visible: BluetoothStatus.connected && BluetoothStatus.firstActiveDevice !== null
            text: BluetoothStatus.firstActiveDevice?.name ?? ""
            font.pixelSize: 13
            color: Appearance.colors.colOnLayer1
            Layout.maximumWidth: 150
            elide: Text.ElideRight
        }
    }
    Item {
        id: ghostAnchor
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        width: bluetoothPopup.implicitWidth || 220
        height: 1
    }
    BluetoothPopup {
        id: bluetoothPopup
        hoverTarget: ghostAnchor
        active: root.isPopupOpen
    }
}
