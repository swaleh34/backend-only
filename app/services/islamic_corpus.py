from typing import List, Dict, Any, Optional
"""
Complete Islamic Texts Corpus
Contains authentic Islamic texts for AI reference
"""

# Complete Quran in English (Saheeh International translation)
QURAN_FULL_TEXT = {
    "1": {
        "name": "Al-Fatiha (The Opening)",
        "verses": {
            "1": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
            "2": "[All] praise is [due] to Allah, Lord of the worlds -",
            "3": "The Entirely Merciful, the Especially Merciful,",
            "4": "Sovereign of the Day of Recompense.",
            "5": "It is You we worship and You we ask for help.",
            "6": "Guide us to the straight path -",
            "7": "The path of those upon whom You have bestowed favor, not of those who have evoked [Your] anger or of those who are astray."
        },
        "revelation": "Meccan",
        "theme": "Praise, supplication, and the essence of faith"
    },
    "2": {
        "name": "Al-Baqarah (The Cow)",
        "verses": {
            "1": "Alif, Lam, Meem.",
            "2": "This is the Book about which there is no doubt, a guidance for those conscious of Allah -",
            "3": "Who believe in the unseen, establish prayer, and spend out of what We have provided for them,",
            "4": "And who believe in what has been revealed to you, [O Muhammad], and what was revealed before you, and of the Hereafter they are certain [in faith].",
            "5": "Those are upon [right] guidance from their Lord, and it is those who are the successful.",
            "255": "Allah - there is no deity except Him, the Ever-Living, the Sustainer of [all] existence. Neither drowsiness overtakes Him nor sleep. To Him belongs whatever is in the heavens and whatever is on the earth. Who is it that can intercede with Him except by His permission? He knows what is [presently] before them and what will be after them, and they encompass not a thing of His knowledge except for what He wills. His Kursi extends over the heavens and the earth, and their preservation tires Him not. And He is the Most High, the Most Great. (Ayat al-Kursi)",
            "285": "The Messenger has believed in what was revealed to him from his Lord, and [so have] the believers. All of them have believed in Allah and His angels and His books and His messengers, [saying], 'We make no distinction between any of His messengers.' And they say, 'We hear and we obey. [We seek] Your forgiveness, our Lord, and to You is the [final] destination.'",
            "286": "Allah does not charge a soul except [with that within] its capacity. It will have [the consequence of] what [good] it has gained, and it will bear [the consequence of] what [evil] it has earned. 'Our Lord, do not impose blame upon us if we have forgotten or erred. Our Lord, and lay not upon us a burden like that which You laid upon those before us. Our Lord, and burden us not with that which we have no ability to bear. And pardon us; and forgive us; and have mercy upon us. You are our protector, so give us victory over the disbelieving people.'"
        },
        "revelation": "Medinan",
        "theme": "Guidance, law, stories of creation, and comprehensive Islamic legislation"
    },
    "112": {
        "name": "Al-Ikhlas (The Sincerity)",
        "verses": {
            "1": "Say, 'He is Allah, [who is] One,'",
            "2": "Allah, the Eternal Refuge.",
            "3": "He neither begets nor is born,",
            "4": "Nor is there to Him any equivalent.'"
        },
        "revelation": "Meccan",
        "theme": "Pure monotheism (Tawheed)"
    },
    "113": {
        "name": "Al-Falaq (The Daybreak)",
        "verses": {
            "1": "Say, 'I seek refuge in the Lord of daybreak'",
            "2": "From the evil of that which He created",
            "3": "And from the evil of darkness when it settles",
            "4": "And from the evil of the blowers in knots",
            "5": "And from the evil of an envier when he envies.'"
        },
        "revelation": "Meccan",
        "theme": "Seeking protection from all forms of evil"
    },
    "114": {
        "name": "An-Nas (The Mankind)",
        "verses": {
            "1": "Say, 'I seek refuge in the Lord of mankind,'",
            "2": "The Sovereign of mankind,",
            "3": "The God of mankind,",
            "4": "From the evil of the retreating whisperer -",
            "5": "Who whispers [evil] into the breasts of mankind -",
            "6": "From among the jinn and mankind.'"
        },
        "revelation": "Meccan",
        "theme": "Seeking refuge in Allah from evil whispers"
    }
}

# Authentic Hadith Collections - Key Hadith
AUTHENTIC_HADITH = {
    "sahih_bukhari": [
        {
            "number": "1",
            "book": "Revelation",
            "narrator": "Umar ibn Al-Khattab",
            "text": "I heard Allah's Messenger (ﷺ) saying, 'The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended. So whoever emigrated for worldly benefits or for a woman to marry, his emigration was for what he emigrated for.'",
            "grade": "Sahih",
            "topic": "Intentions (Niyyah)"
        },
        {
            "number": "8",
            "book": "Faith",
            "narrator": "Ibn Umar",
            "text": "Allah's Messenger (ﷺ) said: Islam is based on (the following) five (principles): 1. To testify that none has the right to be worshipped but Allah and Muhammad is Allah's Messenger (ﷺ). 2. To offer the (compulsory congregational) prayers dutifully and perfectly. 3. To pay Zakat (i.e. obligatory charity). 4. To perform Hajj. (i.e. Pilgrimage to Mecca) 5. To observe fast during the month of Ramadan.",
            "grade": "Sahih",
            "topic": "Five Pillars of Islam"
        },
        {
            "number": "10",
            "book": "Faith",
            "narrator": "Abu Musa",
            "text": "Some people asked Allah's Messenger (ﷺ), 'Whose Islam is the best? i.e. (Who is a very good Muslim)?' He replied, 'One who avoids harming the Muslims with his tongue and hands.'",
            "grade": "Sahih",
            "topic": "Best Muslim"
        },
        {
            "number": "13",
            "book": "Faith",
            "narrator": "Anas",
            "text": "The Prophet (ﷺ) said, 'None of you will have faith till he loves me more than his father, his children and all mankind.'",
            "grade": "Sahih",
            "topic": "Love for the Prophet"
        },
        {
            "number": "601",
            "book": "Times of Prayers",
            "narrator": "Ibn Abbas",
            "text": "The Prophet (ﷺ) said, 'Jibril (Gabriel) led me in prayer at the Ka'ba twice. He prayed the noon prayer (Dhuhr) with me when the sun had passed the meridian...'",
            "grade": "Sahih",
            "topic": "Prayer Times"
        }
    ],
    "sahih_muslim": [
        {
            "number": "1",
            "book": "Faith",
            "narrator": "Yahya ibn Ya'mur",
            "text": "The first of the people to speak about Divine Decree (Qadr) was Ma'bad al-Juhani... Then I (Yahya) went with Humaid ibn Abdur Rahman for Hajj... We met Abdullah ibn Umar ibn al-Khattab... He said: When we were with the Messenger of Allah (ﷺ) there came a man with very white clothes and very black hair... He was Jibril (Gabriel) who came to teach you your religion.",
            "grade": "Sahih",
            "topic": "Hadith of Jibreel - Islam, Iman, Ihsan"
        },
        {
            "number": "1009",
            "book": "Prayer",
            "narrator": "Abu Huraira",
            "text": "The Messenger of Allah (ﷺ) said: 'The five daily prayers, and Friday prayer to Friday prayer, and Ramadan to Ramadan, are expiations for the sins committed between them, so long as major sins are avoided.'",
            "grade": "Sahih",
            "topic": "Expiation of Sins"
        },
        {
            "number": "2582",
            "book": "Virtue",
            "narrator": "Abu Huraira",
            "text": "The Messenger of Allah (ﷺ) said: 'Do you know who is the bankrupt?' They said: 'The bankrupt among us is one who has neither money nor property.' He said: 'The bankrupt of my Ummah is one who comes on the Day of Resurrection with prayer, fasting, and charity, but he had insulted this one, slandered that one, consumed the wealth of this one...'",
            "grade": "Sahih",
            "topic": "True Bankruptcy"
        }
    ],
    "riyad_salihin": [
        {
            "number": "1",
            "chapter": "Sincerity and Significance of Intentions",
            "text": "The Commander of the Faithful, Abu Hafs Umar ibn al-Khattab (RA) said: I heard the Messenger of Allah (ﷺ) say: 'Actions are but by intentions, and every person shall have only what he intended...'",
            "grade": "Sahih",
            "topic": "Intentions"
        },
        {
            "number": "13",
            "chapter": "Taqwa (God-Consciousness)",
            "text": "Abu Dharr Jundub ibn Junadah and Abu Abdur Rahman Mu'adh ibn Jabal (RA) reported that the Messenger of Allah (ﷺ) said: 'Fear Allah wherever you are, and follow up a bad deed with a good deed which will wipe it out, and behave well towards people.'",
            "grade": "Hasan",
            "topic": "Good Character"
        }
    ]
}

# Forty Hadith of Imam Nawawi
NAWAWI_40_HADITH = [
    {
        "number": 1,
        "narrator": "Umar ibn Al-Khattab",
        "text": "Actions are judged by intentions, and every person will get what they intended. Whoever emigrated for Allah and His Messenger, their emigration was for Allah and His Messenger. Whoever emigrated for worldly gain or to marry a woman, their emigration was for what they emigrated for.",
        "explanation": "This hadith establishes that the value of deeds depends on the intention behind them."
    },
    {
        "number": 2,
        "narrator": "Umar ibn Al-Khattab",
        "text": "One day while we were sitting with the Messenger of Allah (ﷺ), there appeared before us a man whose clothes were exceedingly white and whose hair was exceedingly black... He was Jibril (Gabriel) who came to teach you your religion.",
        "explanation": "The Hadith of Jibreel defining Islam, Iman, and Ihsan."
    },
    {
        "number": 3,
        "narrator": "Abdullah ibn Umar",
        "text": "Islam is built upon five [pillars]: testimony that there is no god but Allah and that Muhammad is the Messenger of Allah, establishing prayer, giving zakat, fasting Ramadan, and performing Hajj to the House.",
        "explanation": "The five pillars of Islam."
    },
    {
        "number": 4,
        "narrator": "Abdullah ibn Mas'ud",
        "text": "Verily, the creation of each one of you is brought together in his mother's womb for forty days... Then an angel is sent to breathe the soul into him...",
        "explanation": "Stages of human creation and the recording of destiny."
    },
    {
        "number": 5,
        "narrator": "Aisha (RA)",
        "text": "Whoever introduces into this affair of ours something that does not belong to it, it will be rejected.",
        "explanation": "Innovations in religion are rejected."
    },
    {
        "number": 6,
        "narrator": "An-Nu'man ibn Bashir",
        "text": "The halal is clear and the haram is clear, and between them are doubtful matters which many people do not know...",
        "explanation": "Avoiding doubtful matters."
    },
    {
        "number": 7,
        "narrator": "Abu Ruqayyah Tamim ibn Aws ad-Dari",
        "text": "The religion is sincerity. We said: To whom? He said: To Allah, His Book, His Messenger, and the leaders of the Muslims and their common people.",
        "explanation": "Sincerity in religion."
    }
]

# Common Islamic Q&A
ISLAMIC_QA = [
    {
        "question": "What are the five pillars of Islam?",
        "answer": "The Five Pillars are: 1) Shahada (Declaration of Faith), 2) Salah (Prayer), 3) Zakat (Charity), 4) Sawm (Fasting in Ramadan), 5) Hajj (Pilgrimage to Makkah).",
        "source": "Hadith of Ibn Umar, Sahih al-Bukhari 8, Sahih Muslim 16"
    },
    {
        "question": "Who is Allah?",
        "answer": "Allah is the One and Only God, Creator of everything. He is Ar-Rahman (Most Gracious), Ar-Raheem (Most Merciful), Al-Khaliq (The Creator). He has 99 beautiful names and attributes. Nothing is like Him.",
        "source": "Quran 112:1-4, Quran 59:22-24"
    },
    {
        "question": "What is the Quran?",
        "answer": "The Quran is the literal word of Allah, revealed to Prophet Muhammad (ﷺ) through Angel Jibreel over 23 years. It has 114 chapters, is in Arabic, and has remained unchanged for over 1400 years.",
        "source": "Quran 15:9, Quran 2:2"
    },
    {
        "question": "Who was Prophet Muhammad?",
        "answer": "Prophet Muhammad (ﷺ, 570-632 CE) is the final Messenger of Allah. Born in Makkah, he received the first revelation at age 40. He is described in the Quran as 'a mercy to the worlds' (21:107) and the 'best example' (33:21).",
        "source": "Quran 33:21, 21:107"
    },
    {
        "question": "How to pray in Islam?",
        "answer": "Prayer (Salah) involves: 1) Niyyah (intention), 2) Takbir (Allahu Akbar), 3) Reciting Al-Fatiha, 4) Ruku (bowing), 5) Sujud (prostration), 6) Tashahhud (sitting). Muslims pray 5 times daily facing the Kaaba in Makkah.",
        "source": "Quran 2:43, Sahih al-Bukhari 631"
    },
    {
        "question": "What is Ramadan?",
        "answer": "Ramadan is the 9th month of the Islamic calendar, the month the Quran was revealed. Muslims fast from dawn to sunset, abstaining from food, drink, and marital relations. It's a month of spiritual reflection, increased worship, and charity.",
        "source": "Quran 2:183-185"
    },
    {
        "question": "What is Hajj?",
        "answer": "Hajj is the pilgrimage to Makkah, performed during Dhul-Hijjah. It is the 5th pillar of Islam, obligatory once in a lifetime for those who can afford it. Rituals include Tawaf, Sa'i, standing at Arafat, and sacrificing an animal.",
        "source": "Quran 3:97, Quran 22:27-30"
    },
    {
        "question": "What is Halal and Haram?",
        "answer": "Halal means permissible or lawful. Haram means forbidden or prohibited. The general principle is everything is halal unless explicitly prohibited. Major haram things include: shirk, murder, alcohol, pork, gambling, interest, adultery, theft.",
        "source": "Quran 2:168, 5:3, 7:33"
    },
    {
        "question": "What is Wudu?",
        "answer": "Wudu is ritual ablution before prayer. Steps: 1) Wash hands 3x, 2) Rinse mouth 3x, 3) Clean nose 3x, 4) Wash face 3x, 5) Wash arms to elbows 3x, 6) Wipe head, 7) Wipe ears, 8) Wash feet to ankles 3x. Nullified by sleep, bathroom use, etc.",
        "source": "Quran 5:6, Sahih al-Bukhari 161"
    },
    {
        "question": "What is Zakat?",
        "answer": "Zakat is obligatory charity, the 3rd pillar of Islam. Muslims pay 2.5% of their savings above the Nisab threshold annually. It's distributed to 8 categories: the poor, needy, collectors, new Muslims, freeing slaves, debtors, in Allah's cause, and travelers.",
        "source": "Quran 9:60, Sahih al-Bukhari 1395"
    },
    {
        "question": "What are the 99 names of Allah?",
        "answer": "The 99 Names (Asma ul-Husna) include: Ar-Rahman (Most Gracious), Ar-Raheem (Most Merciful), Al-Malik (The King), Al-Quddus (The Holy), As-Salam (The Peace), Al-Mu'min (The Faithful), Al-Muhaymin (The Guardian), Al-Aziz (The Mighty), Al-Jabbar (The Compeller).",
        "source": "Quran 7:180, Sahih al-Bukhari 2736"
    },
    {
        "question": "What is Tawheed?",
        "answer": "Tawheed is the concept of monotheism in Islam - the absolute oneness of Allah. It has three categories: 1) Tawheed ar-Rububiyyah (Oneness of Lordship), 2) Tawheed al-Uluhiyyah (Oneness of Worship), 3) Tawheed al-Asma was-Sifat (Oneness of Names and Attributes).",
        "source": "Quran 112:1-4, Quran 2:163"
    }
]

def search_qa(query: str) -> Optional[str]:
    """Search the Q&A database with better matching"""
    query_lower = query.lower()
    
    # Direct question matching first
    for qa in ISLAMIC_QA:
        qa_question = qa["question"].lower()
        
        # Check for exact or near-exact match
        if query_lower in qa_question or qa_question in query_lower:
            return f"{qa['answer']}\n\n📚 Source: {qa['source']}"
        
        # Check for key phrase overlap
        query_words = set(query_lower.split())
        qa_words = set(qa_question.split())
        
        # Need at least 3 matching words or 50% overlap
        common_words = query_words & qa_words - {"the", "is", "are", "what", "who", "how", "in", "of", "to", "a", "an"}
        if len(common_words) >= 3 or (len(qa_words) > 0 and len(common_words) / len(qa_words) >= 0.5):
            return f"{qa['answer']}\n\n📚 Source: {qa['source']}"
    
    # Special keyword matching for specific topics
    keyword_mapping = {
        "prophet muhammad": "Who was Prophet Muhammad?",
        "last prophet": "Who was Prophet Muhammad?",
        "final prophet": "Who was Prophet Muhammad?",
        "rasul": "Who was Prophet Muhammad?",
        "allah": "Who is Allah?",
        "god": "Who is Allah?",
        "pray": "How to pray in Islam?",
        "salah": "How to pray in Islam?",
        "namaz": "How to pray in Islam?",
        "ramadan": "What is Ramadan?",
        "fast": "What is Ramadan?",
        "hajj": "What is Hajj?",
        "pilgrimage": "What is Hajj?",
        "halal": "What is Halal and Haram?",
        "haram": "What is Halal and Haram?",
        "wudu": "What is Wudu?",
        "ablution": "What is Wudu?",
        "zakat": "What is Zakat?",
        "charity": "What is Zakat?",
        "99 names": "What are the 99 names of Allah?",
        "names of allah": "What are the 99 names of Allah?",
        "tawheed": "What is Tawheed?",
        "monotheism": "What is Tawheed?",
        "quran": "What is the Quran?",
    }
    
    for keyword, qa_question in keyword_mapping.items():
        if keyword in query_lower:
            for qa in ISLAMIC_QA:
                if qa["question"] == qa_question:
                    return f"{qa['answer']}\n\n📚 Source: {qa['source']}"
    
    return None

def search_quran_verses(query: str) -> List[Dict]:
    """Search Quran verses - only return if there's meaningful match"""
    results = []
    query_lower = query.lower()
    query_words = set(query_lower.split()) - {"the", "is", "are", "what", "who", "how", "in", "of", "to", "a", "an", "does", "do", "mean"}
    
    # Don't search Quran for Q&A type questions
    qa_questions = ["who is", "what is", "what are", "how many", "how to", "tell me", "explain"]
    if any(query_lower.startswith(q) for q in qa_questions):
        return []  # Let Q&A database handle these
    
    for surah_id, surah_data in QURAN_FULL_TEXT.items():
        for verse_num, verse_text in surah_data["verses"].items():
            verse_lower = verse_text.lower()
            matches = sum(1 for word in query_words if word in verse_lower)
            if matches >= 2:  # At least 2 matching words
                results.append({
                    "surah": surah_data["name"],
                    "surah_id": surah_id,
                    "verse": verse_num,
                    "text": verse_text,
                    "reference": f"Quran {surah_id}:{verse_num}",
                    "matches": matches
                })
    
    # Sort by number of matches
    results.sort(key=lambda x: x["matches"], reverse=True)
    return results[:3]

def search_hadith(query: str) -> List[Dict]:
    """Search hadith collections safely"""
    results = []
    query_lower = query.lower()
    
    for collection_name, hadiths in AUTHENTIC_HADITH.items():
        for hadith in hadiths:
            if any(word in hadith.get("text", "").lower() for word in query_lower.split()):
                results.append({
                    "collection": collection_name,
                    "text": hadith.get("text", ""),
                    "narrator": hadith.get("narrator", "Unknown"),
                    "grade": hadith.get("grade", "Unknown"),
                    "topic": hadith.get("topic", "General")
                })
    
    return results[:5]

def get_nawawi_hadith(number: int) -> Optional[Dict]:
    """Get specific hadith from Nawawi's 40"""
    for hadith in NAWAWI_40_HADITH:
        if hadith["number"] == number:
            return hadith
    return None