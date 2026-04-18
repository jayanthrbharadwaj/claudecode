const Sanscript = require('@indic-transliteration/sanscript');
const { getPanchanga } = require('../panchangaLibrary.js');

const SANSCRIPT_LANGS = {
  'sa': 'devanagari',
  'te': 'telugu',
  'ta': 'tamil',
  'ml': 'malayalam',
  'hi': 'devanagari',
  'kn': 'kannada'
};

/**
 * Returns current date in IST
 */
const getISTDate = () => new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));

/**
 * Transliterates the timeMap from Kannada to target languages
 */
function buildTransliteratedMap(timeMap, langCode) {
  if (langCode === 'en' || langCode === 'kn') return timeMap;
  const targetScheme = SANSCRIPT_LANGS[langCode];
  if (!targetScheme) return timeMap;

  console.log(` - Transliterating timeMap for: ${langCode}`);
  const result = {};
  for (const [key, val] of Object.entries(timeMap)) {
    result[key] = {
      ...val,
      text: Sanscript.t(val.text, 'kannada', targetScheme)
    };
  }
  return result;
}

/**
 * Generates the Panchanga text in Kannada
 */
const generatePanchangaText = () => {
  const pData = JSON.parse(getPanchanga(getISTDate()));
  const toKannada = (text, from = 'itrans') => Sanscript.t(text, from, 'kannada');

  const samvatsara = toKannada(pData.samvatsara.name, 'devanagari');
  const ritu = toKannada(pData.ritu.nameEnglish.toLowerCase());
  const maasa = toKannada(pData.maasa.name, 'devanagari');
  const paksha = toKannada(pData.tithi.paksha, 'devanagari');
  const tithi = toKannada(pData.tithi.name, 'devanagari');
  const vara = toKannada(pData.vara.name, 'devanagari');
  const nakshatra = toKannada(pData.nakshatra.name, 'devanagari');
  const yoga = toKannada(pData.yoga.name, 'devanagari');
  const karana = toKannada(pData.karana.name, 'devanagari');
  const aayana = toKannada("uttaraayaNe");

  const fullText = `${aayana},${ritu}ಋತೌ,${maasa}ಮಾಸೇ,${paksha}:,${tithi}ಪುಣ್ಯತಿಥೌ,${vara}ವಾಸರಯುಕ್ತಾಯಾಂ,${nakshatra}ನಕ್ಷತ್ರೇ,${yoga}ಯೋಗೇ,${karana}ಕರಣೇ,ಏವಂಗುಣ ವಿಶೇಷಣವಿಶಿಷ್ಟಾಯಾಮ್,ಶುಭತಿಥೌ. ಮಮ ಶಕ್ತಿ..., ಭಕ್ತಿ..., ಯುಕ್ತಿ... ದೃಢತಾಪ್ರಾಪ್ತ್ಯರ್ಥಂ, ಶುಭ ಕರ್ಮ ಪ್ರಾರಮ್ಭಂ ಕರಿಷ್ಯೇ...`;
  return { fullText, pData, samvatsara, maasa };
}

module.exports = {
  SANSCRIPT_LANGS,
  getISTDate,
  buildTransliteratedMap,
  generatePanchangaText
};
