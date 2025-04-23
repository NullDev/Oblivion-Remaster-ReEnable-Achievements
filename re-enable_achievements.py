#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

# ========================= #
# = Copyright (c) NullDev = #
# ========================= #

def locate_save_folder():
    documents = Path.home() / "Documents"
    default_path = documents / "My Games" / "Oblivion Remastered" / "Saved" / "SaveGames"
    if default_path.exists():
        print(f"✅ Save folder found automatically: {default_path}\n")
        return default_path
    else:
        print("⚠️ Save folder not found automatically.")
        return Path(input("Please enter the full path to your SaveGames folder: ").strip())

def patch_bIsAchievementsDisabled(filepath):
    print(f"🔧 Patching {filepath}...\n")
    with open(filepath, "rb") as f:
        data = bytearray(f.read())

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
            # Location of bIsAchievementsDisabled relative to the window
            ach_start = ess_index + ach_index + len(b"bIsAchievementsDisabled")
            prop_index = data.find(b"BoolProperty", ach_start, ach_start + 64)
            if prop_index != -1:
                value_index = prop_index + value_offset
                if value_index < len(data) and data[value_index] != 0x00:
                    data[value_index] = 0x00
                    patches += 1

        index = ess_index + 1

    bak_path = filepath.with_suffix(".sav.BAK")
    shutil.copy2(filepath, bak_path)

    with open(filepath, "wb") as f:
        f.write(data)

    if patches == 0:
        print("❌ No occurrences of bIsAchievementsDisabled found.")
    elif patches == 1:
        print("✅ Patched 1 occurrence of bIsAchievementsDisabled to false.")
    else:
        print(f"✅ Patched {patches} occurrences of bIsAchievementsDisabled to false.")
    print(f"🛡️ Backup saved as: {bak_path}")

def main():
    print("🔧 Oblivion Remastered - Re-enable Achievements Script")
    print("🔧 By NullDev")
    print("🔧 https://github.com/NullDev/Oblivion-Remaster-ReEnable-Achievements\n")

    folder = locate_save_folder()
    file_path = folder / "saves_meta.sav"

    if not file_path.exists():
        print(f"❌ Error: {file_path} does not exist.")
        return

    patch_bIsAchievementsDisabled(file_path)

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
