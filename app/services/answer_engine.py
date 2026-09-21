"""
MEGA ISLAMIC ANSWER ENGINE
Answers ALL Islamic questions using multiple sources:
- External APIs (Quran Cloud, Hadith API, Aladhan, IslamHouse)
- Internal Knowledge Base
- Q&A Database
- Vector Search
- Quran/Hadith Search
"""
from typing import Dict, Any, List, Optional
from app.services.multi_api_service import multi_api
from app.services.query_router import query_router
from app.services.islamic_corpus import search_qa, search_quran_verses, search_hadith
from app.services.vector_store import vector_store
from app.services.text_ingester import text_ingester

class IslamicAnswerEngine:
    """Ultimate Islamic answer engine - API-first with local fallbacks"""
    
    def __init__(self):
        self.initialized = False
        self.knowledge_cache = {}
    
    def initialize(self):
        """Load all local texts into vector store"""
        if not self.initialized:
            text_ingester.load_all_texts()
            self.initialized = True
    
    def answer(self, query: str) -> Dict[str, Any]:
        """Answer any Islamic question - tries multiple sources"""
        self.initialize()
        query_lower = query.lower()
        
        # Step 1: Try external APIs (fastest, most accurate for specific queries)
        api_answer = self._try_api_sources(query)
        if api_answer and api_answer.get("confidence", 0) > 0.8:
            return api_answer
        
        # Step 2: Try specific knowledge base (common questions)
        specific = self._try_specific_knowledge(query_lower)
        if specific:
            return specific
        
        # Step 3: Try Q&A database
        qa = self._try_qa_database(query_lower)
        if qa:
            return qa
        
        # Step 4: Try Quran search
        quran = self._try_quran_search(query)
        if quran:
            return quran
        
        # Step 5: Try Hadith search
        hadith = self._try_hadith_search(query)
        if hadith:
            return hadith
        
        # Step 6: Try vector search
        vector = self._try_vector_search(query)
        if vector:
            return vector
        
        # Step 7: Combine API + local results
        combined = self._try_combined_search(query)
        if combined:
            return combined
        
        # Step 8: Final fallback
        return self._get_ai_response(query)
    
    # ==================== EXTERNAL API SOURCES ====================
    
    def _try_api_sources(self, query: str) -> Optional[Dict]:
        """Try external APIs for answer"""
        try:
            # Classify the query
            classification = query_router.classify_query(query)
            
            if not classification.get("needs_api", False):
                return None
            
            # Execute API calls based on classification
            for api_call in classification.get("api_calls", []):
                api_name = api_call["api"]
                method_name = api_call["method"]
                params = api_call.get("params", {})
                
                try:
                    api_method = getattr(multi_api, method_name, None)
                    if not api_method:
                        continue
                    
                    # Quran verse lookup
                    if method_name == "get_quran_verse":
                        surah = params.get("surah", 1)
                        ayah = params.get("ayah", 1)
                        result = api_method(surah, ayah)
                        
                        if result and "translation" in result:
                            return {
                                "answer": (
                                    f"📖 **{result.get('surah', f'Surah {surah}')} "
                                    f"({surah}:{ayah})**\n\n"
                                    f"_{result.get('translation', '')}_\n\n"
                                    f"📚 Source: {result.get('source', 'Quran API')}"
                                ),
                                "source": result.get('source', 'Quran Cloud API'),
                                "confidence": 0.95,
                                "method": "api_quran_verse"
                            }
                    
                    # Hadith search
                    elif method_name == "search_hadith_multi":
                        results = api_method(params.get("query", query))
                        if results:
                            answer = "📜 **From Hadith:**\n\n"
                            for i, r in enumerate(results[:3], 1):
                                text = r.get('text', '')[:300]
                                answer += f"**{i}.** _{text}_\n"
                                answer += f"└─ {r.get('source', 'Hadith')}\n\n"
                            
                            return {
                                "answer": answer,
                                "source": "Hadith API",
                                "confidence": 0.9,
                                "method": "api_hadith_search"
                            }
                    
                    # Prayer times
                    elif method_name == "get_prayer_times":
                        city = params.get("city", "Makkah")
                        result = api_method(city)
                        
                        if result and "timings" in result:
                            timings = result["timings"]
                            answer = f"🕌 **Prayer Times**\n\n"
                            answer += f"📍 {result.get('city', city)}\n"
                            answer += f"📅 {result.get('date', 'Today')}\n\n"
                            
                            for prayer in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                                if prayer in timings:
                                    answer += f"• **{prayer}**: {timings[prayer]}\n"
                            
                            return {
                                "answer": answer + f"\n📚 Source: {result.get('source', 'Aladhan API')}",
                                "source": "Aladhan API",
                                "confidence": 0.95,
                                "method": "api_prayer_times"
                            }
                    
                    # IslamHouse search
                    elif method_name == "search_islamhouse":
                        results = api_method(params.get("query", query))
                        if results:
                            answer = "📚 **From Islamic Resources:**\n\n"
                            for r in results[:3]:
                                title = r.get('title', 'Resource')
                                desc = r.get('description', '')[:200]
                                answer += f"**{title}**\n{desc}...\n\n"
                            
                            return {
                                "answer": answer + f"📚 Source: IslamHouse",
                                "source": "IslamHouse API",
                                "confidence": 0.85,
                                "method": "api_islamhouse"
                            }
                
                except Exception as e:
                    print(f"  ⚠️ API {method_name} error: {e}")
                    continue
        
        except Exception as e:
            print(f"⚠️ API routing error: {e}")
        
        return None
    
    # ==================== LOCAL KNOWLEDGE SOURCES ====================
    
    def _try_specific_knowledge(self, query: str) -> Optional[Dict]:
        """Try specific knowledge base for exact matches"""
        
        knowledge = {
            # ========== ALLAH ==========
            "who is allah": {
                "answer": "Allah is the One and Only God, Creator of everything. He is Ar-Rahman (Most Gracious), Ar-Raheem (Most Merciful). He has 99 beautiful names. He is Eternal, Self-Sufficient, and nothing is comparable to Him.\n\n📖 \"Say, He is Allah, [who is] One. Allah, the Eternal Refuge. He neither begets nor is born, nor is there to Him any equivalent.\" (Quran 112:1-4)",
                "source": "Quran 112:1-4",
                "confidence": 0.95
            },
            "who created allah": {
                "answer": "Allah is the Creator of everything and is Himself UNCREATED. He is Al-Awwal (The First - nothing was before Him) and Al-Akhir (The Last - nothing will remain after Him). This question itself is flawed because the Creator cannot be created - He has always existed. The universe and everything in it is created, but the Creator is eternal with no beginning.",
                "source": "Quran 57:3, Islamic Theology",
                "confidence": 0.95
            },
            "where is allah": {
                "answer": "Allah is above His Throne (Arsh) above the seven heavens, as mentioned in the Quran: 'The Most Merciful [who is] above the Throne established' (20:5). However, His knowledge encompasses everything, and He is with us by His knowledge, hearing, and seeing. He is not contained within His creation.",
                "source": "Quran 20:5, 67:16, Islamic Theology",
                "confidence": 0.9
            },
            "does allah exist": {
                "answer": "Yes, Allah exists. Evidence includes:\n\n1. The order and complexity of the universe points to a Creator\n2. The Quran as a miraculous, preserved book\n3. The innate human disposition (fitrah) to believe in a Creator\n4. The prophecies of Prophet Muhammad ﷺ that came true\n5. The answered prayers of believers throughout history\n\n📖 \"Were they created by nothing, or were they themselves the creators?\" (Quran 52:35)",
                "source": "Quran 52:35, Islamic Theology",
                "confidence": 0.9
            },
            "99 names of allah": {
                "answer": "Allah has 99 beautiful names (Asma ul-Husna). Key names include:\n\n• Ar-Rahman (الرحمن) - The Most Gracious\n• Ar-Raheem (الرحيم) - The Most Merciful\n• Al-Malik (الملك) - The King\n• Al-Quddus (القدوس) - The Most Holy\n• As-Salam (السلام) - The Source of Peace\n• Al-Khaliq (الخالق) - The Creator\n• Al-Ghaffar (الغفار) - The All-Forgiving\n• Ar-Razzaq (الرزاق) - The Provider\n• Al-Alim (العليم) - The All-Knowing\n• Al-Hakim (الحكيم) - The Wise\n\n📖 \"And to Allah belong the best names, so invoke Him by them.\" (Quran 7:180)\n📜 The Prophet ﷺ said: \"Allah has 99 names. Whoever memorizes them enters Paradise.\" (Sahih al-Bukhari 2736)",
                "source": "Quran 7:180, Sahih al-Bukhari 2736",
                "confidence": 0.95
            },
            "what is rahman": {
                "answer": "AR-RAHMAN (الرحمن) means The Most Gracious, The Most Merciful. It indicates Allah's vast, all-encompassing mercy that extends to ALL creation - believers and non-believers, humans and animals, in this world. It is one of Allah's greatest names and appears at the beginning of every surah (except Surah 9).\n\n📖 \"The Most Merciful (Ar-Rahman) - Taught the Quran, Created man.\" (Quran 55:1-3)\n\nDifference between Ar-Rahman and Ar-Raheem:\n• Ar-Rahman: General mercy for all in this world\n• Ar-Raheem: Special mercy for believers in the Hereafter",
                "source": "Quran 55:1-3, Tafsir",
                "confidence": 0.9
            },
            
            # ========== PROPHET MUHAMMAD ==========
            "who is prophet muhammad": {
                "answer": "PROPHET MUHAMMAD ﷺ (570-632 CE) is the final Messenger of Allah, sent as a mercy to all mankind.\n\n• Born in Makkah, Year of the Elephant (570 CE)\n• Received first revelation at age 40 in Cave Hira\n• Migrated to Madinah in 622 CE (Hijrah - start of Islamic calendar)\n• Passed away in 632 CE at age 63\n• Known as Al-Amin (Trustworthy) and As-Sadiq (Truthful)\n\n📖 \"And We have not sent you, [O Muhammad], except as a mercy to the worlds.\" (Quran 21:107)\n📖 \"Indeed, in the Messenger of Allah you have an excellent example.\" (Quran 33:21)",
                "source": "Quran 21:107, 33:21",
                "confidence": 0.95
            },
            "when was prophet muhammad born": {
                "answer": "Prophet Muhammad ﷺ was born on Monday, 12th of Rabi' al-Awwal, in the Year of the Elephant (approximately 570 CE). He was born in Makkah to Abdullah (father, who died before his birth) and Aminah (mother, who died when he was 6 years old).\n\nThis date is known as Mawlid al-Nabi. There are scholarly differences regarding celebrating this day. What is agreed upon is that we should love and follow the Prophet ﷺ every day.",
                "source": "Seerah of Ibn Ishaq",
                "confidence": 0.9
            },
            "did muhammad write the quran": {
                "answer": "NO. Prophet Muhammad ﷺ did NOT write the Quran. He was illiterate (Ummi) - he could not read or write. The Quran is the literal word of Allah, revealed to him through Angel Jibreel (Gabriel) over 23 years.\n\n📖 \"And you [O Muhammad] did not recite any scripture before it, nor did you inscribe it with your right hand. Otherwise the falsifiers would have had [cause for] doubt.\" (Quran 29:48)\n\nScribes wrote down the revelations as they were revealed, and it was compiled into a book after his death during the caliphate of Abu Bakr (RA) and standardized during Uthman (RA).",
                "source": "Quran 29:48, Sahih al-Bukhari",
                "confidence": 0.95
            },
            
            # ========== QURAN ==========
            "what is the quran": {
                "answer": "THE HOLY QURAN is the literal word of Allah, revealed to Prophet Muhammad ﷺ through Angel Jibreel over approximately 23 years (610-632 CE).\n\n• 114 Surahs (chapters)\n• ~6,236 verses\n• 30 Juz (parts)\n• Revealed in Arabic\n• Preserved unchanged for 1400+ years\n\n📖 \"Indeed, it is We who sent down the Quran and indeed, We will be its guardian.\" (Quran 15:9)\n\nThe Quran is the primary source of Islamic guidance, covering faith, worship, law, morality, and stories of previous prophets.",
                "source": "Quran 15:9",
                "confidence": 0.95
            },
            "how many surahs in quran": {
                "answer": "The Quran has 114 Surahs (chapters).\n\n• 86 Makki (Meccan - revealed before Hijrah)\n• 28 Madani (Medinan - revealed after Hijrah)\n\nTotal verses: Approximately 6,236 (scholars differ slightly on the count).\n\nThe longest surah is Al-Baqarah (286 verses) and the shortest is Al-Kawthar (3 verses).",
                "source": "Quran",
                "confidence": 0.95
            },
            "is the quran preserved": {
                "answer": "YES, the Quran is perfectly preserved. Allah promised: 'Indeed, it is We who sent down the Quran and indeed, We will be its guardian.' (15:9)\n\nPreservation methods:\n1. Memorized by thousands during the Prophet's lifetime\n2. Written down by scribes as revealed\n3. Compiled into a book by Abu Bakr (RA)\n4. Standardized and distributed by Uthman (RA)\n5. Continuous oral transmission (Tawatur) generation after generation\n6. Today, every Quran in the world is IDENTICAL - letter for letter\n\nThis is a unique miracle - no other religious scripture has this level of preservation.",
                "source": "Quran 15:9, Sahih al-Bukhari",
                "confidence": 0.95
            },
            
            # ========== PRAYER ==========
            "how to pray": {
                "answer": "HOW TO PERFORM SALAH (PRAYER):\n\n1. **Niyyah** - Intention in heart\n2. **Takbir** - Raise hands, say 'Allahu Akbar'\n3. **Qiyam** - Standing, recite Al-Fatiha + additional surah\n4. **Ruku** - Bow, say 'Subhana Rabbi al-Azim' 3x\n5. **Stand up** - 'Sami Allahu liman hamidah'\n6. **Sujud** - Prostrate, say 'Subhana Rabbi al-A'la' 3x (do twice)\n7. **Repeat** for each rak'ah\n8. **Tashahhud** - Final sitting, recite Tashahhud\n9. **Salam** - Turn head right then left, 'Assalamu alaikum wa rahmatullah'\n\nPrayer times: Fajr (2), Dhuhr (4), Asr (4), Maghrib (3), Isha (4)\n\n📖 'Indeed, prayer has been decreed upon the believers a decree of specified times.' (Quran 4:103)",
                "source": "Quran 4:103, Sahih al-Bukhari",
                "confidence": 0.9
            },
            "what breaks wudu": {
                "answer": "WUDU (ABLUTION) IS NULLIFIED BY:\n\n1. Natural discharges - urine, stool, passing gas\n2. Deep sleep (where one loses consciousness)\n3. Loss of consciousness - fainting, intoxication\n4. Touching private parts directly without barrier (difference of opinion)\n5. Eating camel meat (according to Hanbali school)\n6. Sexual intercourse (requires Ghusl - full bath)\n7. Anything that exits the body from private parts\n\n📜 The Prophet ﷺ said: 'Allah does not accept the prayer of any of you if he breaks his wudu until he performs wudu again.' (Sahih al-Bukhari)",
                "source": "Sahih al-Bukhari, Sahih Muslim",
                "confidence": 0.9
            },
            
            # ========== FASTING ==========
            "what breaks fast": {
                "answer": "THINGS THAT BREAK THE FAST:\n\n1. Eating or drinking intentionally\n2. Sexual intercourse during fasting hours\n3. Intentional vomiting\n4. Menstruation or post-natal bleeding\n5. Ejaculation from intentional stimulation\n6. Nutritional injections\n\nTHINGS THAT DO NOT BREAK THE FAST:\n• Brushing teeth (avoid swallowing)\n• Showering/bathing\n• Unintentional vomiting\n• Swallowing saliva\n• Medical injections (non-nutritional)\n• Tasting food without swallowing (if necessary)\n\n📖 '...Eat and drink until the white thread of dawn becomes distinct from the black thread. Then complete the fast until sunset.' (Quran 2:187)",
                "source": "Quran 2:187, Fiqh of Fasting",
                "confidence": 0.9
            },
            
            # ========== MARRIAGE/DIVORCE ==========
            "nikah conditions": {
                "answer": "CONDITIONS FOR VALID NIKAH (MARRIAGE):\n\n1. **Mutual consent** of both bride and groom\n2. **Wali** (male guardian) for the bride\n3. **Two adult Muslim male witnesses** (or 1 male + 2 females)\n4. **Mahr** (dowry) given by groom to bride\n5. **Offer and acceptance** (Ijab wa Qabul) in same sitting\n6. Both parties must be eligible (not mahram, not in iddah)\n\n📖 'And marry the unmarried among you...' (Quran 24:32)\n📜 The Prophet ﷺ said: 'There is no marriage without a guardian.' (Sunan Abu Dawud 2085)",
                "source": "Quran 24:32, Sunan Abu Dawud",
                "confidence": 0.9
            },
            "triple talaq": {
                "answer": "TRIPLE TALAQ (Three divorces at once):\n\nGiving three divorces at one time is considered **BID'AH** (innovation) and HARAM by most scholars. The Prophet ﷺ was angry when he heard someone did this.\n\nAccording to the majority of scholars (Hanafi, Maliki, Hanbali), triple talaq in one sitting counts as three divorces and is final (the couple cannot remarry without the wife marrying another man legitimately).\n\nHowever, some scholars (Ibn Taymiyyah, some contemporary scholars) view it as only ONE divorce.\n\nThe CORRECT Islamic procedure is to give ONE divorce at a time, with waiting periods (iddah) between each, allowing reconciliation.\n\n📖 'Divorce is twice. Then either keep [her] in an acceptable manner or release [her] with good treatment.' (Quran 2:229)",
                "source": "Quran 2:229, Sahih Muslim",
                "confidence": 0.85
            },
            
            # ========== HALAL/HARAM ==========
            "is music haram": {
                "answer": "The ruling on MUSIC differs among scholars:\n\n**Majority opinion (Hanafi, Shafi'i, Maliki, Hanbali):**\nMusical instruments are HARAM based on hadith.\n\n📜 The Prophet ﷺ said: 'There will be among my Ummah people who will permit silk, alcohol, and musical instruments.' (Sahih al-Bukhari 5590)\n\n**Minority opinion:**\nSome scholars permit vocals (nasheed) without instruments. A few permit all music with good, moral lyrics.\n\n**All scholars agree:**\n• Music promoting sin (alcohol, sex, violence) is absolutely haram\n• Religious nasheeds with duff (simple drum) are permitted by most\n• Quran recitation with proper Tajweed is praiseworthy\n\nThe safest opinion is to avoid instrumental music.",
                "source": "Sahih al-Bukhari 5590, Scholarly consensus",
                "confidence": 0.85
            },
            "is smoking haram": {
                "answer": "Most CONTEMPORARY scholars rule SMOKING as HARAM because:\n\n1. It harms the body - 📖 'Do not throw yourselves into destruction' (2:195)\n2. It wastes money (Israf) - wasteful spending is prohibited\n3. It harms others (second-hand smoke)\n4. It is addictive and intoxicating\n\nEarlier scholars (before medical evidence) often said it was MAKRUH (disliked). Today, with clear medical evidence of harm, the majority say it is HARAM.\n\n📖 'Do not kill yourselves. Allah is merciful to you.' (Quran 4:29)",
                "source": "Quran 2:195, 4:29, Contemporary Fiqh",
                "confidence": 0.85
            },
            "is cryptocurrency halal": {
                "answer": "Scholars DIFFER on cryptocurrency:\n\n**Those who say HALAL:**\n• It is a digital asset with value\n• No interest (riba) involved in trading\n• Can be used for legitimate transactions\n\n**Those who say HARAM:**\n• Extreme volatility (gharar - uncertainty)\n• Used for illegal activities (anonymity)\n• Speculative gambling (maysir)\n• Not regulated by any authority\n\n**Middle opinion:**\nPermissible if used as currency (not speculation), avoiding haram activities, and following Islamic finance principles.\n\nConsult your local scholar for personalized guidance.",
                "source": "Contemporary Islamic Finance Scholars",
                "confidence": 0.7
            },
            
            # ========== JESUS IN ISLAM ==========
            "jesus in islam": {
                "answer": "MUSLIMS BELIEVE IN PROPHET ISA (JESUS) عليه السلام:\n\n• Born miraculously to Virgin Maryam (Mary)\n• Not the son of God - he is a Prophet and Messenger\n• Performed miracles by Allah's permission\n• Was NOT crucified - Allah raised him to heaven\n• Will RETURN before the Day of Judgment\n• Will defeat the Dajjal (Antichrist)\n• Will rule with justice according to Islam\n• Will die and be buried in Madinah\n\n📖 'The Messiah, Jesus, son of Mary, was only a messenger of Allah.' (Quran 4:171)\n📖 'They did not kill him, nor did they crucify him; but [another] was made to resemble him.' (Quran 4:157)",
                "source": "Quran 4:171, 4:157, 3:45-55",
                "confidence": 0.95
            },
            
            # ========== DEATH/AFTERLIFE ==========
            "what happens after death": {
                "answer": "AFTER DEATH IN ISLAM:\n\n1. **Death** - Soul taken by Angel of Death\n2. **Grave** - Questioning by Munkar and Nakir\n   - 'Who is your Lord?' - 'Allah'\n   - 'What is your religion?' - 'Islam'\n   - 'Who is your prophet?' - 'Muhammad ﷺ'\n3. **Barzakh** - Period between death and resurrection (comfort or torment)\n4. **Resurrection** - All souls resurrected on Judgment Day\n5. **Accountability** - Deeds weighed on scales\n6. **Sirat** - Bridge over Hell, thinner than hair\n7. **Jannah or Jahannam** - Final destination\n\n📖 'Every soul will taste death. Then to Us will you be returned.' (Quran 29:57)",
                "source": "Quran 29:57, Sahih al-Bukhari",
                "confidence": 0.9
            },
            "how to go to jannah": {
                "answer": "TO ENTER JANNAH (PARADISE):\n\n1. Believe in One Allah and Prophet Muhammad ﷺ\n2. Perform the 5 pillars of Islam\n3. Avoid major sins (kaba'ir)\n4. Do righteous deeds sincerely for Allah\n5. Repent regularly (Tawbah)\n6. Have good character (Husn al-Khuluq)\n7. Treat others with justice and mercy\n\n📜 The Prophet ﷺ said: 'Whoever dies while not associating anything with Allah will enter Paradise.' (Sahih al-Bukhari)\n\n📖 'And give good tidings to those who believe and do righteous deeds that they will have gardens [in Paradise] beneath which rivers flow.' (Quran 2:25)",
                "source": "Quran 2:25, Sahih al-Bukhari",
                "confidence": 0.9
            },
            
            # ========== MODERN ISSUES ==========
            "organ donation islam": {
                "answer": "Most scholars PERMIT organ donation based on:\n\n1. Saving a life: 'Whoever saves one - it is as if he had saved mankind entirely' (Quran 5:32)\n2. Necessity (darurah) makes the prohibited permissible\n3. It is a form of ongoing charity (sadaqah jariyah)\n\n**Conditions:**\n• Free consent (no coercion)\n• No financial compensation (donation, not sale)\n• No harm to living donor's health\n• Genuine medical need\n• Deceased donor must be confirmed dead by medical experts\n\nSome scholars are cautious due to sanctity of the body. Consult your local scholar.",
                "source": "Quran 5:32, Islamic Medical Ethics",
                "confidence": 0.8
            },
            "is insurance halal": {
                "answer": "CONVENTIONAL INSURANCE is generally HARAM due to:\n\n1. **Gharar** (uncertainty) - you pay but may never receive anything\n2. **Maisir** (gambling) - payment depends on uncertain future events\n3. **Riba** (interest) - insurance companies invest in interest-bearing instruments\n\n**ISLAMIC INSURANCE (TAKAFUL)** is HALAL:\n• Based on mutual cooperation and shared responsibility\n• Participants contribute to a common fund\n• Operates on Islamic principles (no riba, no gharar)\n• Widely available in Muslim countries and some Western countries\n\n📖 'And cooperate in righteousness and piety, but do not cooperate in sin and aggression.' (Quran 5:2)",
                "source": "Quran 5:2, Islamic Finance",
                "confidence": 0.85
            },
            
            # ========== SECTS ==========
            "sunni vs shia difference": {
                "answer": "SUNNI AND SHIA - MAIN DIFFERENCES:\n\nThe split occurred after Prophet Muhammad's ﷺ death over leadership.\n\n**SUNNI (85-90% of Muslims):**\n• Abu Bakr (RA) was the rightful first Caliph\n• Follow the Prophet's Sunnah and consensus of companions\n• 4 main madhabs: Hanafi, Maliki, Shafi'i, Hanbali\n• Main hadith collections: Bukhari, Muslim, etc.\n\n**SHIA (10-15% of Muslims):**\n• Ali (RA) should have been the first Caliph\n• Believe in Imams as divinely guided leaders\n• Main sub-groups: Twelvers (largest), Ismailis, Zaidis\n• Main hadith collections: Al-Kafi, etc.\n\n**COMMON BELIEFS:**\n• One Allah, Quran, Prophet Muhammad ﷺ\n• Five pillars, Six articles of faith\n• Qibla (Kaaba), Hajj, Ramadan\n\nMuslims should focus on unity and what we share, not divisions.",
                "source": "Islamic History",
                "confidence": 0.85
            },
            "what is ahmadiyya": {
                "answer": "AHMADIYYA is a movement founded by Mirza Ghulam Ahmad (1835-1908) in British India. He claimed to be a prophet, the promised Messiah, and the Mahdi.\n\n**Why mainstream Islam considers them outside Islam:**\n\n📖 'Muhammad is not the father of any of your men, but he is the Messenger of Allah and the Seal of the Prophets.' (Quran 33:40)\n\nThe Quran clearly states Prophet Muhammad ﷺ is the FINAL Prophet. Anyone claiming prophethood after him contradicts this fundamental belief.\n\n**Key differences:**\n• They believe Mirza Ghulam Ahmad was a prophet\n• They reject that Prophet Muhammad ﷺ is the final prophet\n• Most Muslim scholars worldwide do NOT recognize Ahmadiyya as Muslims\n\nPakistan constitutionally declared them non-Muslims in 1974. The OIC and major Islamic organizations worldwide do not recognize them as Muslims.",
                "source": "Quran 33:40, Islamic Scholars Consensus",
                "confidence": 0.9
            },
            
            # ========== WOMEN ==========
            "why hijab": {
                "answer": "MUSLIM WOMEN WEAR HIJAB because Allah commanded it:\n\n📖 'And tell the believing women to lower their gaze and guard their private parts and not expose their adornment except that which [necessarily] appears thereof and to wrap [a portion of] their headcovers over their chests...' (Quran 24:31)\n\n📖 'O Prophet, tell your wives and your daughters and the women of the believers to bring down over themselves [part] of their outer garments. That is more suitable that they will be known and not be abused.' (Quran 33:59)\n\n**Purposes of Hijab:**\n1. Obedience to Allah (act of worship)\n2. Modesty and dignity\n3. Protection from objectification\n4. Identity as a Muslim woman\n5. Liberation from being judged by appearance",
                "source": "Quran 24:31, 33:59",
                "confidence": 0.95
            },
            "women rights in islam": {
                "answer": "ISLAM GAVE WOMEN RIGHTS 1400 YEARS AGO:\n\n• **Right to own property** - independently from husband\n• **Right to inheritance** - specified shares in Quran 4:11-12\n• **Right to choose spouse** - forced marriage is invalid\n• **Right to divorce** (Khula) - if marriage fails\n• **Right to education** - the Prophet ﷺ said seeking knowledge is obligatory for every Muslim, male and female\n• **Right to work** - with modesty and Islamic guidelines\n• **Right to vote/participate** - women gave bay'ah (pledge) to the Prophet ﷺ\n\n📖 'Whoever does righteousness, whether male or female, while believing - We will surely cause them to live a good life.' (Quran 16:97)\n\n📜 The Prophet ﷺ said: 'Women are the twin halves of men.' (Sunan Abu Dawud)",
                "source": "Quran 16:97, 4:11-12, Sunan Abu Dawud",
                "confidence": 0.9
            },
            "can women read quran during period": {
                "answer": "SCHOLARS DIFFER:\n\n**Majority opinion (Hanafi, Shafi'i, Hanbali):**\nWomen should NOT touch the mushaf (physical Quran) during menstruation but CAN read from memory, phone, or with a barrier.\n\n**Maliki opinion:**\nPermits touching the Quran during menstruation for study, teaching, or fear of forgetting.\n\n**What ALL agree on:**\n• Can make dua (supplication)\n• Can do dhikr (remembrance of Allah)\n• Can listen to Quran recitation\n• Can read Quran on phone/tablet\n\n📖 'None touch it except the purified.' (Quran 56:79) - This verse is the basis for requiring purification before touching the mushaf.",
                "source": "Quran 56:79, Fiqh of Purification",
                "confidence": 0.85
            },
        }
        
        # Check for matches (longer queries first for better matching)
        for key in sorted(knowledge.keys(), key=len, reverse=True):
            if key in query:
                data = knowledge[key]
                return {
                    "answer": data["answer"] + f"\n\n---\n📚 *Source: {data['source']}*",
                    "source": data["source"],
                    "confidence": data["confidence"],
                    "method": "specific_knowledge"
                }
        
        return None
    
    def _try_qa_database(self, query: str) -> Optional[Dict]:
        """Try Q&A database"""
        result = search_qa(query)
        if result:
            return {
                "answer": result,
                "source": "Q&A Database",
                "confidence": 0.9,
                "method": "qa_database"
            }
        return None
    
    def _try_quran_search(self, query: str) -> Optional[Dict]:
        """Try Quran search"""
        results = search_quran_verses(query)
        if results:
            answer = "📖 **From the Quran:**\n\n"
            for r in results[:3]:
                answer += f"**{r['reference']}** - {r['surah']}\n"
                answer += f"_{r['text'][:300]}_\n\n"
            
            return {
                "answer": answer,
                "source": "Quran",
                "confidence": 0.8,
                "method": "quran_search"
            }
        return None
    
    def _try_hadith_search(self, query: str) -> Optional[Dict]:
        """Try Hadith search"""
        if any(w in query for w in ["hadith", "prophet said", "narrated", "saying"]):
            results = search_hadith(query)
            if results:
                answer = "📜 **From Hadith:**\n\n"
                for r in results[:2]:
                    answer += f"_{r.get('text', '')[:300]}..._\n"
                    answer += f"— {r.get('collection', 'Hadith')}"
                    if r.get('grade'):
                        answer += f", Grade: {r['grade']}"
                    answer += "\n\n"
                
                return {
                    "answer": answer,
                    "source": "Hadith",
                    "confidence": 0.75,
                    "method": "hadith_search"
                }
        return None
    
    def _try_vector_search(self, query: str) -> Optional[Dict]:
        """Try vector search"""
        results = vector_store.search(query, top_k=1)
        if results and results[0]['relevance'] > 0.3:
            return {
                "answer": f"بسم الله الرحمن الرحيم\n\n{results[0]['content'][:500]}",
                "source": results[0].get('source', 'Knowledge Base'),
                "confidence": results[0]['relevance'],
                "method": "vector_search"
            }
        return None
    
    def _try_combined_search(self, query: str) -> Optional[Dict]:
        """Try combining multiple sources"""
        # Try API + local together
        from app.services.multi_api_service import multi_api
        
        try:
            # Try Quran search via API
            quran_results = multi_api.search_quran_multi(query)
            if quran_results:
                answer = "📖 **Quran Search Results:**\n\n"
                for r in quran_results[:3]:
                    answer += f"• _{r.get('text', '')[:200]}..._\n"
                    answer += f"  └─ {r.get('source', 'Quran')}\n\n"
                
                return {
                    "answer": answer,
                    "source": "Quran APIs",
                    "confidence": 0.85,
                    "method": "combined_api_quran"
                }
        except:
            pass
        
        return None
    
    def _get_ai_response(self, query: str) -> Dict:
        """Final fallback response"""
        if "?" in query:
            return {
                "answer": (
                    "This is an important question. While I don't have a specific answer "
                    "in my database for this exact query, I recommend:\n\n"
                    "1. **Consulting a qualified Islamic scholar** for authoritative guidance\n"
                    "2. **Searching the Quran** at quran.com for relevant verses\n"
                    "3. **Checking authentic hadith** at sunnah.com\n"
                    "4. **Asking your local imam** for personalized advice\n\n"
                    "I can help with questions about:\n"
                    "• Allah, His names and attributes\n"
                    "• Prophet Muhammad ﷺ and his life\n"
                    "• Quran and its preservation\n"
                    "• Prayer, fasting, zakat, hajj\n"
                    "• Halal and haram rulings\n"
                    "• Marriage, divorce, inheritance\n"
                    "• Jesus in Islam\n"
                    "• Modern issues (crypto, insurance, organ donation)\n"
                    "• Death, afterlife, paradise, hell\n"
                    "• Women's rights and hijab\n"
                    "• Sunni, Shia, Ahmadiyya\n\n"
                    "والله أعلم (And Allah knows best)"
                ),
                "source": "General Guidance",
                "confidence": 0.2,
                "method": "fallback_question"
            }
        
        return {
            "answer": (
                "Assalamu Alaikum! 👋\n\n"
                "Please ask your Islamic question, and I'll do my best to answer "
                "based on the Quran, authentic Sunnah, and scholarly sources.\n\n"
                "**I can help with:**\n"
                "• Quran verses and explanations\n"
                "• Hadith references\n"
                "• Prayer, fasting, zakat, hajj\n"
                "• Halal and haram\n"
                "• Marriage and family\n"
                "• Islamic beliefs\n"
                "• And much more...\n\n"
                "What would you like to know?"
            ),
            "source": "General",
            "confidence": 0.5,
            "method": "welcome"
        }

# Global instance
answer_engine = IslamicAnswerEngine()