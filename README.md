# Arch Linux and Hyprland Dotfiles

Configurazioni di sistema personali gestite tramite GNU Stow.

## Struttura del repository

La struttura delle directory all'interno del repository rispecchia la gerarchia della directory home (~):

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
└── starship/
    └── .config/
        └── starship.toml   # Starship shell prompt
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

3. Applicare i symlink tramite Stow:
   ```bash
   cd ~/dotfiles
   stow -v -R -t ~ hypr kitty nvim starship
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
