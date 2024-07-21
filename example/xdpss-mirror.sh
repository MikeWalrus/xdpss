#! /usr/bin/bash

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

main() {
    local is_first_line=true

    while read -r pw_node; do
        if [[ "$is_first_line" == "true" ]]; then
            bash "$__dir"/stream-pw-node.sh "$pw_node" "$@"
            return
        fi
        is_first_line=false
    done < <(PYTHONUNBUFFERED=true xdpss)
}

main "$@"
