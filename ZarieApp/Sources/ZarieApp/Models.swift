import Foundation

struct LatencyBreachEvent: Codable {
    let timestamp: Date
    let event: String
    let metric: String
    let value: Double
    let overrideTriggered: Bool
    let protocol: String
}

struct OverrideProposal: Codable {
    let id: UUID
    let timestamp: Date
    let proposal: String
    let votes: [Vote]
    let outcome: String?
}

struct Vote: Codable {
    let heirId: String
    let decision: Bool // true for approve, false for reject
    let timestamp: Date
}

struct VoiceDeclaration: Codable {
    let id: UUID
    let timestamp: Date
    let text: String
    let audioFileName: String?
}
