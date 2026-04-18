const { WaveFile } = require('wavefile');
const fs = require('fs');

/**
 * Mixes a speech audio file with a background music/ambience file.
 * Loops the background if it's shorter than the speech.
 */
const mixAudioWithBackground = (speechWavPath, musicWavPath, outputPath, musicVolume = 0.3) => {
  console.log(`Mixing ${speechWavPath} with background ambience...`);
  
  // Load both files
  const speechWav = new WaveFile(fs.readFileSync(speechWavPath));
  const musicWav = new WaveFile(fs.readFileSync(musicWavPath));

  // Convert both to 32f for mixing
  speechWav.toBitDepth('32f');
  musicWav.toBitDepth('32f');

  // Use the first channel for mixing (assume mono for processing)
  const speechSamples = speechWav.getSamples(false, Float32Array);
  const musicSamples = musicWav.getSamples(false, Float32Array);
  
  const speechData = Array.isArray(speechSamples) ? speechSamples[0] : speechSamples;
  const musicData = Array.isArray(musicSamples) ? musicSamples[0] : musicSamples;
  
  const sampleRate = speechWav.fmt.sampleRate;

  // Resample music to match speech sample rate if needed
  let finalMusicSamples = musicData;
  if (musicWav.fmt.sampleRate !== sampleRate) {
    console.log(` - Resampling background audio from ${musicWav.fmt.sampleRate}Hz to ${sampleRate}Hz`);
    const ratio = musicWav.fmt.sampleRate / sampleRate;
    const newLength = Math.round(musicData.length / ratio);
    finalMusicSamples = new Float32Array(newLength);
    for (let i = 0; i < newLength; i++) {
      finalMusicSamples[i] = musicData[Math.round(i * ratio)];
    }
  }

  // Mix — loop music if shorter than speech
  const mixed = new Float32Array(speechData.length);
  for (let i = 0; i < speechData.length; i++) {
    const musicSample = finalMusicSamples[i % finalMusicSamples.length] * musicVolume;
    mixed[i] = speechData[i] + musicSample;
  }

  // Normalize to prevent clipping
  let maxAbs = 0;
  for (let i = 0; i < mixed.length; i++) {
    const abs = Math.abs(mixed[i]);
    if (abs > maxAbs) maxAbs = abs;
  }

  if (maxAbs > 1.0) {
    console.log(` - Normalizing mixed audio (Max amplitude: ${maxAbs.toFixed(2)})`);
    for (let i = 0; i < mixed.length; i++) {
      mixed[i] /= maxAbs;
    }
  }

  // Save output
  const outWav = new WaveFile();
  outWav.fromScratch(1, sampleRate, '32f', mixed);
  fs.writeFileSync(outputPath, outWav.toBuffer());
  console.log(`   [AudioService] Mixed audio saved to: ${outputPath}`);
};

module.exports = {
  mixAudioWithBackground
};
