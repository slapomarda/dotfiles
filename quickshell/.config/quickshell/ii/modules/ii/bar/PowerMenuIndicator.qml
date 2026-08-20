import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

MouseArea {
    id: root
    property bool borderless: Config.options.bar.borderless

    implicitWidth: 32
    implicitHeight: Appearance.sizes.barHeight

    hoverEnabled: false
    cursorShape: Qt.PointingHandCursor

    readonly property bool isPopupOpen: BarPopupState.openPopup === "powermenu"

    onClicked: BarPopupState.toggle("powermenu")

    onIsPopupOpenChanged: {
        if (isPopupOpen) {
            Qt.callLater(() => {
                if (powerMenuPopup.item) {
                    GlobalFocusGrab.addDismissable(powerMenuPopup.item);
                }
            });
        } else {
            if (powerMenuPopup.item) {
                GlobalFocusGrab.removeDismissable(powerMenuPopup.item);
            }
        }
    }

    Connections {
        target: GlobalFocusGrab
        function onDismissed() {
            BarPopupState.close("powermenu");
        }
    }

    MaterialSymbol {
        anchors.centerIn: parent
        text: "power_settings_new"
        iconSize: Appearance.font.pixelSize.larger
        color: Appearance.colors.colOnLayer1
    }

    Item {
        id: ghostAnchor
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        width: powerMenuPopup.implicitWidth || 64
        height: 1
    }

    PowerMenuPopup {
        id: powerMenuPopup
        hoverTarget: ghostAnchor
        active: root.isPopupOpen
    }
}
