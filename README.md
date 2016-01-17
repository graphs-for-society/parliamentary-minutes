# Parliamentary Minutes (Meclis Konuşmaları)

(Türkçe metin için aşağıya bakınız)

This project is a collection of Python libraries written for creating a graph representation of
talks given by the members of the parliament and interactions made by other parliaments to these
talks. These range from applause, laughter, defamatory remarks, insults and to even physical
violence.

This work was mainly done in Creative Use of Complex Networks Hackathon during 9-10 January 2016.

We believe that this project laid a foundation for further analysis of the interactions during
the talks in the parliament.

The way we designed our system also allows others to use our code to begin analyzing their own
data of interest. This is because we first use the ```crawler``` module to generate a data
capture file to be used by ```extraction``` module to generate a data file which contains edges
and nodes to be inserted by the more generic ```graph``` module.

You can explore the resulting graph at https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph

The visualization of the graph was made possible by the service given by [Graph Commons](http://graphcommons.com).

# Getting Started

1. First ensure that there is a directory named data in the current directory

2. Run the crawler. You can give a date range.

```
python crawl/__init__.py --start_date 11/01/2016 --end_date 13/01/2016
```

3. Run the extractor on the output of step #2 above.
```
python extraction/__init__.py --input data/all-talks-combined.json --function create_reactions_data
```

4. Ensure that you have an environment variable named API_KEY which contains your API key from
Graphcommons.

5. Upload the reactions extracted in step #3 above to your own graph.

```
python graph/__init__.py data/extraction_output-1452724616000.json --graph_id YOUR_GRAPHS_ID
```

# People

- Onur Güngör
- Osman Başkaya
- Doruk Tunaoğlu
- Fevzi Kahraman


# Notes

We also wrote a webapp for further analysis of the data. It currently includes a form which you
can query for all paths from a representative to a party.

# Introductory text for the graph at [Graph Commons](https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph)

## English version

In this graph, laughters, taunts and rumbles during parliamentary talks are mapped. Green points
represent `talk`s, red points represent `representative`s, blue points represent the `parties`.

You can find it interesting to begin by examining a talk located between all parties and which have
received interest from more than one party.

We would be glad to hear your comments through the comment section at the upper right side of the
window.

[Visit Graph](https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph)

## Kısaca

Bu haritada TBMM Genel Kurulu'nda milletvekilleri tarafından yapılan konuşmalara gelen gülüşme,
sataşma veya gürültü gibi tepkileri görülebilir. YEŞİL noktalar konuşmaları, KIRMIZI noktalar
milletvekillerini, MAVİ noktalar ise partileri temsil ediyor.

İncelemeye tüm partilerin ortasında kalan ve birden çok partiden çeşitli tepkiler almış bir
konuşma bularak başlayabilirsiniz.

Yorumlarınızı sağ üstteki konuşma balonu aracılığıyla bize iletebilirsiniz.

[Ağ haritasını ziyaret edin](https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph)

## Biraz daha ayrıntılı anlatım

Meclis Konuşmaları Etkileşim Haritası

Mecliste konuşulanların merak edilmekten gittikçe uzaklaştığı, siyaset "usta"larının iki
dudağının arasında oynanan bir demokrasicilik oyununu izlemeye devam ediyoruz.

Karşınızdaki harita, meclisteki konuşmalara başka bir açıdan bakma denemesi.

Teoride, ülkenin her ilinde halk tarafından seçilmiş milletvekillerinin ülkenin karşı karşıya
kaldığı sorunları kıyasıya tartışıp, enine boyuna irdelemesi beklenir.

Ancak bunun için yapılan genel kurul konuşmaları, konulara iyi hazırlanmış vekillerin yaptığı
retoriği güçlü konuşmalar olmaktan çok, diğer milletvekilleri tarafından sataşma, gülüşme ve
bazen fiziksel şiddeti de içeren şekillerde karşılık bulan veya sadece kendi partisinden kuru
bir alkış alan konuşmalar olmaktan öteye gidemiyor.

İşte bu etkileşimlerin sıklığının anlaşılması ve üzerinde anlaşmazlık olan konuların
belirginleştirilmesi amacıyla Graphcommons Hackathon'u kapsamında konuşmalarda bahsi geçen konu
başlıklarını şimdilik dışarıda bırakarak bu tür tepkileri görselleştiren bir harita oluşturduk.

Haritaya nasıl bakmalı?

Haritaya bakınca yüzlerce farklı renkte nokta göreceksiniz.

Diğerlerinden çok daha büyük 4 tane MAVİ nokta partileri simgeliyor.

Yeşil noktalar yapılan konuşmaları gösteriyor.

Kırmızı noktalar ise bu konuşmaları yapan milletvekillerini temsil ediyor.

Her noktanın üzerine tıklayıp daha fazla bilgi alabilirsiniz. Örneğin bir konuşmanın üzerine
tıkladığınızda o konuşmanın metnine ulaşabilir, kırmızı noktalarda ise milletvekilinin
bilgilerine ulaşabilirsiniz.

İncelemeye tüm partilerin ortasında kalan ve birden çok partiden çeşitli tepkiler almış bir
konuşma bularak başlayabilirsiniz.

Yorumlarınızı sağ üstteki konuşma balonu aracılığıyla bize iletebilirsiniz.

[Ağ haritasını ziyaret edin](https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph)
