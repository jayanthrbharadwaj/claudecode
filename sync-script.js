const axios = require('axios');
const Sanscript = require('@indic-transliteration/sanscript');
const { getPanchanga } = require('./panchangaLibrary.js');
const { pipeline } = require('@xenova/transformers');
const { MPEGDecoder } = require('mpg123-decoder');
const { WaveFile } = require('wavefile');
const fs = require('fs');

const AudioPrefixMode = {
  PREFIX_TRIM_AUDIO_ONE_SEC: 'PREFIX_TRIM_AUDIO_ONE_SEC',
  NONE: 'NONE'
};

const AudioSuffixMode = {
  SUFFIX_APPEND_BELL_TWO_SEC: 'SUFFIX_APPEND_BELL_TWO_SEC',
  NONE: 'NONE'
};

const makeApiCall = async (fullText) => {
  const url = 'https://yourvoic.com/api/generate';
  const data = {
    text: `This speaker speaks with a Indian Sanskrit accent.:\n<yes!>${fullText}`,
    voice: "Fenrir",
    language: "sa"
  };
  const headers = {
    'sec-ch-ua-platform': '"macOS"',
    'Referer': 'https://yourvoic.com/tools/sanskrit-text-to-speech-india',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0'
  };

  const curlCommand = `curl -X POST '${url}' \\\n` +
    Object.entries(headers).map(([k, v]) => `  -H '${k}: ${v}'`).join(' \\\n') +
    ` \\\n  -d '${JSON.stringify(data)}'`;

  console.log("--- Voice Generation Request (curl) ---");
  console.log(curlCommand);

  const response = await axios.post(url, data, { headers });

  console.log("--- Voice Generation Response ---");
  console.log(JSON.stringify(response.data, null, 2));

  return response;
}

const generatePanchangaText = () => {
  const pData = JSON.parse(getPanchanga(getISTDate()));
  const toDeva = (text) => Sanscript.t(text.toLowerCase(), 'itrans', 'devanagari');

  const samvatsara = toDeva(pData.samvatsara.nameEnglish);
  const ritu = toDeva(pData.ritu.nameEnglish);
  const maasa = (pData.maasa.name);
  const paksha = (pData.tithi.paksha);
  const tithi = (pData.tithi.name);
  const vara = (pData.vara.name);
  const nakshatra = (pData.nakshatra.name);
  const yoga = (pData.yoga.name);
  const karana = (pData.karana.name);
  const aayana = "उत्तरायणे";

  const fullText = `${aayana},${ritu}ऋतौ,${maasa}मासे,${paksha}:,${tithi}पुण्यतिथौ,${vara}वासरयुक्तायां,${nakshatra}नक्षत्रे,${yoga}योगे,${karana}करणे,एवंगुण विषेषणविशिश्टायाम्,शुभतिथौ`;

  console.log("--- Transliterated Data --- ", pData);
  console.log(`Samvatsara: ${samvatsara} (${pData.samvatsara.nameEnglish})`);
  console.log(`Maasa: ${maasa} (${pData.maasa.nameEnglish})`);
  console.log("Full Generated Text:", fullText);

  return { fullText, pData };
}

const fetchGeneratedAudio = async (fullText) => {
  console.log("Making API calls for voice generation...");
  let response = await makeApiCall(fullText);
  // forcibly make 2 API calls so that 2nd audio is better than 1st audio
  response = await makeApiCall(fullText);

  const audioUrl = response.data.audio_url || response.data.url || response.data;
  console.log("audioUrl:", audioUrl);

  if (audioUrl) {
    return await axios.get(audioUrl, { responseType: 'arraybuffer' });
  }
  return null;
}

const decodeAndResample = async (audioRes) => {
  const decoder = new MPEGDecoder();
  await decoder.ready;

  const mp3Buffer = audioRes ? Buffer.from(audioRes.data) : fs.readFileSync('sample_audio/Vaishakha_1775980563_47107.mp3');
  const { channelData, sampleRate: originalSampleRate } = decoder.decode(mp3Buffer);

  let pcmData = channelData[0];

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

  return { pcmData, originalSampleRate };
}

const transcribe = async (pcmData) => {
  console.log("Starting Whisper transcription...");
  const transcriber = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny', {
    dtype: 'q8',
    device: 'cpu',
  });

  return await transcriber(pcmData, {
    language: 'sanskrit',
    task: 'transcribe',
    return_timestamps: 'word',
  });
}

const createBellSound = () => {
  const bellWav = new WaveFile(fs.readFileSync('assets/audio/temple-bell-sound_So7H1ACm.wav'));
  const bellSampleRate = bellWav.fmt.sampleRate;
  let bellPcm = bellWav.getSamples(false, Float32Array)[0];

  if (bellSampleRate !== 16000) {
    const bellRatio = bellSampleRate / 16000;
    const bellResampled = new Float32Array(Math.round(bellPcm.length / bellRatio));
    for (let i = 0; i < bellResampled.length; i++) {
      const srcStart = i * bellRatio;
      const srcEnd = srcStart + bellRatio;
      const iStart = Math.floor(srcStart);
      const iEnd = Math.min(Math.ceil(srcEnd), bellPcm.length);
      let sum = 0;
      for (let j = iStart; j < iEnd; j++) sum += bellPcm[j];
      bellResampled[i] = sum / (iEnd - iStart);
    }
    bellPcm = bellResampled;
  }
  return bellPcm;
}

const audioSuffixProcessing = (pcmData, mode = AudioSuffixMode.SUFFIX_APPEND_BELL_TWO_SEC) => {
  if (mode === AudioSuffixMode.NONE) {
    return pcmData;
  }

  const bellPcm = createBellSound();
  // Name suggests TWO_SEC, but previous was 0.5s. Implementation now uses 2.0s as per enum name.
  const gapDuration = mode === AudioSuffixMode.SUFFIX_APPEND_BELL_TWO_SEC ? 2.0 : 0.5;
  const silenceSamples = Math.round(gapDuration * 16000);

  const combined = new Float32Array(pcmData.length + silenceSamples + bellPcm.length);
  combined.set(pcmData, 0);
  combined.set(bellPcm, pcmData.length + silenceSamples);
  console.log(`Appended temple bell sound with ${gapDuration}s gap (${bellPcm.length} samples).`);
  return combined;
}

const trimAudioPrefixApprox1Sec = (pcmData, timeOffset) => {
  const samplesToSkip = Math.round(timeOffset * 16000);
  return pcmData.slice(samplesToSkip);
}

const audioPrefixProcessing = (pcmData, yesChunk, mode = AudioPrefixMode.PREFIX_TRIM_AUDIO_ONE_SEC) => {
  if (mode === AudioPrefixMode.NONE || !yesChunk) {
    return { croppedPcm: pcmData, timeOffset: 0 };
  }

  const timeOffset = yesChunk.timestamp[1] - 0.2;
  const croppedPcm = trimAudioPrefixApprox1Sec(pcmData, timeOffset);
  console.log(`Cropping ${timeOffset}s from the start of audio.`);
  return { croppedPcm, timeOffset };
}

const processAndTrimAudio = async (transcript, pcmData) => {
  console.log("Transcription:", transcript.text);

  const yesChunk = transcript.chunks.find(chunk => {
    const cleanText = chunk.text.trim().toLowerCase().replace(/[,.!]/g, '');
    return cleanText === 'yes';
  });

  let finalPcm = pcmData;
  let timeOffset = 0;

  if (yesChunk) {
    const prefixResult = audioPrefixProcessing(pcmData, yesChunk, AudioPrefixMode.PREFIX_TRIM_AUDIO_ONE_SEC);
    timeOffset = prefixResult.timeOffset;
    // finalPcm = audioSuffixProcessing(prefixResult.croppedPcm, AudioSuffixMode.NONE);
    finalPcm = prefixResult.croppedPcm
  }

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

  return { finalPcm, filteredChunks, timeOffset };
}

const saveOutputs = (finalPcm, filteredChunks, fullText) => {
  const today = getISTDate();
  const dd = String(today.getDate()).padStart(2, '0');
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const yyyy = today.getFullYear();
  const dateString = `${dd}-${mm}-${yyyy}`;

  const wavFileName = `panchanga_trimmed_${dateString}.wav`;
  const jsonFileName = `panchanga_metadata_${dateString}.json`;

  const wav = new WaveFile();
  wav.fromScratch(1, 16000, '32f', finalPcm);
  fs.writeFileSync(wavFileName, wav.toBuffer());
  console.log(`Trimmed audio saved to ${wavFileName}`);

  filteredChunks.unshift({ fullText });
  fs.writeFileSync(jsonFileName, JSON.stringify(filteredChunks, null, 2));
  console.log(`Metadata saved to ${jsonFileName}`);
}

const getISTDate = () => new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));

async function run() {
  try {
    // 1. Generate text
    const { fullText } = generatePanchangaText();

    // 2. Fetch audio
    const audioRes = await fetchGeneratedAudio(fullText);

    // 3. Decode and resample
    const { pcmData } = await decodeAndResample(audioRes);

    // 4. Transcription
    const transcript = await transcribe(pcmData);

    // 5. Process, Crop, and Append Bell
    const { finalPcm, filteredChunks } = await processAndTrimAudio(transcript, pcmData);

    // 6. Save outputs
    saveOutputs(finalPcm, filteredChunks, fullText);

    console.log("Saved to storage successfully.");

  } catch (e) {
    console.error("Task failed:", e);
    process.exit(1);
  }
}

run();
