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

    readonly property bool isPopupOpen: BarPopupState.openPopup === "notifications"

    onClicked: BarPopupState.toggle("notifications")

    onIsPopupOpenChanged: {
        if (isPopupOpen) {
            Notifications.timeoutAll();
            Notifications.markAllRead();
            Qt.callLater(() => {
                if (notificationPopup.item) {
                    GlobalFocusGrab.addDismissable(notificationPopup.item);
                }
            });
        } else {
            if (notificationPopup.item) {
                GlobalFocusGrab.removeDismissable(notificationPopup.item);
            }
        }
    }

    Connections {
        target: GlobalFocusGrab
        function onDismissed() {
            BarPopupState.close("notifications");
        }
    }

    RowLayout {
        id: layout
        anchors.centerIn: parent
        spacing: 3

        MaterialSymbol {
            text: Notifications.silent ? "notifications_paused" : "notifications"
            iconSize: Appearance.font.pixelSize.larger
            color: Appearance.colors.colOnLayer1
        }

        // Unread badge
        Rectangle {
            visible: !Notifications.silent && Notifications.unread > 0
            implicitWidth: Math.max(badgeText.implicitWidth + 6, 16)
            implicitHeight: 16
            radius: Appearance.rounding.full
            color: Appearance.colors.colOnLayer0

            StyledText {
                id: badgeText
                anchors.centerIn: parent
                font.pixelSize: Appearance.font.pixelSize.smallest
                color: Appearance.colors.colLayer0
                text: Notifications.unread > 99 ? "99+" : Notifications.unread.toString()
            }
        }
    }

    Item {
        id: ghostAnchor
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        width: notificationPopup.implicitWidth || 320
        height: 1
    }

    NotificationPopup {
        id: notificationPopup
        hoverTarget: ghostAnchor
        active: root.isPopupOpen
    }
}
