const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');

function loadProverbsByFidel(fidelLetter, skip = 0, limit = 100) {
  const filePath = path.join(dataDir, `${fidelLetter.trim()}.json`);
  if (!fs.existsSync(filePath)) return [];

  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(fileContent);
    if (Array.isArray(data)) {
      return data.slice(skip, skip + limit);
    }
    return [];
  } catch (error) {
    return [];
  }
}

function loadAllProverbs(skip = 0, limit = 100) {
  if (!fs.existsSync(dataDir)) return [];

  let allProverbs = [];
  const files = fs.readdirSync(dataDir);

  files.forEach(file => {
    if (file.endsWith('.json')) {
      const filePath = path.join(dataDir, file);
      try {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const data = JSON.parse(fileContent);
        if (Array.isArray(data)) {
          allProverbs = allProverbs.concat(data);
        }
      } catch (error) {
        // Skip unreadable files
      }
    }
  });

  return allProverbs.slice(skip, skip + limit);
}

function getRandomProverb() {
  const proverbs = loadAllProverbs(0, 100000);
  if (proverbs.length === 0) return null;
  return proverbs[Math.floor(Math.random() * proverbs.length)];
}

function searchProverbs(query, limit = 50) {
  const lowerQuery = query.toLowerCase();
  const proverbs = loadAllProverbs(0, 100000);
  const results = [];

  for (const p of proverbs) {
    if (
      p.proverb_amharic?.toLowerCase().includes(lowerQuery) ||
      p.proverb_english?.toLowerCase().includes(lowerQuery) ||
      p.category?.toLowerCase().includes(lowerQuery)
    ) {
      results.push(p);
      if (results.length >= limit) break;
    }
  }
  return results;
}

module.exports = {
  loadProverbsByFidel,
  loadAllProverbs,
  getRandomProverb,
  searchProverbs
};
