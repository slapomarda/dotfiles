path = "Network.qml"
with open(path, "r") as f:
    content = f.read()

changes = []

# 1) Nuova proprieta' primaryConnection
old1 = '''    property string wifiStatus: "disconnected"'''
new1 = '''    property string wifiStatus: "disconnected"
    // "wifi" o "ethernet": quale interfaccia ha attualmente la metrica di route piu' bassa (preferita)
    property string primaryConnection: "ethernet"'''
changes.append((old1, new1, "proprieta' primaryConnection"))

# 2) Nuove funzioni dopo disconnectWifiNetwork
old2 = '''    function disconnectWifiNetwork(): void {
        if (active) disconnectProc.exec(["nmcli", "connection", "down", active.ssid]);
    }'''
new2 = '''    function disconnectWifiNetwork(): void {
        if (active) disconnectProc.exec(["nmcli", "connection", "down", active.ssid]);
    }

    // Scambia le metriche di route tra il profilo wifi attivo e quello ethernet attivo,
    // invece di spegnere fisicamente l'interfaccia. Entrambe restano connesse.
    function setPrimaryConnection(primary: string): void {
        if (primary !== "wifi" && primary !== "ethernet") return;
        setPrimaryProc.exec({
            "environment": {
                "PRIMARY": primary
            },
            "command": ["bash", "-c", "WIFI_CONN=$(nmcli -t -f NAME,TYPE connection show --active | awk -F: '$2==\\"802-11-wireless\\"{print $1; exit}'); ETH_CONN=$(nmcli -t -f NAME,TYPE connection show --active | awk -F: '$2==\\"802-3-ethernet\\"{print $1; exit}'); if [ \\"$PRIMARY\\" = \\"wifi\\" ]; then WM=50; EM=100; else WM=100; EM=50; fi; if [ -n \\"$WIFI_CONN\\" ]; then nmcli connection modify \\"$WIFI_CONN\\" ipv4.route-metric $WM ipv6.route-metric $WM; nmcli connection up \\"$WIFI_CONN\\"; fi; if [ -n \\"$ETH_CONN\\" ]; then nmcli connection modify \\"$ETH_CONN\\" ipv4.route-metric $EM ipv6.route-metric $EM; nmcli connection up \\"$ETH_CONN\\"; fi"]
        })
    }

    function refreshPrimaryConnection(): void {
        primaryQueryProc.running = false;
        primaryQueryProc.running = true;
    }

    Process {
        id: setPrimaryProc
        onExited: (exitCode, exitStatus) => {
            root.refreshPrimaryConnection();
        }
    }

    Process {
        id: primaryQueryProc
        running: true
        command: ["bash", "-c", "WIFI_CONN=$(nmcli -t -f NAME,TYPE connection show --active | awk -F: '$2==\\"802-11-wireless\\"{print $1; exit}'); ETH_CONN=$(nmcli -t -f NAME,TYPE connection show --active | awk -F: '$2==\\"802-3-ethernet\\"{print $1; exit}'); WM=600; EM=600; if [ -n \\"$WIFI_CONN\\" ]; then WM=$(nmcli -g ipv4.route-metric connection show \\"$WIFI_CONN\\"); fi; if [ -n \\"$ETH_CONN\\" ]; then EM=$(nmcli -g ipv4.route-metric connection show \\"$ETH_CONN\\"); fi; [ \\"$WM\\" = \\"-1\\" ] && WM=600; [ \\"$EM\\" = \\"-1\\" ] && EM=600; echo \\"$WM $EM\\""]
        stdout: StdioCollector {
            onStreamFinished: {
                const parts = text.trim().split(/\\s+/).map(Number);
                const wm = isNaN(parts[0]) ? 600 : parts[0];
                const em = isNaN(parts[1]) ? 600 : parts[1];
                root.primaryConnection = wm <= em ? "wifi" : "ethernet";
            }
        }
    }'''
changes.append((old2, new2, "funzioni setPrimaryConnection/refreshPrimaryConnection + Process"))

# 3) Richiama il refresh ad ogni update()
old3 = '''    function update() {
        updateConnectionType.startCheck();
        wifiStatusProcess.running = true
        updateNetworkName.running = true;
        updateNetworkStrength.running = true;
    }'''
new3 = '''    function update() {
        updateConnectionType.startCheck();
        wifiStatusProcess.running = true
        updateNetworkName.running = true;
        updateNetworkStrength.running = true;
        root.refreshPrimaryConnection();
    }'''
changes.append((old3, new3, "refreshPrimaryConnection() richiamata in update()"))

ok = True
for old, new, label in changes:
    count = content.count(old)
    if count != 1:
        print(f"ATTENZIONE: blocco '{label}' trovato {count} volte (atteso 1). Nessuna modifica per questo blocco.")
        ok = False
        continue
    content = content.replace(old, new)
    print(f"OK: applicato '{label}'.")

with open(path, "w") as f:
    f.write(content)

if ok:
    print("Tutte le modifiche applicate correttamente.")
else:
    print("Alcune modifiche NON sono state applicate, controlla i messaggi sopra prima di committare.")
