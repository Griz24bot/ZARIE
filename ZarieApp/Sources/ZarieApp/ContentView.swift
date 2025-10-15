import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Label("Dashboard", systemImage: "chart.bar")
                }
            ZarieGlyphView()
                .tabItem {
                    Label("Glyph", systemImage: "star.circle")
                }
        }
    }
}
