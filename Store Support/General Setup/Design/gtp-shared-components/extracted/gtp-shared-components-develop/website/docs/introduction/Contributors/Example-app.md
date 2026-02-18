---
sidebar_position: 3
---

# Example app

The current `example/` folder contains a standalone showcase app.

Before you run the app for the first time, please refer to the [Setup page](./Setup.md) for instructions on how to set up your local development environment.

Running the example app should start a Metro bundler automatically, which will be spawned in a Terminal during the build. If this is not the case, run `yarn start --reset-cache` in a separate terminal to start one.

## Run the example app

### Android

- Ensure [Android Studio 3+][1] is installed and an [emulator is set up][2]
- Alternatively, you can run the app on a USB tethered device

  - connect the device via USB
  - run `adb devices` to make sure the device is mounted and visible to adb

    ```bash
    adb devices
    List of devices attached
    R58M404T6DM     device
    ```

  - you can project the device screen on the laptop via `scrcpy`

    ```bash
    brew install scrcpy
    scrcpy -t &
    ```

  - make sure you have accepted all licenses:

    ```bash
    $ANDROID_SDK/tools/bin/sdkmanager --licenses
    ```

    where $ANDROID_SDK is a variable that points to your SDK installation e.g. `/Users/a0b0ccc/Library/Android/sdk`

  - Install dependencies

    ```bash npm2yarn
    nvm install
    npm install
    cd example
    npm install
    cd ..
    ```

  Open the device in an iOS simulator
  ```bash npm2yarn
  npm run android
  ```
  OR
  - open the `android` folder in Android Studio (`studio android/`)

### iOS

- Ensure [Xcode 12+][3] is installed
- Install dependencies

  ```bash npm2yarn
  nvm install
  npm install
  cd example
  npm install
  pod install
  cd ..
  ```

Open the device in an iOS simulator
```bash npm2yarn
npm run ios
```
OR
- open the `ios` folder in Xcode (`xed ios/`), select the simulator and click the Run button

- Alternatively, you can run the app on an iOS tethered device
  - Enable Developer Mode, by following these instructions: https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device
  - Follow the instructions for running the app on the React Native docs: https://reactnative.dev/docs/running-on-device?platform=ios
  - If you get an error while configuring code signing: "The app identifier xxx cannot be registered to your development team because it is not available. Change your bundle identifier to a unique string to try again."
    - Change the Bundle Identifier by adding a few random alphanumeric characters at the end to make it unique.
  - If you get an error while building: "Untrusted Developer: Your device management do not allow using apps from developer on this iPhone/iPad."
    - On your device, go to Settings -> General -> VPN & Device Management. Under Developer App, select your profile and tap "Trust."
  - While running the the app for the first time, you may get a popup "LDRNEXample would like to find and connect to devices on your local network. "This app will be able to discover and connect to devices on the network you use.".
    - Click Allow
  - If the running app is not connecting to the metro bundler (the terminal that was opened during the build), disconnect from the Walmart VPN and make sure your iOS device and computer are on the same Wifi network.

[1]: https://developer.android.com/studio/index.html#downloads
[2]: https://developer.android.com/studio/run/emulator.html
[3]: https://developer.apple.com/xcode/
