import SwiftUI
import Charts

struct DashboardView: View {
    @StateObject private var viewModel = DashboardViewModel()

    var body: some View {
        VStack {
            LatencyTimelineView(data: viewModel.latencyData)
            OverrideLogView(logs: viewModel.overrideLogs)
            GlyphOverlayView(isBreach: viewModel.isBreachActive, isOverride: viewModel.isOverrideActive)
            VoiceLogView(voiceLogs: viewModel.voiceLogs)
        }
        .onAppear {
            viewModel.loadData()
        }
    }
}

struct LatencyTimelineView: View {
    let data: [LatencyDataPoint]

    var body: some View {
        Chart(data) { point in
            LineMark(
                x: .value("Time", point.timestamp),
                y: .value("Latency", point.value)
            )
            .foregroundStyle(point.isBreach ? .red : .blue)
        }
        .frame(height: 200)
        .padding()
    }
}

struct OverrideLogView: View {
    let logs: [OverrideLogEntry]

    var body: some View {
        List(logs) { log in
            VStack(alignment: .leading) {
                Text(log.proposal)
                Text("Outcome: \(log.outcome)")
                    .font(.caption)
            }
        }
    }
}

struct GlyphOverlayView: View {
    let isBreach: Bool
    let isOverride: Bool

    var body: some View {
        ZStack {
            if isBreach {
                Circle()
                    .fill(Color.red.opacity(0.5))
                    .frame(width: 100, height: 100)
                    .scaleEffect(isBreach ? 1.2 : 1.0)
                    .animation(.easeInOut(duration: 0.5), value: isBreach)
            }
            if isOverride {
                Circle()
                    .fill(Color.yellow.opacity(0.5))
                    .frame(width: 100, height: 100)
                    .scaleEffect(isOverride ? 1.2 : 1.0)
                    .animation(.easeInOut(duration: 0.5), value: isOverride)
            }
        }
    }
}

struct VoiceLogView: View {
    let voiceLogs: [VoiceLogEntry]

    var body: some View {
        List(voiceLogs) { log in
            Button(action: {
                // Play voice log
                print("Playing: \(log.text)")
            }) {
                Text(log.timestamp.formatted())
                Text(log.text)
                    .font(.caption)
            }
        }
    }
}

class DashboardViewModel: ObservableObject {
    @Published var latencyData: [LatencyDataPoint] = []
    @Published var overrideLogs: [OverrideLogEntry] = []
    @Published var voiceLogs: [VoiceLogEntry] = []
    @Published var isBreachActive: Bool = false
    @Published var isOverrideActive: Bool = false

    func loadData() {
        // Load data from storage or API
        // For demo purposes, using sample data
        latencyData = [
            LatencyDataPoint(timestamp: Date().addingTimeInterval(-3600), value: 150, isBreach: false),
            LatencyDataPoint(timestamp: Date().addingTimeInterval(-1800), value: 320, isBreach: true),
            LatencyDataPoint(timestamp: Date(), value: 180, isBreach: false)
        ]
        overrideLogs = [
            OverrideLogEntry(id: UUID(), proposal: "Switch mining pool to SovereignHash", outcome: "Approved")
        ]
        voiceLogs = [
            VoiceLogEntry(id: UUID(), timestamp: Date(), text: "Override protocol Z-7 initiated...")
        ]
    }
}

struct LatencyDataPoint: Identifiable {
    let id = UUID()
    let timestamp: Date
    let value: Double
    let isBreach: Bool
}

struct OverrideLogEntry: Identifiable {
    let id: UUID
    let proposal: String
    let outcome: String
}

struct VoiceLogEntry: Identifiable {
    let id: UUID
    let timestamp: Date
    let text: String
}
