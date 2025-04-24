# Oblivion-Remaster-ReEnable-Achievements
This script Re-Enables the achievements on all your current saves, after you e.g. used Console commands. <br>
It's a python script that goes through all your save files and re-enables achievements for all of them.

---

**IMPORTANT**: <br>

The script won't prevent them from being disabled again. But you can always re-run it.
You can also use it in combination with https://www.nexusmods.com/oblivionremastered/mods/125 to enable achievements on your existing saves.

Also, it appears this currently does NOT work on the gamepass version.

If you get a virus warning, those are false positives. To make it easier to use, I packed the python script as an EXE so that people don't have to use the Terminal. The code is fully open source (link at the bottom). I talked to nexus about the false detections, so they reviewed it for me and approved it.

---

**Usage:** <br>
- [Download the ZIP](https://github.com/NullDev/Oblivion-Remaster-ReEnable-Achievements/releases/download/1.2.4/re-enable_achievements.zip)
- Extract it anywhere
- Run `re-enable_achievements.exe`
  - If prompted, enter path to your saves.
  - Usually: `C:\Users\<USERNAME>\Documents\My Games\Oblivion Remastered\Saved\SaveGames` 

---

Or, Usage for Devs: 
- Make sure to have [Python3](https://www.python.org/downloads/) installed.
- Download the script to wherever you want.
  - Either from [GitHub](https://raw.githubusercontent.com/NullDev/Oblivion-Remaster-ReEnable-Achievements/refs/heads/master/re-enable_achievements.py)
  - Or from [Nexus Mods](https://www.nexusmods.com/oblivionremastered/mods/112?tab=files)
- Run it using `python3 re-enable_achievements.py`
  - If prompted, enter path to your saves.
  - Usually: `C:\Users\<USERNAME>\Documents\My Games\Oblivion Remastered\Saved\SaveGames`
- Done!

---

**How does it work:**<br>

The game stores flags about disable achievements in all save files. There are autosave/quicksave, manual saves and a file called saves_meta.sav (which stores info about all saves). All of these different saves use a different format to handle this achievement flag. e.g. saves_meta: 

```
bIsESS 
   BoolProperty              bNeedTheWholeGameDownloaded 
   BoolProperty             bIsAchievementsDisabled 
   BoolProperty              SaveHash    StrProperty
```

where "BoolProperty" always comes after the flag name. So the script searches the entire window starting from bIsESS to get the correct offset. <br>
For the manual saves it was pretty easy, you have "FlagName 00 0D 00 Bool XX" where XX was the actual flag. Like, Bool00 for false and Bool01 for true. 

![image](https://github.com/user-attachments/assets/cf075a65-0738-4c3f-8320-bbbfeb0cdb6a)

---

Nexus Mods Page: https://www.nexusmods.com/oblivionremastered/mods/112
