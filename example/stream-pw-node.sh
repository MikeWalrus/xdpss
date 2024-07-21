#! /usr/bin/bash

main() {
    declare pw_node="$1"
    declare cmd="$2"

    declare -a pipeline

    if [[ -z $cmd ]]; then
        cmd=mirror
        echo "Defaulting to mirror"
    fi

    if [[ $cmd == mirror ]]; then
        pipeline=(autovideosink)
    elif [[ $cmd == record ]]; then
        declare filepath="$3"
        if [[ -z $filepath ]]; then
            filepath=$(xdg-user-dir VIDEOS)/$(date --iso-8601=seconds).mp4
        fi
        pipeline=(vaapih264enc ! h264parse ! mp4mux ! filesink location="$filepath")
    fi
    set -x
    gst-launch-1.0 -e pipewiresrc path="$pw_node" ! videoconvert ! "${pipeline[@]}"
    set +x
}

main "$@"
