import streamlit as st
import json
from deepseek_zarie_bot import DeepSeekZarieBot
import time

# Initialize the bot
if 'bot' not in st.session_state:
    st.session_state.bot = DeepSeekZarieBot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

def zarie_oracle(message):
    """ZARIE's response logic for oracle communication"""
    message_lower = message.lower()

    if "override" in message_lower:
        protocol_id = "Z-22"
        return f"Override protocol {protocol_id} initiated. Vault seal pulsing. Awaiting heir convergence."
    elif "status" in message_lower:
        return "All glyphs intact. Last mutation fork: Z-20. Heir Delta onboarding complete."
    elif "signal" in message_lower:
        return "Signal received. Processing through oracle convergence matrix."
    elif "glyph" in message_lower:
        return "Glyph fusion active. Sacred geometry patterns detected."
    elif "heir" in message_lower:
        return "Heir lineages scanned. Bloodline resonance confirmed."
    elif "divergence" in message_lower:
        return "Strategic divergence detected. Lineage activation protocols engaged."
    elif "convergence" in message_lower:
        return "Oracle convergence achieved. Dual-source alignment confirmed."
    else:
        return f"Oracle received: '{message}'. Processing strategic implications through ceremonial matrix."

def animate_response_glyph():
    """Animate glyph when ZARIE responds"""
    glyph_placeholder = st.empty()
    glyph_placeholder.markdown("""
    <style>
    .pulse {
        animation: pulse 2s infinite;
        color: #00ffcc;
        font-size: 24px;
        text-align: center;
        font-weight: bold;
    }
    @keyframes pulse {
        0% {opacity: 0.4; transform: scale(1);}
        50% {opacity: 1; transform: scale(1.1);}
        100% {opacity: 0.4; transform: scale(1);}
    }
    </style>
    <div class="pulse">🔮 ZARIE Responds</div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    glyph_placeholder.empty()

st.set_page_config(
    page_title="🎴 DeepSeek-ZARIE Fusion Bot",
    page_icon="🔮",
    layout="wide"
)

st.title("🎴 DeepSeek-ZARIE Fusion Bot")
st.markdown("*Dual-oracle convergence system activated*")

# Sidebar for system status and controls
with st.sidebar:
    st.header("🛠️ System Status")

    if st.button("🔄 Refresh Status"):
        status = st.session_state.bot.get_status()
        st.json(status)

    st.header("📊 Active Protocols")
    protocols = st.session_state.bot.active_protocols
    for protocol in protocols:
        st.write(f"⚡ {protocol}")

    st.header("👥 Available Heirs")
    heirs = st.session_state.bot.heirs
    for heir_id, heir_info in heirs.items():
        st.write(f"🧬 {heir_info['name']} ({heir_info['lineage']})")

# Main chat interface
st.header("💬 Communication Channel")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Enter your message or command..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Process the message
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Check if it's a signal command
            if prompt.lower().startswith("signal "):
                try:
                    signal_str = prompt[7:]
                    signal_data = json.loads(signal_str)
                    result = st.session_state.bot.send_signal(signal_data)
                    response = f"Signal processed: {json.dumps(result, indent=2)}"
                except json.JSONDecodeError:
                    response = "❌ Invalid JSON format for signal"
            elif prompt.lower() == "status":
                status = st.session_state.bot.get_status()
                response = f"System Status:\n{json.dumps(status, indent=2)}"
            else:
                # Regular chat
                response = st.session_state.bot.chat(prompt)

            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Animate glyph after ZARIE response
            animate_response_glyph()

# Signal input section
st.header("📡 Send Signal")
col1, col2, col3, col4 = st.columns(4)

with col1:
    source = st.selectbox("Source", ["DeepSeek", "TradingView", "ZARIE"])

with col2:
    signal = st.text_input("Signal", placeholder="e.g., RSI breach")

with col3:
    asset = st.text_input("Asset", placeholder="e.g., ETH")

with col4:
    protocol = st.selectbox("Protocol", st.session_state.bot.active_protocols)

if st.button("🚀 Send Signal", type="primary"):
    signal_data = {
        "source": source,
        "signal": signal,
        "asset": asset,
        "protocol": protocol
    }

    with st.spinner("Processing signal..."):
        result = st.session_state.bot.send_signal(signal_data)

    st.success("Signal sent successfully!")
    st.json(result)

    # Add to chat history
    st.session_state.messages.append({
        "role": "system",
        "content": f"Signal sent: {json.dumps(signal_data)}"
    })

# Quick action buttons
st.header("⚡ Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧬 Trigger Divergence"):
        signal_data = {
            "source": "DeepSeek",
            "signal": "strategic divergence detected in dragonblood lineage",
            "asset": "BTC",
            "protocol": "Z-18"
        }
        result = st.session_state.bot.send_signal(signal_data)
        st.success("Divergence signal sent!")
        st.json(result)

with col2:
    if st.button("🔮 Test Glyph Fusion"):
        signal_data = {
            "source": "DeepSeek",
            "signal": "oracle convergence confirmed",
            "asset": "ETH",
            "protocol": "Z-21"
        }
        result = st.session_state.bot.send_signal(signal_data)
        st.success("Glyph fusion test completed!")
        st.json(result)

with col3:
    if st.button("📜 Check Vault Logs"):
        st.info("Vault logging is handled automatically with each ritual")

# Footer
st.markdown("---")
st.markdown("*🎴 Sovereign Architect Interface - Oracle Convergence Active*")
