import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import Quickshell

StyledPopup {
    id: root

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 8

        // ── Header ────────────────────────────────────────────────────
        StyledPopupHeaderRow {
            Layout.minimumWidth: 320
            Layout.maximumWidth: 320
            icon: Notifications.silent ? "notifications_paused" : "notifications"
            label: "Notifications"
        }

        // ── List ──────────────────────────────────────────────────────
        NotificationListView {
            id: notifList
            Layout.minimumWidth: 320
            Layout.maximumWidth: 320
            Layout.preferredHeight: Math.min(contentHeight, 420)
            popup: false
            clip: true
        }

        // ── Empty state ───────────────────────────────────────────────
        StyledText {
            visible: Notifications.list.length === 0
            text: "No notifications"
            color: Appearance.colors.colOnLayer1
            Layout.alignment: Qt.AlignHCenter
            Layout.minimumWidth: 320
            Layout.topMargin: 4
            Layout.bottomMargin: 4
        }

        // ── Separator ─────────────────────────────────────────────────
        Rectangle {
            Layout.minimumWidth: 320
            Layout.fillWidth: true
            implicitHeight: 1
            color: Appearance.colors.colLayer0Border
        }

        // ── Status bar ────────────────────────────────────────────────
        RowLayout {
            Layout.minimumWidth: 320
            Layout.maximumWidth: 320
            spacing: 6

            // Mute toggle
            Rectangle {
                implicitWidth: 40
                implicitHeight: 36
                radius: Appearance.rounding.normal
                color: muteMa.containsPress
                    ? Appearance.colors.colLayer1Active
                    : Notifications.silent
                        ? Appearance.colors.colSecondaryContainer
                        : muteMa.containsMouse
                            ? Appearance.colors.colLayer1Hover
                            : "transparent"
                Behavior on color { ColorAnimation { duration: 120 } }
                MaterialSymbol {
                    anchors.centerIn: parent
                    text: "notifications_paused"
                    iconSize: 18
                    color: Notifications.silent
                        ? Appearance.m3colors.m3primary
                        : Appearance.colors.colOnLayer1
                }
                MouseArea {
                    id: muteMa
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Notifications.silent = !Notifications.silent
                }
            }

            // Count
            StyledText {
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                text: Notifications.list.length + " notifications"
                color: Appearance.colors.colOnLayer1
                font.pixelSize: Appearance.font.pixelSize.small
            }

            // Clear all
            Rectangle {
                implicitWidth: 40
                implicitHeight: 36
                radius: Appearance.rounding.normal
                color: clearMa.containsPress
                    ? Appearance.colors.colLayer1Active
                    : clearMa.containsMouse
                        ? Appearance.colors.colLayer1Hover
                        : "transparent"
                Behavior on color { ColorAnimation { duration: 120 } }
                MaterialSymbol {
                    anchors.centerIn: parent
                    text: "delete_sweep"
                    iconSize: 18
                    color: Appearance.colors.colOnLayer1
                }
                MouseArea {
                    id: clearMa
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Notifications.discardAllNotifications()
                }
            }
        }
    }
}
