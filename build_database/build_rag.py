import os
import json


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--rag_path', dest='rag_path')
    parameter_args = parser.parse_args()

    rag_path = parameter_args.rag_path
    test_set = []

    # %%
    data = {}
    data['question'] = '40K 純遊戲機 \n預算/用途：法環、魔物獵人、Minecraft模組包和射擊遊戲以外的其他3A遊戲'
    data['items'] = \
    '''
    CPU (中央處理器)：【需搭主機板】AMD【6核】Ryzen5 7500F 3.7GHz(Turbo 5.0GHz)/ZEN4
    /6C12T/快取32MB/65W/無外盒/含散熱器/代理商三年 $4990
    MB      (主機板)：技嘉 B650M GAMING X AX(mATX/1H1P/Realtek 2.5Gb/Wi-Fi 6E+BT 5.2
    /註冊五年保) $4690
    RAM     (記憶體)：Acer Predator Pallas II DDR5-6000 32G(16G*2)-黑(CL30/支援XMP&E
    XPO) $3099
    VGA     (顯示卡)：華碩 PROART-RTX4070-12G/std:2565MHz/三風扇/註冊五年保(30cm $19
    790
    Cooler  (散熱器)：Thermalright 利民 Assassin X 120 R SE (4導管/TL-C12C風扇*1/高1
    48mm) $690
    SSD   (固態硬碟)：鎧俠 KIOXIA Exceria Pro 1TB/M.2 PCIe Gen4/讀:7300M/寫:6400M/TL
    C/五年保 $2490
    HDD       (硬碟)：
    PSU (電源供應器)：BitFenix 火鳥科技 WHISPER 650W (80+金牌/ATX/全模組/全日系/十年
    保固) $2690
    CHASSIS   (機殼)：視博通 SW300 M 黑 玻璃透側機殼 (M-ATX/Type-C/內建風扇前3後1/顯
    卡350mm/塔散166mm)      $1,490
    MONITOR   (螢幕)：已有KG240先頂著用，有閒錢後會換掉
    Mouse/KB  (鼠鍵)：已有G304/cynosa lite
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709216263.A.A87.html'
    data['class'] = '4'
    test_set.append(data)


    # %%
    data = {}
    data['question'] = '40k工作遊戲機\n預算/用途：3A遊戲順跑 工作需求'
    data['items'] = \
    '''
    CPU (中央處理器)：AMD【6核】Ryzen5 7500F 3.7GHz(Turbo 5.0GHz)/ZEN4/6C12T/快取32MB/65W/無外盒/含
    散熱器/代理商三年

    MB      (主機板)：技嘉B650M GAMING X AX 或 技嘉 B650 EAGLE AX
    RAM     (記憶體)：Acer Predator Pallas II DDR5-6000 32G(16G*2)-銀(CL30/支援XMP&EXPO)
    VGA     (顯示卡)：技嘉 RTX 4070 EAGLE OC V2 12G/std:2505MHz/三風扇/註冊五年保(長28.2cm)
    Cooler  (散熱器)：DEEPCOOL 九州風神 AG400
    SSD   (固態硬碟)：鎧俠 KIOXIA Exceria Pro 1TB/M.2 PCIe Gen4/讀:7300M/寫:6400M/TLC/五年保
    HDD       (硬碟)：
    PSU (電源供應器)：BitFenix 火鳥科技 WHISPER 650W (80+金牌/ATX/全模組/全日系/十年保固)
    CHASSIS   (機殼)：MONTECH 君主 SKY TWO 白 玻璃透側機殼 (ATX/Type-C/內建風扇側2後1下1/顯卡400mm/
    塔散168mm/水冷360mm)
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709220044.A.388.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '80K工作影音遊戲機\n預算/用途： 打4K遊戲 偶爾剪片 預算80K可小捏'
    data['items'] = \
    '''
    CPU (中央處理器)： 真威 技嘉Z790 D DDR4+INTEL I5-13600K
    MB      (主機板)： 同上
    RAM     (記憶體)： 十銓 T-FORCE VULCAN Z DDR4 3200 32g
    VGA     (顯示卡)： 技嘉 RTX 4080 SUPER GAMING OC 16G
    Cooler  (散熱器)： 利民 Peerless Assassin 120絕雙刺客
    SSD   (固態硬碟)： 鎧俠 KIOXIA Exceria Pro 1T
                    鎧俠 KIOXIA Exceria G2 2T
    HDD       (硬碟)：
    PSU (電源供應器)： 君主 TITAN 1000W(80+金牌/ATX3.0/PCIe 5.0
    CHASSIS   (機殼)： Fractal Design Torrent 黑靜音殼
    MONITOR   (螢幕)： MPG321URX(已有)
    OS    (作業系統)： WINDOWS 11 Home 彩盒
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709224477.A.8EA.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '45-50k 遊戲機含螢幕\n2k解析度 法環 魔物 3A順跑'
    data['items'] = \
    '''
    CPU (中央處理器)： Ryzen5 7500F, $4990
    MB      (主機板)： ASUS TUF GAMING A620M-PLUS WIFI, $3990
    RAM     (記憶體)： Acer Predator Pallas II DDR5-6000 32G(16G*2), $3099
    VGA     (顯示卡)： 技嘉 RTX-4070 SUPER WINDFORCE OC 12G, $20990
    Cooler  (散熱器)： DEEPCOOL AG400, $690
    SSD   (固態硬碟)： 美光 Crucial T500 2TB, $4550
    PSU (電源供應器)： Montech TITAN GOLD 750W, $3190
    CHASSIS   (機殼)： Montech AIR 903 MAX, $1890
    MONITOR   (螢幕)： ASUS VG27AQL3A-W, $6688/BenQ EX2710q, $6988
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709232565.A.600.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '16k日用機 畫CAD和Sketchup，日常使用看yt，偶而玩遊戲例如紀元1800之類的'
    data['items'] = \
    '''
    CPU (中央處理器)：AMD 7500F MPK
    MB      (主機板) ：華碩 PRIME B650M-A II-CSM(M-ATX)
    RAM     (記憶體) ：UMAX 32GB(雙通16GB*2) DDR5 5600/CL46
    VGA     (顯示卡) ：暫時先沿用ASUS DUAL-RTX2070S-O8G
    Cooler  (散熱器) ：酷碼 Hyper 620S
    PSU (電源供應器)：華碩 TUF GAMING 550W銅牌電源
    CHASSIS   (機殼)：華碩 Prime AP201
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709228118.A.E73.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '21k 文書手遊 預算/用途： 21k 一般文書(word excel)跟雙開手遊 時不時會用一下photoshop'
    data['items'] = \
    '''
    CPU (中央處理器)：Intel i5-12600K【10核/16緒】(↑4.9G)
    MB      (主機板)：華碩 PRIME Z790M-PLUS-CSM DDR5
    RAM     (記憶體)：威剛 32GB(雙通16GB*2) DDR5 6000 XPG Lancer/CL30
    Cooler  (散熱器)：利民 Peerless Assassin 120
    SSD   (固態硬碟)：Solidigm(原INTEL) P44 Pro 1TB
    PSU (電源供應器)：全漢 聖武士 350W
    CHASSIS   (機殼)：全漢 CST350 PLUS
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709263317.A.140.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '50K 深度學習機含螢幕\n預算/用途：50K/深度學習(tensorflow)使用'
    data['items'] = \
    '''
    CPU (中央處理器)：【任搭板支持價】Intel i5-12600KF【10核/16緒】(↑4.9G)
                    /無內顯/代理盒三年全球保, $4990
    MB      (主機板)：技嘉 Z690 AORUS ELITE DDR4(ATX/1H1P/Realtek 2.5G/註冊五年保)
                    16+1+2相電源, $5990
    RAM     (記憶體)：威剛 64GB(雙通32GB*2) D4 3600 XPG D35/CL18
                    (AX4U360032G18I-DTBKD35)黑, $3899
    VGA     (顯示卡)：華碩 PROART-RTX4060TI-O16G(2685MHz/30cm/三風扇/註冊五年)優惠
                    價到2/29, $15990 ◆ ★ ↓任搭300↓
    Cooler  (散熱器)：利民 Peerless Assassin 120 /6導管(6mm)/雙塔雙扇/高15.7cm
                    【WXHZ】, $1350
    SSD   (固態硬碟)：SK 海力士 Platinum P41 1TB/Gen4 PCIE 4.0
                    /讀:7000/寫:6500/DRAM快取(五年), $2750
    PSU (電源供應器)：Montech TITAN GOLD 750W 雙8/金牌/全模/ATX3.0(PCIe 5.0)/
                    全日系/10年▼下殺到 3/15 20:00, $3690↘$3190
    CHASSIS   (機殼)：Montech SKY TWO 黑 顯卡長40/CPU高16.8/創新風流設計/玻璃透側
                    /ATX, $2390
    MONITOR   (螢幕)：【主機搭購】ViewSonic VX2479-HD-PRO(2H1P/1ms/IPS/165Hz/無喇叭
                    /Adaptive-Sync)保亮點 $3788↘, $3288↘$325
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709263483.A.9F6.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '65K 影音遊戲機 含螢幕 A家I家都有\n預算/用途：順跑2k 3A遊戲，RDR2 天際線2 2077等，順便玩一下AI算圖'
    data['items'] = \
    '''
    CPU (中央處理器)：AMD Ryzen 5 7500F MPK                 　　　　　　　$4990
    MB      (主機板)：華擎 A620M PRO RS WiFi                              $3790
    RAM     (記憶體)：威剛 ADATA XPG LANCER DDR5-6000 64G(32G*2)-黑       $6399
    VGA     (顯示卡)：技嘉 RTX 4070 Ti EAGLE OC 12G(rev 2.0)      VGA+PSU=$27690
    Cooler  (散熱器)：DEEPCOOL AG400                                      $690
    SSD   (固態硬碟)：鎧俠 KIOXIA Exceria Pro   1TB/M.2 PCIe Gen4 系統碟  $2490
                    宏碁 acer Predator GM3500 2TB/M.2 PCIe Gen3 遊戲碟  $3090
    HDD       (硬碟)：Toshiba 3TB 舊機沿用
    PSU (電源供應器)：君主 TITAN 1000W
    CHASSIS   (機殼)：安鈦克 P10C                                         $2690
    MONITOR   (螢幕)：DELL G3223D                                         $8888
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709274326.A.FC5.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '20K 文書影音機\n預算/用途：一般文書、影音(YT、Netflix等)，預算20K內'
    data['items'] = \
    '''
    CPU (中央處理器)：i5-12400
    MB      (主機板)：華擎B660M PG Riptide
    RAM     (記憶體)：博帝 DDR4-3200 16GB(CL22)
    VGA     (顯示卡)：用內顯
    SSD   (固態硬碟)：鎧俠 G2 1TB
    PSU (電源供應器)：全漢 聖武士 350W
    CHASSIS   (機殼)：視博通 SW300 M
    '''
    data['link'] = ''
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '30k 帕魯遊戲機\n30k可小捏 帕魯/2077遊戲機 希望3A遊戲至少有一定順暢度'
    data['items'] = \
    '''
    CPU (中央處理器)：Intel i5-12600K【10核/16緒】(↑4.9G)
    MB      (主機板)：華碩 PRIME Z790M-PLUS-CSM DDR5
    RAM     (記憶體)：威剛 32GB(雙通16GB*2) DDR5 6000 XPG Lancer/CL30 黑
    VGA     (顯示卡)：撼訊 AXRX6650XT 8GBD6-3DH 競技版
    Cooler  (散熱器)：ID-COOLING SE-206-XT BLACK
    SSD   (固態硬碟)：金士頓 KC3000 1TB
    PSU (電源供應器)：海韻 FOCUS GX-550(550W)
    CHASSIS   (機殼)：darkFlash MOTI 鏡之島 黑
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709281237.A.9AC.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '輕遊戲文書\n14k 大學生文書報告用 偶爾玩lol跟掛手遊'
    data['items'] = \
    '''
    CPU (中央處理器)：AMD【6核】Ryzen5 5500GT
    MB      (主機板)：華碩 PRIME B550M-K ARGB-CSM
    RAM     (記憶體)：威剛 ADATA XPG D10 DDR4-3200 32G(16G*2)
    Cooler  (散熱器)：Thermalright 利民 AXP90-X47 下吹式
    SSD   (固態硬碟)：鎧俠 KIOXIA Exceria G2 1TB
    PSU (電源供應器)：FSP 全漢 聖武士 350W
    CHASSIS   (機殼)：JONSBO 喬思伯 C6 白 電腦機殼
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709192209.A.1DB.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '35k-40k 程式遊戲股票機\n預算35k-40k，股票程式交易回測，平常玩玩steam遊戲，暗黑4、最後紀元'
    data['items'] = \
    '''
    CPU (中央處理器)：Intel i7-12700K【12核/20緒】(↑4.9G)/UHD770內顯 $7990
    MB      (主機板)：華碩 TUF GAMING B760M-E D4(M-ATX/Realtek2.5Gb/註五年) $3990
    RAM     (記憶體)：十銓 T-Force Vulcan Z 火神散熱片 32GB(雙通16GB*2) DDR4-3200/CL16,$1999
    VGA     (顯示卡)：華碩 TUF-RTX4060TI-O8G-GAMING(2655MHz/30cm/三風扇/註五年) $13990
    Cooler  (散熱器)：DEEPCOOL AG620 ARGB 6導管(6mm)/雙塔雙扇/高15.7cm/TDP:260W $1390
    SSD   (固態硬碟)：Solidigm P44 Pro 1TB/Gen4 PCIe 4.0/讀:7000M/寫:6500M/DRAM快取 $2588
    HDD       (硬碟)：舊電腦的3.5吋硬碟 2T
    PSU (電源供應器)：Montech TITAN GOLD 750W 雙8/金牌/全模/ATX3.0(PCIe 5.0)/全日系/10年 $3190
    CHASSIS   (機殼)：Montech Air 1000 PREMIUM 白 顯卡34/cpu16.5/ATX $2190
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709195469.A.088.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '20k 美工編輯 文書上網 多開視窗  用，常開網頁跟PS與AI軟體，美術軟體'
    data['items'] = \
    '''
    CPU (中央處理器)：Intel i5-12600K【10核/16緒】 $5790
    MB      (主機板)：華碩 TUF GAMING B760M-E D4(M-ATX/Realtek2.5Gb/註

    五年) $3990
    RAM     (記憶體)：威剛 32GB(雙通16G*2) D4-3200 D10超頻CL16  $2299
    VGA     (顯示卡)：
    Cooler  (散熱器)：利民 PA120 /6導管(6mm)/雙塔雙扇[WXHZ] $1350
    SSD   (固態硬碟)：solidigm(原INTEL) P44 Pro 1TB/Gen4 PCIe 4.0 $2588
    PSU (電源供應器)：全漢 聖武士 350W $1090
    CHASSIS   (機殼)：視博通 SW300 黑 $1890
                    或  darkFlash MOTI 鏡之島 黑 /玻璃透側 $2390
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709199106.A.F20.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '35k 模擬器多開遊戲股票機 股票程式交易與回測 '
    data['items'] = \
    '''
    CPU (中央處理器)：Intel【14核】Core i5-13500 $6990
    MB      (主機板)：華碩 PRIME B760M-A WIFI D4-CSM $4590 (待改?)
    RAM     (記憶體)：Kingston Fury Beast DDR4-3200 32G(16G*2) $2100
    VGA     (顯示卡)：技嘉 RTX 4060 Ti EAGLE OC 8G $13990
    Cooler  (散熱器)：Scythe 鎌刀 SCKTT-3000 $990
    SSD   (系統碟)：鎧俠 KIOXIA Exceria Pro 1TB/M.2 PCIe Gen4 $2490
    SSD   (遊戲碟)：美光 MX300 750G (沿用)
    HDD   (資料碟)：Toshiba DT01ACA200 2TB (沿用)
    PSU (電源供應器)：FSP 全漢 HYDRO GSM PRO 650W $2390
    選手1：Antec 安鈦克 P10 FLUX
    選手2：Antec 安鈦克 P10C
    選手3：MONTECH 君主 AIR 1000 SILENT
    選手4：BE Quiet BASE500 靜音版=
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709208783.A.495.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '80k遊戲程式機請益\n寫程式、Docker、練習LLM與玩遊戲，像是2077、柏德之門與Relink等'
    data['items'] = \
    '''
    CPU (中央處理器)：【真威】華碩 TUF GAMING B760M-PLUS WIFI D4+Intel【20核】Core i7-14700
    MB      (主機板)：同CPU
    RAM     (記憶體)：十銓 TEAM T-CREATE EXPERT DDR4-3200 64G(32G*2)(CL16)
    VGA     (顯示卡)：微星 RTX 4080 SUPER GAMING X SLIM 16G/std:2625MHz/三風扇/註冊五年保(長32.2cm)
    Cooler  (散熱器)：DEEPCOOL 九州風神 AK620 DIGITAL (6導管/12cm風扇*2/黑化/數位顯示/雙塔雙扇/高
    162mm)
    SSD   (固態硬碟)：美光 Crucial T500 2TB/M.2 PCIe Gen4/讀:7400M/寫:7000M/無散熱片/五年保*捷元代理
    商公司貨*
    PSU (電源供應器)：海韻 Focus GX-850 ATX3.0 (80+金牌/ATX3.0/PCIe 5.0/全模組/十年保固)
    CHASSIS   (機殼)：Fractal Design 瑞典 Torrent Compact RGB TG 黑 淺色玻璃機殼 (E-ATX/Type-C/內建
    風扇前2/顯卡330mm /塔散174mm) FD-C-TOR1C-02
    OS    (作業系統)：Microsoft Office 2021 家用中文版
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709211670.A.EFE.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    data = {}
    data['question'] = '45K SolidWorks/Creo 3D繪圖機\n預算/用途：Solidwork/Creo/3D繪圖/AutoCAD'
    data['items'] = \
    '''
    CPU (中央處理器)：Intel【20核】Core i7-14700 20C28T/2.1GHz
    MB      (主機板)：華碩 TUF GAMING B760M-E D4
    RAM     (記憶體)：威剛 ADATA XPG D35 DDR4-3200 64G(32G*2)-白(CL16)
    VGA     (顯示卡)：華碩 DUAL RTX 3060 OC 12G White/std:1867MHz/雙風扇/註
    Cooler  (散熱器)：利民 Frost Commander 140 (5導管/12cm+14cm PWM風扇/雙塔雙扇
    SSD   (固態硬碟)：Solidigm P44 Pro 1TB/M.2 PCIe Gen4/讀:7000M/寫:6500M/TLC/
    PSU (電源供應器)：全漢 HYDRO G PRO 650W (80+金牌/ATX/全模組/全日系/十年保固)
    CHASSIS   (機殼)：Antec 安鈦克 P10C 靜音機殼 (ATX/Type-C/內建風扇前3後1/顯卡
    '''
    data['link'] = 'https://www.ptt.cc/bbs/PC_Shopping/M.1709210225.A.0F5.html'
    data['class'] = '4'
    test_set.append(data)

    # %%
    index_num = 1
    for data in test_set:
        data['index'] = str(index_num)
        index_num += 1

    # %%
    with open(rag_path, 'w') as file:
        json.dump(test_set, file, ensure_ascii=False, indent=4)
        
    print('Build RAG successfully')


