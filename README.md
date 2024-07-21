# XDPSS
`xdpss` creates a Xdg Desktop Portal ScreenCast Session and outputs the
PipeWire node of the stream.
On Ctrl-C, it closes the session.

# Use Case
Get the PipeWire node number,
use gstreamer to mirror the screen
([`example/xdpss-mirror.sh`](example/xdpss-mirror.sh)` mirror`),
record the screen
([`example/xdpss-mirror.sh`](example/xdpss-mirror.sh)` record record.mp4`)
or launch a rootful XWayland window with screen sharing
([`example/xwayland-rootful-openbox.sh`](example/xwayland-rootful-openbox.sh)).
