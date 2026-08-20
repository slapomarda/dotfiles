import os

# Percorsi dei file
service_file = os.path.expanduser("~/.config/quickshell/ii/services/ResourceUsage.qml")
popup_file = os.path.expanduser("~/.config/quickshell/ii/modules/ii/bar/ResourcesPopup.qml")

# 1. PATCH SERVIZIO (Aggiunge GPU, Temp CPU/GPU)
service_content = """pragma Singleton
pragma ComponentBehavior: Bound
import qs.modules.common
import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: root
    property real memoryTotal: 1
    property real memoryFree: 0
    property real memoryUsed: memoryTotal - memoryFree
    property real memoryUsedPercentage: memoryUsed / memoryTotal
    property real cpuUsage: 0
    property real gpuUsage: 0
    property real cpuTemp: 0
    property real gpuTemp: 0
    property var previousCpuStats

    Timer {
        interval: 2000; running: true; repeat: true
        onTriggered: {
            fileMeminfo.reload(); fileStat.reload();
            const textMeminfo = fileMeminfo.text();
            memoryTotal = Number(textMeminfo.match(/MemTotal: *(\\d+)/)?.[1] ?? 1);
            memoryFree = Number(textMeminfo.match(/MemAvailable: *(\\d+)/)?.[1] ?? 0);
            
            const textStat = fileStat.text();
            const cpuLine = textStat.match(/^cpu\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)/);
            if (cpuLine) {
                const stats = cpuLine.slice(1).map(Number);
                const total = stats.reduce((a, b) => a + b, 0);
                const idle = stats[3];
                if (previousCpuStats) {
                    const totalDiff = total - previousCpuStats.total;
                    const idleDiff = idle - previousCpuStats.idle;
                    cpuUsage = totalDiff > 0 ? (1 - idleDiff / totalDiff) : 0;
                }
                previousCpuStats = { total, idle };
            }
        }
    }

    Process {
        id: sensorProc
        command: ["bash", "-c", "echo $(nvidia-smi --query-gpu=utilization.gpu,temperature.gpu --format=csv,noheader,nounits | sed 's/,/ /'); sensors | grep 'Tdie' | awk '{print $2}' | sed 's/+//;s/°C//'"]
        running: true
        stdout: StdioCollector {
            onStreamFinished: {
                let lines = text.trim().split(/\\s+/);
                if (lines.length >= 3) {
                    root.gpuUsage = (root.gpuUsage * 0.7) + (Number(lines[0])/100 * 0.3);
                    root.gpuTemp = Number(lines[1]);
                    root.cpuTemp = Number(lines[2]);
                }
                Qt.callLater(() => sensorProc.running = true, 2000);
            }
        }
    }

    FileView { id: fileMeminfo; path: "/proc/meminfo" }
    FileView { id: fileStat; path: "/proc/stat" }
}
"""

# 2. PATCH POPUP (Sostituisce Swap con GPU + Temperature)
popup_content = """import qs.modules.common
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
"""

with open(service_file, "w") as f: f.write(service_content)
with open(popup_file, "w") as f: f.write(popup_content)

print("[+] Servizio e Pop-up aggiornati correttamente!")
