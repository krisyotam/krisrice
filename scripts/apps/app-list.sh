#!/bin/bash

# Multi-Distribution Application List Generator
# Supports various Linux distributions and package managers

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to display available distributions
show_distributions() {
    echo -e "${CYAN}Supported distributions:${NC}"
    echo -e "  ${GREEN}arch${NC}     - Arch Linux (pacman, yay)"
    echo -e "  ${GREEN}kali${NC}     - Kali Linux (apt)"
    echo -e "  ${GREEN}gentoo${NC}   - Gentoo Linux (emerge)"
    echo -e "  ${GREEN}ubuntu${NC}   - Ubuntu/Debian (apt)"
    echo -e "  ${GREEN}debian${NC}   - Debian (apt)"
    echo -e "  ${GREEN}fedora${NC}   - Fedora (dnf)"
    echo -e "  ${GREEN}rhel${NC}     - RHEL/CentOS (yum/dnf)"
    echo -e "  ${GREEN}opensuse${NC} - openSUSE (zypper)"
    echo -e "  ${GREEN}alpine${NC}   - Alpine Linux (apk)"
    echo -e "  ${GREEN}void${NC}     - Void Linux (xbps)"
    echo -e "  ${GREEN}nixos${NC}    - NixOS (nix)"
    echo ""
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get clipboard command
get_clipboard_cmd() {
    if command_exists xclip; then
        echo "xclip -selection clipboard"
    elif command_exists xsel; then
        echo "xsel --clipboard --input"
    elif command_exists pbcopy; then
        echo "pbcopy"
    elif command_exists wl-copy; then
        echo "wl-copy"
    else
        echo ""
    fi
}

# Function to list applications for Arch Linux
list_arch_apps() {
    {
        if command_exists pacman; then
            echo "### Pacman Packages (official repo)"
            pacman -Qqe 2>/dev/null || echo "Error: Could not list pacman packages"
        fi

        if command_exists yay; then
            echo; echo "### Yay / AUR Packages"
            yay -Qqm 2>/dev/null || echo "No AUR packages found or yay not available"
        elif command_exists paru; then
            echo; echo "### Paru / AUR Packages"
            paru -Qqm 2>/dev/null || echo "No AUR packages found or paru not available"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        if command_exists snap; then
            echo; echo "### Snap Packages"
            snap list 2>/dev/null | tail -n +2 | awk '{print $1}' || echo "No Snap packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for Debian/Ubuntu/Kali
list_debian_apps() {
    {
        if command_exists apt; then
            echo "### APT Packages (user-installed)"
            apt list --installed 2>/dev/null | grep -v "^WARNING" | tail -n +2 | cut -d'/' -f1 || echo "Error: Could not list APT packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        if command_exists snap; then
            echo; echo "### Snap Packages"
            snap list 2>/dev/null | tail -n +2 | awk '{print $1}' || echo "No Snap packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for Fedora
list_fedora_apps() {
    {
        if command_exists dnf; then
            echo "### DNF Packages (user-installed)"
            dnf list installed 2>/dev/null | tail -n +2 | awk '{print $1}' | cut -d'.' -f1 || echo "Error: Could not list DNF packages"
        elif command_exists yum; then
            echo "### YUM Packages (user-installed)"
            yum list installed 2>/dev/null | tail -n +2 | awk '{print $1}' | cut -d'.' -f1 || echo "Error: Could not list YUM packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        if command_exists snap; then
            echo; echo "### Snap Packages"
            snap list 2>/dev/null | tail -n +2 | awk '{print $1}' || echo "No Snap packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for Gentoo
list_gentoo_apps() {
    {
        if command_exists equery; then
            echo "### Portage Packages (installed)"
            equery list '*' 2>/dev/null | cut -d' ' -f1 || echo "Error: Could not list Portage packages"
        elif [ -d /var/db/pkg ]; then
            echo "### Portage Packages (installed)"
            find /var/db/pkg -mindepth 2 -maxdepth 2 -type d | sed 's|/var/db/pkg/||' || echo "Error: Could not list Portage packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for openSUSE
list_opensuse_apps() {
    {
        if command_exists zypper; then
            echo "### Zypper Packages (installed)"
            zypper search --installed-only 2>/dev/null | grep '^i' | awk '{print $3}' || echo "Error: Could not list Zypper packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        if command_exists snap; then
            echo; echo "### Snap Packages"
            snap list 2>/dev/null | tail -n +2 | awk '{print $1}' || echo "No Snap packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for Alpine
list_alpine_apps() {
    {
        if command_exists apk; then
            echo "### APK Packages (installed)"
            apk info 2>/dev/null || echo "Error: Could not list APK packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for Void Linux
list_void_apps() {
    {
        if command_exists xbps-query; then
            echo "### XBPS Packages (installed)"
            xbps-query -l 2>/dev/null | awk '{print $2}' | cut -d'-' -f1 || echo "Error: Could not list XBPS packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Function to list applications for NixOS
list_nixos_apps() {
    {
        if command_exists nix-env; then
            echo "### Nix Packages (user profile)"
            nix-env -q 2>/dev/null || echo "Error: Could not list Nix packages"
        fi

        if command_exists flatpak; then
            echo; echo "### Flatpak Packages"
            flatpak list --app --columns=application 2>/dev/null || echo "No Flatpak packages found"
        fi

        echo; echo "### AppImage Files"
        find ~/ -type f -iname '*.AppImage' 2>/dev/null || echo "No AppImage files found"
    }
}

# Main function to list applications based on distribution
list_applications() {
    local distro="$1"
    
    echo -e "${BLUE}Generating application list for ${GREEN}${distro}${NC}..."
    echo ""
    
    case "$distro" in
        arch)
            list_arch_apps
            ;;
        kali|ubuntu|debian)
            list_debian_apps
            ;;
        fedora|rhel|centos)
            list_fedora_apps
            ;;
        gentoo)
            list_gentoo_apps
            ;;
        opensuse)
            list_opensuse_apps
            ;;
        alpine)
            list_alpine_apps
            ;;
        void)
            list_void_apps
            ;;
        nixos)
            list_nixos_apps
            ;;
        *)
            echo -e "${RED}Error: Unsupported distribution '${distro}'${NC}"
            show_distributions
            exit 1
            ;;
    esac
}

# Main script execution
main() {
    echo -e "${PURPLE}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║      Multi-Distribution App List Generator   ║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════╝${NC}"
    echo ""

    # Check if distribution was provided as argument
    if [ $# -eq 1 ]; then
        distro="$1"
    else
        # Show available distributions
        show_distributions
        
        # Prompt for distribution
        echo -e "${YELLOW}Enter your distribution:${NC} "
        read -r distro
        
        # Validate input
        if [ -z "$distro" ]; then
            echo -e "${RED}Error: No distribution specified${NC}"
            exit 1
        fi
    fi

    # Convert to lowercase
    distro=$(echo "$distro" | tr '[:upper:]' '[:lower:]')

    # Generate application list
    output=$(list_applications "$distro")
    
    # Display output
    echo "$output"
    echo ""

    # Copy to clipboard if possible
    clipboard_cmd=$(get_clipboard_cmd)
    if [ -n "$clipboard_cmd" ]; then
        echo "$output" | $clipboard_cmd
        echo -e "${GREEN}✓ Application list copied to clipboard!${NC}"
    else
        echo -e "${YELLOW}⚠ No clipboard utility found (install xclip, xsel, wl-copy, or pbcopy)${NC}"
        echo -e "${BLUE}Output saved above for manual copying${NC}"
    fi
}

# Run main function with all arguments
main "$@"
