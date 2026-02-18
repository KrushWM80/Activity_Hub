# Language Translation Package - Refresh Touring Guide

This folder contains all files related to the internationalization (i18n) implementation for the Refresh Touring Guide application.

## 📁 Contents

### `/locales/`
- `en-US.json` - English (United States) translations
- `es-MX.json` - Spanish (Mexico) translations  
- `zh-CN.json` - Mandarin (China) translations

### `/components/`
- `LanguageSwitcher.tsx` - Language selector component

### `/config/`
- `i18n.ts` - i18next configuration

### `/docs/`
- `LANGUAGE_TRANSLATION.md` - Complete implementation guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install react-i18next i18next i18next-browser-languagedetector --legacy-peer-deps
```

### 2. Copy Files to Your Project

**Locale Files:**
```
client/src/locales/
├── en-US.json
├── es-MX.json
└── zh-CN.json
```

**i18n Configuration:**
```
client/src/i18n.ts
```

**Language Switcher Component:**
```
client/src/components/LanguageSwitcher/LanguageSwitcher.tsx
```

### 3. Initialize i18n in App.tsx
```tsx
import './i18n';  // Import at the top of App.tsx
```

### 4. Add Language Switcher to Header
```tsx
import LanguageSwitcher from './components/LanguageSwitcher/LanguageSwitcher';

// In your header/navbar component:
<LanguageSwitcher />
```

## 📖 Usage in Components

```tsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('dashboard.title')}</h1>
      <p>{t('dashboard.welcome', { name: 'John' })}</p>
    </div>
  );
}
```

## 🌍 Supported Languages

- **English (US)** - `en-US` - Base/Fallback language
- **Spanish (Mexico)** - `es-MX`
- **Mandarin (China)** - `zh-CN`

## 📚 Documentation

See `docs/LANGUAGE_TRANSLATION.md` for complete implementation details, including:
- Adding new translations
- Adding new languages
- Testing strategies
- Walmart-specific localization guidelines

## 🔧 Configuration

The i18n configuration includes:
- Automatic language detection from localStorage and browser
- Fallback to English (en-US)
- React Suspense support
- Debug mode in development

## 📦 Package Requirements

```json
{
  "react-i18next": "^13.0.0",
  "i18next": "^23.0.0",
  "i18next-browser-languagedetector": "^7.0.0"
}
```

## 🎯 Features

- ✅ 3 languages supported
- ✅ Automatic language detection
- ✅ Persistent language selection
- ✅ Fallback to English
- ✅ Mobile-responsive switcher
- ✅ Flag emojis for visual identification
- ✅ Dynamic interpolation support

## 📝 Notes

- All translation keys use dot notation (e.g., `dashboard.title`)
- Variables in translations use double curly braces `{{variable}}`
- New strings should be added to `en-US.json` first
- Language preference is stored in `localStorage`

## 🤝 Contributing

When adding new translations:
1. Add the key to `en-US.json` first
2. Translate to all other language files
3. Use the `t()` function in components
4. Test all languages before committing

---

**Last Updated:** November 20, 2025  
**Version:** 3.0.0
