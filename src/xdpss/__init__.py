#!/usr/bin/env python3

from typing import Any, Dict
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

import sys
import time


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ScreenCast:
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()
        self.my_name = self.bus.get_connection().get_unique_name()[1:].replace(".", "_")
        self.session_token = "my_session_token"
        desktop = self.bus.get_object(
            "org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop"
        )
        self.interface = dbus.Interface(desktop, "org.freedesktop.portal.ScreenCast")
        self.session_handle = None
        eprint(f"[INFO] My name: {self.my_name}")

    def start_stream(self):
        token = "start"
        response_path = self.response_path(token)

        def handler(response, results):
            if response != 0:
                eprint("[ERROR] Failed to start stream.")
                return
            eprint("[INFO] Started a stream.")
            pipewire_node = results["streams"][0][0]
            eprint(f"[INFO] PipeWire Node: {pipewire_node}")
            print(pipewire_node)

        self.bus.add_signal_receiver(
            handler,
            dbus_interface="org.freedesktop.portal.Request",
            path=response_path,
        )

        self.interface.Start(self.session_handle, "", {"handle_token": token})
        pass

    def start(self):
        token = "select_sources"
        response_path = self.response_path(token)

        def handler(response, _results):
            if response != 0:
                eprint("[ERROR] Failed to select sources.")
                return
            eprint("[INFO] Select sources done.")
            self.start_stream()

        self.bus.add_signal_receiver(
            handler,
            dbus_interface="org.freedesktop.portal.Request",
            path=response_path,
        )
        self.interface.SelectSources(self.session_handle, {"handle_token": token})

    def start_session(self):
        def create_session_handler(response, results: Dict[str, Any]):
            if response != 0:
                eprint("[ERROR] invalid response")
                return
            eprint("[INFO] Session created.")
            self.session_handle = results["session_handle"]
            self.start()

        token = "create_session"
        response_path = self.response_path(token)
        self.bus.add_signal_receiver(
            create_session_handler,
            dbus_interface="org.freedesktop.portal.Request",
            path=response_path,
        )

        options = {
            "handle_token": token,
            "session_handle_token": self.session_token,
        }
        self.interface.CreateSession(options)

    def response_path(self, token) -> str:
        return f"/org/freedesktop/portal/desktop/request/{self.my_name}/{token}"

    def close(self):
        session_object = self.bus.get_object(
            "org.freedesktop.portal.Desktop", self.session_handle
        )
        session = dbus.Interface(session_object, "org.freedesktop.portal.Session")
        session.Close()
        eprint("[INFO] Session closed.")


def main():
    screen_cast = ScreenCast()
    screen_cast.start_session()
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        time.sleep(1)
        screen_cast.close()
        loop.quit()


if __name__ == "__main__":
    main()
