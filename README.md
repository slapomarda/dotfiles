# Arch Linux and Hyprland Dotfiles

Configurazioni di sistema personali gestite tramite GNU Stow.

## Struttura del repository

```text
~/dotfiles/
├── hypr/
│   └── .config/
│       └── hypr/           # Hyprland, Hyprlock, Hypridle
├── kitty/
│   └── .config/
│       └── kitty/          # Kitty terminal emulator
├── nvim/
│   └── .config/
│       └── nvim/           # Neovim text editor
├── starship/
│   └── .config/
│       └── starship.toml   # Starship shell prompt
├── quickshell/
│   └── .config/
│       └── quickshell/     # Quickshell widgets/status bar (illogical impulse)
├── matugen/
│   └── .config/
│       └── matugen/        # Material You color generator
├── fuzzel/
│   └── .config/
│       └── fuzzel/         # Fuzzel application launcher
├── wlogout/
│   └── .config/
│       └── wlogout/        # Logout menu
├── gtk-3.0/
│   └── .config/
│       └── gtk-3.0/        # GTK 3 theme settings
├── gtk-4.0/
│   └── .config/
│       └── gtk-4.0/        # GTK 4 theme settings
├── Kvantum/
│   └── .config/
│       └── Kvantum/        # Kvantum (Qt) theme engine configurations
└── ly/
    └── etc/
        └── ly/
            └── config.ini  # Ly login manager configuration (Solo Backup)
```

## Installazione e Ripristino

Procedura per applicare le configurazioni su un nuovo sistema:

1. Installare le dipendenze:
   ```bash
   sudo pacman -S git stow
   ```

2. Clonare il repository nella home directory:
   ```bash
   git clone https://github.com/slapomarda/dotfiles.git ~/dotfiles
   ```

3. Applicare tutti i symlink per l'utente locale tramite Stow:
   ```bash
   cd ~/dotfiles
   stow -v -R -t ~ hypr kitty nvim starship quickshell matugen fuzzel wlogout gtk-3.0 gtk-4.0 Kvantum
   ```

4. Ripristinare manualmente la configurazione di Ly:
   ```bash
   sudo cp ~/dotfiles/ly/etc/ly/config.ini /etc/ly/config.ini
   ```

## Aggiunta di nuovi moduli/applicazioni

Procedura per aggiungere una nuova configurazione (es. `fish`):

1. Creare la gerarchia di directory corrispondente:
   ```bash
   mkdir -p ~/dotfiles/fish/.config
   ```

2. Spostare la directory di configurazione originale nel repository:
   ```bash
   mv ~/.config/fish ~/dotfiles/fish/.config/
   ```

3. Creare il symlink tramite Stow:
   ```bash
   cd ~/dotfiles
   stow -v -R -t ~ fish
   ```
