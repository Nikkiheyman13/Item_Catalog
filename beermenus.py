from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Beer, MenuItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# beerstodelete = session.query(Beer);
# for beer in beerstodelete:
#        session.delete(beer);
# menuitemstotodelete = session.query(MenuItem);
# for menuitem in menuitemstotodelete:
#        session.delete(menuitem);

# Menu for Pale Ales
beer1 = Beer(name="Pale Ales")

session.add(beer1)
session.commit()

menuItem1 = MenuItem(name="American Pale Ale", description="An American interpretation of a classic English style. The American pale ale is characterized by floral, fruity, citrus-like, piney, resinous, or sulfur-like American-variety hop character, producing medium to medium-high hop bitterness, flavor and aroma. American-style pale ales have medium body and low to medium maltiness that may include low caramel malt character.", beer=beer1)

session.add(menuItem1)
session.commit()


menuItem2 = MenuItem(name="Blonde Ale", description="One of the most approachable styles, a golden or blonde ale is an easy-drinking beer that is visually appealing and has no particularly dominating malt or hop characteristics. Rounded and smooth, it is an American classic known for its simplicity. Sometimes referred to as 'golden ale.' These beers can have honey, spices and fruit added, and may be fermented with lager or ale yeast.", beer=beer1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="English-Style Pale Ale (ESB)", description="ESB stands for 'extra special bitter.' This style is known for its balance and the interplay between malt and hop bitterness. English pale ales display earthy, herbal English-variety hop character. Medium to high hop bitterness, flavor and aroma should be evident. The yeast strains used in these beers lend a fruitiness to their aromatics and flavor, referred to as esters. The residual malt and defining sweetness of this richly flavored, full-bodied bitter is medium to medium-high.", beer=beer1)

session.add(menuItem3)
session.commit()


# Menu for India Pale Ales
beer2 = Beer(name="IPA")

session.add(beer2)
session.commit()


menuItem1 = MenuItem(name="American IPA", description="Characterized by floral, fruity, citrus-like, piney or resinous American-variety hop character, the IPA beer style is all about hop flavor, aroma and bitterness. This has been the most-entered category at the Great American Beer Festival for more than a decade, and is the top-selling craft beer style in supermarkets and liquor stores across the U.S.", beer=beer2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
    name="English-Style IPA", description="Steeped in lore (and extra hops), the IPA is a stronger version of a pale ale. The English-style IPA is characterized by stiff English-style hop character (earthy, floral) and increased alcohol content. English yeast lends a fruity flavor and aroma. Different from its American counterpart, this style strikes a balance between malt and hops for a more rounded flavor. There is also a lot of mythology surrounding the creation of this style, which is still debated today.", beer=beer2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="Imperial India Pale Ale", description="The imperial India Pale Ale features high hop bitterness, flavor and aroma. Hop character is fresh and evident from utilization of any variety of hops. Alcohol content is medium-high to high and notably evident with a medium-high to full body. The intention of this style is to exhibit the fresh and evident character of hops.", beer=beer2)

session.add(menuItem3)
session.commit()


# Menu for Belgian Beers
beer3 = Beer(name="Belgian Beers")

session.add(beer3)
session.commit()


menuItem1 = MenuItem(name="Belgian-Style Dubbel", description="The Belgian-style dubbel ranges from brown to very dark in color. They have a malty sweetness and can have cocoa and caramel aromas and flavors. Hop bitterness is medium-low to medium. Yeast-generated fruity esters (especially banana) can be apparent. Often bottle-conditioned, a slight yeast haze and flavor may be evident. 'Dubbel' meaning 'double,'' this beer is still not so big in intensity as to surpass the Belgian-style quadrupel that is often considered its sibling.", beer=beer3)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name="Belgian-Style Quadrupel", description="The Belgian-style Quadrupel is amber to dark brown in color. Caramel, dark sugar and malty sweet flavors dominate, with medium-low to medium-high hop bitterness. Quads have a relatively light body compared to their alcoholic strength. If aged, oxidative qualities should be mild and not distracting. Sometimes referred to as Belgian strong dark.", beer=beer3)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="Saison", description="Beers in this category are gold to light amber in color. Often bottle-conditioned, with some yeast character and high carbonation. Belgian-style saison may have Brettanomyces or lactic character, and fruity, horsey, goaty and/or leather-like aromas and flavors. Specialty ingredients, including spices, may contribute a unique and signature character. Commonly called 'farmhouse ales' and originating as summertime beers in Belgium, these are not just warm-weather treats. U.S. craft brewers brew them year-round and have taken to adding a variety of additional ingredients.", beer=beer3)

session.add(menuItem3)
session.commit()

# Menu for Wheat Beers
beer4 = Beer(name="Wheat Beers")

session.add(beer4)
session.commit()

menuItem1 = MenuItem(name="American Wheat", description="Color is pale to light amber. This beer can be made using either ale or lager yeast. American wheat beer is generally brewed with at least 30 percent malted wheat. These beers are typically served with the yeast in the bottle, and pour cloudy. Traditionally more hoppy than a German hefeweizen, American wheat beer differs in that it should not offer flavors of banana or clove. It is a refreshing summer style. Darker versions of this style also exist but are not as common.", beer=beer4)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name="Hefeweizen", description="The German-style hefeweizen is straw to amber in color and made with at least 50 percent malted wheat. The aroma and flavor of a weissbier comes largely from the yeast and is decidedly fruity (banana) and phenolic (clove). 'Weizen' means 'wheat' and 'hefe' means 'yeast.'' There are multiple variations to this style. Filtered versions are known as 'Kristal Weizen' and darker versions are referred to as 'Dunkels,' with a stronger, bock-like version called 'Weizenbock.' This is commonly a very highly carbonated style with a long-lasting collar of foam.", beer=beer4)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="Witbier", description="Belgian-style witbier is brewed using unmalted wheat, sometimes oats and malted barley. Witbiers are spiced with coriander and orange peel. A style that dates back hundreds of years, it fell into relative obscurity until it was revived by Belgian brewer Pierre Celis in the 1960s. This style is currently enjoying a renaissance, especially in the American market.", beer=beer4)

session.add(menuItem3)
session.commit()


# Menu for Porters
beer5 = Beer(name="Porters")

session.add(beer5)
session.commit()


menuItem1 = MenuItem(name="American Imperial Porter", description="Definitively American, the imperial porter should have no roasted barley flavors or strong burnt/black malt character. Medium caramel and cocoa-like sweetness is present, with complementing hop character and malt-derived sweetness.", beer=beer5)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name="Smoke Porter", description="Typically the base for the smoke porter beer style is a robust porter that is given smoky depth thanks to wood-smoked malt. Traditionally, brewers will cite the specific wood used to smoke the malt, and different woods will lend different flavors to the finished product. Smoke flavors dissipate over time.", beer=beer5)

session.add(menuItem2)
session.commit()

menuItem1 = MenuItem(name="Robust Porter", description="The Robust Porter features more bitter and roasted malt flavor than a brown porter, but not quite as much as a stout. Robust porters have a roast malt flavor, often reminiscent of cocoa, but no roast barley flavor. Their caramel and malty sweetness is in harmony with the sharp bitterness of black malt. Hop bitterness is evident. With U.S. craft brewers doing so much experimentation in beer styles and ingredients, the lines between certain stouts and porters are often blurred. Yet many deliberate examples of these styles do exist. Diacetyl is acceptable at very low levels.", beer=beer5)

session.add(menuItem3)
session.commit()

# Menu for Stout Beers
beer6 = Beer(name="Stouts")

session.add(beer6)
session.commit()

menuItem1 = MenuItem(name="American Stout", description="The American stout is a coffee- and chocolate-forward ale, but with a hop aroma and flavor, often from a citrus-forward variety. American stouts are bold, with a distinctive dry-roasted bitterness in the finish. Fruity esters should be low, but head retention high. The addition of oatmeal is acceptable in this style and lends to the body and head retention.", beer=beer6)

session.add(menuItem1)
session.commit()


menuItem2 = MenuItem(name="Oatmeal Stout", description="The addition of oatmeal adds a smooth, rich body to the oatmeal stout. This beer style is dark brown to black in color. Roasted malt character is caramel-like and chocolate-like, and should be smooth and not bitter. Coffee-like roasted barley and malt aromas are prominent. This low- to medium-alcohol style is packed with darker malt flavors and a rich and oily body from oatmeal.", beer=beer6)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="Irish-style Dry Stout", description="Dry stout is black beer with a dry-roasted character thanks to the use of roasted barley. The emphasis on coffee-like roasted barley and a moderate degree of roasted malt aromas define much of the character. Hop bitterness is medium to medium high. This beer is often dispensed via nitrogen gas taps that lend a smooth, creamy body to the palate.", beer=beer6)

session.add(menuItem3)
session.commit()

# Menu for Sours
beer7 = Beer(name="Sours")

session.add(beer7)
session.commit()

menuItem1 = MenuItem(name="American Sours", description="The acidity present in sour beer is usually in the form of lactic, acetic and other organic acids naturally developed with acidified malt in the mash, or produced during fermentation by the use of various microorganisms. These beers may derive their sour flavor from pure cultured forms of souring agents or from the influence of barrel aging.", beer=beer7)

session.add(menuItem1)
session.commit()


menuItem2 = MenuItem(name="Fruit Lambic", description="Often known as cassis, framboise, kriek, or peche, a fruit lambic takes on the color and flavor of the fruit it is brewed with. It can be dry or sweet, clear or cloudy, depending on the ingredients. Notes of Brettanomyces yeast are often present at varied levels. Sourness is an important part of the flavor profile, though sweetness may compromise the intensity. These flavored lambic beers may be very dry or mildly sweet.", beer=beer7)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="Gose", description="Straw to medium amber, the contemporary Gose is cloudy from suspended yeast. A wide variety of herbal, spice, floral or fruity aromas other than found in traditional Leipzig-Style Gose are present, in harmony with other aromas. Salt (table salt) character is traditional in low amounts, but may vary from absent to present. Body is low to medium-low. Low to medium lactic acid character is evident in all examples as sharp, refreshing sourness.", beer=beer7)

session.add(menuItem3)
session.commit()

# Menu for Brown Ales
beer8 = Beer(name="Brown Ales")

session.add(beer8)
session.commit()

menuItem1 = MenuItem(name="American Brown Ale", description="Roasted malt, caramel-like and chocolate-like characters should be of medium intensity in both flavor and aroma for the American brown ale. American-style brown ales have evident low to medium hop flavor and aroma and medium to high hop bitterness. The history of this style dates back to U.S. homebrewers who were inspired by English-style brown ales and porters. It sits in flavor between those British styles and is more bitter than both.", beer=beer8)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(name="English-style Brown Ale", description="The English-style brown ale ranges from dryer (Northern English) to sweeter (Southern English) maltiness. Roast malt tones (chocolate, nutty) may sometimes contribute to the flavor and aroma profile. Hop bitterness is very low to low, with very little hop flavor and aroma. Known for rich and advanced malt aroma and flavor without centering too much on hops, the English-style mild is extremely sessionable and food-friendly.", beer=beer8)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(name="English-style Mild", description="Malt and caramel are part of the flavor and aroma profile of the English-style mild while licorice and roast malt tones may sometimes contribute as well. Hop bitterness is very low to low. U.S. brewers are known to make lighter-colored versions as well as the more common 'dark mild.' These beers are very low in alcohol, yet often are still medium-bodied due to increased dextrin malts.", beer=beer8)

session.add(menuItem3)
session.commit()


print "added beer-- cheers!"