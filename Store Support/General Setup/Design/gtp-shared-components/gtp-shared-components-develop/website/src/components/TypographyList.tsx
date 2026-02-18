import ScreenshotTabs from './ScreenshotTabs';
export default function TypographyList({
  imageData,
  baseUrl = '/pages/electrode-mobile-platform/gtp-shared-components/',
}) {
  return (
    <div className="typography">
      <ScreenshotTabs
        screenshotData={`screenshots/${imageData}`}
        baseUrl={`${baseUrl}`}
      />
    </div>
  );
}
