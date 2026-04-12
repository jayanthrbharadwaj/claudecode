const admin = require('firebase-admin');
const axios = require('axios');
const Sanscript = require('@indic-transliteration/sanscript');
const { getPanchanga } = require('./panchangaLibrary.js');
const { pipeline } = require('@xenova/transformers');
const { MPEGDecoder } = require('mpg123-decoder');
const { WaveFile } = require('wavefile');
const fs = require('fs');
const serviceAccount = require('./serviceAccount.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: `${serviceAccount.project_id}.appspot.com`
});

const db = admin.firestore();
const storage = admin.storage();
const makeApiCall = async (fullText) => {
  // 5. Hit the Voice Generation API
  const response = await axios.post('https://yourvoic.com/api/generate', {
    text: `This speaker speaks with a Indian Sanskrit accent.:\n<yes!>${fullText}`,
    voice: "Fenrir",
    language: "sa"
  }, {
    headers: {
      'sec-ch-ua-platform': '"macOS"',
      'Referer': 'https://yourvoic.com/tools/sanskrit-text-to-speech-india',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
      'Content-Type': 'application/json',
      'sec-ch-ua-mobile': '?0'
    }
  });
  return response
}

async function run() {
  try {
    // 1. Get English Panchanga Data
    const pData = JSON.parse(getPanchanga(new Date()));

    // 2. Transliteration Function Helper
    // 'itrans' or 'iast' are common input schemes; 'devanagari' is the target.
    const toDeva = (text) => Sanscript.t(text.toLowerCase(), 'itrans', 'devanagari');

    // 3. Extract and Transliterate Fields
    const samvatsara = toDeva(pData.samvatsara.nameEnglish);
    const ritu = toDeva(pData.ritu.nameEnglish);
    const maasa = (pData.maasa.nameEnglish);
    const paksha = (pData.tithi.paksha);
    const tithi = toDeva(pData.tithi.nameEnglish);
    const vara = (pData.vara.name);
    const nakshatra = (pData.nakshatra.name);
    const yoga = (pData.yoga.name);
    const karana = (pData.karana.name);
    // उत्तरायणे,वसन्तऋतौ,वैशखमासे,क्रिश्न पक्श:,दशमिपुण्यतिथौ,रविवारवासरयुक्तायां,श्रवणनक्षत्रे,सध्ययोगे,विश्तिकरणे,एवंगुण विषेषणविशिश्टायाम्,शुभतिथौ
    // Note: Manually setting Aayana as it often needs separate calculation
    const aayana = "उत्तरायणे";

    // 4. Construct Final Sanskrit Text
    // const fullText = `<yes!>${samvatsara}नाम संवत्सरे,${aayana},${ritu}ऋतौ,${maasa}मासे,${paksha}:,${tithi}पुण्यतिथौ,${vara}वासरयुक्तायां,${nakshatra}नक्षत्रे,${yoga}योगे,${karana}करणे,एवंगुण विषेषणविशिश्टायाम्,शुभतिथौ`;
    const fullText = `${aayana},${ritu}ऋतौ,${maasa}मासे,${paksha}:,${tithi}पुण्यतिथौ,${vara}वासरयुक्तायां,${nakshatra}नक्षत्रे,${yoga}योगे,${karana}करणे,एवंगुण विषेषणविशिश्टायाम्,शुभतिथौ`;

    console.log("--- Transliterated Data --- ", pData);
    console.log(`Samvatsara: ${samvatsara} (${pData.samvatsara.nameEnglish})`);
    console.log(`Maasa: ${maasa} (${pData.maasa.nameEnglish})`);
    console.log("Full Generated Text:", fullText);

    const isGitHubActions = process.env.GITHUB_ACTIONS === 'true';
    let audioRes;

    if (true) {
      console.log("Running in GitHub Actions - making API call...");
      const response = await makeApiCall(fullText);
      const audioUrl = response.data.audio_url || response.data.url || response.data; // Adjust based on actual key
      console.log("audioUrl:", audioUrl);
      if (audioUrl) {
        audioRes = await axios.get(audioUrl, { responseType: 'arraybuffer' });
      }
    } else {
      console.log("Running locally - using sample audio...");
    }

    if (true) {
      // --- WHISPER INTEGRATION STARTS HERE ---
      console.log("Starting Whisper transcription...");

      // 1. Initialize the pipeline (using the tiny English model as per your link)
      // Note: For Sanskrit, use 'Xenova/whisper-tiny' (multilingual) instead of 'whisper-tiny.en'
      const transcriber = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny', {
        // 'q8' specifically loads the *_quantized.onnx files
        dtype: 'q8',
        device: 'cpu', // Default for Node.js
      });

      // 2. Decode the MP3 buffer using mpg123-decoder (pure JS)
      const decoder = new MPEGDecoder();
      await decoder.ready;

      const mp3Buffer = (typeof audioRes !== 'undefined') ? Buffer.from(audioRes.data) : fs.readFileSync('sample_audio/Vaishakha_1775980563_47107.mp3');
      const { channelData, sampleRate: originalSampleRate } = decoder.decode(mp3Buffer);

      // Use the first channel (mono) for Whisper
      let pcmData = channelData[0];

      // Simple Resampling to 16kHz if needed
      if (originalSampleRate !== 16000) {
        console.log(`Resampling from ${originalSampleRate}Hz to 16000Hz...`);
        const ratio = originalSampleRate / 16000;
        const newLength = Math.round(pcmData.length / ratio);
        const resampledData = new Float32Array(newLength);
        for (let i = 0; i < newLength; i++) {
          resampledData[i] = pcmData[Math.round(i * ratio)];
        }
        pcmData = resampledData;
      }

      console.log(`Processing ${pcmData.length} samples at 16kHz`);

      const transcript = await transcriber(pcmData, {
        language: 'sanskrit',
        task: 'transcribe',
        return_timestamps: 'word',
      });
      console.log("Transcription:", transcript.text);

      // 1. Find the "Yes," chunk to determine the crop point
      const yesChunk = transcript.chunks.find(chunk => {
        const cleanText = chunk.text.trim().toLowerCase().replace(/[,.!]/g, '');
        return cleanText === 'yes';
      });

      let finalPcm = pcmData;
      let timeOffset = 0;

      if (yesChunk) {
        timeOffset = yesChunk.timestamp[1] - 0.2; // End of the "Yes" chunk JAYA -0.2 random offset to not swallow first akshara of next chunk
        const samplesToSkip = Math.round(timeOffset * 16000);
        finalPcm = pcmData.slice(samplesToSkip);
        console.log(`Cropping ${timeOffset}s from the start of audio.`);
      }

      // 2. Filter out "Yes" and shift timestamps for remaining chunks
      const filteredChunks = transcript.chunks
        .filter(chunk => {
          const cleanText = chunk.text.trim().toLowerCase().replace(/[,.!]/g, '');
          return cleanText !== 'yes';
        })

        .map(chunk => ({
          text: chunk.text,
          timestamp: [
            Math.max(0, chunk.timestamp[0] - timeOffset).toFixed(3),
            Math.max(0, chunk.timestamp[1] - timeOffset - 0.2).toFixed(3)
          ]
        }));

      console.log("Filtered & Shifted Chunks:", JSON.stringify(filteredChunks, null, 2));

      // Calculate current date in dd-mm-yyyy format
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
      const yyyy = today.getFullYear();
      const dateString = `${dd}-${mm}-${yyyy}`;

      const wavFileName = `panchanga_trimmed_${dateString}.wav`;
      const jsonFileName = `panchanga_metadata_${dateString}.json`;

      // 3. Save the trimmed audio as a WAV file
      const wav = new WaveFile();
      wav.fromScratch(1, 16000, '32f', finalPcm);
      fs.writeFileSync(wavFileName, wav.toBuffer());
      console.log(`Trimmed audio saved to ${wavFileName}`);

      // 4. Save metadata to a local JSON file
      fs.writeFileSync(jsonFileName, JSON.stringify(filteredChunks, null, 2));
      console.log(`Metadata saved to ${jsonFileName}`);
      // const bucket = admin.storage().bucket();
      // const file = bucket.file(`audio/${docRef.id}.mp3`);

      // await file.save(Buffer.from(audioRes.data), {
      //   metadata: { contentType: 'audio/mpeg' }
      // });
      console.log("Saved to storage successfully.");
    }

  } catch (e) {
    console.error("Task failed:", e);
    process.exit(1);
  }
}

run();
