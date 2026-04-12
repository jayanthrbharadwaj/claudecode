const admin = require('firebase-admin');
const axios = require('axios');
const Sanscript = require('@indic-transliteration/sanscript'); // Transliteration library
const { getPanchanga } = require('./panchangaLibrary.js');

// ... [Firebase Admin Initialization] ...

async function run() {
  try {
    // 1. Get English Panchanga Data
    const pData = getPanchanga(new Date(), { lang: 'en' });

    // 2. Transliteration Function Helper
    // 'itrans' or 'iast' are common input schemes; 'devanagari' is the target.
    const toDeva = (text) => Sanscript.t(text, 'itrans', 'devanagari');

    // 3. Extract and Transliterate Fields
    const samvatsara = toDeva(pData.samvatsara.nameEnglish);
    const ritu       = toDeva(pData.ritu.nameEnglish);
    const maasa      = toDeva(pData.maasa.nameEnglish);
    const paksha     = toDeva(pData.tithi.pakshaEnglish);
    const tithi      = toDeva(pData.tithi.nameEnglish);
    const vara       = toDeva(pData.vara.nameEnglish);
    const nakshatra  = toDeva(pData.nakshatra.nameEnglish);
    const yoga       = toDeva(pData.yoga.nameEnglish);
    const karana     = toDeva(pData.karana.nameEnglish);

    // Note: Manually setting Aayana as it often needs separate calculation
    const aayana = "उत्तरायणे"; 

    // 4. Construct Final Sanskrit Text
    const fullText = `${samvatsara} नाम संवत्सरे, ${aayana}, ${ritu} ऋतौ, ${maasa} मासे, ${paksha}, ${tithi} पुण्यतिथौ, ${vara} वासर युक्तायां, ${nakshatra} नक्षत्रे, ${yoga} योगे, ${karana} करणे, एवंगुण विषेषण विशिश्टायाम्, शुभतिथौ`;

    console.log("--- Transliterated Data ---");
    console.log(`Samvatsara: ${samvatsara} (${pData.samvatsara.nameEnglish})`);
    console.log(`Maasa: ${maasa} (${pData.maasa.nameEnglish})`);
    console.log("Full Generated Text:", fullText);

    // 5. Hit the Voice Generation API
    const response = await axios.post('https://yourvoic.com', {
      text: fullText,
      voice: "Fenrir",
      language: "sa"
    }, {
      headers: { 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0..." 
      }
    });

    // ... [Firestore and Storage Logic] ...

  } catch (e) {
    console.error("Task failed:", e);
    process.exit(1);
  }
}

run();
