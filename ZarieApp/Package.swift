// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "ZarieApp",
    platforms: [
        .iOS(.v16)
    ],
    products: [
        .library(name: "ZarieApp", targets: ["ZarieApp"])
    ],
    dependencies: [
        .package(url: "https://github.com/airbnb/lottie-ios.git", from: "4.0.0"),
        .package(url: "https://github.com/apple/swift-algorithms.git", from: "1.0.0")
    ],
    targets: [
        .target(
            name: "ZarieApp",
            dependencies: [
                "Lottie",
                .product(name: "Algorithms", package: "swift-algorithms")
            ],
            path: "Sources/ZarieApp"
        )
    ]
)
