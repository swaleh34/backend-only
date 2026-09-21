"""
Islamic Text Ingester
Loads authentic Islamic texts into the vector store
"""
import json
from typing import List, Dict
from app.services.vector_store import vector_store

class IslamicTextIngester:
    """Ingests Islamic texts into the vector database"""
    
    def __init__(self):
        self.is_loaded = False
    
    def load_all_texts(self):
        """Load all Islamic texts into the vector store"""
        if self.is_loaded:
            return
        
        print("📚 Loading Islamic texts...")
        documents = []
        
        # Load Quranic knowledge
        documents.extend(self._get_quran_documents())
        
        # Load Hadith knowledge
        documents.extend(self._get_hadith_documents())
        
        # Load Fiqh knowledge
        documents.extend(self._get_fiqh_documents())
        
        # Load General Islamic knowledge
        documents.extend(self._get_general_documents())
        
        # Add to vector store
        vector_store.add_documents(documents)
        self.is_loaded = True
        print(f"✅ Loaded {len(documents)} Islamic text chunks")
    
    def _get_quran_documents(self) -> List[Dict]:
        """Get Quran-related documents"""
        return [
            {
                'content': 'The Quran has 114 surahs (chapters). 86 are Meccan (revealed before Hijrah) and 28 are Medinan (revealed after Hijrah). The total number of verses is approximately 6,236.',
                'source': 'Quran',
                'topic': 'quran_structure',
                'type': 'fact'
            },
            {
                'content': 'Surah Al-Fatiha is the first chapter of the Quran. It has 7 verses and is recited in every rak\'ah of prayer. It is called Umm al-Kitab (Mother of the Book) and As-Sab\' al-Mathani (The Seven Oft-Repeated Verses).',
                'source': 'Quran 1:1-7',
                'topic': 'al_fatiha',
                'type': 'surah_info'
            },
            {
                'content': 'Surah Al-Baqarah is the longest surah with 286 verses. It contains Ayat al-Kursi (verse 255) which is the greatest verse in the Quran. It was revealed in Madinah.',
                'source': 'Quran 2',
                'topic': 'al_baqarah',
                'type': 'surah_info'
            },
            {
                'content': 'Surah Al-Ikhlas (Chapter 112) is about the Oneness of Allah. The Prophet Muhammad (peace be upon him) said it equals one-third of the Quran in reward. It has 4 verses.',
                'source': 'Quran 112, Sahih al-Bukhari 5013',
                'topic': 'al_ikhlas',
                'type': 'surah_info'
            },
            {
                'content': 'Surah Ya-Sin (Chapter 36) is called the Heart of the Quran. It has 83 verses and is often recited for the dying and deceased. It discusses prophethood, resurrection, and Allah\'s signs.',
                'source': 'Quran 36',
                'topic': 'ya_sin',
                'type': 'surah_info'
            },
            {
                'content': 'Surah Al-Mulk (Chapter 67) has 30 verses. The Prophet (peace be upon him) said it intercedes for its reciter until they are forgiven. It protects from the punishment of the grave.',
                'source': 'Quran 67, Sunan al-Tirmidhi 2891',
                'topic': 'al_mulk',
                'type': 'surah_info'
            },
            {
                'content': 'The Quran was revealed to Prophet Muhammad (peace be upon him) over 23 years through Angel Jibreel (Gabriel). The first revelation was in Cave Hira in 610 CE. The last verse was revealed during the Farewell Pilgrimage in 632 CE.',
                'source': 'Quran 96:1-5, Seerah',
                'topic': 'quran_revelation',
                'type': 'fact'
            },
            {
                'content': 'Tajweed refers to the rules of Quranic recitation. It ensures proper pronunciation of Arabic letters and application of rules like Idgham, Iqlab, Ikhfa, and Madd. Learning Tajweed is Fard Kifayah (communal obligation).',
                'source': 'Islamic Sciences',
                'topic': 'tajweed',
                'type': 'fact'
            }
        ]
    
    def _get_hadith_documents(self) -> List[Dict]:
        """Get Hadith-related documents"""
        return [
            {
                'content': 'The most authentic hadith collections are Sahih al-Bukhari and Sahih Muslim, known as Sahihayn. They contain only authentic (sahih) hadiths. Bukhari has 7,563 hadiths and Muslim has about 4,000.',
                'source': 'Hadith Sciences',
                'topic': 'hadith_collections',
                'type': 'fact'
            },
            {
                'content': 'The Six Major Hadith Collections (Kutub al-Sittah) are: Sahih al-Bukhari, Sahih Muslim, Sunan Abu Dawud, Jami al-Tirmidhi, Sunan al-Nasa\'i, and Sunan Ibn Majah. Some scholars replace Ibn Majah with Muwatta Malik.',
                'source': 'Hadith Sciences',
                'topic': 'kutub_sittah',
                'type': 'fact'
            },
            {
                'content': 'A hadith consists of two parts: Isnad (chain of narrators) and Matn (text). Hadith are graded as: Sahih (authentic), Hasan (good), Da\'if (weak), or Mawdu\' (fabricated).',
                'source': 'Hadith Sciences',
                'topic': 'hadith_structure',
                'type': 'fact'
            },
            {
                'content': 'The Prophet Muhammad (peace be upon him) said: "Actions are judged by intentions, and every person will get what they intended." This is the first hadith in Sahih al-Bukhari and Imam Nawawi\'s 40 Hadith.',
                'source': 'Sahih al-Bukhari 1, Nawawi 40 Hadith #1',
                'topic': 'intentions',
                'type': 'hadith'
            },
            {
                'content': 'The Prophet (peace be upon him) said: "None of you truly believes until he loves for his brother what he loves for himself." This hadith emphasizes empathy and brotherhood in Islam.',
                'source': 'Sahih al-Bukhari 13, Sahih Muslim 45',
                'topic': 'brotherhood',
                'type': 'hadith'
            },
            {
                'content': 'The Prophet (peace be upon him) said: "The best among you are those who have the best manners and character." Good character (Husn al-Khuluq) is a fundamental aspect of Islam.',
                'source': 'Sahih al-Bukhari 3559',
                'topic': 'character',
                'type': 'hadith'
            },
            {
                'content': 'The Prophet (peace be upon him) said: "Whoever believes in Allah and the Last Day should speak good or remain silent. Whoever believes in Allah and the Last Day should be generous to his neighbor. Whoever believes in Allah and the Last Day should be generous to his guest."',
                'source': 'Sahih al-Bukhari 6018, Sahih Muslim 47',
                'topic': 'manners',
                'type': 'hadith'
            },
            {
                'content': 'The Prophet (peace be upon him) said: "The strong person is not the one who can wrestle, but the one who controls himself when angry." This teaches self-control and anger management.',
                'source': 'Sahih al-Bukhari 6114, Sahih Muslim 2609',
                'topic': 'anger_management',
                'type': 'hadith'
            }
        ]
    
    def _get_fiqh_documents(self) -> List[Dict]:
        """Get Fiqh-related documents"""
        return [
            {
                'content': 'Muslims pray five times daily: Fajr (2 rakats fard), Dhuhr (4 rakats fard), Asr (4 rakats fard), Maghrib (3 rakats fard), and Isha (4 rakats fard). Prayer times are determined by the position of the sun.',
                'source': 'Fiqh of Worship',
                'topic': 'prayer_times',
                'type': 'fiqh'
            },
            {
                'content': 'Wudu (ablution) is required before prayer. Steps: 1) Intention and Bismillah, 2) Wash hands 3 times, 3) Rinse mouth 3 times, 4) Clean nose 3 times, 5) Wash face 3 times, 6) Wash arms to elbows 3 times, 7) Wipe head once, 8) Wipe ears, 9) Wash feet to ankles 3 times.',
                'source': 'Fiqh of Purification',
                'topic': 'wudu',
                'type': 'fiqh'
            },
            {
                'content': 'Fasting in Ramadan is obligatory for every adult Muslim who is sane, resident, and able. The fast is from Fajr (dawn) to Maghrib (sunset). Exemptions include illness, travel, pregnancy, breastfeeding, menstruation, and extreme old age.',
                'source': 'Fiqh of Fasting',
                'topic': 'fasting_rules',
                'type': 'fiqh'
            },
            {
                'content': 'Zakat is due on wealth that reaches the Nisab threshold and has been held for one lunar year. The rate is 2.5% on gold, silver, cash, and trade goods. Different rates apply to agricultural produce (5-10%) and livestock.',
                'source': 'Fiqh of Zakat',
                'topic': 'zakat_rules',
                'type': 'fiqh'
            },
            {
                'content': 'Hajj is obligatory once in a lifetime for those who are physically and financially able. It is performed from 8th to 13th Dhul-Hijjah. Main rituals: Ihram, Tawaf, Sa\'i, standing at Arafat (9th Dhul-Hijjah), staying at Muzdalifah, stoning Jamarat, sacrifice, and Tawaf al-Ifadah.',
                'source': 'Fiqh of Hajj',
                'topic': 'hajj_rituals',
                'type': 'fiqh'
            },
            {
                'content': 'Halal food must be: 1) From permissible animals (no pork, carnivores, etc.), 2) Slaughtered in Allah\'s name (Dhabiha), 3) Blood must be drained. Seafood is generally halal. Haram includes: pork, blood, carrion, alcohol, and animals not slaughtered properly.',
                'source': 'Fiqh of Food',
                'topic': 'halal_food',
                'type': 'fiqh'
            }
        ]
    
    def _get_general_documents(self) -> List[Dict]:
        """Get general Islamic knowledge documents"""
        return [
            {
                'content': 'Islam means "submission" to the will of Allah. A Muslim is one who submits to Allah. Islam is not named after a person or tribe but describes the relationship between the Creator and creation.',
                'source': 'Islamic Theology',
                'topic': 'what_is_islam',
                'type': 'general'
            },
            {
                'content': 'The Five Pillars of Islam are: 1) Shahada (Declaration of Faith), 2) Salah (Prayer), 3) Zakat (Charity), 4) Sawm (Fasting in Ramadan), 5) Hajj (Pilgrimage to Makkah). These are the foundation of Muslim life.',
                'source': 'Sahih al-Bukhari 8, Sahih Muslim 16',
                'topic': 'five_pillars',
                'type': 'general'
            },
            {
                'content': 'The Six Articles of Faith (Iman) are: Belief in 1) Allah, 2) His Angels, 3) His Books, 4) His Messengers, 5) The Day of Judgment, 6) Divine Decree (Qadr), both good and bad.',
                'source': 'Sahih Muslim 8 (Hadith of Jibreel)',
                'topic': 'six_articles',
                'type': 'general'
            },
            {
                'content': 'Allah has 99 beautiful names (Asma ul-Husna). Key names include: Ar-Rahman (Most Gracious), Ar-Raheem (Most Merciful), Al-Malik (The King), Al-Quddus (The Holy), As-Salam (The Peace), Al-Khaliq (The Creator), Al-Ghaffar (The Forgiver).',
                'source': 'Quran 7:180, Sahih al-Bukhari 2736',
                'topic': 'allah_names',
                'type': 'general'
            },
            {
                'content': 'Prophet Muhammad (peace be upon him) was born in 570 CE in Makkah. He received the first revelation at age 40. He migrated to Madinah in 622 CE (Hijrah). He passed away in 632 CE at age 63. He is the final Prophet.',
                'source': 'Seerah',
                'topic': 'prophet_life',
                'type': 'general'
            },
            {
                'content': 'The four Rightly Guided Caliphs (Khulafa ar-Rashidun) are: 1) Abu Bakr as-Siddiq (632-634 CE), 2) Umar ibn al-Khattab (634-644 CE), 3) Uthman ibn Affan (644-656 CE), 4) Ali ibn Abi Talib (656-661 CE).',
                'source': 'Islamic History',
                'topic': 'caliphs',
                'type': 'general'
            },
            {
                'content': 'The Islamic calendar (Hijri) started in 622 CE with the Hijrah (migration) of Prophet Muhammad from Makkah to Madinah. It has 12 lunar months: Muharram, Safar, Rabi al-Awwal, Rabi al-Thani, Jumada al-Ula, Jumada al-Thani, Rajab, Sha\'ban, Ramadan, Shawwal, Dhul-Qa\'dah, Dhul-Hijjah.',
                'source': 'Islamic Calendar',
                'topic': 'hijri_calendar',
                'type': 'general'
            },
            {
                'content': 'Ramadan is the 9th month of the Islamic calendar. It is the month the Quran was revealed. Muslims fast from dawn to sunset. It contains Laylat al-Qadr (Night of Power) which is better than 1000 months.',
                'source': 'Quran 2:185, Quran 97:3',
                'topic': 'ramadan',
                'type': 'general'
            },
            {
                'content': 'The Quran mentions 25 prophets by name. The most mentioned is Prophet Musa (Moses) - mentioned 136 times. Prophet Muhammad is mentioned 4 times by name. All prophets preached the same core message of Tawheed (Oneness of Allah).',
                'source': 'Quran',
                'topic': 'prophets',
                'type': 'general'
            },
            {
                'content': 'Jannah (Paradise) has 8 gates: Baab as-Salah (for those who prayed), Baab al-Jihad, Baab ar-Rayyan (for those who fasted), Baab as-Sadaqah (for charity givers), Baab al-Hajj, Baab al-Kazimeen al-Ghayz (for those who controlled anger), Baab al-Iman, and Baab al-Dhikr.',
                'source': 'Sahih al-Bukhari, Sahih Muslim',
                'topic': 'jannah',
                'type': 'general'
            }
        ]

# Global instance
text_ingester = IslamicTextIngester()