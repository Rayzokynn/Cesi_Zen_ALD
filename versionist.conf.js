const fs = require('fs');
const path = require('path');

module.exports = {
  // Récupère la version actuelle depuis le package.json du frontend
  getCurrentBaseVersion: () => {
    const pkgPath = path.join(__dirname, 'Cesi_Zen_Front/CesiZen/package.json');
    if (fs.existsSync(pkgPath)) {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      return pkg.version || '0.2.0';
    }
    return '0.2.0';
  },

  // Détermine le niveau d'incrément en fonction du commit
  getIncrementLevelFromCommit: (commit) => {
    // Si le sujet contient "major" ou "breaking" -> Incrément Majeur (X)
    if (commit.subject.match(/major/i) || commit.subject.match(/breaking/i)) {
      return 'major';
    }
    // Si le sujet commence par "feat" ou "add" -> Incrément Mineur (Y)
    if (commit.subject.match(/^(feat|add)/i)) {
      return 'minor';
    }
    // Par défaut, incrément correctif / patch (Z)
    return 'patch';
  },

  // Incrémentation personnalisée au format Major.Minor.Patch (ex: 0.2.0 -> 0.2.1)
  incrementVersion: (version, incrementLevel) => {
    const parts = version.split('.');
    const major = parseInt(parts[0], 10) || 0;
    const minor = parseInt(parts[1], 10) || 0;
    const patch = parseInt(parts[2], 10) || 0;

    if (incrementLevel === 'major') {
      return `${major + 1}.0.0`;
    } else if (incrementLevel === 'minor') {
      return `${major}.${minor + 1}.0`;
    }
    return `${major}.${minor}.${patch + 1}`;
  },

  // Écrit la nouvelle version dans le package.json du frontend
  updateVersion: (cwd, version, callback) => {
    const pkgPath = path.join(cwd, 'Cesi_Zen_Front/CesiZen/package.json');
    if (fs.existsSync(pkgPath)) {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      pkg.version = version;
      fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n');
    }
    callback();
  }
};
