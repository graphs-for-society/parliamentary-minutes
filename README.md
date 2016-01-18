# Parliamentary Minutes (Meclis Konuşmaları)

(Türkçe metin için aşağıya bakınız)

This project is a collection of Python libraries written for creating a graph representation of
talks given by the members of the parliament. Project consists of three main parts:

- Crawling
- Information Extraction
- Graph Creation


`Crawling` and `Graph Creation` parts are mostly static. However, `Information Extraction` determines the semantic of the graph.
What does semantic mean? For instance, In [Creative Use of Complex Networks Hackathon](http://graphcommons.github.io/hackathons/2015/12/23/istanbul-creative-use-of-complex-networks/) we
focussed on interactions made by other parties to parliaments talks. These interactions range from applause, laughter, defamatory remarks, insults and to even physical
violence. In this example, semantic means that various reactions between speecher and parties in the graph. Without any effort, you can use this dataset where you reveal different semantics. Only by writing a function which extracts the information (like the function that extracts the reaction between speecher and parties), you can illustrate this by graph representation.

You can explore the resulting [graph](https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph) we created in the hackathon. The visualization of the graph was made possible by the service given by [Graph Commons](http://graphcommons.com).

You can find a random speech [here](https://www.tbmm.gov.tr/develop/owa/genel_kurul.cl_getir?pEid=42406). So, if you want to analyze 
talks of parliaments, this project provides you almost everything. We believe that this project laid a foundation for further analysis of the interactions during the talks in the parliament. 


# Getting Started

1. First ensure that there is a directory named data in the current directory
2. Run the crawler. You can give a date range.
    ```
    python crawl/__init__.py --start_date 11/01/2016 --end_date 13/01/2016
    ```
3. Information extraction part expects two parameters. `--input` is the talks you have just fetched in Step #1. `--function` is the information extraction function in `extraction/__init__.py`. In this example, we provided our function, `create_reaction_data`, whose aim is to extract reaction between parliament who gives the speech and the parties in The Grand National Assembly of Turkey.
    ```
    python extraction/__init__.py --input data/all-talks-combined.json --function create_reactions_data
    ```
In order to create a graph that focus on different semantic (e.g., What are the main topics in the speeches?), all you need to do is writing a function which extracts the topic information and returns signals like `create_reaction_data` does. That's all. 
4. Upload the reactions extracted in step #3 above to your own graph
    ```
    python graph/__init__.py data/extraction_output-1452724616000.json --graph_id YOUR_GRAPHS_ID --api-key YOUR_GRAPH_COMMONS_API_KEY
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

## English version of Reaction Graph

In this graph, laughters, taunts and rumbles during parliamentary talks are mapped. Green points
represent `talk`s, red points represent `representative`s, blue points represent the `parties`.

You can find it interesting to begin by examining a talk located between all parties and which have
received interest from more than one party.

We glad to hear your thoughts through the comment section at the upper right side of the
window at Graph Commons website.

[Visit Graph](https://graphcommons.com/graphs/de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed?show=graph)

## Harita Hakkında Kısa Bilgi

Bu haritada TBMM Genel Kurulu'nda milletvekilleri tarafından yapılan konuşmalara gelen gülüşme,
sataşma veya gürültü gibi tepkileri görülebilir. YEŞİL noktalar konuşmaları, KIRMIZI noktalar
milletvekillerini, MAVİ noktalar ise partileri temsil ediyor.

İncelemeye tüm partilerin ortasında kalan ve birden çok partiden çeşitli tepkiler almış bir
konuşma bularak başlayabilirsiniz.

Yorumlarınızı haritanın bulunduğu sayfanın sağ köşesindeki konuşma balonu aracılığıyla bize iletebilirsiniz.

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
belirginleştirilmesi amacıyla Graph Commons'ın düzenlemiş olduğu hackathon kapsamında konuşmalarda bahsi geçen konu
başlıklarını şimdilik dışarıda bırakarak bu tür tepkileri görselleştiren bir harita oluşturduk.

### Haritaya nasıl bakmalı?

Haritaya bakınca yüzlerce farklı renkte nokta göreceksiniz.

Diğerlerinden çok daha büyük 4 tane MAVİ nokta partileri simgeliyor.

Yeşil noktalar yapılan konuşmaları gösteriyor.

Kırmızı noktalar ise bu konuşmaları yapan milletvekillerini temsil ediyor.

Her noktanın üzerine tıklayıp daha fazla bilgi alabilirsiniz. Örneğin bir konuşmanın üzerine
tıkladığınızda o konuşmanın metnine ulaşabilir, kırmızı noktalarda ise milletvekilinin
bilgilerine ulaşabilirsiniz.
