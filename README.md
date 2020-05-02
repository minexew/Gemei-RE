# Gemei A330 Archaeology

![photo](https://raw.githubusercontent.com/minexew/Gemei-RE/master/_images/gemei-a330-small.png)

Some links:

- [Executable format (CCDL) description](https://github.com/flatmush/dingoo-sdk/blob/master/dingoo_sdk/doc/CCDL_APP_Format.txt)
- [SDK, examples etc.](https://code.google.com/archive/p/mp4sdk/downloads)
- [USB boot tool](https://github.com/iggarpe/cc1800)
- [Reverse engineering of 7 Days: Salvation](https://github.com/minexew/7days-RE), a game also released on the GA330

## GA330 Specs

Per https://gbatemp.net/threads/gemei-tech-a330-review.277717/#b1:

- CPU - CC1800, ARM-11 @ 600 MHz (Under-clocked to 500 MHz)
- RAM - 64MB
- Internal Storage - 4GB NAND
- External Storage - Mini SD (4-32GB microSD/SDHC via Mini SD adapter)
- Display - 3-inch 320×240 resolution, 16 million colors
- Menu Language - Simplified Chinese, Traditional Chinese, English, Japanese, French, German, Spanish, etc
- Audio Decoding - Cirrus Chipset
- Input - D-Pad, 2 shoulder, 4 face, Start & Select buttons
- Output - video output (TV-OUT), audio output (3.5mm headphone jack)
- Computer Connectivity I/O - USB 2.0
- Battery - Rechargeable 1800mA Li-battery
- Video Formats - 3GP, ASF, AVI (DIVX, H.264, XVID), DAT (VCD format), FLV, MKV, MOV, MP4, MPeG, PMP, RM, RMVB, TP, TS, VOB, WMV
- Playback Compatibility - 1920X1080 Max Resolution
- Display Aspect Ratio - 4:3, 12:11, 10:11, 16:9, 16:11, 40:33, 2.35:1, 1:1
- Audio Formats - AC3, FLAC, MOD, MP3, S3M, WAV, WMA, XM, and LRC lyric files
- Audio Channels - Stereo w/EQ functionality
- E-Book - CHM, HTML, PDB, TXT, UMD, and TTS voice reading mode
- Radio - FM tuner between 76MHZ ~ 108MHZ
- Recording - MP3 and WAV, voice and radio recording
- Photo Viewer - BMP, GIF, JPG, PNG
- Emulation - CPS1, CSP2, GBA, MD, NeoGeo, NES, SNES
- 2-player - Local wireless EMU support between 2 units
- Dimensions 5.31 inches x 2.40 inches x 0.63 inches
- Weight 4.16oz
- Supported O/S – Windows 98SE/ME, 2000, XP

## Q&A

- Main firmware (ccpmp.bin) is loaded @ 0x1050_0000
- RAM is where?
- Reset vectors are where?
- How is firmware booted?
- Text encoding for filenames etc is [GB 2312](https://en.wikipedia.org/wiki/GB_2312)
