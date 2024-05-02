from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_base")

# text = """
# Cristiano Ronaldo dos Santos Aveiro
# (Portuguese pronunciation: [kɾiʃˈtjɐnu ʁɔˈnaldu]; born 5 February 1985)
# is a Portuguese professional footballer who plays as a forward for
# and captains both Saudi Pro League club Al Nassr and the Portugal national
# team. Widely regarded as one of the greatest players of all time,
# Ronaldo has won five Ballon d'Or awards,[note 3] a record three
# UEFA Men's Player of the Year Awards, and four European Golden Shoes,
# the most by a European player. He has won 33 trophies in his career,
# including seven league titles, five UEFA Champions Leagues,
# the UEFA European Championship and the UEFA Nations League.
# Ronaldo holds the records for most appearances (183), goals (140)
# and assists (42) in the Champions League, goals in the
# European Championship (14), international goals (128) and
# international appearances (205).
# He is one of the few players to have made over 1,200 professional
# career appearances, the most by an outfield player,
# and has scored over 850 official senior career goals for club and country,
# making him the top goalscorer of all time.
# """
#
# labels = ["person", "award", "date", "competitions", "teams"]
#
# entities = model.predict_entities(text, labels, threshold=0.5)
#
# for entity in entities:
#     print(entity["text"], "=>", entity["label"])
#


text = """Expansion

From the 9th to the 12th centuries, Venice developed into a powerful maritime empire (an Italian thalassocracy known also as repubblica marinara). In addition to Venice there were seven others: the most important ones were Genoa, Pisa, and Amalfi; and the lesser known were Ragusa, Ancona, Gaeta and Noli. Its own strategic position at the head of the Adriatic made Venetian naval and commercial power almost invulnerable.[35] With the elimination of pirates along the Dalmatian coast, the city became a flourishing trade centre between Western Europe and the rest of the world, especially with the Byzantine Empire and Asia, where its navy protected sea routes against piracy.[36]
The Republic of Venice seized a number of places on the eastern shores of the Adriatic before 1200, mostly for commercial reasons, because pirates based there were a menace to trade. The doge already possessed the titles of Duke of Dalmatia and Duke of Istria. Later mainland possessions, which extended across Lake Garda as far west as the Adda River, were known as the Terraferma; they were acquired partly as a buffer against belligerent neighbours, partly to guarantee Alpine trade routes, and partly to ensure the supply of mainland wheat (on which the city depended). In building its maritime commercial empire, Venice dominated the trade in salt,[37] acquired control of most of the islands in the Aegean, including Crete, and Cyprus in the Mediterranean, and became a major power-broker in the Near East. By the standards of the time, Venice's stewardship of its mainland territories was relatively enlightened and the citizens of such towns as Bergamo, Brescia, and Verona rallied to the defence of Venetian sovereignty when it was threatened by invaders.

Venice remained closely associated with Constantinople, being twice granted trading privileges in the Eastern Roman Empire, through the so-called golden bulls or "chrysobulls", in return for aiding the Eastern Empire to resist Norman and Turkish incursions. In the first chrysobull, Venice acknowledged its homage to the empire; but not in the second, reflecting the decline of Byzantium and the rise of Venice's power.[38]
Venice became an imperial power following the Fourth Crusade, which, having veered off course, culminated in 1204 by capturing and sacking Constantinople and establishing the Latin Empire. As a result of this conquest, considerable Byzantine plunder was brought back to Venice. This plunder included the gilt bronze horses from the Hippodrome of Constantinople, which were originally placed above the entrance to the cathedral of Venice, St Mark's Basilica (The originals have been replaced with replicas, and are now stored within the basilica.) After the fall of Constantinople, the former Eastern Roman Empire was partitioned among the Latin crusaders and the Venetians. Venice subsequently carved out a sphere of influence in the Mediterranean known as the Duchy of the Archipelago, and captured Crete.[39]
The seizure of Constantinople proved as decisive a factor in ending the Byzantine Empire as the loss of the Anatolian themes, after Manzikert. Although the Byzantines recovered control of the ravaged city a half-century later, the Byzantine Empire was terminally weakened, and existed as a ghost of its old self, until Sultan Mehmet The Conqueror took the city in 1453.

Situated on the Adriatic Sea, Venice had always traded extensively with the Byzantine Empire and the Middle East. By the late 13th century, Venice was the most prosperous city in all of Europe. At the peak of its power and wealth, it had 36,000 sailors operating 3,300 ships, dominating Mediterranean commerce. Venice's leading families vied with each other to build the grandest palaces and to support the work of the greatest and most talented artists. The city was governed by the Great Council, which was made up of members of the noble families of Venice. The Great Council appointed all public officials, and elected a Senate of 200 to 300 individuals. Since this group was too large for efficient administration, a Council of Ten (also called the Ducal Council, or the Signoria), controlled much of the administration of the city. One member of the great council was elected "doge", or duke, to be the chief executive; he would usually hold the title until his death, although several Doges were forced, by pressure from their oligarchical peers, to resign and retire into monastic seclusion, when they were felt to have been discredited by political failure.

The Venetian governmental structure was similar in some ways to the republican system of ancient Rome, with an elected chief executive (the doge), a senator-like assembly of nobles, and the general citizenry with limited political power, who originally had the power to grant or withhold their approval of each newly elected doge. Church and various private property was tied to military service, although there was no knight tenure within the city itself. The Cavalieri di San Marco was the only order of chivalry ever instituted in Venice, and no citizen could accept or join a foreign order without the government's consent. Venice remained a republic throughout its independent period, and politics and the military were kept separate, except when on occasion the Doge personally headed the military. War was regarded as a continuation of commerce by other means. Therefore, the city's early employment of large numbers of mercenaries for service elsewhere, and later its reliance on foreign mercenaries when the ruling class was preoccupied with commerce."""



labels = [
    "political organization",
    "person",
    "geographic region",
    "date or period",
    "military action"
]

for par in text.split('\n\n'):
    print('\n' * 5)
    print(par)
    entities = model.predict_entities(par, labels, threshold=0.25)

    for entity in entities:
        print(entity["text"], "=>", entity["label"])

