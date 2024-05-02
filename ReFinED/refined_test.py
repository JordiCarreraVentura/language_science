from refined.inference.processor import Refined


refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikipedia")

# spans = refined.process_text("England won the FIFA World Cup in 1966.")
#
# for span in spans:
#     print(span)


spans = refined.process_text("From the 9th to the 12th centuries, Venice developed into a powerful maritime empire (an Italian thalassocracy known also as repubblica marinara). In addition to Venice there were seven others: the most important ones were Genoa, Pisa, and Amalfi; and the lesser known were Ragusa, Ancona, Gaeta and Noli. Its own strategic position at the head of the Adriatic made Venetian naval and commercial power almost invulnerable. With the elimination of pirates along the Dalmatian coast, the city became a flourishing trade centre between Western Europe and the rest of the world, especially with the Byzantine Empire and Asia, where its navy protected sea routes against piracy. The Republic of Venice seized a number of places on the eastern shores of the Adriatic before 1200, mostly for commercial reasons, because pirates based there were a menace to trade. The doge already possessed the titles of Duke of Dalmatia and Duke of Istria. Later mainland possessions, which extended across Lake Garda as far west as the Adda River, were known as the Terraferma; they were acquired partly as a buffer against belligerent neighbours, partly to guarantee Alpine trade routes, and partly to ensure the supply of mainland wheat (on which the city depended). In building its maritime commercial empire, Venice dominated the trade in salt, acquired control of most of the islands in the Aegean, including Crete, and Cyprus in the Mediterranean, and became a major power-broker in the Near East. By the standards of the time, Venice's stewardship of its mainland territories was relatively enlightened and the citizens of such towns as Bergamo, Brescia, and Verona rallied to the defence of Venetian sovereignty when it was threatened by invaders.")

for span in spans:
    print(span)