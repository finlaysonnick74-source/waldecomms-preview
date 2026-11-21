# ALL WaldeComms site copy and data. Edit here, then run: python3 build.py
import html
E=html.escape
# CONTACT: PLACEHOLDER. The deck has no email/phone. Confirm Niki's real address + number, then set PHONE.
EMAIL='hello@waldecomms.com'  # UNCONFIRMED: Niki isn't sure this mailbox exists
PHONE=None  # e.g. ('+614xxxxxxxx','04xx xxx xxx') once confirmed
NAV=[('/work/','Work'),('/services/','Services'),('/noise-makers/','Noise-Makers'),('/what-people-say/','What People Say'),('/contact/','Contact')]
import json as _json, os as _os
COV=_json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','coverage','coverage.json'))) if _os.path.exists(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','coverage','coverage.json')) else _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'coverage.json')))
CASES=[
 dict(slug='hamilton-island',title='Hamilton Island',tape='Island of paradise',tags='travel',tag='Travel',img='hamilton-island',stat='#1',statl="Australia's most Google-searched destination, 2025",
  line="Helped Hamilton Island become Australia's #1 Google searched destination in 2025.",
  coverage=["Sunrise: “Island of Paradise”","AFR Weekend","“No trouble in paradise: Oatleys dig in on island”"],counters=[('#1','',"Google-searched destination in Australia, 2025")]),
 dict(slug='million-moves-ausactive',title='AUSactive & Million Moves',tape='Fit for Office',tags='health',tag='Health / Fitness',img='million-moves',stat='Million Moves',statl='+ Fit for Office campaigns for AUSactive',
  line='Million Moves and Fit for Office: two campaigns for AUSactive.',
  quote=("WaldeComms are absolute PR guns of the highest calibre. Creative, persistent and lateral thinkers, they were the driving force behind the success of our Million Moves and Fit for Office campaigns.","Barrie Elvish, CEO, AUSactive"),
  coverage=['TV news','Print and online'],counters=[]),
 dict(slug='neon-dynamo-sonar-music',title='Neon Dynamo & Sonar Music',tape='Vivid Sydney & NYE',tags='music',tag='Music / Events',img='neon-dynamo',stat='Vivid + NYE',statl="Sydney New Year's Eve Midnight Soundtrack",
  line="Neon Dynamo and Sonar Music across Vivid Sydney and Sydney New Year's Eve, featuring Jono Ma (composer, Sydney New Year's Eve Midnight Soundtrack) and Antony Partos (co-founder, Sonar Music).",
  coverage=['“Short-cut cave gets Glastonbury tour”','TV news: Jono Ma, Antony Partos, Heath Campanaro'],counters=[]),
 dict(slug='a-lasting-tale',title='A Lasting Tale',tape='27M reach',tags='impact',tag='Social impact',img='lasting-tale',stat='27M reach',statl='= $80k new business',
  line='A human story that travelled: Good Weekend’s “For decades, Vince remembered what one teacher had told him. Then they met again.”',
  coverage=['Good Weekend: “Two of Us”','TV news'],counters=[(27,'M','reach'),(80,'k','new business ($)')]),
 dict(slug='noasis',title='Noasis',tape='Oasis reunion',tags='music',tag='Music / Events',img='noasis',stat='Oasis reunion',statl='News hook: Noasis, the tribute act to the British rock group',
  line='When the Oasis reunion was confirmed, Noasis (the tribute act to the British rock group) was ready for the headlines.',
  coverage=['“Oasis reunion confirmed”','“Oasis… more like Noasis”'],counters=[]),
 dict(slug='36-months',title='36 Months',tape='World-first legislation',tags='impact',tag='Social impact',img='36-months',stat='World-first',statl='Legislation change for Australia',
  line="36 Months: the campaign that drove Australia's landmark world-first legislation change.",
  quote=("WaldeComms are weapons. Gritty hustlers who know the media landscape inside out and pitch like machines. They were mission critical in the success of 36 Months driving Australia’s landmark world-first legislation change.","Michael “Wippa” Wipfli, Nova host & 36 Months co-founder"),
  coverage=['14 international awards','7,000 stories','2.3 billion impressions'],counters=[(14,'','international awards'),(7000,'','stories'),(2.3,' billion','impressions')]),
 dict(slug='national-expansion',title='National Expansion',tape='500+ stories',tags='expansion',tag='Expansion',img='national-expansion',stat='500+',statl='stories',
  line='A national expansion pushed into 500+ stories.',
  coverage=['Futures','“Music saved me”','Mouse Man'],counters=[(500,'+','stories')]),
]
FILTERS=[('all','All'),('travel','Travel'),('health','Health / Fitness'),('music','Music / Events'),('impact','Social impact'),('expansion','Expansion')]
# QUOTES: Albanese (PM), Sunrise, Today Show quotes are PENDING PERMISSION to publish (see site-plan.md). Shown for v1 review only.
QUOTES=[
 ("WaldeComms are weapons. Gritty hustlers who know the media landscape inside out and pitch like machines. They were mission critical in the success of 36 Months driving Australia’s landmark world-first legislation change.","Michael “Wippa” Wipfli, Nova host & 36 Months co-founder",False),
 ("Thank you again for all the commitment, determination and energy you have poured into 36 Months. You are making a difference, one that will change so many lives for the better.","Anthony Albanese, Prime Minister",True),
 ("WaldeComms are absolute PR guns of the highest calibre. Creative, persistent and lateral thinkers, they were the driving force behind the success of our Million Moves and Fit for Office campaigns.","Barrie Elvish, CEO, AUSactive",False),
 ("I wanted to say a big thank you for Saturday, was such a pleasure! Only YOU could find Guinness World Record-holding sheep, miniature ponies and a llama with just 24 hours’ notice! We really appreciate you bringing all the animals down from the Hunter Valley. It made our year – looking forward to the next one!","Ashleigh McCurtayne, Producer, Sunrise",True),
 ("Thank you so much for your help in coordinating today’s segment! Sarah and Jayne loved talking to Kathryn. It was such a great segment and an important chat.","Ruby Busutti, Producer, Today Show",True),
 ("Oh my goodness, what a weekend! I will treasure these memories for life! There are so many places this news can go. Thank you so much for going the extra mile to make it so special, and the fun times throughout!","Susannah George, Founder, Urban List",False),
 ("Thank you for putting my name to Channel 9. I’m now flooded with enquiries wanting to join my classes. This has made my 21-year effort serving the community worthwhile.","Dominic Yam, 88, Tai Chi Teacher",False),
]
# Team: Niki's own titles + bios (brief, 19 Nov 2026). Only who each person is and what they do. Four people, Helen removed.
# Each BIOS entry: (title after the dash, bio, LinkedIn url)
BIOS={
'niki':("NOISE WITH IMPACT","Big-picture thinker. International award-winner. Sharp news instincts, strategic thinking and serious impact. A straight-talking northern monkey. Former life on Fleet Street.","https://linkedin.com/in/niki-waldegrave-bb125a7"),
'lee':("DATA KING + AI WIZARD","Former partner of MullenLowe Sydney. Campaigns span government, South Park, TK Maxx, Harley-Davidson and BAFTA-winning documentaries. Didn\u2019t kill Kenny.","https://linkedin.com/in/lee-robson-pr"),
'eloise':("ENGINE BEHIND THE OUTREACH","Fast-moving, trend-spotting and brings heart and hustle. Knows what makes young Australians tick. Special interests in youth culture, entertainment, health, lifestyle and social change.","https://linkedin.com/in/eloise-brain-a0b735378"),
'risham':("STORYTELLER + BRAND SPECIALIST","Journalist-turned-marketer. Connects brands with audiences. Creative flair and strategic smarts. Health, advocacy, NFPs and higher education specialist. Alliteration ninja.","https://linkedin.com/in/risham-zaigham-7a1a3232"),
}
TEAM=[('niki','Niki Waldegrave','NIKI'),('lee','Lee Robson','LEE'),('eloise','Eloise Brain','ELOISE'),('risham','Risham Zaigham','RISHAM')]

# WORK page: one entry per campaign, in Niki's order. Text is hers (typos fixed). Nothing invented.
# splats = key stats shown in a teal paint splat: (big, label). bullets = proof points (<b> = bold result). quotes = pull quotes.
# img = deck image in /img (every Work card must have one). link = existing case-study page. ext = real outside coverage links (outlet, headline, url) for cards with no case-study page yet.
WORK=[
 dict(title='36 Months',desc='World-first law. Global impact.',
  line='From an idea by two worried dads to world-first legislation in just 6 months. Advocacy-led grassroots campaigns moved faster and further than almost any other in Australian political history.',
  splats=[('2.3B','impressions'),('7,000+','stories in Australia alone')],
  bullets=['<b>14 international awards</b> including <b>Cannes Lion Silver</b> for PR Effectiveness','UN General Assembly High-Level Week recognition','Sparked global movement'],
  img='36-months',link='36-months',crop=True),  # crop=True hides the deck image's footer box, which still says "13x international awards" (Niki: use 14)  # TODO(Niki): photo of the Cannes Lion, plus any extra impact stats and a clear photo or video
 dict(title='AUSactive',desc='Making movement national news',
  line="Put Australia\u2019s peak body for active health at the heart of national conversation.",
  splats=[('500+','stories'),('25M','reach'),('15,000+','sign-ups for Million Moves')],bullets=[],
  img='million-moves',link='million-moves-ausactive'),
 dict(title='The Sundays, Hamilton Island',desc='When paradise becomes the No.1 searched destination',
  line='',splats=[('#1','Google searched destination in 2025')],bullets=[],
  img='hamilton-island',link='hamilton-island'),  # TODO(Niki): Sundays has only one proof point ("More to come" x2 dropped)
 dict(title='NeonDynamo',desc='Where Vivid meets Glastonbury',
  line="When Vivid Sydney\u2019s Time: Warped turned Argyle Cut into a rave, we turned it into mainstream front-page news.",
  splats=[],bullets=[],img='neon-dynamo',link='neon-dynamo-sonar-music'),
 dict(title='Sonar Music',desc='From global fireworks to copyright firestorms',
  line="Making serious noise for Australia\u2019s most celebrated screen composers.",
  splats=[('241M','media reach')],
  bullets=["Amplified Jono Ma\u2019s euphoric Sydney NYE 9 x tonnes firework anthem, Higher Together",'<b>425 million</b> globally tuned in \u2013 we reached 241 million more',"Antony Partos\u2019 Artful Dodger score won a <b>2026 Screen Music Award</b>",'Backed his challenge taking on AI copyright dodgers with <b>3 million impressions</b>'],
  img='sonar-music',link=None,alt='Antony Partos with his 2026 Screen Music Award, the Sonar Music team wearing Human Made badges, and the Higher Together EP artwork for Jono Ma\u2019s Sydney NYE fireworks soundtrack',
  ext=[('The Sydney Morning Herald','\u2018Big and explosive\u2019: Musician behind NYE fireworks reveals his gameplan','https://www.smh.com.au/culture/music/big-and-explosive-musician-behind-nye-fireworks-reveals-his-gameplan-20251226-p5nq4q.html'),
       ('LBB','Sonar Music co-founders lead Sydney NYE and new Sydney Sweeney film','https://lbbonline.com/news/sonar-music-sydney-nye-jono-mar'),
       ('ABC News','Tales from Outer Suburbia composers win big at 2026 Screen Music Awards','https://www.abc.net.au/news/2026-10-28/screen-music-awards-winners-2026/107289982'),
       ('Campaign Brief','Composers wear Human Made badges at Screen Music Awards as Antony Partos takes on AI','https://campaignbrief.com/composers-wear-human-made-badges-at-screen-music-awards-as-antony-partos-takes-on-ai/')]),
 dict(title='MMAD \u2013 Futures Radio',desc='World-first \u201cradio rehab\u201d for young Australians in detention centres',
  line='Adult crime = adult time? No. Futures replaces the silence of the cell with positive programming \u2013 and it works.',
  splats=[],
  quotes=['\u201cIt only takes one person to believe in you \u2013 I never had that until Futures\u201d','\u201cIf it wasn\u2019t for Music Making a Difference, I wouldn\u2019t be here\u201d'],
  bullets=['Launched Futures \u201cStraight Outta Cobham\u201d with blanket Tier 1 coverage','Secured NSW Youth Justice Minister Jihad Dib and Tupac\u2019s friend, \u2018Mouseman\u2019','<b>500+ stories</b> helped national expansion; their voices changed perceptions #proud'],
  img='national-expansion',link='national-expansion'),
 dict(title='NOASIS',desc='Australia\u2019s supersonic rock n roll family half the world away',
  line='A baker by day, when he takes the stage, he turns into his father\u2019s older brother as Noel Gallagher \u2013 IYKYK',
  splats=[],bullets=[],img='noasis',link='noasis'),  # FLAG: Niki's NOASIS bullets are garbled, so only the descriptor and baker line are shown
 dict(title='Monique van Tulder',desc='From family breakdown to bestseller',
  line='When life got too much, Monique emailed her family from the airport \u2014 and took off.',
  splats=[],
  bullets=['Launched A Grown-Up\u2019s Gap Year, her unapologetic tale of midlife reinvention.','Secured national Tier 1 coverage and helped propel it to <b>#1 bestseller</b>.','Established Monique as a media go-to on relationships, family, work and running away from it all.'],
  img='monique-van-tulder',link=None,alt='The cover of A Grown-Up\u2019s Gap Year by Monique van Tulder, with the 9honey headline about her book',
  ext=[('Nine.com.au / 9honey','Fed up with the mental load, Monique drove away from her husband and kids and didn\u2019t return for months','https://www.nine.com.au/lifestyle/grown-up-gap-year-monique-van-tulder-book-exclusive-20250111-p5qp7x.html'),
       ('The Sydney Morning Herald','Midlife gap years and solo travel: why more mums are opting out of the mental load','https://www.smh.com.au/lifestyle/life-and-relationships/after-years-caring-for-her-family-monique-found-a-new-priority-herself-20250703-p5mc6i.html'),
       ('Mamamia','The Gap Year That Saved A Marriage','https://www.mamamia.com.au/podcasts/mid/monique-van-tulder-grown-up-gap-year/'),
       ('Booktopia','A Grown Up\u2019s Gap Year (the book)','https://www.booktopia.com.au/a-grown-up-s-gap-year-monique-van-tulder/book/9781923289543.html')]),
 dict(title='A Lasting Tale',desc='Making every life story count',
  line='Reached more than <b>27 million</b> Australians through launch publicity.',
  splats=[],bullets=[],img='lasting-tale',link='a-lasting-tale'),
]

# Services blocks (copy from Niki, 30 Oct 2026)
SERVICES=[
 ('Shape the news','Sharp news sense and premium contacts, so the story is told your way.'),
 ('Dominate the headlines','Precision execution that turns coverage into impact.'),
 ('Social','Smart social strategy that keeps the conversation going long after the headlines fade.'),
 ('Events','We love a party, a conference and the occasional hair-brained stunt that gets everyone talking.'),
 ('Content','Words that work. From punchy copy and compelling profiles to thought leadership and stories worth sharing.'),
]

# ---- Westwood Zine redesign (19 Nov 2026): small UI copy, all in one place ----
HOME_KICK=('PR','Sydney')   # ransom tiles + label (the old "Communications & content · Sydney" tagline stays deleted)
PIN_NOTE='That\u2019s Niki Waldegrave \u00b7 Noise with impact'
CLIPPINGS_H='The clippings'
MASTHEADS=['Sunrise','Today Show','Nova','Channel 9','AFR Weekend','Good Weekend','Urban List']  # PENDING PERMISSION: names stand in for masthead logos
# Character poses (files are byte-identical copies of Nick's PNGs in /workspace/waldecomms/characters; never edit them)
POSES={'instigator':('niki-instigator.png','Illustration of Niki Waldegrave, megaphone on her shoulder, hand on hip'),
       'rebel':('niki-rebel.png','Illustration of Niki Waldegrave with her fist raised, megaphone at her side'),
       'rally':('niki-rally.png','Illustration of Niki Waldegrave calling through her megaphone')}
CASE_POSE={'36-months':'rebel','a-lasting-tale':'rebel','national-expansion':'rebel'}  # other case studies use 'rally'
NOW_SHOWING=dict(kick='Now showing',title='NeonDynamo: Time: Warped',text='Where Vivid meets Glastonbury. When Vivid Sydney\u2019s Time: Warped turned Argyle Cut into a rave, we turned it into mainstream front-page news.',youtube='TSCt61_0Z-E',cap='Play the video')
# Showreel (Home). Files in /video, poster in /img.
REEL=dict(kick='Showreel',h2a='Watch the',h2b='REEL',btn='Sound on',aria='WaldeComms showreel',sm='/video/reel-720.mp4',lg='/video/reel-1080.mp4',poster='/img/reel-poster.jpg')

# TEMP hero bubble: speech bubble from Niki's megaphone on Home. Set to None to remove it. (Nick: temporary.)
HERO_BUBBLE="I never show up when I say I will"
