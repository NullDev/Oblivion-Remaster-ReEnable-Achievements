#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import time
from pathlib import Path

# ========================= #
# = Copyright (c) NullDev = #
# ========================= #

def read_file(filepath: Path) -> bytearray:
    try:
        with open(filepath, "rb") as f:
            data = bytearray(f.read())
        return data
    except PermissionError:
        print(f"❌ Unable to read {filepath.name}, check permissions.")
    except Exception as exc:
        print(f"❌ Unknown error occurred accessing {filepath.name}: {exc}.")
    return None

def write_file(filepath: Path, data: bytearray) -> None:
    try:
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"✅ Patched {filepath.name}. Backup created.")
    except PermissionError:
        print(f"❌ Unable to write to {filepath.name}, check permissions.")
    except Exception as exc:
        print(f"❌ Unknown error occurred writing to {filepath.name}: {exc}.")

def locate_save_folder() -> Path:
    documents = Path.home() / "Documents"
    default_path = documents / "My Games" / "Oblivion Remastered" / "Saved" / "SaveGames"

    linux_path = Path.home() / ".local" / "share" / "Steam" / "steamapps" / \
                 "compatdata" / "2623190" / "pfx" / "drive_c" / "users" / "steamuser" / "Documents" / \
                 "My Games" / "Oblivion Remastered" / "Saved" / "SaveGames"

    gamepass_path = Path.home() / "AppData" / "Local" / "Packages" / \
                    "BethesdaSoftworks.ProjectAltar_3275kfvn8vcwc" / "SystemAppData" / \
                    "wgs" / "00090000040802E4_0000000000000000000000006516997E"

    if os.name == 'nt':
        if default_path.exists():
            print(f"✅ Save folder found automatically: {default_path}\n")
            return default_path
        elif gamepass_path.exists():
            print(f"✅ Gamepass save folder found automatically: {gamepass_path}\n")
            return gamepass_path
    elif os.name == 'posix':
        if linux_path.exists():
            print(f"✅ Save directory found automatically: {linux_path}\n")
            return linux_path

    while True:
        print("⚠️ Save folder not found automatically or system not detected.")
        path = Path(input("Please enter the full path to your SaveGames folder: ").strip())
        if path.exists():
            return path

def patch_bIsAchievementsDisabled(filepath: Path) -> None:
    print(f"🔧 Patching {filepath.name} (saves_meta mode)...")
    data = read_file(filepath)
    if not data:
        return

    value_offset = 21  # Offset from BoolProperty to value byte
    patches = 0
    index = 0

    while index < len(data):
        ess_index = data.find(b"bIsESS", index)
        if ess_index == -1:
            break

        window = data[ess_index:ess_index + 256]
        need_index = window.find(b"bNeedTheWholeGameDownloaded")
        ach_index = window.find(b"bIsAchievementsDisabled")

        if need_index != -1 and ach_index != -1 and need_index < ach_index:
            ach_start = ess_index + ach_index + len(b"bIsAchievementsDisabled")
            prop_index = data.find(b"BoolProperty", ach_start, ach_start + 64)
            if prop_index != -1:
                value_index = prop_index + value_offset
                if value_index < len(data) and data[value_index] != 0x00:
                    data[value_index] = 0x00
                    patches += 1

        index = ess_index + 1

    if patches:
        shutil.copy2(filepath, filepath.with_suffix(filepath.suffix + f".BAK{int(time.time())}"))
        write_file(filepath, data)
    else:
        print("❌ No patches applied.\n")

def patch_quick_autosaves(folder: Path) -> None:
    for file in folder.iterdir():
        if (file.name.startswith("autosave") or file.name == "quicksave.sav") and not ".BAK" in file.name:
            print(f"🔧 Patching {file.name} (quick/autosave mode)...")
            data = read_file(file)
            if not data:
                continue

            patched = False
            idx = 0

            while True:
                idx = data.find(b"bIsAchievementsDisabledBool", idx)
                if idx == -1:
                    break

                end_idx = idx + len(b"bIsAchievementsDisabledBool")
                if data[end_idx] == 0x00 and end_idx + 1 < len(data):
                    value_index = end_idx + 1
                    if data[value_index] == 0x01:
                        data[value_index] = 0x00
                        patched = True
                idx = end_idx

            if patched:
                shutil.copy2(file, file.with_suffix(file.suffix + f".BAK{int(time.time())}"))
                write_file(file, data)
            else:
                print("❌ No patch needed or pattern not found.")

        elif file.name.startswith("Save ") and not ".BAK" in file.name:
            print(f"🔧 Patching {file.name} (manual save mode)...")
            data = read_file(file)
            if not data:
                continue

            patched = False
            idx = 0

            while True:
                idx = data.find(b"bIsAchievementsDisabled", idx)
                if idx == -1:
                    break

                bool_pattern = b"\x00\x0D\x00Bool"
                start = idx + len(b"bIsAchievementsDisabled")

                if data[start:start + len(bool_pattern)] == bool_pattern:
                    value_index = start + len(bool_pattern)
                    if value_index < len(data) and data[value_index] == 0x01:
                        data[value_index] = 0x00
                        patched = True
                idx = start

            if patched:
                shutil.copy2(file, file.with_suffix(file.suffix + f".BAK{int(time.time())}"))
                write_file(file, data)
            else:
                print("❌ No patch needed or pattern not found.")

def main() -> None:
    print("🔧 Oblivion Remastered - Re-enable Achievements Script")
    print("🔧 By NullDev")
    print("🔧 https://github.com/NullDev/Oblivion-Remaster-ReEnable-Achievements\n")

    folder = locate_save_folder()
    meta_file = folder / "saves_meta.sav"

    if meta_file.exists():
        patch_bIsAchievementsDisabled(meta_file)
    else:
        print(f"⚠️ {meta_file.name} not found. Skipping.\n")

    patch_quick_autosaves(folder)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
