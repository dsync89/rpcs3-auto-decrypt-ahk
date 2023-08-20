# About

AHK scripts that ON-DEMAND extract your zipped PS3 Encrypted ISO (such as the one downloaded from Erista) from remote storage (e.g. NAS) to your local drive, then decrypt and mount to VirtualDrive. Finally start RPCS3 PS3 Emulator. The AHK script is readily integrated with your favorite frontend such as Launchbox! It also work independantly by simply double clicking the AHK script.

This is useful if you don't want to consume too much storage on your local drive, but rather to only extract and decrypt when you want to launch a game. This is inspired by the way eXoDOS v5 works!

Note:
- Your ROM must be named following [Redump DAT](redump.org/downloads/) format for this to work, due to how the Decryption Disk Key is looked up.

Just like my other repo work on [vita3k-ahk-generator](https://github.com/dsync89/vita3k-ahk-generator), the `AHK` file is the same for all game titles, and variables are read from `.config.ini`.

# Tools Needed

- AutoHotKey, duh!
- DaemonToolsLite

# Quick Start

Start by generating AHK scripts from your source ROM folder.

```
cd scripts
python gen_ahk.py
```

Modify `source_directory` and `destination_directory` in the script as needed.

Then, modify `.config.ini`

```
[Settings]
DaemonToolsCLIPath=C:\Program Files\DAEMON Tools Lite\DTCommandLine.exe
TargetVirtualDriveLetter=Q
UtilsPath=.\utils
EmuPath=C:\Programs\LaunchBox\Emulators\rpcs3-v0.0.28-15213-e2bced97_win64\rpcs3.exe

[RomPath]
SourceRomDir=z:\roms-1g1r\erista-redump-sony-playstation-3-1g1r
ExtractedRomDir=.
```

If both your source and destination ROM dir are the same, then set `.` for both.

Double click any of the AHK file and the script will handle the rest:
1. Extract your ROM.zip from `SourceRomDir` to your ROM dir `ExtractedRomDir` specified in `.config.ini`
2. Find the disc decryption key for your ROM.
3. Decrypt your ROM using `PS3Dec.exe` with the provided disc key.
4. The decrypted ROM will be renamed as `game.dec.iso` first, then it will delete the previously extracted `game.iso`. Finally rename `game.dec.iso` to `game.iso`.
5. Mount the decrypted `game.iso` to virtual drive `Q` via `DaemonToolsCLIPath`.

Pressing `Esc` any time while the script is running will:
- Kill the emulator `rpcs3.exe` process
- Unmount the previously mounted ISO

Your final directory structure for your PS3 roms should be like:
```
|- .config.ini
|- utils
|- Game1.ahk
|- Game2.ahk
...
```

# Credits

Credit to @SarbiaMurloc comment on https://archive.org/details/sony_playstation3_numberssymbols which made automating this workflow possible. Previously I was using the GUI method using `PS3 ISO Patcher` and `IsoTools` which does not have command line interface, and require downloading IRD file from https://ps3.aldostools.org/ird.html. 

```
Reviewer: SarbiaMurloc - favoritefavoritefavoritefavoritefavorite - March 26, 2023
Subject: Play these games on RPCS3
Because RPCS3 does not support loading ISO files, you need to decrypt these ISO files yourself.
1. Download PS3Dec from Github, release or build it by yourself https://github.com/creative-username-ggn/PS3Dec
2. Download keys from 'Sony - PlayStation 3 - Disc Keys TXT' https://archive.org/download/video_game_keys_and_sbi
3. Open your cmd/Terminal/Powershell, enter the working directory, run 'PS3Dec d key xxxxxxxxx(key from last step) redump.iso decrypted.iso'. You need to prefix the command with '. \' while using Powershell.
4. Then extract the decrypted ISO (with 7-zip or else), enjoy it.
```