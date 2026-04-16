const fs = require('fs');
const { getISTDate, generatePanchangaText, buildTransliteratedMap, SANSCRIPT_LANGS } = require('./utils/textUtils');
const { synthesize, transcribeWithTimestamps } = require('./services/googleCloudService');
const { testFirestoreConnectivity, submitSync } = require('./services/firebaseService');
const { mixAudioWithBackground } = require('./services/audioService');

async function run() {
  try {
    const now = getISTDate();
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();
    const dateId = `${day}-${month}-${year}`; // dd-mm-yyyy format

    const { fullText, samvatsara, maasa } = generatePanchangaText();
    const outputFilename = 'output.wav';
    const backgroundAudioPath = 'assets/audio/temple-crowd-sound-edit2.wav';
    const finalOutputFilename = 'output_final.wav';

    console.log(`\n--- Panchanga for ${dateId} ---`);
    console.log(`Samvatsara: ${samvatsara}`);
    console.log(`Maasa: ${maasa}`);
    console.log(`Full Text: ${fullText}\n`);

    // 0. Test Firestore permissions first
    await testFirestoreConnectivity();

    // 1. Generate Audio (Synthesize)
    await synthesize("temple purohit reciting", fullText, outputFilename);

    // 1b. Mix with Background
    if (fs.existsSync(backgroundAudioPath)) {
      mixAudioWithBackground(outputFilename, backgroundAudioPath, finalOutputFilename, 0.9);
    } else {
      console.warn(`[WARNING] Background audio not found at ${backgroundAudioPath}. Skipping mixing.`);
    }

    // 2. Transcribe (Speech-to-Text)
    // const words = await transcribeWithTimestamps(outputFilename);

    // 3. Format Metadata
    // const timeMap = {};
    // words.forEach((w, index) => {
    //   timeMap[index.toString()] = {
    //     time: parseFloat(w.start.toFixed(3)),
    //     text: w.text
    //   };
    // });

    // // 4. Submit to Firebase Sync
    // await submitSync({
    //   syncMode: 'word',
    //   dateId,
    //   timeMap,
    //   activeText: fullText,
    //   transliterateMapFn: buildTransliteratedMap,
    //   langList: [...Object.keys(SANSCRIPT_LANGS), 'en']
    // });

    console.log("\n==================================================");
    console.log("             SANKALPA MANTRA & TIMESTAMPS          ");
    console.log("==================================================");
    console.log("\n--- Full Mantra (Kannada) ---");
    console.log(fullText);

    console.log("\n--- Word-Level Timestamps ---");
    // Object.entries(timeMap).forEach(([index, data]) => {
    //   console.log(`[${data.time.toFixed(3)}s]: ${data.text}`);
    // });
    console.log("==================================================");

    console.log(`\nMetadata for ${dateId} synced to Firebase successfully.`);
    console.log("Process completed successfully.");
  } catch (e) {
    if (e.response && e.response.data) {
      console.error("API Error Response:", JSON.stringify(e.response.data, null, 2));
    }
    console.error("Task failed:", e.stack || e.message || e);
    process.exit(1);
  }
}

run();
