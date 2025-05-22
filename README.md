# Sonar Translator

## Overview

This project is a simple translator that uses the Sonar concept-level auto-encoder to translate text from Japanese to English.

## Installation

### Install the dependencies
```bash
uv sync
```

### Activate the virtual environment
```bash
source .venv/bin/activate
```

## Usage

### Arguments

* `-i`: Input file to translate.
  * The input file should be a text file in the `2_InputData` directory.
* `-s`: Language to translate from (FLORES-200 code) (e.g., jpn_Jpan, eng_Latn).
* `-t`: Language to translate to (FLORES-200 code) (e.g., deu_Latn, zho_Hans).
* `-v`: Enable verbose output.
* `-q`: Process sentences sequentially.

### Example
The command below will translate the file `松山鏡ーThe_Mirror_of_Matsuyamaー日本語_Clean.txt` from Japanese to English.

```bash
python ./fb_sonar_translator/Translator.py -i 松山鏡ーThe_Mirror_of_Matsuyamaー日本語_Clean.txt -s jpn_Jpan -t eng_Latn
```

Input:
```text
松山鏡ーから
むかしむかし、昔の日本の越後国に、今でも日本の非常に僻地である男とその妻が住んでいました。この話が始まったとき、彼らは結婚して数年経ち、一人の幼い娘に恵まれていました。彼女は二人の人生の喜びであり誇りであり、彼女の中に彼らの老後のための無限の幸福の源が蓄えられていました.
赤ちゃんの頃から彼女が成長していくのを特徴づけた、彼らの記憶の中でどんな黄金の手紙の日々でしたか。彼女が生後わずか 30 日のときに寺院を訪れたとき、誇り高き母親が彼女を担ぎ、儀式用の着物を着て、家族の家庭の神の保護下に置かれました。それから彼女の最初の人形祭りで、彼女の両親が彼女に一連の人形とそのミニチュアの持ち物を与え、翌年に追加されました。そしておそらく最も重要な出来事は、彼女の 3 歳の誕生日に、緋色と金色の最初の帯 (幅広の錦帯) が彼女の小さな腰に結ばれたときでした。彼女が7歳になった今、愛情深い両親の心にとても大切ないくつかの小さな方法で話し、両親を待つことを学んだので、彼らの幸せの杯はいっぱいになったようでした.アイランド エンパイア全体で、これほど幸せな小さな家族は見つかりませんでした。
ある日、父が用事で突然都に呼び出されたため、家庭内は大騒ぎになった。鉄道や人力車などの急速な移動手段が発達した現代では、松山から京都への旅が何を意味するのかを理解するのは困難です。道はでこぼこで悪路で、百マイルでも数百マイルでも、普通の人は一歩一歩歩かなければなりませんでした。実際、当時、日本人がヨーロッパに航海するのと同じくらい、首都に上ることは大仕事でした。
妻は、夫が長い旅の準備をするのを手伝っている間、非常に心配していた。むなしく同行したかったのですが、母子ともに行くには距離が遠すぎて、家事は妻の義務でした。
ついにすべての準備が整い、夫は小さな家族と一緒にポーチに立っていました。
その男は言った、「心配しないでください。すぐに戻ってきます」。 「私が留守の間、すべてのこと、特に私たちの幼い娘の世話をしてください。」
「はい、私たちは大丈夫です – でもあなたは – 自分の面倒を見て、私たちに戻ってくるのを一日も遅らせないでください」と妻は言い、涙が彼女の目から雨のように落ちました.
微笑んでいるのは少女だけでした。なぜなら、彼女は別れの悲しみを知らなかったからです。また、王都に行くことが、父親が頻繁に行っていた次の村への散歩とまったく違うことを知らなかったからです。彼女は彼のそばに駆け寄ると、彼の長袖を掴んで少し待った。
「お父さん、あなたが帰ってくるのを待っている間、私はとても元気になりますので、プレゼントを持ってきてください。」
...
```

Output:
```text
There was a man and his wife who lived in Matsumoto-shi, in the old back country of Japan, which is still a very isolated part of Japan.
When this story began, they had been married for several years and were blessed with a little girl.
She was the joy and pride of their lives, and in her was stored the source of infinite happiness for their old age.
What were the golden letters in their memories that characterized her growth as a baby?
When she was only thirty days old when she went to the temple, her proud mother carried her, dressed her in ceremonial attire, and placed her under the protection of the God of her family home.
Then, at her first puppet festival, her parents gave her a set of dolls and their miniature items, which were added the following year.
And perhaps the most significant event was, on her third birthday, when her first ribbon of brown and gold was wrapped around her small waist.
Now that she's seven years old, she's learned to speak in a few small ways that are so important to her loving parents, and she's waiting for them to speak.
In the whole of the Irish Empire, there was no happier little family to be found.
One day my father was summoned to the city for work, and there was a great commotion in the house.
...
```

Note, some sentences may not be translated correctly. This is because the Sonar concept-level auto-encoder is not word-for-word perfect, as it performs a concept-level translation. This means that individual granular details may be skimmed over in the abstration process, e.g. "Irish Empire" in the above example.