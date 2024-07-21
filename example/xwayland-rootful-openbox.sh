#!/usr/bin/bash

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

main() {
    local xwayland_display="$1"
    if [[ -z $xwayland_display ]]; then
        xwayland_display=:12
    fi

    Xwayland -geometry 1024x768 "$xwayland_display" &

    unset WAYLAND_DISPLAY
    export DISPLAY="$xwayland_display"
    export XIM_PROGRAM=fcitx
    export XIM=fcitx
    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS="@im=fcitx"
    export XDG_SESSION_TYPE=x11

    openbox &
    tint2 &
    picom &
    bash "$__dir"/xdpss-mirror.sh &
}

main "$@"
