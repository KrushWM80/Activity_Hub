import React from 'react';
import { IconButton, Menu, MenuItem, Box, Typography } from '@mui/material';
import { Language as LanguageIcon } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const languages = [
    { code: 'en-US', name: 'English', flag: '🇺🇸' },
    { code: 'es-MX', name: 'Español', flag: '🇲🇽' },
    { code: 'zh-CN', name: '中文', flag: '🇨🇳' },
  ];

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLanguageChange = (languageCode: string) => {
    i18n.changeLanguage(languageCode);
    localStorage.setItem('i18nextLng', languageCode);
    handleClose();
  };

  return (
    <Box>
      <IconButton
        color="inherit"
        onClick={handleClick}
        sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
      >
        <LanguageIcon />
        <Box sx={{ display: { xs: 'none', sm: 'flex' }, alignItems: 'center', gap: 0.5 }}>
          <Typography variant="body2">{currentLanguage.flag}</Typography>
          <Typography variant="body2" sx={{ fontSize: '0.875rem' }}>
            {currentLanguage.name}
          </Typography>
        </Box>
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          sx: {
            mt: 1.5,
            minWidth: 180
          }
        }}
      >
        {languages.map((language) => (
          <MenuItem
            key={language.code}
            onClick={() => handleLanguageChange(language.code)}
            selected={i18n.language === language.code}
            sx={{
              display: 'flex',
              gap: 1.5,
              py: 1.5
            }}
          >
            <Typography variant="body1" sx={{ fontSize: '1.25rem' }}>
              {language.flag}
            </Typography>
            <Typography variant="body2">
              {language.name}
            </Typography>
          </MenuItem>
        ))}
      </Menu>
    </Box>
  );
};

export default LanguageSwitcher;
