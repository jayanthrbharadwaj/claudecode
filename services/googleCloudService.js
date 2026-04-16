const axios = require('axios');
const fs = require('fs');
const { execSync } = require('child_process');
const textToSpeech = require('@google-cloud/text-to-speech');
const speech = require('@google-cloud/speech');

const speechClient = new speech.SpeechClient();

/**
 * Synthesizes speech from the input text using Google Cloud TTS (Gemini models)
 */
const synthesize = async (prompt, text, outputFilePath = 'output.wav') => {
  let token;
  try {
    token = process.env.GOOGLE_ACCESS_TOKEN || execSync('gcloud auth print-access-token').toString().trim();
  } catch (err) {
    if (process.env.GOOGLE_ACCESS_TOKEN) {
      token = process.env.GOOGLE_ACCESS_TOKEN;
    } else {
      console.error("Failed to retrieve auth token. Ensure gcloud is installed or GOOGLE_ACCESS_TOKEN is set.");
      throw err;
    }
  }

  console.log("Synthesizing audio with Google Cloud TTS...");
  const response = await axios.post(
    'https://us-central1-texttospeech.googleapis.com/v1beta1/text:synthesize',
    {
      input: { prompt, text },
      voice: {
        languageCode: 'kn-IN',
        name: 'Algenib',
        model_name: 'gemini-2.5-flash-tts',
      },
      audioConfig: {
        audioEncoding: 'LINEAR16',
        speakingRate: 0.80,
        sampleRateHertz: 16000
      },
    },
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'x-goog-user-project': 'bhaarathverse',
        'Content-Type': 'application/json',
      }
    }
  );

  const audioBuffer = Buffer.from(response.data.audioContent, 'base64');
  fs.writeFileSync(outputFilePath, audioBuffer);
  console.log(`Audio saved to ${outputFilePath}`);
};

/**
 * Transcription using Google Cloud Speech-to-Text for best accuracy & timestamps
 */
const transcribeWithTimestamps = async (wavPath) => {
  console.log("Transcribing with Google Cloud Speech-to-Text...");
  const audioBytes = fs.readFileSync(wavPath).toString('base64');

  const request = {
    audio: { content: audioBytes },
    config: {
      encoding: 'LINEAR16',
      languageCode: 'kn-IN',
      sampleRateHertz: 16000,
      enableWordTimeOffsets: true,
    },
  };

  const [response] = await speechClient.recognize(request);
  const words = response.results
    .flatMap(r => r.alternatives[0].words)
    .map(w => ({
      text: w.word,
      start: parseFloat(w.startTime.seconds) + (w.startTime.nanos / 1e9),
      end: parseFloat(w.endTime.seconds) + (w.endTime.nanos / 1e9),
    }));

  console.log(`   [Speech-to-Text] Detected ${words.length} words.`);
  return words;
}

module.exports = {
  synthesize,
  transcribeWithTimestamps
};
