import os
import re
import sys
import shutil
import struct
import threading
import queue

APP_TITLE = "Mojib-Ribbon Dehasher"

FILE_LIST = r"""
data/common.pak -> C/48F3299C
data/common/font/dfp5.cft -> B/5FFE55AB
data/common/font/dfp5v.cft -> 1/A3AAD7D1
data/common/icon/rapdata01.ico -> C/1EAC659C
data/common/icon/rapdata02.ico -> D/1EBA7D1D
data/common/icon/rapdata03.ico -> E/1EC8949E
data/common/icon/rapdata04.ico -> F/1ED6AC1F
data/common/icon/rapdata05.ico -> 0/1EE4C3A0
data/common/icon/rapdata06.ico -> 1/1EF2DB21
data/common/icon/rapdata07.ico -> 2/1F00F2A2
data/common/icon/rapdata08.ico -> 3/1F0F0A23
data/common/icon/rapdata09.ico -> 4/1F1D21A4
data/common/icon/rapdata10.ico -> A/205326BA
data/common/icon/rapdata11.ico -> B/20613E3B
data/common/icon/rapdata12.ico -> C/206F55BC
data/common/icon/rapdata13.ico -> D/207D6D3D
data/common/icon/rapdata14.ico -> E/208B84BE
data/common/icon/rapdata15.ico -> F/20999C3F
data/common/icon/rapdata16.ico -> 0/20A7B3C0
data/common/icon/rapdata17.ico -> 1/20B5CB41
data/common/icon/rapdata18.ico -> 2/20C3E2C2
data/common/icon/system.ico -> D/7D41658D
data/common/icon/textdata01.ico -> 6/706AC5F6
data/common/icon/textdata02.ico -> 7/7078DD77
data/common/icon/textdata03.ico -> 8/7086F4F8
data/common/icon/textdata04.ico -> 9/70950C79
data/common/icon/textdata05.ico -> A/70A323FA
data/common/icon/textdata06.ico -> B/70B13B7B
data/common/icon/textdata07.ico -> C/70BF52FC
data/common/icon/textdata08.ico -> D/70CD6A7D
data/common/icon/textdata09.ico -> E/70DB81FE
data/common/icon/textdata10.ico -> 4/72118714
data/common/icon/textdata11.ico -> 5/721F9E95
data/common/icon/textdata12.ico -> 6/722DB616
data/common/icon/textdata13.ico -> 7/723BCD97
data/common/icon/textdata14.ico -> 8/7249E518
data/common/icon/textdata15.ico -> 9/7257FC99
data/common/icon/textdata16.ico -> A/7266141A
data/common/icon/textdata17.ico -> B/72742B9B
data/common/icon/textdata18.ico -> C/7282431C
data/common/iopmods/FileUtil.irx -> 2/B980AFD2
data/common/iopmods/IopStd.irx -> D/E1C8F92D
data/common/iopmods/SndServ.irx -> D/43088B0D
data/common/iopmods/ToolsMod.irx -> B/B46BDADB
data/common/iopmods/dbcman.irx -> 9/1721D8E9
data/common/iopmods/dev9.irx -> 8/FD74DD58
data/common/iopmods/ds1o_s1.irx -> E/7F2989FE
data/common/iopmods/ezmidi.irx -> A/31E09A2A
data/common/iopmods/inet.irx -> 8/C72FDB28
data/common/iopmods/inetctl.irx -> 5/A00B6F15
data/common/iopmods/inetlog.irx -> E/7354D3BE
data/common/iopmods/ioprp.img -> A/CCAEABEA
data/common/iopmods/libnet.irx -> C/9B7968CC
data/common/iopmods/libsd.irx -> 4/36A96D64
data/common/iopmods/mcman.irx -> 2/83610AD2
data/common/iopmods/mcserv.irx -> 0/364F5480
data/common/iopmods/modhsyn.irx -> 0/CC1D3FF0
data/common/iopmods/modmidi.irx -> 1/9E689531
data/common/iopmods/msifrpc.irx -> 0/6DF9FA50
data/common/iopmods/netcnf.irx -> 2/49817F72
data/common/iopmods/netcnfif.irx -> F/5383FDCF
data/common/iopmods/ntgui2.irx -> 1/5FDFE271
data/common/iopmods/padman.irx -> B/5E2FE43B
data/common/iopmods/ppp.irx -> E/11436E7E
data/common/iopmods/pppoe.irx -> 4/3CB55614
data/common/iopmods/sdrdrv.irx -> B/E785021B
data/common/iopmods/sio2d.irx -> 9/854E7859
data/common/iopmods/sio2man.irx -> F/9ED8654F
data/common/iopmods/smap.irx -> D/9A09A01D
data/common/iopmods/usbd.irx -> 4/A83D1BF4
data/common/iopmods/usbkb.irx -> 9/6E1A2129
data/common/mbl/bbunit.tm2 -> 6/0A2A7546
data/common/rap/01.sht -> F/3CE8287F
data/common/rap/01.txt -> 0/3CE82E30
data/common/rap/02.sht -> 0/3CF64000
data/common/rap/02.txt -> 1/3CF645B1
data/common/rap/03.sht -> 1/3D045781
data/common/rap/03.txt -> 2/3D045D32
data/common/rap/04.sht -> 2/3D126F02
data/common/rap/04.txt -> 3/3D1274B3
data/common/rap/05.sht -> 3/3D208683
data/common/rap/05.txt -> 4/3D208C34
data/common/rap/06.sht -> 4/3D2E9E04
data/common/rap/06.txt -> 5/3D2EA3B5
data/common/rap/07.sht -> 5/3D3CB585
data/common/rap/07.txt -> 6/3D3CBB36
data/common/rap/08.sht -> 6/3D4ACD06
data/common/rap/08.txt -> 7/3D4AD2B7
data/common/rap/09.sht -> 7/3D58E487
data/common/rap/09.txt -> 8/3D58EA38
data/common/rap/10.sht -> D/3E8EE99D
data/common/rap/10.txt -> E/3E8EEF4E
data/common/rap/11.sht -> E/3E9D011E
data/common/rap/11.txt -> F/3E9D06CF
data/common/rap/12.sht -> F/3EAB189F
data/common/rap/12.txt -> 0/3EAB1E50
data/common/rap/13.sht -> 0/3EB93020
data/common/rap/13.txt -> 1/3EB935D1
data/common/rap/14.sht -> 1/3EC747A1
data/common/rap/14.txt -> 2/3EC74D52
data/common/rap/15.sht -> 2/3ED55F22
data/common/rap/15.txt -> 3/3ED564D3
data/common/rap/16.sht -> 3/3EE376A3
data/common/rap/16.txt -> 4/3EE37C54
data/common/rap/17.sht -> 4/3EF18E24
data/common/rap/17.txt -> 5/3EF193D5
data/common/rap/18.sht -> 5/3EFFA5A5
data/common/rap/18.txt -> 6/3EFFAB56
data/common/rap/extra/01.txt -> F/7CE2734F
data/common/rap/extra/02.txt -> 0/7CF08AD0
data/common/rap/extra/03.txt -> 1/7CFEA251
data/common/rap/extra/04.txt -> 2/7D0CB9D2
data/common/rap/extra/05.txt -> 3/7D1AD153
data/common/rap/extra/06.txt -> 4/7D28E8D4
data/common/rap/extra/07.txt -> 5/7D370055
data/common/rap/extra/08.txt -> 6/7D4517D6
data/common/rap/extra/09.txt -> 7/7D532F57
data/common/rap/extra/10.sht -> C/7E892EBC
data/common/rap/extra/10.txt -> D/7E89346D
data/common/rap/extra/11.sht -> D/7E97463D
data/common/rap/extra/11.txt -> E/7E974BEE
data/common/rap/extra/12.txt -> F/7EA5636F
data/common/rap/extra/13.sht -> F/7EB3753F
data/common/rap/extra/13.txt -> 0/7EB37AF0
data/common/rap/extra/14.sht -> 0/7EC18CC0
data/common/rap/extra/14.txt -> 1/7EC19271
data/common/rap/extra/15.sht -> 1/7ECFA441
data/common/rap/extra/15.txt -> 2/7ECFA9F2
data/common/rap/extra/16.sht -> 2/7EDDBBC2
data/common/rap/extra/16.txt -> 3/7EDDC173
data/common/rap/extra/17.sht -> 3/7EEBD343
data/common/rap/extra/17.txt -> 4/7EEBD8F4
data/common/rap/extra/18.sht -> 4/7EF9EAC4
data/common/rap/extra/18.txt -> 5/7EF9F075
data/common/textures.pak -> 3/6B19DC23
data/common/vrs.pak -> 4/A49D4444
data/common/vrs/22khz-r/fsw22m04.apr -> 0/BBBF3280
data/common/vrs/22khz-r/mym22m02.apr -> 7/E3FC4E67
data/common/vrs_game.pak -> 5/F6550265
data/common/vrs_menu.pak -> 2/3BCB4D52
data/editor.pak -> E/A594901E
data/editor/sap/edit_help001.sap -> 9/FE643699
data/editor/sap/edit_help002.sap -> A/FE724E1A
data/editor/sap/edit_help003.sap -> B/FE80659B
data/editor/sap/edit_help004.sap -> C/FE8E7D1C
data/editor/sap/edit_help005.sap -> D/FE9C949D
data/editor/sap/edit_help006.sap -> E/FEAAAC1E
data/editor/sap/edit_help007.sap -> F/FEB8C39F
data/editor/sap/edit_help008.sap -> 0/FEC6DB20
data/editor/sap/edit_help009.sap -> 1/FED4F2A1
data/editor/sap/edit_help010.sap -> 7/000AF7B7
data/editor/sap/edit_help011.sap -> 8/00190F38
data/editor/sap/edit_help012.sap -> 9/002726B9
data/editor/sap/edit_help013.sap -> A/00353E3A
data/editor/sap/edit_help014.sap -> B/004355BB
data/editor/sap/edit_help015.sap -> C/00516D3C
data/editor/sound/editor.bd -> 6/0BC7E2C6
data/editor/textures.pak -> 1/03F6A7E1
data/game.pak -> 3/EBFF0D63
data/game/sound/main.bd -> F/7AF9B2BF
data/game/stages/01.pak -> F/5715246F
data/game/stages/02.pak -> 0/57233BF0
data/game/stages/03.pak -> 1/57315371
data/game/stages/04.pak -> 2/573F6AF2
data/game/stages/05.pak -> 3/574D8273
data/game/stages/06.pak -> 4/575B99F4
data/game/stages/07.pak -> 5/5769B175
data/game/stages/08.pak -> 6/5777C8F6
data/game/stages/09.pak -> 7/5785E077
data/game/stages/10.pak -> D/58BBE58D
data/game/stages/11.pak -> E/58C9FD0E
data/game/stages/12.pak -> F/58D8148F
data/game/stages/13.pak -> 0/58E62C10
data/game/stages/14.pak -> 1/58F44391
data/game/stages/15.pak -> 2/59025B12
data/game/stages/16.pak -> 3/59107293
data/game/stages/17.pak -> 4/591E8A14
data/game/stages/18.pak -> 5/592CA195
data/game/textures.pak -> C/08D4483C
data/menu.pak -> 0/31755850
data/menu/dnas/authdata -> A/59E3059A
data/menu/logo/7on_logo.tm2 -> 8/578C8518
data/menu/logo/kiyaku1.tm2 -> 3/2DAC6A73
data/menu/logo/kiyaku2.tm2 -> 4/2DBA81F4
data/menu/logo/kiyaku3.tm2 -> 5/2DC89975
data/menu/logo/kiyaku4.tm2 -> 6/2DD6B0F6
data/menu/logo/kiyaku5.tm2 -> 7/2DE4C877
data/menu/logo/kiyaku6.tm2 -> 8/2DF2DFF8
data/menu/logo/kiyaku7.tm2 -> 9/2E00F779
data/menu/logo/kiyaku8.tm2 -> A/2E0F0EFA
data/menu/logo/scelogo2.tm2 -> 6/B6186716
data/menu/serial/clear.pak -> 9/0D593129
data/menu/serial/clear/textures.pak -> 6/C7FF0336
data/menu/serial/fudehen.pak -> D/C8FDDC5D
data/menu/serial/mil.pak -> C/AB3793AC
data/menu/serial/mil/textures.pak -> 3/02C3C413
data/menu/serial/opening.pak -> 4/BEA726B4
data/menu/serial/opening/textures.pak -> B/2A751A0B
data/menu/serial/over.pak -> 0/32DCC6D0
data/menu/serial/over/textures.pak -> F/409BD96F
data/menu/serial/shinri.pak -> D/E3A9A16D
data/menu/serial/shinri/textures.pak -> 2/10AE9F72
data/menu/serial/tutorial.pak -> A/A139B85A
data/menu/serial/tutorial/sound/main.bd -> 6/F71054F6
data/menu/serial/tutorial/textures.pak -> 5/0CD50325
data/menu/sound/menu.bd -> 6/DF720006
data/menu/speech/alert/a_414.sap -> 8/AE7AA698
data/menu/speech/alert/a_421.sap -> 4/B00538B4
data/menu/speech/alert/a_422.sap -> 5/B0135035
data/menu/speech/alert/mc001.sap -> A/6BBC81FA
data/menu/speech/alert/mc002_1.sap -> D/F36E766D
data/menu/speech/alert/mc002_2.sap -> E/F37C8DEE
data/menu/speech/alert/mc002_3.sap -> F/F38AA56F
data/menu/speech/alert/mc002_4.sap -> 0/F398BCF0
data/menu/speech/alert/mc002_5.sap -> 1/F3A6D471
data/menu/speech/alert/mc003_1.sap -> E/2854B1AE
data/menu/speech/alert/mc003_2.sap -> F/2862C92F
data/menu/speech/alert/mc003_3.sap -> 0/2870E0B0
data/menu/speech/alert/mc003_4.sap -> 1/287EF831
data/menu/speech/alert/mc003_5.sap -> 2/288D0FB2
data/menu/speech/alert/mc004.sap -> D/6BE6C87D
data/menu/speech/alert/mc005.sap -> E/6BF4DFFE
data/menu/speech/alert/mc007.sap -> 0/6C110F00
data/menu/speech/alert/mc008.sap -> 1/6C1F2681
data/menu/speech/alert/mc009.sap -> 2/6C2D3E02
data/menu/speech/alert/mc011.sap -> 9/6D715A99
data/menu/speech/alert/mc014.sap -> C/6D9BA11C
data/menu/speech/alert/mc015.sap -> D/6DA9B89D
data/menu/speech/alert/mc016.sap -> E/6DB7D01E
data/menu/speech/alert/mc017.sap -> F/6DC5E79F
data/menu/speech/alert/mc018.sap -> 0/6DD3FF20
data/menu/speech/alert/mc019.sap -> 1/6DE216A1
data/menu/speech/alert/mc020.sap -> 7/6F181BB7
data/menu/speech/alert/mc021.sap -> 8/6F263338
data/menu/speech/alert/mc022.sap -> 9/6F344AB9
data/menu/speech/alert/mc024.sap -> B/6F5079BB
data/menu/speech/alert/mc025.sap -> C/6F5E913C
data/menu/speech/alert/mc026.sap -> D/6F6CA8BD
data/menu/speech/alert/mc027.sap -> E/6F7AC03E
data/menu/speech/alert/mc028.sap -> F/6F88D7BF
data/menu/speech/alert/ne_01.sap -> 8/86082BA8
data/menu/speech/alert/ne_02.sap -> 9/86164329
data/menu/speech/alert/ne_03.sap -> A/86245AAA
data/menu/speech/alert/ne_04.sap -> B/8632722B
data/menu/speech/alert/ne_05.sap -> C/864089AC
data/menu/speech/alert/ne_06.sap -> D/864EA12D
data/menu/speech/alert/ne_07.sap -> E/865CB8AE
data/menu/speech/alert/ne_08.sap -> F/866AD02F
data/menu/speech/alert/ne_09.sap -> 0/8678E7B0
data/menu/speech/alert/ne_10.sap -> 6/87AEECC6
data/menu/speech/alert/ne_11.sap -> 7/87BD0447
data/menu/speech/alert/ne_12n.sap -> E/74FF220E
data/menu/speech/alert/ne_13.sap -> 9/87D93349
data/menu/speech/alert/ne_14.sap -> A/87E74ACA
data/menu/speech/alert/ne_15.sap -> B/87F5624B
data/menu/speech/alert/ne_16.sap -> C/880379CC
data/menu/speech/alert/ne_17.sap -> D/8811914D
data/menu/speech/alert/ne_18.sap -> E/881FA8CE
data/menu/speech/alert/ne_19.sap -> F/882DC04F
data/menu/speech/alert/ne_20n.sap -> 1/A67BAC11
data/menu/speech/alert/ne_21.sap -> 6/8971DCE6
data/menu/speech/alert/ne_22.sap -> 7/897FF467
data/menu/speech/alert/ne_23.sap -> 8/898E0BE8
data/menu/speech/alert/ne_24.sap -> 9/899C2369
data/menu/speech/alert/ne_25.sap -> A/89AA3AEA
data/menu/speech/alert/ne_26.sap -> B/89B8526B
data/menu/speech/alert/ne_27.sap -> C/89C669EC
data/menu/speech/alert/ne_28.sap -> D/89D4816D
data/menu/speech/alert/ne_29.sap -> E/89E298EE
data/menu/speech/alert/ne_30.sap -> 4/8B189E04
data/menu/speech/alert/ne_31.sap -> 5/8B26B585
data/menu/speech/alert/ne_32n.sap -> 0/DECB9890
data/menu/speech/alert/ne_33.sap -> 7/8B42E487
data/menu/speech/alert/ne_34.sap -> 8/8B50FC08
data/menu/speech/help/help001.sap -> 8/B0A37F98
data/menu/speech/help/help002.sap -> 9/B0B19719
data/menu/speech/help/help003.sap -> A/B0BFAE9A
data/menu/speech/help/help004.sap -> B/B0CDC61B
data/menu/speech/help/help005.sap -> C/B0DBDD9C
data/menu/speech/help/help006.sap -> D/B0E9F51D
data/menu/speech/help/help007.sap -> E/B0F80C9E
data/menu/speech/help/help008.sap -> F/B106241F
data/menu/speech/help/help010.sap -> 6/B24A40B6
data/menu/speech/help/help011.sap -> 7/B2585837
data/menu/speech/help/help012.sap -> 8/B2666FB8
data/menu/speech/help/help013.sap -> 9/B2748739
data/menu/speech/help/help014.sap -> A/B2829EBA
data/menu/speech/help/help015.sap -> B/B290B63B
data/menu/speech/help/help016.sap -> C/B29ECDBC
data/menu/speech/help/help017.sap -> D/B2ACE53D
data/menu/speech/help/help019.sap -> F/B2C9143F
data/menu/speech/help/help020.sap -> 5/B3FF1955
data/menu/speech/help/help021.sap -> 6/B40D30D6
data/menu/speech/help/help022.sap -> 7/B41B4857
data/menu/speech/help/help024.sap -> 9/B4377759
data/menu/speech/help/help025.sap -> A/B4458EDA
data/menu/speech/help/help026.sap -> B/B453A65B
data/menu/speech/help/help027.sap -> C/B461BDDC
data/menu/speech/help/help028n.sap -> 9/DCF19B19
data/menu/speech/help/help029.sap -> E/B47DECDE
data/menu/speech/help/help030.sap -> 4/B5B3F1F4
data/menu/speech/help/help031.sap -> 5/B5C20975
data/menu/speech/help/help032.sap -> 6/B5D020F6
data/menu/speech/help/help033.sap -> 7/B5DE3877
data/menu/speech/help/help034.sap -> 8/B5EC4FF8
data/menu/speech/narration/st00.sap -> 4/1F8D9504
data/menu/speech/narration/st01.sap -> 5/1F9BAC85
data/menu/speech/narration/st02.sap -> 6/1FA9C406
data/menu/speech/narration/st03.sap -> 7/1FB7DB87
data/menu/speech/narration/st04_1.sap -> A/95F9A0BA
data/menu/speech/narration/st04_2.sap -> B/9607B83B
data/menu/speech/narration/st05_1.sap -> B/CADFDBFB
data/menu/speech/narration/st05_2.sap -> C/CAEDF37C
data/menu/speech/narration/st06_1.sap -> C/FFC6173C
data/menu/speech/narration/st06_2.sap -> D/FFD42EBD
data/menu/speech/narration/st07.sap -> B/1FF0398B
data/menu/speech/narration/st08_1.sap -> E/69928DBE
data/menu/speech/narration/st08_2.sap -> F/69A0A53F
data/menu/speech/narration/st09_1.sap -> F/9E78C8FF
data/menu/speech/narration/st09_2.sap -> 0/9E86E080
data/menu/speech/narration/st10_1_1.sap -> 7/F1305F07
data/menu/speech/narration/st10_1_2.sap -> 8/F13E7688
data/menu/speech/narration/st10_2.sap -> 6/2A4FF816
data/menu/speech/narration/st11.sap -> 4/21508524
data/menu/speech/narration/st12_1.sap -> 7/940E5717
data/menu/speech/narration/st12_2.sap -> 8/941C6E98
data/menu/speech/narration/st13.sap -> 6/216CB426
data/menu/speech/narration/st13_3.sap -> A/C910C15A
data/menu/speech/narration/st14.sap -> 7/217ACBA7
data/menu/speech/narration/st14_3_2.sap -> E/AC1CA90E
data/menu/speech/narration/st15.sap -> 8/2188E328
data/menu/speech/narration/st16.sap -> 9/2196FAA9
data/menu/speech/narration/st17.sap -> A/21A5122A
data/menu/speech/narration/st18_1.sap -> D/D173BA9D
data/menu/speech/narration/st18_1_3.sap -> 1/93700611
data/menu/speech/narration/st18_2_1.sap -> 0/C83A1250
data/menu/speech/narration/st18_2_2_2.sap -> 4/26D760C4
data/menu/speech/narration/st19.sap -> C/21C1412C
data/menu/speech/narration/st20.sap -> 2/22F74642
data/menu/speech/narration/st21.sap -> 3/23055DC3
data/menu/speech/narration/st22.sap -> 4/23137544
data/menu/speech/narration/st23.sap -> 5/23218CC5
data/menu/speech/narration/st24.sap -> 6/232FA446
data/menu/speech/narration/st25_1.sap -> 9/9AA235B9
data/menu/speech/narration/st25_2.sap -> A/9AB04D3A
data/menu/speech/narration/st26.sap -> 8/234BD348
data/menu/textures.pak -> F/EACEF7EF
data/menu/vsa/dan.vsa -> 1/177CBEB1
data/menu/vsa/kan.vsa -> 8/89C85D78
data/menu/vsa/man.vsa -> A/F394D3FA
data/menu/vsa/ten.vsa -> D/6CB3D53D
data/netgui2/SYS_NET.ICO -> 2/2993E0F2
data/netgui2/bg.rgb -> 4/04BAF9A4
data/netgui2/bg2.rgb -> C/92BDD9EC
data/netgui2/eff.bd -> B/09E3E0EB
data/netgui2/eff.hd -> 5/09E3E1A5
data/netgui2/icon.sys -> 8/340B75D8
data/netgui2/japanese.pf -> 3/9D1E5B53
data/netgui2/jis2ucs.bin -> 0/58A9A3E0
data/netgui2/ucs2jis.bin -> 0/C91D3360
data/xeditor.pak -> C/B93E242C
data/xeditor/sound/rap_help001.sap -> 7/218935D7
data/xeditor/sound/rap_help002.sap -> 8/21974D58
data/xeditor/sound/rap_help003.sap -> 9/21A564D9
data/xeditor/sound/rap_help004.sap -> A/21B37C5A
data/xeditor/sound/rap_help005.sap -> B/21C193DB
data/xeditor/sound/rap_help006.sap -> C/21CFAB5C
data/xeditor/sound/rap_help007.sap -> D/21DDC2DD
data/xeditor/sound/se.bd -> F/4714DF4F
data/xeditor/textures.pak -> 3/CFD7C393
"""

LINE_RE = re.compile(r'^\s*(?P<path>\S.*?)\s*->\s*(?P<dir>[0-9A-Fa-f])[/\\](?P<hash>[0-9A-Fa-f]{8})\s*$')
HEXCHARS = set("0123456789ABCDEF")


def load_list():
    mapping = {}
    for line in FILE_LIST.splitlines():
        m = LINE_RE.match(line)
        if m:
            key = (m.group("dir") + "/" + m.group("hash")).upper()
            mapping[key] = m.group("path").strip().replace("\\", "/")
    return mapping


def mojib_hash(path):
    h = 0
    for b in path.encode("utf-8"):
        h = (31 * h + b) & 0xFFFFFFFF
    return h


def verify_list(mapping):
    bad = 0
    for key, path in mapping.items():
        h = mojib_hash(path)
        if "%X/%08X" % (h & 0xF, h) != key:
            bad += 1
    return bad


def find_hashed_root(folder):
    def has_hex_dirs(d):
        try:
            return [n for n in os.listdir(d)
                    if len(n) == 1 and n.upper() in HEXCHARS and os.path.isdir(os.path.join(d, n))]
        except OSError:
            return []
    level = [folder]
    for _ in range(4):
        nxt = []
        for d in level:
            if has_hex_dirs(d):
                return d
            try:
                for n in sorted(os.listdir(d)):
                    sub = os.path.join(d, n)
                    if os.path.isdir(sub) and not (len(n) == 1 and n.upper() in HEXCHARS):
                        nxt.append(sub)
            except OSError:
                pass
        level = nxt
    return None


def iter_folder_items(root):
    for d in sorted(os.listdir(root)):
        dp = os.path.join(root, d)
        if len(d) == 1 and d.upper() in HEXCHARS and os.path.isdir(dp):
            for entry in sorted(os.scandir(dp), key=lambda e: e.name):
                if entry.is_file():
                    name = entry.name.rstrip(" -.").upper()
                    yield (d.upper() + "/" + name, entry.path, entry.stat().st_size)


class DiscImage:
    CANDIDATES = [(2048, 0), (2352, 16), (2352, 24), (2336, 8)]

    def __init__(self, path):
        if path.lower().endswith(".cue"):
            path = self._bin_from_cue(path)
        self.path = path
        self.f = open(path, "rb")
        self._detect_layout()

    @staticmethod
    def _bin_from_cue(cue):
        base = os.path.dirname(os.path.abspath(cue))
        with open(cue, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                m = re.match(r'\s*FILE\s+"?(.+?)"?\s+(BINARY|MOTOROLA|WAVE)', line, re.I)
                if m:
                    return os.path.join(base, m.group(1))
        raise ValueError("no FILE entry found in da .cue")

    def _detect_layout(self):
        for ss, off in self.CANDIDATES:
            self.f.seek(16 * ss + off)
            d = self.f.read(8)
            if len(d) == 8 and d[1:6] == b"CD001":
                self.ss, self.off = ss, off
                return
        raise ValueError("Not a recognizable ISO9660 disc image")

    def close(self):
        self.f.close()

    def read_sectors(self, lba, count):
        if self.ss == 2048:
            self.f.seek(lba * 2048)
            return self.f.read(count * 2048)
        self.f.seek(lba * self.ss)
        raw = self.f.read(count * self.ss)
        return b"".join(raw[i * self.ss + self.off: i * self.ss + self.off + 2048]
                        for i in range(count))

    def read_extent(self, lba, size, chunk_sectors=256):
        remaining = size
        while remaining > 0:
            n = min(chunk_sectors, (remaining + 2047) // 2048)
            data = self.read_sectors(lba, n)
            if not data:
                break
            data = data[:remaining]
            yield data
            remaining -= len(data)
            lba += n

    def _read_dir(self, lba, size):
        data = self.read_sectors(lba, (size + 2047) // 2048)[:size]
        pos, out = 0, []
        while pos < len(data):
            ln = data[pos]
            if ln == 0:
                pos = (pos // 2048 + 1) * 2048
                continue
            rec = data[pos:pos + ln]
            pos += ln
            ext = struct.unpack_from("<I", rec, 2)[0]
            sz = struct.unpack_from("<I", rec, 10)[0]
            flags = rec[25]
            name = rec[33:33 + rec[32]]
            if name in (b"\x00", b"\x01"):
                continue
            n = name.decode("ascii", "replace").split(";")[0]
            if n.endswith("."):
                n = n[:-1]
            out.append((n, ext, sz, bool(flags & 2)))
        return out

    def walk(self):
        pvd = self.read_sectors(16, 1)
        root_lba = struct.unpack_from("<I", pvd, 156 + 2)[0]
        root_size = struct.unpack_from("<I", pvd, 156 + 10)[0]
        stack = [((), root_lba, root_size)]
        while stack:
            parts, lba, size = stack.pop()
            for name, ext, sz, is_dir in self._read_dir(lba, size):
                if is_dir:
                    stack.append((parts + (name,), ext, sz))
                else:
                    yield (parts + (name,), ext, sz)


def run_job(source, out_dir, preview, move, log, progress):
    mapping = load_list()
    stats = {"extracted": 0, "skipped_existing": 0, "unlisted": 0, "other": 0, "errors": 0}
    seen = set()
    out_full = os.path.abspath(out_dir)

    def safe_dest(rel):
        dest = os.path.abspath(os.path.join(out_full, *rel.split("/")))
        if not (dest + os.sep).startswith(out_full + os.sep):
            raise ValueError("unsafe path: " + rel)
        return dest

    items = []
    disc = None
    if os.path.isdir(source):
        root = find_hashed_root(source)
        if not root:
            raise ValueError("culdn't find the hashed folders (0-9, A-F) in that folder.")
        log("Source folder: " + root)
        for key, path, size in iter_folder_items(root):
            items.append((key, "file", path, size, None))
        for entry in sorted(os.scandir(root), key=lambda e: e.name):
            if entry.is_file():
                items.append((None, "file", entry.path, entry.stat().st_size, entry.name))
        move_ok = move
    else:
        disc = DiscImage(source)
        log("Disc image: %s (sector size %d)" % (disc.path, disc.ss))
        move_ok = False
        for parts, lba, size in disc.walk():
            if len(parts) == 2 and len(parts[0]) == 1 and parts[0].upper() in HEXCHARS:
                key = parts[0].upper() + "/" + parts[1].upper()
                items.append((key, "disc", (lba, size), size, None))
            else:
                items.append((None, "disc", (lba, size), size, "/".join(parts)))

    total = len(items)
    log("Found %d files." % total)
    progress(0, total)

    for i, (key, kind, payload, size, other_name) in enumerate(items, 1):
        try:
            if key is not None and key in mapping:
                rel = mapping[key]
                seen.add(key)
            elif key is not None:
                rel = "_unlisted/" + key
                stats["unlisted"] += 1
            else:
                rel = other_name
                stats["other"] += 1
            dest = safe_dest(rel)

            if os.path.exists(dest):
                stats["skipped_existing"] += 1
            elif preview:
                log("[preview] %s -> %s" % (key or other_name, rel))
                stats["extracted"] += 1
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                if kind == "file":
                    if move_ok:
                        shutil.move(payload, dest)
                    else:
                        shutil.copy2(payload, dest)
                else:
                    lba, sz = payload
                    with open(dest, "wb") as out:
                        for chunk in disc.read_extent(lba, sz):
                            out.write(chunk)
                log("%s -> %s" % (key or other_name, rel))
                stats["extracted"] += 1
        except Exception as e:
            stats["errors"] += 1
            log("ERROR on %s: %s" % (key or other_name, e))
        if i % 5 == 0 or i == total:
            progress(i, total)

    if disc:
        disc.close()

    missing = sorted(set(mapping) - seen)
    log("")
    log("Done%s." % (" (preview only, nothing written)" if preview else ""))
    log("  Written/placed : %d" % stats["extracted"])
    log("  Already there  : %d" % stats["skipped_existing"])
    log("  Not on list    : %d (put in _unlisted)" % stats["unlisted"])
    log("  Root files     : %d (copied to the output root)" % stats["other"])
    log("  Errors         : %d" % stats["errors"])
    log("  List entries not found in source: %d" % len(missing))
    for k in missing:
        log("    missing %s  (%s)" % (k, mapping[k]))
    return stats, missing


def run_gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("760x560")
    root.minsize(600, 420)

    src_var, out_var = tk.StringVar(), tk.StringVar()
    preview_var, move_var = tk.BooleanVar(value=False), tk.BooleanVar(value=False)
    msgs = queue.Queue()

    frm = ttk.Frame(root, padding=10)
    frm.pack(fill="both", expand=True)
    frm.columnconfigure(1, weight=1)
    frm.rowconfigure(5, weight=1)

    ttk.Label(frm, text="Source").grid(row=0, column=0, sticky="w")
    ttk.Entry(frm, textvariable=src_var).grid(row=0, column=1, sticky="ew", padx=6)
    bf = ttk.Frame(frm)
    bf.grid(row=0, column=2)

    def pick_folder():
        p = filedialog.askdirectory(title="Select your extracted Mojib-Ribbon folder")
        if p:
            src_var.set(p)

    def pick_image():
        p = filedialog.askopenfilename(
            title="select da disc image",
            filetypes=[("disc images", "*.cue *.bin *.iso"), ("All files", "*.*")])
        if p:
            src_var.set(p)

    ttk.Button(bf, text="Folder...", command=pick_folder).pack(side="left")
    ttk.Button(bf, text="Disc image...", command=pick_image).pack(side="left", padx=(4, 0))

    ttk.Label(frm, text="Output").grid(row=1, column=0, sticky="w", pady=(8, 0))
    ttk.Entry(frm, textvariable=out_var).grid(row=1, column=1, sticky="ew", padx=6, pady=(8, 0))

    def pick_out():
        p = filedialog.askdirectory(title="Select the output folder")
        if p:
            out_var.set(p)

    ttk.Button(frm, text="Browse...", command=pick_out).grid(row=1, column=2, pady=(8, 0), sticky="e")

    ttk.Checkbutton(frm, text="test run (nothing happens)", variable=preview_var)\
        .grid(row=2, column=1, sticky="w", pady=(8, 0))
    ttk.Checkbutton(frm, text="move into folder source instead of copying", variable=move_var)\
        .grid(row=3, column=1, sticky="w")

    start_btn = ttk.Button(frm, text="Start")
    start_btn.grid(row=4, column=1, sticky="w", pady=8)
    bar = ttk.Progressbar(frm, mode="determinate")
    bar.grid(row=4, column=1, columnspan=2, sticky="e", padx=(110, 0))

    txt = tk.Text(frm, wrap="none", height=10, state="disabled")
    txt.grid(row=5, column=0, columnspan=3, sticky="nsew")
    sb = ttk.Scrollbar(frm, command=txt.yview)
    sb.grid(row=5, column=3, sticky="ns")
    txt.configure(yscrollcommand=sb.set)

    def write(s):
        txt.configure(state="normal")
        txt.insert("end", s + "\n")
        txt.see("end")
        txt.configure(state="disabled")

    def poll():
        try:
            while True:
                kind, val = msgs.get_nowait()
                if kind == "log":
                    write(val)
                elif kind == "progress":
                    done, total = val
                    bar["maximum"] = max(total, 1)
                    bar["value"] = done
                elif kind == "finished":
                    start_btn.config(state="normal")
                    if val:
                        messagebox.showerror(APP_TITLE, val)
        except queue.Empty:
            pass
        root.after(100, poll)

    def worker(src, out, preview, move):
        err = None
        try:
            run_job(src, out, preview, move,
                    lambda s: msgs.put(("log", s)),
                    lambda d, t: msgs.put(("progress", (d, t))))
        except Exception as e:
            err = str(e)
            msgs.put(("log", "FAILED: " + err))
        msgs.put(("finished", err))

    def start():
        src, out = src_var.get().strip(), out_var.get().strip()
        if not src or not os.path.exists(src):
            messagebox.showwarning(APP_TITLE, "pick a proper source folder or disc image. pls.")
            return
        if not out:
            messagebox.showwarning(APP_TITLE, "pick an output folder. pls.")
            return
        start_btn.config(state="disabled")
        bar["value"] = 0
        threading.Thread(target=worker,
                         args=(src, out, preview_var.get(), move_var.get()),
                         daemon=True).start()

    start_btn.config(command=start)

    m = load_list()
    bad = verify_list(m)
    write("Loaded %d known files. Hash self-check: %s" % (len(m), "OK" if bad == 0 else "%d mismatches" % bad))
    write("Pick a source (extracted folder or .cue/.bin/.iso) and an output folder.")
    root.after(100, poll)
    root.mainloop()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) >= 2:
        run_job(args[0], args[1], "--preview" in flags, "--move" in flags,
                lambda s: print(s), lambda d, t: None)
    else:
        run_gui()


if __name__ == "__main__":
    main()
