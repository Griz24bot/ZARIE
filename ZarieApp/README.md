# ZARIE iOS App

An iOS app built with SwiftUI and Lottie animations that integrates with Siri for mining pool override votes.

## Features

- **ZarieGlyphView**: Displays a Lottie animation that pulses when Siri triggers mining or override intents.
- **Siri Integration**: Uses SiriKit to handle "Initiate Override Vote" intents.
- **Dashboard**: Visualizes latency breaches, override history, and voice logs.
- **Voice Synthesis**: ZARIE speaks override proposals and collects votes.

## Setup

1. Clone the repository
2. Open `Package.swift` in Xcode
3. Add your Lottie animation file `zarie_glyph_pulse.json` to the project
4. Build and run

## Siri Integration

To enable Siri integration:
1. Add Siri capability to your app in Xcode
2. Configure the `InitiateOverrideVoteIntent` in your app's intents definition file
3. Train Siri with phrases like "Hey Siri, initiate override"

## Dependencies

- Lottie-iOS: For animations
- Swift Algorithms: For data processing

## Sample Data

The app includes sample latency breach data and override logs for demonstration purposes.
