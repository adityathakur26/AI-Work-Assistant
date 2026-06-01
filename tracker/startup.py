import os
import winshell

startup = winshell.startup()

target = r"D:\AI Work Assistant\tracker\tracker.exe"

shortcut = os.path.join(
    startup,
    "AI Work Assistant.lnk"
)