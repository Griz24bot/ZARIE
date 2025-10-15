import SwiftUI

@main
struct ZarieApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    zarie.speak("Welcome, Sovereign Architect. This vessel is now live.")
                    dashboard.animate("glyph_arrival_pulse", target: "vault_seal")
                }
        }
    }
}
