import qs.modules.common
import qs.modules.common.widgets
import qs.services
import QtQuick
import QtQuick.Layouts

StyledPopup {
    id: root
    function formatKB(kb) { return (kb / (1024 * 1024)).toFixed(1) + " GB"; }

    Row {
        anchors.centerIn: parent
        spacing: 12

        Column {
            anchors.top: parent.top; spacing: 8
            StyledPopupHeaderRow { icon: "memory"; label: "RAM" }
            Column { spacing: 4
                StyledPopupValueRow { icon: "clock_loader_60"; label: "Used:"; value: root.formatKB(ResourceUsage.memoryUsed) }
                StyledPopupValueRow { icon: "check_circle"; label: "Free:"; value: root.formatKB(ResourceUsage.memoryFree) }
            }
        }

        Column {
            anchors.top: parent.top; spacing: 8
            StyledPopupHeaderRow { icon: "developer_board"; label: "GPU" }
            Column { spacing: 4
                StyledPopupValueRow { icon: "speed"; label: "Load:"; value: `${Math.floor(ResourceUsage.gpuUsage * 100)}%` }
                StyledPopupValueRow { icon: "thermometer"; label: "Temp:"; value: `${ResourceUsage.gpuTemp}°C` }
            }
        }

        Column {
            anchors.top: parent.top; spacing: 8
            StyledPopupHeaderRow { icon: "planner_review"; label: "CPU" }
            Column { spacing: 4
                StyledPopupValueRow { icon: "bolt"; label: "Load:"; value: `${Math.round(ResourceUsage.cpuUsage * 100)}%` }
                StyledPopupValueRow { icon: "thermometer"; label: "Temp:"; value: `${ResourceUsage.cpuTemp}°C` }
            }
        }
    }
}
