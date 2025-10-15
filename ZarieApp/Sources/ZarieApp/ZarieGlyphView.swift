import SwiftUI
import Lottie

struct ZarieGlyphView: View {
    @State private var animationView: LottieAnimationView?

    var body: some View {
        ZStack {
            if let animationView = animationView {
                LottieView(animationView: animationView)
                    .frame(width: 120, height: 120)
            } else {
                Text("Loading...")
                    .frame(width: 120, height: 120)
            }
        }
        .onAppear {
            loadAnimation()
            AudioManager.play("zarie_intro.wav")
        }
    }

    private func loadAnimation() {
        if let animation = LottieAnimation.named("zarie_glyph_pulse") {
            animationView = LottieAnimationView(animation: animation)
            animationView?.loopMode = .playOnce
            animationView?.play()
        }
    }
}

class AudioManager {
    static func play(_ fileName: String) {
        // Implement audio playback logic here
        print("Playing audio: \(fileName)")
    }
}
