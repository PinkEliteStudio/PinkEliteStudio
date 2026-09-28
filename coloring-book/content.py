"""All book content in one place. Edit here, then rebuild with: python3 build_book.py

Each design: season, truth (big colorable headline), verse reference + the
book/chapter/verse used to pull the exact public-domain World English Bible
text, an optional `excerpt` (words to keep, in order; "..." marks a cut),
and the scene used for the art prompt.
"""

BOOK = {
    "title": "Made in His Image",
    "subtitle": "A Bible Truth Coloring Book for Brave, Confident Kids",
    "ages": "Ages 5-10",
    "author": "Your Name Here",          # <-- change to your author / brand name
    "year": "2026",
}

SEASONS = ["winter", "spring", "summer", "fall"]

DESIGNS = [
    # ---------------- WINTER ----------------
    dict(season="winter", truth="God made me in His image",
         ref=("genesis", 1, 27), label="Genesis 1:27",
         excerpt="God created man in his own image. ... male and female he created them.",
         scene="a smiling girl and boy building a big snowman together, snowflakes falling, "
               "the snowman has a scarf and a hat"),
    dict(season="winter", truth="I am wonderfully made",
         ref=("psalms", 139, 14), label="Psalm 139:14",
         excerpt="I will give thanks to you, for I am fearfully and wonderfully made.",
         scene="a confident girl ice skating on a frozen pond, arms out, pine trees behind her"),
    dict(season="winter", truth="God is with me wherever I go",
         ref=("joshua", 1, 9), label="Joshua 1:9",
         excerpt="Be strong and courageous. Don't be afraid. ... the LORD your God is with you wherever you go.",
         scene="a happy boy riding a sled down a snowy hill, big smile, snow spraying"),
    dict(season="winter", truth="I can be an example, even now",
         ref=("1timothy", 4, 12), label="1 Timothy 4:12",
         excerpt="Let no man despise your youth; but be an example to those who believe,",
         scene="a girl raising her hand with confidence in a classroom, chalkboard and desks, "
               "classmates around her"),
    dict(season="winter", truth="I do my best for God",
         ref=("colossians", 3, 23), label="Colossians 3:23",
         excerpt="And whatever you do, work heartily, as for the Lord, and not for men,",
         scene="a boy proudly working on a school science project with a model volcano, "
               "books and pencils on the table"),
    dict(season="winter", truth="God cares about how I feel",
         ref=("1peter", 5, 7), label="1 Peter 5:7",
         excerpt="casting all your worries on him, because he cares for you.",
         scene="a girl in a cozy sweater reading a book by a window with a mug of cocoa, "
               "snow outside the window, a cat curled up next to her"),
    dict(season="winter", truth="A good friend loves at all times",
         ref=("proverbs", 17, 17), label="Proverbs 17:17",
         excerpt="A friend loves at all times;",
         scene="two friends, a girl and a boy, making snow angels side by side and laughing"),
    dict(season="winter", truth="God gives me power, not fear",
         ref=("2timothy", 1, 7), label="2 Timothy 1:7",
         excerpt="For God didn't give us a spirit of fear, but of power, love, and self-control.",
         scene="a boy singing boldly on a school stage at a winter concert, microphone, "
               "curtains, music notes"),

    # ---------------- SPRING ----------------
    dict(season="spring", truth="Today is a gift from God",
         ref=("psalms", 118, 24), label="Psalm 118:24",
         excerpt="This is the day that the LORD has made. We will rejoice and be glad in it!",
         scene="a girl and a boy flying kites in a park, clouds, grass and flowers"),
    dict(season="spring", truth="God has good plans for me",
         ref=("jeremiah", 29, 11), label="Jeremiah 29:11",
         excerpt="For I know the thoughts that I think toward you, says the LORD, "
                 "thoughts of peace, and not of evil, to give you hope and a future.",
         scene="a girl planting flowers in a garden with a watering can, "
               "sprouts and a butterfly"),
    dict(season="spring", truth="God looks at my heart",
         ref=("1samuel", 16, 7), label="1 Samuel 16:7",
         excerpt="man looks at the outward appearance, but the LORD looks at the heart.",
         scene="a boy kneeling to help a younger child tie his shoe on a school playground"),
    dict(season="spring", truth="I can do all things through Christ",
         ref=("philippians", 4, 13), label="Philippians 4:13",
         excerpt="I can do all things through Christ, who strengthens me.",
         scene="a girl riding her bike with a helmet for the first time without training "
               "wheels, big proud smile, neighborhood sidewalk and houses"),
    dict(season="spring", truth="I was made to do good things",
         ref=("ephesians", 2, 10), label="Ephesians 2:10",
         excerpt="For we are his workmanship, created in Christ Jesus for good works,",
         scene="kids happily picking up litter in a park with gloves and a bag, "
               "trees and a bench"),
    dict(season="spring", truth="Jesus wants me to come to Him",
         ref=("matthew", 19, 14), label="Matthew 19:14",
         excerpt="Allow the little children, and don't forbid them to come to me;",
         scene="a girl and a boy running happily through a field of flowers toward a "
               "small church with a steeple"),
    dict(season="spring", truth="I choose to be kind",
         ref=("ephesians", 4, 32), label="Ephesians 4:32",
         excerpt="And be kind to one another, tender hearted, forgiving each other,",
         scene="a boy sharing his lunch with a new friend at a school lunch table"),
    dict(season="spring", truth="When I am afraid, I trust God",
         ref=("psalms", 56, 3), label="Psalm 56:3",
         excerpt="When I am afraid, I will put my trust in you.",
         scene="a brave girl at the top of a tall playground slide, about to slide down, smiling"),

    # ---------------- SUMMER ----------------
    dict(season="summer", truth="God makes me strong",
         ref=("isaiah", 40, 31), label="Isaiah 40:31",
         excerpt="They will run, and not be weary. They will walk, and not faint.",
         scene="a girl running a race on a track, number on her shirt, determined smile"),
    dict(season="summer", truth="I let my light shine",
         ref=("matthew", 5, 16), label="Matthew 5:16",
         excerpt="let your light shine before men; that they may see your good works,",
         scene="two kids at a lemonade stand handing a cup of lemonade to a neighbor, "
               "sun shining"),
    dict(season="summer", truth="I am a child of God",
         ref=("1john", 3, 1), label="1 John 3:1",
         excerpt="See how great a love the Father has given to us, that we should be called "
                 "children of God!",
         scene="a boy swinging high on a park swing, legs up, sun and clouds"),
    dict(season="summer", truth="God rejoices over me",
         ref=("zephaniah", 3, 17), label="Zephaniah 3:17",
         excerpt="He will rejoice over you with joy. ... He will rejoice over you with singing.",
         scene="girls jumping rope together on a sidewalk, one jumping in the middle, "
               "music notes in the air"),
    dict(season="summer", truth="God knows every hair on my head",
         ref=("matthew", 10, 30), label="Matthew 10:30",
         excerpt="but the very hairs of your head are all numbered.",
         scene="a girl with curly hair in two puffs building a sandcastle at the beach, "
               "bucket and shovel, waves and a seashell"),
    dict(season="summer", truth="God takes care of me",
         ref=("psalms", 23, 1), label="Psalm 23:1",
         excerpt="The LORD is my shepherd: I shall lack nothing.",
         scene="a boy and a girl camping, sitting by a tent looking at the stars and moon, "
               "a small campfire"),
    dict(season="summer", truth="I don't give up",
         ref=("galatians", 6, 9), label="Galatians 6:9",
         excerpt="Let's not be weary in doing good, for we will reap in due season, "
                 "if we don't give up.",
         scene="a boy shooting a basketball at a driveway hoop, ball in the air"),
    dict(season="summer", truth="I love others like Jesus loves me",
         ref=("john", 15, 12), label="John 15:12",
         excerpt="This is my commandment, that you love one another, even as I have loved you.",
         scene="a group of kids riding bikes together down a neighborhood street, "
               "houses and trees, waving"),

    # ---------------- FALL ----------------
    dict(season="fall", truth="God never leaves me",
         ref=("deuteronomy", 31, 6), label="Deuteronomy 31:6",
         excerpt="Be strong and courageous. ... He will not fail you nor forsake you.",
         scene="a girl and a boy with backpacks walking into school on the first day, "
               "waving, school building and a bus"),
    dict(season="fall", truth="I grow in wisdom like Jesus",
         ref=("luke", 2, 52), label="Luke 2:52",
         excerpt="And Jesus increased in wisdom and stature, and in favor with God and men.",
         scene="a boy reading in a library, sitting on a stack of books, bookshelves around him"),
    dict(season="fall", truth="My actions show who I am",
         ref=("proverbs", 20, 11), label="Proverbs 20:11",
         excerpt="Even a child makes himself known by his doings,",
         scene="a girl soccer player helping a teammate up off the grass, soccer ball and goal"),
    dict(season="fall", truth="I trust God with all my heart",
         ref=("proverbs", 3, 5), label="Proverbs 3:5",
         excerpt="Trust in the LORD with all your heart, and don't lean on your own understanding.",
         scene="kids jumping joyfully into a big pile of autumn leaves, leaves flying"),
    dict(season="fall", truth="I use my gifts to help others",
         ref=("1peter", 4, 10), label="1 Peter 4:10",
         excerpt="As each has received a gift, employ it in serving one another,",
         scene="a boy and a girl raking leaves for an elderly neighbor who is smiling on her porch"),
    dict(season="fall", truth="I am thankful to God",
         ref=("psalms", 136, 1), label="Psalm 136:1",
         excerpt="Give thanks to the LORD, for he is good; for his loving kindness endures forever.",
         scene="kids picking pumpkins at a pumpkin patch with a wagon, hay bales and a barn"),
]

BLESSING = dict(ref=("numbers", 6, 24), label="Numbers 6:24",
                excerpt="The LORD bless you, and keep you.")

# Shared style text appended to every art prompt so all pages match.
STYLE = ("children's coloring book page, black and white line art, thick clean bold outlines, "
         "no shading, no grayscale, no color, no text, no words, pure white background, "
         "simple shapes, cute cartoon style, joyful, age 5-10, full scene, "
         "correct anatomy with five fingers on each hand")
