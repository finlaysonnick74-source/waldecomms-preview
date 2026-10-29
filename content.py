# ALL WaldeComms site copy and data. Edit here, then run: python3 build.py
import html
E=html.escape
# CONTACT: PLACEHOLDER. The deck has no email/phone. Confirm Niki's real address + number, then set PHONE.
EMAIL='hello@waldecomms.com.au'
PHONE=None  # e.g. ('+614xxxxxxxx','04xx xxx xxx') once confirmed
NAV=[('/work/','Work'),('/services/','Services'),('/noise-makers/','Noise-makers'),('/what-people-say/','What people say'),('/contact/','Contact')]
import json as _json, os as _os
COV=_json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','coverage','coverage.json'))) if _os.path.exists(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','coverage','coverage.json')) else _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'coverage.json')))
CASES=[
 dict(slug='hamilton-island',title='Hamilton Island',tape='Island of paradise',tags='travel',tag='Travel',img='hamilton-island',stat='#1',statl="Australia's most Google-searched destination, 2025",
  line="Helped Hamilton Island become Australia's #1 Google searched destination in 2025.",
  coverage=["Sunrise: “Island of Paradise”","AFR Weekend","“No trouble in paradise: Oatleys dig in on island”"],counters=[('#1','',"Google-searched destination in Australia, 2025")]),
 dict(slug='million-moves-ausactive',title='AUSactive & Million Moves',tape='Million Moves',tags='health',tag='Health / Fitness',img='million-moves',stat='Million Moves',statl='+ Fit for Office campaigns for AUSactive',
  line='Million Moves and Fit for Office: two campaigns for AUSactive.',
  quote=("WaldeComms are absolute PR guns of the highest calibre. Creative, persistent and lateral thinkers, they were the driving force behind the success of our Million Moves and Fit for Office campaigns.","Barrie Elvish, CEO, AUSactive"),
  coverage=['TV news','Print and online'],counters=[]),
 dict(slug='neon-dynamo-sonar-music',title='Neon Dynamo & Sonar Music',tape='Vivid Sydney & NYE',tags='music',tag='Music / Events',img='neon-dynamo',stat='Vivid + NYE',statl="Sydney New Year's Eve Midnight Soundtrack",
  line="Neon Dynamo and Sonar Music across Vivid Sydney and Sydney New Year's Eve, featuring Jono Ma (composer, Sydney New Year's Eve Midnight Soundtrack) and Antony Partos (co-founder, Sonar Music).",
  coverage=['“Short-cut cave gets Glastonbury tour”','TV news: Jono Ma, Antony Partos, Heath Campanaro'],counters=[]),
 dict(slug='a-lasting-tale',title='A Lasting Tale',tape='A Lasting Tale',tags='impact',tag='Social impact',img='lasting-tale',stat='27M reach',statl='= $80k new business',
  line='A human story that travelled: Good Weekend’s “For decades, Vince remembered what one teacher had told him. Then they met again.”',
  coverage=['Good Weekend: “Two of Us”','TV news'],counters=[(27,'M','reach'),(80,'k','new business ($)')]),
 dict(slug='noasis',title='Noasis',tape='Noasis',tags='music',tag='Music / Events',img='noasis',stat='Oasis reunion',statl='News hook: Noasis, the tribute act to the British rock group',
  line='When the Oasis reunion was confirmed, Noasis (the tribute act to the British rock group) was ready for the headlines.',
  coverage=['“Oasis reunion confirmed”','“Oasis… more like Noasis”'],counters=[]),
 dict(slug='36-months',title='36 Months',tape='World-first legislation',tags='impact',tag='Social impact',img='36-months',stat='World-first',statl='Legislation change for Australia',
  line="36 Months: the campaign that drove Australia's landmark world-first legislation change.",
  quote=("WaldeComms are weapons. Gritty hustlers who know the media landscape inside out and pitch like machines. They were mission critical in the success of 36 Months driving Australia’s landmark world-first legislation change.","Michael “Wippa” Wipfli, Nova host & 36 Months co-founder"),
  coverage=['13x international awards','7,000 stories','2.3 billion impressions'],counters=[(13,'x','international awards'),(7000,'','stories'),(2.3,' billion','impressions')]),
 dict(slug='national-expansion',title='National Expansion',tape='500+ stories',tags='expansion',tag='Expansion',img='national-expansion',stat='500+',statl='stories',
  line='A national expansion pushed into 500+ stories.',
  coverage=['Futures','“Music saved me”','Mouse Man'],counters=[(500,'+','stories')]),
]
FILTERS=[('all','All'),('travel','Travel'),('health','Health / Fitness'),('music','Music / Events'),('impact','Social impact'),('expansion','Expansion')]
# QUOTES: Albanese (PM), Sunrise, Today Show quotes are PENDING PERMISSION to publish (see site-plan.md). Shown for v1 review only.
QUOTES=[
 ("WaldeComms are absolute PR guns of the highest calibre. Creative, persistent and lateral thinkers, they were the driving force behind the success of our Million Moves and Fit for Office campaigns.","Barrie Elvish, CEO, AUSactive",False),
 ("WaldeComms are weapons. Gritty hustlers who know the media landscape inside out and pitch like machines. They were mission critical in the success of 36 Months driving Australia’s landmark world-first legislation change.","Michael “Wippa” Wipfli, Nova host & 36 Months co-founder",False),
 ("Thank you again for all the commitment, determination and energy you have poured into 36 Months. You are making a difference, one that will change so many lives for the better.","Anthony Albanese, Prime Minister",True),
 ("I wanted to say a big thank you for Saturday, was such a pleasure! Only YOU could find Guinness World Record-holding sheep, miniature ponies and a llama with just 24 hours’ notice! We really appreciate you bringing all the animals down from the Hunter Valley. It made our year – looking forward to the next one!","Ashleigh McCurtayne, Producer, Sunrise",True),
 ("Thank you so much for your help in coordinating today’s segment! Sarah and Jayne loved talking to Kathryn. It was such a great segment and an important chat.","Ruby Busutti, Producer, Today Show",True),
 ("Oh my goodness, what a weekend! I will treasure these memories for life! There are so many places this news can go. Thank you so much for going the extra mile to make it so special, and the fun times throughout!","Susannah George, Founder, Urban List",False),
 ("Thank you for putting my name to Channel 9. I’m now flooded with enquiries wanting to join my classes. This has made my 21-year effort serving the community worthwhile.","Dominic Yam, 88, Tai Chi Teacher",False),
]
# Team bios: facts only, each from the sources listed.
BIOS={
# https://www.theguardian.com/media/2002/oct/31/pressandpublishing (Daily Star Bitches 2001, Sunday Mirror, The People, Mirror 3am 2002)
# https://muckrack.com/niki-waldegrave (Daily Mail, Mirror, Sun; News of the World)
# https://www.bandt.com.au/author/niki-waldegrave/ (award-winning journalist; trained teams of 5 to 37; outdoor media sales AU/UK)
# https://linkedin.com/in/niki-waldegrave-bb125a7 (In The Media PR campaign manager 2018; WaldeComms Jan 2021; NCTJ Darlington College)
'niki':("Fleet Street trained, tabloid tested. Niki was an original on the Daily Star's Bitches column in 2001, worked the Sunday Mirror and The People, then got poached by Piers Morgan for the Mirror's 3am showbiz column in 2002. Since then: News of the World, magazine editing, B&T in Sydney, award-winning reporting and teams of up to 37 trained. Campaign manager at In The Media PR from 2018, WaldeComms since 2021. NCTJ-qualified. Little black book: bursting.","https://linkedin.com/in/niki-waldegrave-bb125a7"),
# https://campaignbrief.com/former-303-mullenlowe-mp-lee-robson-launches-communications-content-consultancy-istories/
# https://istories.io/about ; https://linkedin.com/in/lee-robson-pr
'lee':("25 years making content companies famous. Lee was managing partner at 303 MullenLowe Sydney and head of publicity at Fox Sports, after five years as a senior publicist at Sky Television in the UK. He founded LRPR, named Best New Agency at the 2015 Prolific North awards, then iStories in 2019. Accounts directed: Harley-Davidson, Peugeot, Discovery Channel, TK Maxx, ESPN. Qualified in data analytics and a Claude Certified Associate, he runs the AI side of the noise.","https://linkedin.com/in/lee-robson-pr"),
# https://www.linkedin.com/posts/eloise-brain-a0b735378_always-chasing-those-extra-quotes-and-what-activity-7468258623182454784-HBHk (NeonDynamo coverage post, June 2026)
# WaldeComms credentials deck (role, heart + hustle) — owned source
'eloise':("The engine behind the outreach. Eloise is the one still chasing the extra quote after everyone else has gone home. On NeonDynamo she helped land a run of media coverage and, in her words, \u201ca standout result\u201d. Fast-paced, persistent and switched on to what people are talking about, she brings heart and hustle to every pitch, every follow-up and every campaign that leaves the WaldeComms office. Phone always warm, follow-up always sent.","https://linkedin.com/in/eloise-brain-a0b735378"),
# https://linkedin.com/in/risham-zaigham-7a1a3232
'risham':("Ten-plus years connecting brands with the people who buy into them. Risham has worked at Ogilvy & Mather, in higher education and medical research at Griffith University and Eskitis, and in local government at Brisbane and Logan City Councils. She spent five years running communications for the Hornsby Rainbow Club, a social club for kids with disability. Her toolkit: brand and comms strategy, stakeholder engagement, copywriting, websites and healthcare advocacy. Health, NFP and education stories are her home turf.","https://linkedin.com/in/risham-zaigham-7a1a3232"),
# https://linkedin.com/in/helen-brunton-25804a11a
'helen':("Big screens, bigger crowds. Helen has run giant LED live sites at some of the loudest events going: football and rugby world cups, the Tour de France, the British Lions, NRL, AFL, the Melbourne Cup, Moomba and New Year's Eve. Director of Exclusive Media since 2014 and general manager at Nvisage Media for five years before that, she has worked with councils from Melbourne to Auckland to York. At WaldeComms she keeps the books straight and the events on budget.","https://linkedin.com/in/helen-brunton-25804a11a"),
}

TEAM=[('niki','Niki Waldegrave','Director','Makes noise with impact',"Comms strategist, ex-Fleet Street journalist and straight-talking northern monkey. 30 years' media experience, sharp news sense, premium contacts and precision execution.",'Ex-Fleet Street, 30 yrs'),
 ('lee','Lee Robson','AI / Strategy / Social','Data king + content marketer','Former MullenLowe Sydney managing partner and media veteran of 20+ years. Clients include South Park, The Simpsons, TK Maxx, Harley-Davidson, governments and BAFTA docos.','20+ yrs media'),
 ('eloise','Eloise Brain','PR Executive','Engine behind the outreach','A fast-paced PR go-getter bringing heart and hustle to every campaign, with persistence, energy and a keen eye for trends and conversations.','Heart + hustle'),
 ('risham','Risham Zaigham','PR Executive','Storyteller + brand specialist','Blends creativity with strategy, connecting customers with brands for more than a decade; special interest in NFPs, health, advocacy and higher education.','10+ yrs brand'),
 ('helen','Helen Brunton','Accounts','Bean counter + events','Media and events expert of 30+ years, running events and live sites across Asia Pacific and Europe.','30+ yrs events')]
