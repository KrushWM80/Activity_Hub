import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import enUS from './locales/en-US.json';
import esMX from './locales/es-MX.json';
import zhCN from './locales/zh-CN.json';

// Initialize i18next
i18n
  // Detect user language
  .use(LanguageDetector)
  // Pass the i18n instance to react-i18next
  .use(initReactI18next)
  // Initialize i18next
  .init({
    // Resources for each locale
    resources: {
      'en-US': {
        translation: enUS
      },
      'es-MX': {
        translation: esMX
      },
      'zh-CN': {
        translation: zhCN
      }
    },
    // Fallback language
    fallbackLng: 'en-US',
    // Default namespace
    defaultNS: 'translation',
    // Debug mode (set to false in production)
    debug: process.env.NODE_ENV === 'development',
    // Interpolation options
    interpolation: {
      escapeValue: false, // React already escapes values
    },
    // Detection options
    detection: {
      // Order of detection methods
      order: ['localStorage', 'navigator', 'htmlTag'],
      // Cache user language
      caches: ['localStorage'],
      // localStorage key
      lookupLocalStorage: 'i18nextLng',
    },
    // React options
    react: {
      useSuspense: true,
    },
  });

export default i18n;
