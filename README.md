# 🛠️ My Arch Linux & Hyprland Dotfiles

Questo repository contiene le mie configurazioni personali (dotfiles) per Arch Linux, Hyprland, Kitty, Neovim e altro.
Gestito in modo semplice ed elegante utilizzando **GNU Stow**.

## 📂 Struttura del Repository

GNU Stow funziona creando collegamenti simbolici (symlink) dalla Home directory (`~`) verso i file di questo repository. La struttura riflette esattamente la Home:

```text
~/dotfiles/
├── hypr/
│   └── .config/
│       └── hypr/           # Configurazione di Hyprland, Hyprlock, Hypridle
├── kitty/
│   └── .config/
│       └── kitty/          # Configurazione del terminale Kitty
├── nvim/
│   └── .config/
│       └── nvim/           # Configurazione dell'editor Neovim
└── starship/
    └── .config/
        └── starship.toml   # Configurazione del prompt Starship
```

---

## 🚀 Come Ripristinare (Su una nuova macchina)

Se vuoi installare queste configurazioni su un nuovo sistema Arch Linux o in caso di formattazione:

1. **Installa Git e GNU Stow**:
   ```bash
   sudo pacman -S git stow
   ```

2. **Clona questo repository nella tua home**:
   ```bash
   git clone https://github.com/slapomarda/dotfiles.git ~/dotfiles
   ```

3. **Applica le configurazioni tramite Stow**:
   ```bash
   cd ~/dotfiles
   stow -v -R -t ~ hypr kitty nvim starship
   ```
   *Nota: Se ci sono già file di configurazione predefiniti generati dal sistema che vanno in conflitto, eliminali o rinominali prima di lanciare `stow`.*

---

## ➕ Come Aggiungere una Nuova Applicazione

Se vuoi iniziare a gestire una nuova configurazione (es. `fish` shell) tramite questo repository:

1. Crea la struttura delle cartelle dentro `~/dotfiles` che riproduca il percorso originale a partire dalla home:
   ```bash
   mkdir -p ~/dotfiles/fish/.config
   ```

2. Sposta la cartella di configurazione originale dentro quella nuova:
   ```bash
   mv ~/.config/fish ~/dotfiles/fish/.config/
   ```

3. Usa Stow per creare il collegamento simbolico:
   ```bash
   cd ~/dotfiles
   stow -v -R -t ~ fish
   ```

4. Aggiungi le modifiche a Git, fai il commit e fai il push:
   ```bash
   git add .
   git commit -m "feat: add fish configuration"
   git push origin main
   ```

---

## 🔄 Flusso di Lavoro Giornaliero

Quando modifichi un file (es. modifichi il file di configurazione di Hyprland in `~/.config/hypr/hyprland.conf`), in realtà stai modificando direttamente il file dentro `~/dotfiles/hypr/.config/hypr/hyprland.conf` grazie al symlink.

Per salvare e sincronizzare le modifiche su GitHub ti basta fare:
```bash
cd ~/dotfiles
git add .
git commit -m "style: modifiche al tema di hyprland"
git push
```
