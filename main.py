import re,os.path

_str = '''
00 = {str} 'https://www.gamespot.com/articles/god-of-war-ragnarok-all-jewel-of-yggdrasil-locations/1100-6509474/'
01 = {str} 'https://www.gamespot.com/articles/pokemon-scarlet-and-violet-breeding-and-egg-power-guide/1100-6509460/'
02 = {str} 'https://www.gamespot.com/articles/god-of-war-ragnarok-all-jewel-of-yggdrasil-locations/1100-6509474/'
03 = {str} 'https://www.gamespot.com/articles/pokemon-scarlet-and-violet-breeding-and-egg-power-guide/1100-6509460/'
04 = {str} 'https://www.gamespot.com/articles/amazon-is-selling-super-mario-3d-world-bowsers-fury-for-just-40/1100-6509475/'
05 = {str} 'https://www.gamespot.com/articles/dualsense-ps5-controllers-steeply-discounted-for-black-friday/1100-6509280/'
06 = {str} 'https://www.gamespot.com/articles/black-friday-deal-get-demons-souls-for-29/1100-6509312/'
07 = {str} 'https://www.gamespot.com/articles/get-a-free-metroidvania-on-gog-for-a-limited-time/1100-6509472/'
08 = {str} 'https://www.gamespot.com/articles/new-sling-tv-subscribers-can-get-a-free-amazon-fire-stick-lite-and-a-discounted-month-of-streaming/1100-6509473/'
09 = {str} 'https://www.gamespot.com/articles/fortnite-chapter-4-start-date-battle-pass-leaks/1100-6509089/'
10 = {str} 'https://www.gamespot.com/articles/vampire-survivors-gets-new-stage-and-more-to-help-you-ignore-your-family-on-thanksgiving/1100-6509470/'
11 = {str} 'https://www.gamespot.com/articles/dead-island-2-showcase-will-show-more-action-gore-and-zombies-on-december-6/1100-6509471/'
12 = {str} 'https://www.gamespot.com/articles/all-hail-paimon-hereditary-gingerbread-treehouse-kit-is-here/1100-6509469/'
13 = {str} 'https://www.gamespot.com/articles/you-can-get-an-entire-year-of-paramount-plus-for-half-off-right-now-for-black-friday/1100-6509468/'
14 = {str} 'https://www.gamespot.com/articles/witcher-3-adding-photo-mode-new-camera-settings-for-pc-in-big-new-update/1100-6509459/'
15 = {str} 'https://www.gamespot.com/articles/black-panther-wakanda-forever-writer-reveals-who-almost-took-over-title-role/1100-6509467/'
16 = {str} 'https://www.gamespot.com/articles/gamespot-sweepstakes-in-collaboration-with-stockx/1100-6509050/'
17 = {str} 'https://www.gamespot.com/articles/the-best-switch-controller-is-discounted-for-black-friday/1100-6509454/'
18 = {str} 'https://www.gamespot.com/articles/triangle-strategy-is-just-42-for-black-friday/1100-6509438/'
19 = {str} 'https://www.gamespot.com/articles/there-were-alternate-endings-to-the-walking-dead-finale/1100-6509466/'
20 = {str} 'https://www.gamespot.com/articles/this-500-gaming-chair-is-only-200-for-black-friday/1100-6509457/'
21 = {str} 'https://www.gamespot.com/articles/avatar-2-expected-to-make-lots-more-money-than-the-first-movie-for-its-opening-weekend/1100-6509462/'
22 = {str} 'https://www.gamespot.com/articles/netflix-is-hiring-for-a-brand-new-aaa-pc-game/1100-6509465/'
23 = {str} 'https://www.gamespot.com/articles/the-callisto-protocol-opening-minutes-have-leaked-online/1100-6509463/'
24 = {str} 'https://www.gamespot.com/articles/pokemon-scarlet-and-violet-all-class-answers-and-rewards/1100-6509461/'
25 = {str} 'https://www.gamespot.com/articles/rampant-crunch-at-japanese-game-devs-is-an-unspoken-reality-heres-why/1100-6509422/'
26 = {str} 'https://www.gamespot.com/articles/top-gun-maverick-comes-to-streaming-in-december-heres-when-and-how-to-watch/1100-6509458/'
27 = {str} 'https://www.gamespot.com/articles/elden-ring-is-discounted-to-just-35-for-black-friday/1100-6509318/'
28 = {str} 'https://www.gamespot.com/articles/some-people-still-dont-know-the-right-way-to-remove-gamecube-discs/1100-6509455/'
29 = {str} 'https://www.gamespot.com/articles/netflixs-wednesday-will-tim-burton-be-back-for-season-2/1100-6509456/'
30 = {str} 'https://www.gamespot.com/articles/netflixs-wednesday-season-1-finale-ending-and-cliffhangers-explained-by-showrunners/1100-6509451/'
31 = {str} 'https://www.gamespot.com/articles/get-bayonetta-3-for-45-right-now/1100-6509452/'
32 = {str} 'https://www.gamespot.com/articles/todays-wordle-answer-523-november-24-2022/1100-6509453/'
33 = {str} 'https://www.gamespot.com/articles/for-some-pokemon-fans-scarlet-and-violet-are-the-latest-in-a-string-of-disappointments/1100-6509446/'
34 = {str} 'https://www.gamespot.com/articles/luigis-mansion-3-gets-big-discount-for-black-friday/1100-6509423/'
35 = {str} 'https://www.gamespot.com/articles/sony-mentions-ps6-release-year-if-only-this-document-werent-redacted/1100-6509450/'
36 = {str} 'https://www.gamespot.com/articles/masahiro-sakurai-seemingly-teases-kid-icarus-uprising-for-nintendo-switch/1100-6509449/'
37 = {str} 'https://www.gamespot.com/articles/the-walking-deads-jeffrey-dean-morgan-on-the-future-of-negan/1100-6509448/'
'''

_s1 = "00 = {str} 'https://www.gamespot.com/articles/god-of-war-ragnarok-all-jewel-of-yggdrasil-locations/1100-6509474/'"
_s1 = "fdsfdsf"
xs = re.findall("/\d+-\d+/",_s1)
# if len(xs) > 0:
#     if xs[]
print()
for x in xs:
    x = x.replace('/','')
    if os.path.isfile('./datas/'+x+'.json'):
        print(x)