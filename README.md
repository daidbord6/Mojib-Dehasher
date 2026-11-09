# Mojib-Ribbon Dehasher

Dehashes the real file names and folder structure of the **Mojib-Ribbon** (モジブリボン, ps2, SCPS-11033) game.

The game's disc stores every file under a hashed name like `8/C72FDB28`, because the disc filesystem only allows 8-character names and 8 levels of folders (im pretty sure). This tool dehashes each file back to its original path, such as `data/common/iopmods/inet.irx`. The full list of 370 known files by spiral (spiralpsych on discord) is in the program, so you don't need a game log or any other file to run it.

## Requirements

You need your own **legally obtained dump of the game**, in one of these types for this:

- a disc image (`.cue` / `.bin`, or `.iso`), or
- a folder of files extracted from the disc with tools like poweriso (the folder with the hashed `0`-`F` subfolders).

**This repo contains no game data.** It does not have any game files in it, disc images or dumps, and none should be uploaded anywhere on this project. It is an unofficial fan tool and is not affiliated with or endorsed by Sony Interactive Entertainment or NanaOn-Sha.

## Using it

Run `MojibDehasher` (or `python mojib_dehasher.py`) and:

1. Choose a **source**: *Folder...* for an extracted folder dump, or *Disc image...* for a `.cue`, `.bin` or `.iso`.
2. Choose an **output** folder (where you want the dehashed files to be).
3. Press **Start** and lmk if it breaks somehow.

Options:

- **test run** shows what would happen if you ran it. Does NOT move or copy anything yet.
- **Move instead of copy** moves files out of your dump folder instead of copying them. It only is for the folder source. Copying is the default option for this.

### Command line

No GUI (there is one but if you don't want it do this):

```
python mojib_dehasher.py <dump folder or .cue/.bin/.iso> <output folder> [--preview] [--move]
```

### What you get

- The game's files under their dev paths (`data/...`) in your chosen output folder.
- Files that are at the root of the disc or dump folder (such as `SYSTEM.CNF` and the game executable) are copied/moved to the root of the output folder.
- Files that aren't on the known list go to `_unlisted/`, so nothing is lost (yes rly).
- Files already in the output folder are not redone, waste of time.
- At the end, it lists files missing from your dump.

Properly dumped disc images are supported. When you pick a folder, the tool finds the hashed folders even if you select a parent folder a few levels up (nice QOL feature).

## How the hashing works in the binary

The hash is the one from the game's own code:

```
h = 0
for each byte b of the full path:
    h = (31 * h + b) & 0xFFFFFFFF
```

The path is the full path as the game has it, for example `data/common/iopmods/inet.irx`, and the hash IS case-sensitive. The hash is written as 8 hex digits, and the folder it goes in is its last hex digit, so `data/common/iopmods/inet.irx` becomes `8/C72FDB28`.

The built-in list was checked with this: all 370 entries match and none of the hashes don't match up.

## Building from source

You need python 3 with tkinter. Builds only run on the OS and CPU they were made on, so build once on each system you want.

- **Windows:** double-click `build_exe.bat`. The result is `dist\MojibDehasher.exe`.
- **macOS (Intel and Apple Silicon) and Linux:** run `bash build_mac_linux.sh`.
  - macOS makes `dist/MojibDehasher.app` plus a zip. App is unsigned, so on first launch unblock it.
  - Linux makes a single executable in `dist/`.


## Credits

- Hash function and the file list: **Spiral**, found by reverse engineering the game's code (I'm pretty sure).
- Tool and build scripts: **daidbord6/mlnecrafter65 + Claude LLM**.
- The idea of recovering names from the PCSX2 debug log came out of the PTR2 modding community's discussions of the game's hashed filesystem so yay discord.

## Disclaimer
This project uses Generative AI to assist it's production, if you aren't okay with that, don't use it or make one yourself. I won't mind if you do, I am not even making this for fame, money, or anything, just a passion for a game I like lol.
