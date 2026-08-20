import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts
import Quickshell

StyledPopup {
    id: root
    alignRight: true

    ColumnLayout {
        id: col
        anchors.centerIn: parent
        spacing: 2

        property bool anyHovered: nightMa.containsMouse || settingsMa.containsMouse
                                || sleepMa.containsMouse || rebootMa.containsMouse
                                || shutdownMa.containsMouse

        // Larghezza massima dei label — basta la stringa più lunga ("Night Light")
        // Gli altri si allineano alla stessa larghezza automaticamente
        readonly property real expandedWidth: labelNight.implicitWidth + 52

        // ── Night Light ───────────────────────────────────────────────
        Rectangle {
            implicitWidth: col.anyHovered ? col.expandedWidth : 44
            implicitHeight: 40
            Layout.alignment: Qt.AlignRight
            radius: Appearance.rounding.normal
            Behavior on implicitWidth { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            color: nightMa.containsPress
                ? Appearance.colors.colLayer1Active
                : Hyprsunset.temperatureActive
                    ? Appearance.colors.colSecondaryContainer
                    : nightMa.containsMouse
                        ? Appearance.colors.colLayer1Hover
                        : "transparent"
            Behavior on color { ColorAnimation { duration: 120 } }
            StyledText {
                id: labelNight
                anchors.right: nightIcon.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                text: "Night Light"
                wrapMode: Text.NoWrap
                color: Appearance.colors.colOnLayer1
                opacity: col.anyHovered ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: 120 } }
            }
            MaterialSymbol {
                id: nightIcon
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "bedtime"
                iconSize: 20
                color: Hyprsunset.temperatureActive
                    ? Appearance.m3colors.m3primary
                    : Appearance.colors.colOnLayer1
            }
            MouseArea {
                id: nightMa
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: Hyprsunset.toggleTemperature()
            }
        }

        // ── Settings (right sidebar) ──────────────────────────────────
        Rectangle {
            implicitWidth: col.anyHovered ? col.expandedWidth : 44
            implicitHeight: 40
            Layout.alignment: Qt.AlignRight
            radius: Appearance.rounding.normal
            Behavior on implicitWidth { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            color: settingsMa.containsPress
                ? Appearance.colors.colLayer1Active
                : settingsMa.containsMouse
                    ? Appearance.colors.colLayer1Hover
                    : "transparent"
            Behavior on color { ColorAnimation { duration: 120 } }
            StyledText {
                anchors.right: settingsIcon.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                text: "Settings"
                wrapMode: Text.NoWrap
                color: Appearance.colors.colOnLayer1
                opacity: col.anyHovered ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: 120 } }
            }
            MaterialSymbol {
                id: settingsIcon
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "settings"
                iconSize: 20
                color: Appearance.colors.colOnLayer1
            }
            MouseArea {
                id: settingsMa
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    GlobalStates.sidebarRightOpen = true;
                    BarPopupState.closeAll();
                }
            }
        }

        // ── Separator ─────────────────────────────────────────────────
        Rectangle {
            implicitWidth: col.anyHovered ? col.expandedWidth : 44
            Layout.alignment: Qt.AlignRight
            Behavior on implicitWidth { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            implicitHeight: 1
            color: Appearance.colors.colLayer0Border
            Layout.topMargin: 2
            Layout.bottomMargin: 2
        }

        // ── Sleep ─────────────────────────────────────────────────────
        Rectangle {
            implicitWidth: col.anyHovered ? col.expandedWidth : 44
            implicitHeight: 40
            Layout.alignment: Qt.AlignRight
            radius: Appearance.rounding.normal
            Behavior on implicitWidth { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            color: sleepMa.containsPress
                ? Appearance.colors.colLayer1Active
                : sleepMa.containsMouse
                    ? Appearance.colors.colLayer1Hover
                    : "transparent"
            Behavior on color { ColorAnimation { duration: 120 } }
            StyledText {
                anchors.right: sleepIcon.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                text: "Sleep"
                wrapMode: Text.NoWrap
                color: Appearance.colors.colOnLayer1
                opacity: col.anyHovered ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: 120 } }
            }
            MaterialSymbol {
                id: sleepIcon
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "mode_standby"
                iconSize: 20
                color: Appearance.colors.colOnLayer1
            }
            MouseArea {
                id: sleepMa
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: Quickshell.execDetached(["systemctl", "suspend"])
            }
        }

        // ── Reboot ────────────────────────────────────────────────────
        Rectangle {
            implicitWidth: col.anyHovered ? col.expandedWidth : 44
            implicitHeight: 40
            Layout.alignment: Qt.AlignRight
            radius: Appearance.rounding.normal
            Behavior on implicitWidth { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            color: rebootMa.containsPress
                ? Appearance.colors.colLayer1Active
                : rebootMa.containsMouse
                    ? Appearance.colors.colLayer1Hover
                    : "transparent"
            Behavior on color { ColorAnimation { duration: 120 } }
            StyledText {
                anchors.right: rebootIcon.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                text: "Reboot"
                wrapMode: Text.NoWrap
                color: Appearance.colors.colOnLayer1
                opacity: col.anyHovered ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: 120 } }
            }
            MaterialSymbol {
                id: rebootIcon
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "restart_alt"
                iconSize: 20
                color: Appearance.colors.colOnLayer1
            }
            MouseArea {
                id: rebootMa
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: Quickshell.execDetached(["systemctl", "reboot"])
            }
        }

        // ── Shutdown ──────────────────────────────────────────────────
        Rectangle {
            implicitWidth: col.anyHovered ? col.expandedWidth : 44
            implicitHeight: 40
            Layout.alignment: Qt.AlignRight
            radius: Appearance.rounding.normal
            Behavior on implicitWidth { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
            color: shutdownMa.containsPress
                ? Appearance.colors.colLayer1Active
                : shutdownMa.containsMouse
                    ? Appearance.colors.colLayer1Hover
                    : "transparent"
            Behavior on color { ColorAnimation { duration: 120 } }
            StyledText {
                anchors.right: shutdownIcon.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                text: "Shutdown"
                wrapMode: Text.NoWrap
                color: Appearance.colors.colError
                opacity: col.anyHovered ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: 120 } }
            }
            MaterialSymbol {
                id: shutdownIcon
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "power_settings_new"
                iconSize: 20
                color: Appearance.colors.colError
            }
            MouseArea {
                id: shutdownMa
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: Quickshell.execDetached(["systemctl", "poweroff"])
            }
        }
    }
}
