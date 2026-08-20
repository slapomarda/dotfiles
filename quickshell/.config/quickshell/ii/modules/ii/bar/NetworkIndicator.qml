import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
MouseArea {
    id: root
    property bool borderless: Config.options.bar.borderless

    implicitWidth: layout.implicitWidth + 16
    implicitHeight: Appearance.sizes.barHeight

    hoverEnabled: false
    cursorShape: Qt.PointingHandCursor

    readonly property bool isPopupOpen: BarPopupState.openPopup === "network"

    onClicked: {
        BarPopupState.toggle("network")
    }
    onIsPopupOpenChanged: {
        if (isPopupOpen) {
            Qt.callLater(() => {
                if (networkPopup.item) {
                    GlobalFocusGrab.addDismissable(networkPopup.item);
                }
            });
        } else {
            if (networkPopup.item) {
                GlobalFocusGrab.removeDismissable(networkPopup.item);
            }
        }
    }
    Connections {
        target: GlobalFocusGrab
        function onDismissed() {
            BarPopupState.close("network");
        }
    }
    RowLayout {
        id: layout
        anchors.centerIn: parent
        spacing: 6
        MaterialSymbol {
            id: networkIcon
            text: Network.materialSymbol
            iconSize: Appearance.font.pixelSize.larger
            color: Appearance.colors.colOnLayer1
        }
        StyledText {
            visible: Network.wifiEnabled && Network.wifiStatus === "connected"
            text: Network.networkName ?? ""
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
        width: networkPopup.implicitWidth || 260
        height: 1
    }
    NetworkPopup {
        id: networkPopup
        hoverTarget: ghostAnchor
        active: root.isPopupOpen
    }
}
