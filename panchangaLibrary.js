/**
 * panchangaLibrary.js — Standalone Vedic Panchanga Calculator
 *
 * No React, no bundler required. Works in Node.js or any environment
 * where astronomy-engine is available.
 *
 * Install dependency:
 *   npm install astronomy-engine
 *
 * Usage (module):
 *   const { getPanchanga } = require('./panchangaLibrary');
 *   const json = getPanchanga(new Date(), { lang: 'hi' });   // Hindi (default)
 *   const json = getPanchanga(new Date(), { lang: 'en' });   // English
 *   console.log(json);
 *
 * Usage (CLI):
 *   node panchangaLibrary.js                       # today, Hindi
 *   node panchangaLibrary.js 2026-04-12            # specific date, Hindi
 *   node panchangaLibrary.js 2026-04-12 false en   # English output
 *   node panchangaLibrary.js 2026-04-12 true  hi   # Amanta + Hindi
 */

'use strict';

const Astronomy = require('astronomy-engine');

// ─── Constants ────────────────────────────────────────────────────────────────

const NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
];

const TITHIS = [
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
    'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
    'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
];

const YOGAS = [
    'Vishkumbha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana',
    'Atiganda', 'Sukarma', 'Dhriti', 'Shula', 'Ganda',
    'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
    'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva',
    'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma', 'Indra', 'Vaidhriti'
];

const KARANAS = ['Bava', 'Balava', 'Kaulava', 'Taitila', 'Gara', 'Vanija', 'Vishti'];

const VARAS = ['Ravivara', 'Somavara', 'Mangalavara', 'Budhavara', 'Guruvara', 'Shukravara', 'Shanivara'];

const MAASAS = [
    'Chaitra', 'Vaishakha', 'Jyeshtha', 'Ashadha', 'Shravana', 'Bhadrapada',
    'Ashwina', 'Kartika', 'Margashirsha', 'Pausha', 'Magha', 'Phalguna'
];

const NAKSHATRA_TO_MAASA = {
    'Ashwini': 'Ashwina', 'Bharani': 'Ashwina',
    'Krittika': 'Kartika', 'Rohini': 'Kartika',
    'Mrigashira': 'Margashirsha', 'Ardra': 'Margashirsha',
    'Punarvasu': 'Pausha', 'Pushya': 'Pausha',
    'Ashlesha': 'Magha', 'Magha': 'Magha',
    'Purva Phalguni': 'Phalguna', 'Uttara Phalguni': 'Phalguna',
    'Hasta': 'Chaitra', 'Chitra': 'Chaitra',
    'Swati': 'Vaishakha', 'Vishakha': 'Vaishakha',
    'Anuradha': 'Jyeshtha', 'Jyeshtha': 'Jyeshtha',
    'Mula': 'Ashadha', 'Purva Ashadha': 'Ashadha', 'Uttara Ashadha': 'Ashadha',
    'Shravana': 'Shravana', 'Dhanishta': 'Shravana',
    'Shatabhisha': 'Bhadrapada', 'Purva Bhadrapada': 'Bhadrapada',
    'Uttara Bhadrapada': 'Bhadrapada', 'Revati': 'Bhadrapada'
};

const RITU_THEMES = {
    Vasanta: { name: 'Vasanta', english: 'Spring', hinduMonths: ['Chaitra', 'Vaishakha'] },
    Grishma: { name: 'Grishma', english: 'Summer', hinduMonths: ['Jyeshtha', 'Ashadha'] },
    Varsha: { name: 'Varsha', english: 'Monsoon', hinduMonths: ['Shravana', 'Bhadrapada'] },
    Sharad: { name: 'Sharad', english: 'Autumn', hinduMonths: ['Ashwina', 'Kartika'] },
    Hemanta: { name: 'Hemanta', english: 'Early Winter', hinduMonths: ['Margashirsha', 'Pausha'] },
    Shishira: { name: 'Shishira', english: 'Late Winter', hinduMonths: ['Magha', 'Phalguna'] }
};

const SAMVATSARAS = [
    'Prabhava', 'Vibhava', 'Shukla', 'Pramoda', 'Prajapati',
    'Angirasa', 'Shrimukha', 'Bhava', 'Yuva', 'Dhatri',
    'Ishwara', 'Bahudhanya', 'Pramathi', 'Vikrama', 'Vrishabha',
    'Chitrabhanu', 'Subhanu', 'Tarana', 'Parthiva', 'Vyaya',
    'Sarvajit', 'Sarvadhari', 'Virodhi', 'Vikriti', 'Khara',
    'Nandana', 'Vijaya', 'Jaya', 'Manmatha', 'Durmukha',
    'Hemalamba', 'Vilambi', 'Vikari', 'Sharvari', 'Plava',
    'Shubhakrit', 'Shobhakrit', 'Krodhi', 'Vishvavasu', 'Parabhava',
    'Plavanga', 'Kilaka', 'Saumya', 'Sadharana', 'Virodhikrit',
    'Paridhavi', 'Pramadicha', 'Ananda', 'Rakshasa', 'Nala',
    'Pingala', 'Kalayukta', 'Siddharthi', 'Raudra', 'Durmati',
    'Dundubhi', 'Rudhirodgari', 'Raktakshi', 'Krodhana', 'Akshaya'
];

// Sanskrit vara name → English day key (needed to look up vara translations)
const VARA_TO_DAY = {
    Ravivara: 'Sunday', Somavara: 'Monday', Mangalavara: 'Tuesday',
    Budhavara: 'Wednesday', Guruvara: 'Thursday', Shukravara: 'Friday', Shanivara: 'Saturday'
};

// ─── Translations ─────────────────────────────────────────────────────────────

const TRANSLATIONS = {
    en: {
        tithis: { Pratipada: 'Pratipada', Dwitiya: 'Dwitiya', Tritiya: 'Tritiya', Chaturthi: 'Chaturthi', Panchami: 'Panchami', Shashthi: 'Shashthi', Saptami: 'Saptami', Ashtami: 'Ashtami', Navami: 'Navami', Dashami: 'Dashami', Ekadashi: 'Ekadashi', Dwadashi: 'Dwadashi', Trayodashi: 'Trayodashi', Chaturdashi: 'Chaturdashi', 'Purnima/Amavasya': 'Purnima/Amavasya', Purnima: 'Purnima', Amavasya: 'Amavasya' },
        pakshas: { Shukla: 'Shukla Paksha', Krishna: 'Krishna Paksha' },
        nakshatras: { Ashwini: 'Ashwini', Bharani: 'Bharani', Krittika: 'Krittika', Rohini: 'Rohini', Mrigashira: 'Mrigashira', Ardra: 'Ardra', Punarvasu: 'Punarvasu', Pushya: 'Pushya', Ashlesha: 'Ashlesha', Magha: 'Magha', 'Purva Phalguni': 'Purva Phalguni', 'Uttara Phalguni': 'Uttara Phalguni', Hasta: 'Hasta', Chitra: 'Chitra', Swati: 'Swati', Vishakha: 'Vishakha', Anuradha: 'Anuradha', Jyeshtha: 'Jyeshtha', Mula: 'Mula', 'Purva Ashadha': 'Purva Ashadha', 'Uttara Ashadha': 'Uttara Ashadha', Shravana: 'Shravana', Dhanishta: 'Dhanishta', Shatabhisha: 'Shatabhisha', 'Purva Bhadrapada': 'Purva Bhadrapada', 'Uttara Bhadrapada': 'Uttara Bhadrapada', Revati: 'Revati' },
        yogas: { Vishkumbha: 'Vishkumbha', Priti: 'Priti', Ayushman: 'Ayushman', Saubhagya: 'Saubhagya', Shobhana: 'Shobhana', Atiganda: 'Atiganda', Sukarma: 'Sukarma', Dhriti: 'Dhriti', Shula: 'Shula', Ganda: 'Ganda', Vriddhi: 'Vriddhi', Dhruva: 'Dhruva', Vyaghata: 'Vyaghata', Harshana: 'Harshana', Vajra: 'Vajra', Siddhi: 'Siddhi', Vyatipata: 'Vyatipata', Variyan: 'Variyan', Parigha: 'Parigha', Shiva: 'Shiva', Siddha: 'Siddha', Sadhya: 'Sadhya', Shubha: 'Shubha', Shukla: 'Shukla', Brahma: 'Brahma', Indra: 'Indra', Vaidhriti: 'Vaidhriti' },
        karanas: { Bava: 'Bava', Balava: 'Balava', Kaulava: 'Kaulava', Taitila: 'Taitila', Gara: 'Gara', Vanija: 'Vanija', Vishti: 'Vishti' },
        varas: { Sunday: 'Sunday', Monday: 'Monday', Tuesday: 'Tuesday', Wednesday: 'Wednesday', Thursday: 'Thursday', Friday: 'Friday', Saturday: 'Saturday' },
        maasas: { Chaitra: 'Chaitra', Vaishakha: 'Vaishakha', Jyeshtha: 'Jyeshtha', Ashadha: 'Ashadha', Shravana: 'Shravana', Bhadrapada: 'Bhadrapada', Ashwina: 'Ashwina', Kartika: 'Kartika', Margashirsha: 'Margashirsha', Pausha: 'Pausha', Magha: 'Magha', Phalguna: 'Phalguna' },
        ritus: { Vasanta: 'Vasanta', Grishma: 'Grishma', Varsha: 'Varsha', Sharad: 'Sharad', Hemanta: 'Hemanta', Shishira: 'Shishira' },
        samvatsaras: { Prabhava: 'Prabhava', Vibhava: 'Vibhava', Shukla: 'Shukla', Pramoda: 'Pramoda', Prajapati: 'Prajapati', Angirasa: 'Angirasa', Shrimukha: 'Shrimukha', Bhava: 'Bhava', Yuva: 'Yuva', Dhatri: 'Dhatri', Ishwara: 'Ishwara', Bahudhanya: 'Bahudhanya', Pramathi: 'Pramathi', Vikrama: 'Vikrama', Vrishabha: 'Vrishabha', Chitrabhanu: 'Chitrabhanu', Subhanu: 'Subhanu', Tarana: 'Tarana', Parthiva: 'Parthiva', Vyaya: 'Vyaya', Sarvajit: 'Sarvajit', Sarvadhari: 'Sarvadhari', Virodhi: 'Virodhi', Vikriti: 'Vikriti', Khara: 'Khara', Nandana: 'Nandana', Vijaya: 'Vijaya', Jaya: 'Jaya', Manmatha: 'Manmatha', Durmukha: 'Durmukha', Hemalamba: 'Hemalamba', Vilambi: 'Vilambi', Vikari: 'Vikari', Sharvari: 'Sharvari', Plava: 'Plava', Shubhakrit: 'Shubhakrit', Shobhakrit: 'Shobhakrit', Krodhi: 'Krodhi', Vishvavasu: 'Vishvavasu', Parabhava: 'Parabhava', Plavanga: 'Plavanga', Kilaka: 'Kilaka', Saumya: 'Saumya', Sadharana: 'Sadharana', Virodhikrit: 'Virodhikrit', Paridhavi: 'Paridhavi', Pramadicha: 'Pramadicha', Ananda: 'Ananda', Rakshasa: 'Rakshasa', Nala: 'Nala', Pingala: 'Pingala', Kalayukta: 'Kalayukta', Siddharthi: 'Siddharthi', Raudra: 'Raudra', Durmati: 'Durmati', Dundubhi: 'Dundubhi', Rudhirodgari: 'Rudhirodgari', Raktakshi: 'Raktakshi', Krodhana: 'Krodhana', Akshaya: 'Akshaya' },
    },
    hi: {
        tithis: { Pratipada: 'प्रतिपदा', Dwitiya: 'द्वितीया', Tritiya: 'तृतीया', Chaturthi: 'चतुर्थी', Panchami: 'पञ्चमी', Shashthi: 'षष्ठी', Saptami: 'सप्तमी', Ashtami: 'अष्टमी', Navami: 'नवमी', Dashami: 'दशमी', Ekadashi: 'एकादशी', Dwadashi: 'द्वादशी', Trayodashi: 'त्रयोदशी', Chaturdashi: 'चतुर्दशी', 'Purnima/Amavasya': 'पूर्णिमा/अमावस्या', Purnima: 'पूर्णिमा', Amavasya: 'अमावस्या' },
        pakshas: { Shukla: 'शुक्ल पक्ष', Krishna: 'कृष्ण पक्ष' },
        nakshatras: { Ashwini: 'अश्विनी', Bharani: 'भरणी', Krittika: 'कृत्तिका', Rohini: 'रोहिणी', Mrigashira: 'मृगशिरा', Ardra: 'आर्द्रा', Punarvasu: 'पुनर्वसु', Pushya: 'पुष्य', Ashlesha: 'आश्लेषा', Magha: 'मघा', 'Purva Phalguni': 'पूर्व फाल्गुनी', 'Uttara Phalguni': 'उत्तर फाल्गुनी', Hasta: 'हस्त', Chitra: 'चित्रा', Swati: 'स्वाती', Vishakha: 'विशाखा', Anuradha: 'अनुराधा', Jyeshtha: 'ज्येष्ठा', Mula: 'मूल', 'Purva Ashadha': 'पूर्वाषाढ़ा', 'Uttara Ashadha': 'उत्तराषाढ़ा', Shravana: 'श्रवण', Dhanishta: 'धनिष्ठा', Shatabhisha: 'शतभिषा', 'Purva Bhadrapada': 'पूर्व भाद्रपदा', 'Uttara Bhadrapada': 'उत्तर भाद्रपदा', Revati: 'रेवती' },
        yogas: { Vishkumbha: 'विष्कुम्भ', Priti: 'प्रीति', Ayushman: 'आयुष्मान', Saubhagya: 'सौभाग्य', Shobhana: 'शोभन', Atiganda: 'अतिगण्ड', Sukarma: 'सुकर्मा', Dhriti: 'धृति', Shula: 'शूल', Ganda: 'गण्ड', Vriddhi: 'वृद्धि', Dhruva: 'ध्रुव', Vyaghata: 'व्याघात', Harshana: 'हर्षण', Vajra: 'वज्र', Siddhi: 'सिद्धि', Vyatipata: 'व्यतीपात', Variyan: 'वरीयान', Parigha: 'परिघ', Shiva: 'शिव', Siddha: 'सिद्ध', Sadhya: 'साध्य', Shubha: 'शुभ', Shukla: 'शुक्ल', Brahma: 'ब्रह्म', Indra: 'इन्द्र', Vaidhriti: 'वैधृति' },
        karanas: { Bava: 'बव', Balava: 'बालव', Kaulava: 'कौलव', Taitila: 'तैतिल', Gara: 'गर', Vanija: 'वणिज', Vishti: 'विष्टि' },
        varas: { Sunday: 'रविवार', Monday: 'सोमवार', Tuesday: 'मंगलवार', Wednesday: 'बुधवार', Thursday: 'गुरुवार', Friday: 'शुक्रवार', Saturday: 'शनिवार' },
        maasas: { Chaitra: 'चैत्र', Vaishakha: 'वैशाख', Jyeshtha: 'ज्येष्ठ', Ashadha: 'आषाढ़', Shravana: 'श्रावण', Bhadrapada: 'भाद्रपद', Ashwina: 'आश्विन', Kartika: 'कार्तिक', Margashirsha: 'मार्गशीर्ष', Pausha: 'पौष', Magha: 'माघ', Phalguna: 'फाल्गुन' },
        ritus: { Vasanta: 'वसन्त', Grishma: 'ग्रीष्म', Varsha: 'वर्षा', Sharad: 'शरद्', Hemanta: 'हेमन्त', Shishira: 'शिशिर' },
        samvatsaras: { Prabhava: 'प्रभव', Vibhava: 'विभव', Shukla: 'शुक्ल', Pramoda: 'प्रमोद', Prajapati: 'प्रजापति', Angirasa: 'अङ्गिरस', Shrimukha: 'श्रीमख', Bhava: 'भव', Yuva: 'युव', Dhatri: 'धातृ', Ishwara: 'ईश्वर', Bahudhanya: 'बहुधान्य', Pramathi: 'प्रमाथि', Vikrama: 'विक्रम', Vrishabha: 'वृषभ', Chitrabhanu: 'चित्रभानु', Subhanu: 'सुभानु', Tarana: 'तारण', Parthiva: 'पार्थिव', Vyaya: 'व्यय', Sarvajit: 'सर्वजित्', Sarvadhari: 'सर्वधारी', Virodhi: 'विरोधी', Vikriti: 'विकृति', Khara: 'खर', Nandana: 'नन्दन', Vijaya: 'विजय', Jaya: 'जय', Manmatha: 'मन्मथ', Durmukha: 'दुर्मुख', Hemalamba: 'हेमलम्ब', Vilambi: 'विलम्बी', Vikari: 'विकारी', Sharvari: 'शार्वरी', Plava: 'प्लव', Shubhakrit: 'शुभकृत्', Shobhakrit: 'शोभकृत्', Krodhi: 'क्रोधी', Vishvavasu: 'विश्ववसु', Parabhava: 'पराभव', Plavanga: 'प्लवङ्ग', Kilaka: 'कीलक', Saumya: 'सौम्य', Sadharana: 'साधारण', Virodhikrit: 'विरोधकृत्', Paridhavi: 'परिधावी', Pramadicha: 'प्रमादीचा', Ananda: 'आनन्द', Rakshasa: 'राक्षस', Nala: 'नल', Pingala: 'पिङ्गल', Kalayukta: 'कालयुक्त', Siddharthi: 'सिद्धार्थी', Raudra: 'रौद्र', Durmati: 'दुर्मति', Dundubhi: 'दुन्दुभि', Rudhirodgari: 'रुधिरोद्गारी', Raktakshi: 'रक्ताक्षी', Krodhana: 'क्रोधन', Akshaya: 'अक्षय' },
    },
};

function tr(lang, category, key) {
    const map = (TRANSLATIONS[lang] || TRANSLATIONS.hi)[category] || {};
    return map[key] || (TRANSLATIONS.en[category] || {})[key] || key;
}

const MAASA_TO_RITU = {
    'Chaitra': 'Vasanta', 'Vaishakha': 'Vasanta',
    'Jyeshtha': 'Grishma', 'Ashadha': 'Grishma',
    'Shravana': 'Varsha', 'Bhadrapada': 'Varsha',
    'Ashwina': 'Sharad', 'Kartika': 'Sharad',
    'Margashirsha': 'Hemanta', 'Pausha': 'Hemanta',
    'Magha': 'Shishira', 'Phalguna': 'Shishira'
};

// ─── Astronomy helpers ────────────────────────────────────────────────────────

const AYANAMSA_2024 = 24.17;

function getAyanamsa(date) {
    const yearDiff = date.getFullYear() - 2024 + date.getMonth() / 12;
    return AYANAMSA_2024 + yearDiff * 50.3 / 3600;
}

function toSidereal(tropicalLong, date) {
    let s = tropicalLong - getAyanamsa(date);
    return s < 0 ? s + 360 : s;
}

function getSunLongitude(date) {
    return Astronomy.SunPosition(Astronomy.MakeTime(date)).elon;
}

function getMoonLongitude(date) {
    const pos = Astronomy.GeoMoon(Astronomy.MakeTime(date));
    return Astronomy.Ecliptic(pos).elon;
}

// ─── Panchanga calculations ───────────────────────────────────────────────────

function calculateTithi(date) {
    const d = new Date(date);
    d.setHours(6, 0, 0, 0); // use sunrise reference
    const sunLong = getSunLongitude(d);
    const moonLong = getMoonLongitude(d);
    let diff = moonLong - sunLong;
    if (diff < 0) diff += 360;
    const tithiNum = Math.floor(diff / 12) + 1;
    const tithiProgress = (diff % 12) / 12;
    const hoursToEnd = ((12 - diff % 12) / (13.176 - 0.9856)) * 24;
    return {
        number: tithiNum,
        name: TITHIS[(tithiNum - 1) % 15],
        paksha: tithiNum <= 15 ? 'Shukla' : 'Krishna',
        pakshaDay: tithiNum <= 15 ? tithiNum : tithiNum - 15,
        progress: tithiProgress,
        endTime: new Date(d.getTime() + hoursToEnd * 3600000)
    };
}

function calculateNakshatra(date) {
    const sid = toSidereal(getMoonLongitude(date), date);
    const num = Math.floor(sid / (360 / 27));
    return {
        number: num + 1,
        name: NAKSHATRAS[num],
        progress: (sid % (360 / 27)) / (360 / 27)
    };
}

function calculateYoga(date) {
    const sun = toSidereal(getSunLongitude(date), date);
    const moon = toSidereal(getMoonLongitude(date), date);
    let sum = sun + moon;
    if (sum >= 360) sum -= 360;
    const num = Math.floor(sum / (360 / 27));
    return { number: num + 1, name: YOGAS[num] };
}

function calculateKarana(date) {
    const tithi = calculateTithi(date);
    const idx = ((tithi.number - 1) * 2 + Math.floor(tithi.progress * 2)) % 7;
    return { name: KARANAS[idx] };
}

function calculateVara(date) {
    return { number: date.getDay() + 1, name: VARAS[date.getDay()] };
}

function getMoonPhase(date) {
    const phase = Astronomy.MoonPhase(Astronomy.MakeTime(date));
    return {
        angle: phase,
        illumination: (1 - Math.cos(phase * Math.PI / 180)) / 2 * 100,
        isWaxing: phase < 180
    };
}

function findNextPurnima(date) {
    const fm = Astronomy.SearchMoonPhase(180, Astronomy.MakeTime(date), 30);
    return fm ? fm.date : date;
}

function findPreviousPurnima(date) {
    for (const offset of [29, 45]) {
        const start = new Date(date.getTime() - offset * 86400000);
        const fm = Astronomy.SearchMoonPhase(180, Astronomy.MakeTime(start), 30);
        if (fm && fm.date < date) return fm.date;
    }
    return date;
}

function findPreviousAmavasya(date) {
    for (const [offset, window] of [[30, 35], [45, 50]]) {
        const start = new Date(date.getTime() - offset * 86400000);
        const nm = Astronomy.SearchMoonPhase(0, Astronomy.MakeTime(start), window);
        if (nm && nm.date < date) return nm.date;
    }
    return date;
}

function findNextAmavasya(date) {
    const nm = Astronomy.SearchMoonPhase(0, Astronomy.MakeTime(date), 30);
    return nm ? nm.date : date;
}

function getMaasaFromPurnima(purnimaDate, date) {
    const sid = toSidereal(getMoonLongitude(purnimaDate), purnimaDate);
    const nakshatraNum = Math.floor(sid / (360 / 27));
    const purnimaNakshatra = NAKSHATRAS[nakshatraNum];
    let maasaName = NAKSHATRA_TO_MAASA[purnimaNakshatra];
    if (!maasaName) {
        const rashiNum = Math.floor(toSidereal(getSunLongitude(date), date) / 30);
        maasaName = MAASAS[rashiNum];
    }
    return { maasaName, purnimaNakshatra };
}

function calculateMaasa(date, isAmant = false) {
    let purnimaDate, maasaName, purnimaNakshatra;
    if (isAmant) {
        const prevAm = findPreviousAmavasya(date);
        const nextAm = findNextAmavasya(date);
        const pm = Astronomy.SearchMoonPhase(180, Astronomy.MakeTime(prevAm), 20);
        purnimaDate = (pm && pm.date > prevAm && pm.date < nextAm) ? pm.date : findNextPurnima(prevAm);
    } else {
        purnimaDate = findNextPurnima(date);
    }
    const r = getMaasaFromPurnima(purnimaDate, date);
    maasaName = r.maasaName;
    purnimaNakshatra = r.purnimaNakshatra;
    return {
        name: maasaName,
        number: MAASAS.indexOf(maasaName) + 1,
        purnimaNakshatra,
        purnimaDate,
        system: isAmant ? 'Amant (South)' : 'Purnimant (North)'
    };
}

function calculateRitu(date, maasaName) {
    const maasa = maasaName || calculateMaasa(date).name;
    const rituName = MAASA_TO_RITU[maasa] || 'Vasanta';
    return RITU_THEMES[rituName];
}

function calculateSamvatsara(date) {
    const year = date.getFullYear();
    const meshaDt = new Date(year, 3, 14);
    const newMoon = Astronomy.SearchMoonPhase(0, Astronomy.MakeTime(meshaDt), -40);
    const chaitraPP = newMoon.date;

    let sakaYear, startDate, endDate;
    if (date < chaitraPP) {
        sakaYear = year - 79;
        const pm = Astronomy.SearchMoonPhase(0, Astronomy.MakeTime(new Date(year - 1, 3, 14)), -40);
        startDate = pm.date;
        endDate = chaitraPP;
    } else {
        sakaYear = year - 78;
        startDate = chaitraPP;
        const nm = Astronomy.SearchMoonPhase(0, Astronomy.MakeTime(new Date(year + 1, 3, 14)), -40);
        endDate = nm.date;
    }
    const index = (sakaYear + 11) % 60;
    return { number: index + 1, name: SAMVATSARAS[index], sakaYear, startDate, endDate };
}

// ─── Public API ───────────────────────────────────────────────────────────────

/**
 * Calculate the full Panchanga for a given date and return it as a JSON string.
 *
 * @param {Date|string} date     - Date to calculate for (default: today)
 * @param {object}      options
 * @param {boolean}     options.isAmant  - Use Amanta (South Indian) system (default: false)
 * @param {string}      options.lang     - Output language: 'hi' (Hindi, default) | 'en' (English)
 * @returns {string} JSON string with names translated into the requested language
 */
function getPanchanga(date = new Date(), options = {}) {
    const { isAmant = true, lang = 'hi' } = options;
    const d = date instanceof Date ? date : new Date(date);

    const maasa = calculateMaasa(d, isAmant);
    const tithi = calculateTithi(d);
    const nakshatra = calculateNakshatra(d);
    const yoga = calculateYoga(d);
    const karana = calculateKarana(d);
    const vara = calculateVara(d);
    const ritu = calculateRitu(d, maasa.name);
    const samvatsara = calculateSamvatsara(d);
    const moonPhase = getMoonPhase(d);

    // Translate a tithi name: last tithi (15) is Purnima or Amavasya based on paksha
    const tithiKey = tithi.number === 15 ? 'Purnima' : tithi.number === 30 ? 'Amavasya' : tithi.name;

    const varaDayKey = VARA_TO_DAY[vara.name] || vara.name;

    const result = {
        tithi: {
            ...tithi,
            name: tr(lang, 'tithis', tithiKey),
            nameEnglish: tr('en', 'tithis', tithiKey),
            paksha: tr(lang, 'pakshas', tithi.paksha),
            pakshaEnglish: tr('en', 'pakshas', tithi.paksha),
        },
        nakshatra: {
            ...nakshatra,
            name: tr(lang, 'nakshatras', nakshatra.name),
            nameEnglish: tr('en', 'nakshatras', nakshatra.name),
        },
        yoga: {
            ...yoga,
            name: tr(lang, 'yogas', yoga.name),
            nameEnglish: tr('en', 'yogas', yoga.name),
        },
        karana: {
            name: tr(lang, 'karanas', karana.name),
            nameEnglish: tr('en', 'karanas', karana.name),
        },
        vara: {
            ...vara,
            name: tr(lang, 'varas', varaDayKey),
            nameEnglish: tr('en', 'varas', varaDayKey),
        },
        maasa: {
            ...maasa,
            name: tr(lang, 'maasas', maasa.name),
            nameEnglish: tr('en', 'maasas', maasa.name),
        },
        ritu: {
            ...ritu,
            name: tr(lang, 'ritus', ritu.name),
            nameEnglish: tr('en', 'ritus', ritu.name),
        },
        samvatsara: {
            ...samvatsara,
            name: tr(lang, 'samvatsaras', samvatsara.name),
            nameEnglish: tr('en', 'samvatsaras', samvatsara.name),
        },
        moonPhase,
        paksha: tr(lang, 'pakshas', tithi.paksha),
        pakshaEnglish: tr('en', 'pakshas', tithi.paksha),
    };

    return JSON.stringify(result, null, 2);
}

// ─── Exports ──────────────────────────────────────────────────────────────────

module.exports = {
    getPanchanga,
    // individual calculators also exported for granular use
    calculateTithi,
    calculateNakshatra,
    calculateYoga,
    calculateKarana,
    calculateVara,
    calculateMaasa,
    calculateRitu,
    calculateSamvatsara,
    getMoonPhase,
};

// ─── CLI entry point ──────────────────────────────────────────────────────────

if (require.main === module) {
    const [, , dateArg, amantArg, langArg] = process.argv;
    const date = dateArg ? new Date(dateArg) : new Date();
    const isAmant = amantArg === 'true';
    const lang = langArg || 'hi';
    if (isNaN(date.getTime())) {
        console.error(`Invalid date: "${dateArg}". Use ISO format e.g. 2026-04-12`);
        process.exit(1);
    }
    console.log(getPanchanga(date, { isAmant, lang }));
}
