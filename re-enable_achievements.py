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
    print(f"🔧 Patching {filepath.name} (saves_meta mode)...")
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
            ach_start = ess_index + ach_index + len(b"bIsAchievementsDisabled")
            prop_index = data.find(b"BoolProperty", ach_start, ach_start + 64)
            if prop_index != -1:
                value_index = prop_index + value_offset
                if value_index < len(data) and data[value_index] != 0x00:
                    data[value_index] = 0x00
                    patches += 1

        index = ess_index + 1

    if patches:
        shutil.copy2(filepath, filepath.with_suffix(filepath.suffix + ".BAK"))
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"✅ Patched {patches} occurrence(s). Backup created.")
    else:
        print("❌ No patches applied.")

def patch_quick_autosaves(folder):
    for file in folder.iterdir():
        if file.name.startswith("autosave") or file.name == "quicksave.sav":
            print(f"🔧 Patching {file.name} (quick/autosave mode)...")
            with open(file, "rb") as f:
                data = bytearray(f.read())

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
                shutil.copy2(file, file.with_suffix(file.suffix + ".BAK"))
                with open(file, "wb") as f:
                    f.write(data)
                print("✅ Patch applied. Backup created.")
            else:
                print("❌ No patch needed or pattern not found.")

def main():
    print("🔧 Oblivion Remastered - Re-enable Achievements Script")
    print("🔧 By NullDev")
    print("🔧 https://github.com/NullDev/Oblivion-Remaster-ReEnable-Achievements\n")

    folder = locate_save_folder()
    meta_file = folder / "saves_meta.sav"

    if meta_file.exists():
        patch_bIsAchievementsDisabled(meta_file)
    else:
        print(f"⚠️ {meta_file.name} not found. Skipping.")

    patch_quick_autosaves(folder)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
