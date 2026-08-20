pragma Singleton
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
            memoryTotal = Number(textMeminfo.match(/MemTotal: *(\d+)/)?.[1] ?? 1);
            memoryFree = Number(textMeminfo.match(/MemAvailable: *(\d+)/)?.[1] ?? 0);
            
            const textStat = fileStat.text();
            const cpuLine = textStat.match(/^cpu\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)/);
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
        // GPU da nvidia-smi, CPU (Package id 0) da sensors
        command: ["sh", "-c", "nvidia-smi --query-gpu=utilization.gpu,temperature.gpu --format=csv,noheader,nounits; sensors | grep 'Package id 0' | awk '{print $4}' | sed 's/+//;s/°C//'"]
        running: true
        stdout: StdioCollector {
            onStreamFinished: {
                let lines = text.trim().split(/\r?\n/);
                if (lines.length >= 2) {
                    let gpuData = lines[0].split(', ');
                    // Smussiamo il valore (media mobile)
                    root.gpuUsage = (root.gpuUsage * 0.7) + ((Number(gpuData[0]) / 100) * 0.3);
                    root.gpuTemp = Number(gpuData[1]);
                    root.cpuTemp = Number(lines[1]);
                }
                // --- IL FRENO È QUI: 2000 millisecondi di pausa ---
                Qt.callLater(() => sensorProc.running = true, 2000);
          }
        }
    }

    FileView { id: fileMeminfo; path: "/proc/meminfo" }
    FileView { id: fileStat; path: "/proc/stat" }
}
