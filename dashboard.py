import streamlit as st
import requests
import time
import os

# Wallets
wallets = {
    "ETH": "0xA1b2C3D4E5F678901234567890abcdef12345678",
    "KASPA": "kaspa:qq1234567890abcdef"
}

# Telegram config (set these in environment variables)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7575096974:AAGn1yVwkaNbsNFYHkz6cvPq6crAWkMaoeE")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id_here")

# Access control
approved_emails = ["andregrizzlejr@gmail.com"]
pending_requests = ["heir1@example.com", "heir2@example.com"]

def check_access(user_email):
    if user_email in approved_emails:
        return True
    else:
        st.error("Access denied. Awaiting sovereign approval.")
        return False

def approve_email(email):
    approved_emails.append(email)
    zarie_speak(f"Access granted to {email}. Lineage encoded.")
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Access Approved - {{'email': '{email}'}}")

# Bots monitoring
bots = {
    "kaspa_bot": {"status": "active", "coin": "KASPA", "latency": 142, "pool": "KaspaPool.io", "wallet": wallets["KASPA"]},
    "eth_bot": {"status": "active", "coin": "ETH", "latency": 98, "pool": "Ethermine.org", "wallet": wallets["ETH"]}
}

# ZARIE speak
def zarie_speak(message):
    st.markdown(f"**ZARIE:** {message}")
    send_telegram_alert(f"⚠️ {message}")

# Trigger override
def trigger_override(protocol_id):
    st.markdown(f"Animating glyph_override_{protocol_id} on vault_seal", unsafe_allow_html=True)
    zarie_speak(f"Override protocol {protocol_id} initiated. Heirs summoned.")
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Override Trigger - {{'protocol': '{protocol_id}'}}")

# Fetch Ethermine stats
def fetch_eth_stats(wallet):
    try:
        url = f"https://api.ethermine.org/miner/{wallet}/dashboard"
        response = requests.get(url).json()
        stats = response["data"]["currentStatistics"]
        return stats
    except Exception as e:
        st.error(f"Error fetching ETH stats: {e}")
        return None

# Fetch KASPA stats
def fetch_kaspa_stats(wallet):
    try:
        url = f"https://api.kaspa-pool.io/api/wallet/{wallet}"
        response = requests.get(url).json()
        return {
            "hashrate": response.get("hashrate", 0),
            "balance": response.get("balance", 0),
            "workers": response.get("workers", 0)
        }
    except Exception as e:
        st.error(f"Error fetching KASPA stats: {e}")
        return {"hashrate": 0, "balance": 0, "workers": 0}

# Send Telegram alert
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        st.error(f"Error sending Telegram alert: {e}")

# Narrate event
def narrate_event(event):
    if event == "payout":
        message = "KASPA payout received. Vault updated. Glyph pulsed."
    elif event == "vote":
        message = "Reinvestment vote initiated. Override protocol Z-16 active."
    elif event == "breach":
        message = "Sovereign breach: latency spike detected. Override protocol Z-16 initiated."
    else:
        message = f"Event: {event}"
    st.markdown(f"**ZARIE:** {message}")
    send_telegram_alert(f"⚠️ {message}")

# Glyph animation SVG
def glyph_animation():
    return """
<svg width="200" height="200">
  <path d="M10 80 C 40 10, 65 10, 95 80 S 150 150, 180 80"
        stroke="gold" fill="transparent" stroke-width="4">
    <animate attributeName="stroke-dashoffset" from="1000" to="0" dur="2s" repeatCount="1" />
  </path>
</svg>
"""

# Animate glyph convergence
def animate_glyph_convergence(protocol_id):
    layers = ["pulse", "trail", "ripple", "seal"]
    for layer in layers:
        st.markdown(f"Animating {protocol_id}_{layer} on vault_seal", unsafe_allow_html=True)
        time.sleep(0.4)
    narrate_event(f"Glyph convergence complete. Protocol {protocol_id} sealed.")
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Glyph Convergence - {{'protocol': '{protocol_id}'}}")

# Onboard heir
def onboard_heir(heir_id, lineage):
    st.markdown(f"Animating glyph_scroll_{lineage} on heir_panel", unsafe_allow_html=True)
    narrate_event(f"Welcome, heir {heir_id}. You are bound to lineage {lineage}.")
    # Play doctrine (placeholder)
    st.markdown(f"Playing doctrine: intro_{lineage}")
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Heir Onboarded - {{'heir': '{heir_id}', 'lineage': '{lineage}'}}")

# Animate lineage scroll
def animate_lineage_scroll(heir_id, lineage):
    glyph = f"glyph_scroll_{lineage}"
    st.markdown(f"Animating {glyph} on heir_panel", unsafe_allow_html=True)
    zarie_speak(f"Welcome, heir {heir_id}. Lineage {lineage} scroll activated.")
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Heir Onboarded - {{'heir': '{heir_id}', 'lineage': '{lineage}'}}")

# Declare breach recovery
def declare_breach_recovery(reason):
    zarie_speak(f"Breach resolved: {reason}. Vault seal restored. Cycle resumed.")
    st.markdown("Animating glyph_reboot_pulse on vault_seal", unsafe_allow_html=True)
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Breach Recovery - {{'reason': '{reason}'}}")

# Declare mutation fork
def declare_mutation_fork(fork_id, strategy):
    zarie_speak(f"Mutation fork {fork_id} initiated. Strategic shift: {strategy}. Heirs, prepare to vote.")
    st.markdown(f"Animating glyph_mutation_{fork_id} on vote_panel", unsafe_allow_html=True)
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Mutation Fork - {{'fork': '{fork_id}', 'strategy': '{strategy}'}}")

# Animate glyph fusion
def animate_glyph_fusion(protocol_id, heirs):
    for heir in heirs:
        st.markdown("Animating glyph_vote_green_trail on vault_seal", unsafe_allow_html=True)
        time.sleep(0.3)
    st.markdown("Animating glyph_fusion_core on vault_seal", unsafe_allow_html=True)
    zarie_speak(f"Glyph fusion complete. Protocol {protocol_id} sealed by unanimous override.")
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Glyph Fusion - {{'protocol': '{protocol_id}', 'heirs': {heirs}}}")

# Declare veto
def declare_veto(protocol_id, reason):
    zarie_speak(f"Proposal rejected. Oracle veto enacted. Protocol {protocol_id} sealed with null glyph.")
    st.markdown("Animating glyph_veto_flash on vote_panel", unsafe_allow_html=True)
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Veto Enacted - {{'protocol': '{protocol_id}', 'reason': '{reason}'}}")

# Declare reinvestment ritual
def declare_reinvestment(coin, amount, strategy):
    zarie_speak(f"Vault threshold breached: {amount:.4f} {coin}. Reinvestment ritual initiated. Strategy: {strategy}.")
    st.markdown("Animating glyph_reinvest_trigger on vault_seal", unsafe_allow_html=True)
    # Log to vault (placeholder)
    st.markdown(f"Vault logged: Reinvestment Ritual - {{'coin': '{coin}', 'amount': {amount}, 'strategy': '{strategy}'}}")

# Access check (placeholder - in real app, get from session)
user_email = "andregrizzlejr@gmail.com"  # Placeholder
if not check_access(user_email):
    st.stop()

# Layout
st.set_page_config(page_title="Sovereign Bot Monitor", layout="wide")
st.title("🛡️ Sovereign Mining Bot Dashboard")

# Bot Monitoring Panel
st.subheader("🛠️ Bot Monitoring")
for bot_name, bot_data in bots.items():
    st.markdown(f"**{bot_name}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Status", bot_data["status"])
    with col2:
        st.metric("Coin", bot_data["coin"])
    with col3:
        st.metric("Latency", f"{bot_data['latency']} ms")
    with col4:
        st.metric("Pool", bot_data["pool"])

# ETH Panel
st.subheader("💰 ETH Mining Status")
eth_stats = fetch_eth_stats(wallets["ETH"])
if eth_stats:
    unpaid_eth = eth_stats['unpaid'] / 1e18
    st.metric("Unpaid Balance (ETH)", f"{unpaid_eth:.5f}")
    st.metric("Hashrate", f"{eth_stats['reportedHashrate'] / 1e6:.2f} MH/s")
    st.metric("Active Workers", eth_stats["activeWorkers"])

    # Glyph Pulse Trigger
    if unpaid_eth >= 0.05:
        st.success("🔔 Threshold breached: Reinvestment vote triggered")
        narrate_event("vote")
        st.markdown(glyph_animation(), unsafe_allow_html=True)
        trigger_override("Z-16")

# KASPA Panel
st.subheader("💎 KASPA Mining Status")
kaspa_stats = fetch_kaspa_stats(wallets["KASPA"])
st.metric("Balance (KASPA)", f"{kaspa_stats['balance']:.5f}")
st.metric("Hashrate", f"{kaspa_stats['hashrate']:.2f} GH/s")
st.metric("Active Workers", kaspa_stats["workers"])

# Glyph Pulse on KASPA balance update
if kaspa_stats['balance'] > 0:
    st.info("🔔 KASPA payout detected")
    narrate_event("payout")
    st.markdown(glyph_animation(), unsafe_allow_html=True)

# Email Approval System
st.subheader("🛡️ Heir Approval System")
if pending_requests:
    st.markdown("Pending Requests:")
    for email in pending_requests:
        if st.button(f"Approve {email}"):
            approve_email(email)
            pending_requests.remove(email)
            st.success(f"Approved {email}")
else:
    st.markdown("No pending requests.")

# Override Log
st.subheader("📜 Override History")
st.markdown("""
- **Z-13**: Bot offline → reboot
- **Z-14**: Latency spike → NEURA rotation
- **Z-16**: ETH ≥ 0.05 → KASPA/DOGE reinvestment
""")

# Lineage Tree
st.subheader("🌐 Reinvestment Lineage")
lineage_data = {
    "Z-13": {"trigger": "Bot offline", "mutation": "Reboot + KASPA/DOGE split", "fusion": "❌"},
    "Z-14": {"trigger": "Latency spike", "mutation": "Override vote + NEURA rotation", "fusion": "❌"},
    "Z-16": {"trigger": "ETH ≥ 0.05", "mutation": "Reinvest ETH → KASPA/DOGE", "fusion": "✅ Fusion"}
}
st.table(lineage_data)

# Real-time updates
st.subheader("🔄 Live Updates")
placeholder = st.empty()
while True:
    with placeholder.container():
        eth_stats = fetch_eth_stats(wallets["ETH"])
        kaspa_stats = fetch_kaspa_stats(wallets["KASPA"])
        if eth_stats:
            unpaid_eth = eth_stats['unpaid'] / 1e18
            st.metric("Live Unpaid Balance (ETH)", f"{unpaid_eth:.5f}")
            if unpaid_eth >= 0.05:
                st.warning("⚠️ Reinvestment threshold reached!")
                narrate_event("breach")
        if kaspa_stats:
            st.metric("Live Balance (KASPA)", f"{kaspa_stats['balance']:.5f}")
    time.sleep(60)  # Update every minute
