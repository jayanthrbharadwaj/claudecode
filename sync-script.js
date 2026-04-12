const admin = require('firebase-admin');
const axios = require('axios');

const serviceAccount = JSON.parse(process.env.FIREBASE_CONFIG);
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: `${serviceAccount.project_id}.appspot.com`
});

async function run() {
  try {
    // 1. Hit the API
    const response = await axios.post('https://yourvoic.com', {
      text: "उत्तरायणे...", // Your full Sanskrit text here
      voice: "Fenrir",
      language: "sa"
    }, {
      headers: { "Content-Type": "application/json", "User-Agent": "Mozilla/5.0..." }
    });

    const audioUrl = response.data.url; // Adjust based on actual key

    // 2. Save JSON to Firestore
    const docRef = await admin.firestore().collection('generations').add({
      ...response.data,
      timestamp: admin.firestore.FieldValue.serverTimestamp()
    });

    // 3. Download and Save to Storage
    if (audioUrl) {
      const audioRes = await axios.get(audioUrl, { responseType: 'arraybuffer' });
      const bucket = admin.storage().bucket();
      const file = bucket.file(`audio/${docRef.id}.mp3`);
      
      await file.save(Buffer.from(audioRes.data), {
        metadata: { contentType: 'audio/mpeg' }
      });
      console.log("Saved to storage successfully.");
    }
  } catch (e) {
    console.error("Task failed:", e);
    process.exit(1);
  }
}
run();
