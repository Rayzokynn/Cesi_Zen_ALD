import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.ionic.starter', // (Garde ce que tu as déjà)
  appName: 'CesiZen',        // (Garde ce que tu as déjà)
  webDir: 'www',
  server: {
    cleartext: true,
    androidScheme: 'http'
  }
};

export default config;