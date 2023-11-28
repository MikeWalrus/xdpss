# XDPSS
`xdpss` creates a Xdg Desktop Portal ScreenCast Session and outputs the
PipeWire node of the stream.
On Ctrl-C, it closes the session.

# Use Case
Get the PipeWire node number, use gstreamer to mirror the screen, and launch
wemeet in a rootful Xwayland window: see `example/wemeet_with_screencast.sh`
