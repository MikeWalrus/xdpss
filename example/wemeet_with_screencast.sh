#!/usr/bin/bash

stream-pw-node() {
    local pw_node="$1"
    GST_DEBUG=3 gst-launch-1.0 pipewiresrc path="$pw_node" ! videoconvert ! autovideosink
}

launch() {
    unset WAYLAND_DISPLAY
    export DISPLAY="$xwayland_display"
    export XIM_PROGRAM=fcitx
    export XIM=fcitx
    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS="@im=fcitx"

    openbox &
    sleep 0.5
    picom &
    sleep 0.5
    stream-pw-node "$pw_node" &
    wemeet-x11 &
}

xwayland_display=:12

Xwayland -geometry 1024x768 -retro "$xwayland_display" &

is_first_line=true

PYTHONUNBUFFERED=true xdpss |
    while read -r pw_node; do
        if [[ "$is_first_line" == "true" ]]; then
            launch
        fi
        is_first_line=false
    done
