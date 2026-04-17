const admin = require('firebase-admin');
const path = require('path');

// Initialize Firebase Admin using the service account in the root directory
const serviceAccountPath = path.resolve(__dirname, '../bhaarathverse-90a6480c00b5.json');
const serviceAccount = require(serviceAccountPath);

if (!admin.apps.length) {
  if (process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    // CI / production — use ADC via the env var set by the auth step
    admin.initializeApp({
      credential: admin.credential.applicationDefault(),
      projectId: 'bhaarathverse'
    });
  } else {
    // Local development — use the local key file
    const serviceAccount = require('../bhaarathverse-90a6480c00b5.json');
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });
  }
}

const db = admin.firestore();
const bhaarathverseDb = db;

/**
 * Fail-fast check to verify Firestore write permissions
 */
async function testFirestoreConnectivity() {
  console.log("Testing Firestore connectivity...");
  const testPath = `_connectivity_test/node_script_${Date.now()}`;
  try {
    await db.doc(testPath).set({ timestamp: admin.firestore.FieldValue.serverTimestamp() });
    await db.doc(testPath).delete();
    console.log("Firestore connectivity check: SUCCESS");
  } catch (err) {
    console.error(`[CRITICAL] Firestore connectivity check FAILED for path: ${testPath}`);
    console.error("Please verify that the service account has the 'Cloud Datastore User' role.");
    throw err;
  }
}

/**
 * Granularly submits sync data with path-level error logging
 */
async function submitSync({ syncMode, dateId, timeMap, activeText, transliterateMapFn, langList }) {
  console.log(`Submitting sync for ${dateId} (${syncMode})...`);
  const syncDataStr = JSON.stringify(timeMap);

  const payload = {
    dateId,
    syncData: syncDataStr,
    text: activeText,
    updatedAt: admin.firestore.FieldValue.serverTimestamp(),
  };

  const safeSet = async (dbInstance, path, data) => {
    try {
      const docRef = dbInstance.doc(path);
      await docRef.set(data, { merge: true });
    } catch (err) {
      console.error(`[ERROR] Failed to write to path: ${path}`);
      throw err;
    }
  };

  // 1. Legacy master field
  const masterPath = `sankalpaMaster/${dateId}`;
  await safeSet(db, masterPath, {
    [syncMode === 'word' ? 'syncData' : 'letterSyncData']: syncDataStr,
  });
  console.log(`   [Firebase] Updated legacy master doc: ${masterPath}`);

  // 2. Per-language transliterated maps
  const promises = langList.map(async (langCode) => {
    const transliteratedMap = transliterateMapFn(timeMap, langCode);

    // sankalpaMaster/{dateId}/{syncMode}Sync/{langCode}
    const variantPath = `sankalpaMaster/${dateId}/${syncMode}Sync/${langCode}`;
    await safeSet(db, variantPath, transliteratedMap);
    console.log(`   [Firebase] Updated language variant: ${variantPath}`);

    // userLibrary mirrors
    if (syncMode === 'word') {
      if (langCode === 'sa') {
        const path = `userLibrary/sa/sankalpaMantra/${dateId}/syncData/wordSync`;
        await safeSet(db, path, {
          ...payload,
          syncData: JSON.stringify(transliteratedMap)
        });
        console.log(`   [Firebase] Updated userLibrary mirror (sa): ${path}`);
      } else {
        const path = `userLibrary/${langCode}/sankalpaMantra/${dateId}/syncData/wordSync`;
        await safeSet(bhaarathverseDb, path, {
          ...payload,
          syncData: JSON.stringify(transliteratedMap)
        });
        console.log(`   [Firebase] Updated userLibrary mirror (${langCode}): ${path}`);
      }
    }
  });

  await Promise.all(promises);
}

module.exports = {
  db,
  bhaarathverseDb,
  testFirestoreConnectivity,
  submitSync
};
