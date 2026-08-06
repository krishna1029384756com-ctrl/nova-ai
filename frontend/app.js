// =========================
// Startup
// =========================

async function startup() {
    try {
        const response = await fetch("/api/startup");
        const data = await response.json();
        console.log("Backend Connected", data);
        setStatus(true, data.ai_available);
    } catch (error) {
        console.error("Backend Offline");
        setStatus(false, false);
    }
}

function setStatus(online, aiAvailable) {
    const statusEl = document.getElementById("status");
    if (!statusEl) return;

    if (!online) {
        statusEl.textContent = "🔴 Offline";
        return;
    }

    statusEl.textContent = aiAvailable ? "🟢 Online · 🧠 AI Ready" : "🟢 Online · 🧠 Basic Mode";
}

startup();


// =========================
// Screen switching
// =========================

const homeScreen = document.getElementById("homeScreen");
const chatScreen = document.getElementById("chatScreen");
const chatBtn = document.getElementById("chatBtn");
const backBtn = document.getElementById("backBtn");
const settingsBtn = document.getElementById("settingsBtn");

function openChatScreen() {
    homeScreen.classList.add("hidden");
    chatScreen.classList.remove("hidden");
    chatInput.focus();

    if (chatLog.childElementCount === 0) {
        addMessage("nova", "Hi Krishna, I'm NOVA. How can I help you?");
    }
}

chatBtn.addEventListener("click", openChatScreen);

backBtn.addEventListener("click", () => {
    chatScreen.classList.add("hidden");
    homeScreen.classList.remove("hidden");
});

// =========================
// Settings: customizable wake word
// =========================

const DEFAULT_WAKE_WORD = "hey nova";

const settingsModal = document.getElementById("settingsModal");
const wakeWordInput = document.getElementById("wakeWordInput");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const closeSettingsBtn = document.getElementById("closeSettingsBtn");
const wakeWordLabel = document.getElementById("wakeWordLabel");

let currentWakeWord = localStorage.getItem("novaWakeWord") || DEFAULT_WAKE_WORD;

function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Turns a plain phrase like "hey nova" into a regex that also captures
// anything said right after it, e.g. "hey nova what time is it" -> "what time is it"
function buildWakeRegex(phrase) {
    const escaped = escapeRegex(phrase.trim().toLowerCase()).replace(/\s+/g, "\\s+");
    return new RegExp(escaped + "[,]?\\s*(.*)", "i");
}

function titleCase(str) {
    return str.replace(/\w\S*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1));
}

function updateWakeWordLabel() {
    if (wakeWordLabel) {
        wakeWordLabel.textContent = `Enable "${titleCase(currentWakeWord)}" wake word`;
    }
}

let WAKE_PHRASE = buildWakeRegex(currentWakeWord);
updateWakeWordLabel();

settingsBtn.addEventListener("click", () => {
    wakeWordInput.value = titleCase(currentWakeWord);
    settingsModal.classList.remove("hidden");
});

closeSettingsBtn.addEventListener("click", () => {
    settingsModal.classList.add("hidden");
});

settingsModal.addEventListener("click", (e) => {
    if (e.target === settingsModal) settingsModal.classList.add("hidden");
});

saveSettingsBtn.addEventListener("click", () => {
    const newWord = wakeWordInput.value.trim();

    if (!newWord) {
        alert("Please enter a wake word phrase.");
        return;
    }

    currentWakeWord = newWord.toLowerCase();
    localStorage.setItem("novaWakeWord", currentWakeWord);
    WAKE_PHRASE = buildWakeRegex(currentWakeWord);
    updateWakeWordLabel();
    settingsModal.classList.add("hidden");
});


// =========================
// Chat
// =========================

const chatLog = document.getElementById("chatLog");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const wakeIndicator = document.getElementById("wakeIndicator");
const wakeWordToggle = document.getElementById("wakeWordToggle");

function addMessage(sender, text) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${sender}`;
    bubble.textContent = text;
    chatLog.appendChild(bubble);
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendMessage(message) {
    if (!message || !message.trim()) return;

    addMessage("user", message);
    chatInput.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        addMessage("nova", data.reply);

    } catch (error) {
        console.error(error);
        addMessage("nova", "Sorry, I couldn't reach the backend.");
    }
}

sendBtn.addEventListener("click", () => sendMessage(chatInput.value));

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage(chatInput.value);
    }
});


// =========================
// Debug log (visible on-page, no DevTools needed)
// =========================

const debugLogEl = document.getElementById("debugLog");
const debugToggleBtn = document.getElementById("debugToggleBtn");

debugToggleBtn.addEventListener("click", () => {
    debugLogEl.classList.toggle("hidden");
});

function logDebug(msg) {
    console.log(msg);
    const time = new Date().toLocaleTimeString();
    const line = document.createElement("div");
    line.textContent = `[${time}] ${msg}`;
    debugLogEl.appendChild(line);
    debugLogEl.scrollTop = debugLogEl.scrollHeight;
    while (debugLogEl.children.length > 60) {
        debugLogEl.removeChild(debugLogEl.firstChild);
    }
}

// Tells the desktop status window (window.py) what's happening, so you get
// visible confirmation on your desktop too, not just in the browser.
function notifyWindow(event, text) {
    fetch("/api/wake-event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event, text: text || "" })
    }).catch(() => { /* desktop window bridge is a nice-to-have, fail silently */ });
}


// =========================
// Voice: shared recognition engine
// =========================
//
// One SpeechRecognition instance is shared between two modes, since a
// browser only allows one active recognition session at a time:
//   - "manual" : one-shot, triggered by clicking the mic button
//   - "wake"   : listens for the wake word using a RESTART LOOP
//
// Why a restart loop instead of the built-in `continuous: true` mode:
// continuous mode is notoriously unreliable across Chrome versions/OSes
// (silent stalls, no results ever firing). Restarting a fresh short
// recognition session every time one ends is a well-known, more robust
// workaround that behaves like continuous listening in practice.
//
// Note: this only listens while this browser tab is open and has mic
// permission — it's not a true system-wide background wake word.

const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;
let currentMode = "idle";   // "idle" | "manual" | "wake"
let pendingMode = null;     // mode to switch into once current one has stopped
let awaitingCommand = false;
let wakeWordEnabled = false;

function playChime(freq) {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.frequency.value = freq;
        osc.connect(gain);
        gain.connect(ctx.destination);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        osc.start();
        osc.stop(ctx.currentTime + 0.15);
    } catch (e) {
        // Audio not available - not critical, ignore.
    }
}

// =========================
// Fuzzy wake-word matching
// =========================
//
// Speech-to-text rarely transcribes a short wake phrase perfectly every
// time ("hey nova" might come back as "a nova" or "hey nova's"). An exact
// regex match alone misses these. So: try exact match first (fast, clean
// remainder extraction), and if that fails, fall back to comparing the
// first few words against the wake phrase by edit-distance similarity.

function levenshtein(a, b) {
    const m = a.length, n = b.length;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            dp[i][j] = a[i - 1] === b[j - 1]
                ? dp[i - 1][j - 1]
                : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
        }
    }
    return dp[m][n];
}

function similarity(a, b) {
    const dist = levenshtein(a, b);
    const maxLen = Math.max(a.length, b.length) || 1;
    return 1 - dist / maxLen;
}

const FUZZY_THRESHOLD = 0.72;

// Returns { matched, remainder, fuzzy, score } for a heard transcript.
function matchWakeWord(transcript) {
    const exact = transcript.match(WAKE_PHRASE);
    if (exact) {
        return { matched: true, remainder: exact[1].trim(), fuzzy: false };
    }

    const wakeWords = currentWakeWord.trim().toLowerCase().split(/\s+/);
    const words = transcript.toLowerCase().trim().split(/\s+/);
    if (words.length < wakeWords.length) return { matched: false };

    const windowText = words.slice(0, wakeWords.length).join(" ");
    const score = similarity(windowText, currentWakeWord.toLowerCase());

    if (score >= FUZZY_THRESHOLD) {
        const remainder = words.slice(wakeWords.length).join(" ").replace(/^[,.]?\s*/, "");
        return { matched: true, remainder, fuzzy: true, score };
    }

    return { matched: false };
}

function showWakeIndicator(awaiting) {
    if (!wakeIndicator) return;
    if (!wakeWordEnabled) {
        wakeIndicator.classList.add("hidden");
        return;
    }
    wakeIndicator.classList.remove("hidden");
    wakeIndicator.textContent = awaiting
        ? "🎙️ Yes? I'm listening..."
        : `👂 Listening for "${titleCase(currentWakeWord)}"...`;
    wakeIndicator.classList.toggle("active", awaiting);
}

function startWakeListening() {
    if (!recognition || currentMode !== "idle" || !wakeWordEnabled) return;
    currentMode = "wake";
    recognition.continuous = false;
    recognition.interimResults = false;
    try {
        recognition.start();
        logDebug(`listening cycle started (wake word: "${currentWakeWord}")`);
    } catch (e) {
        logDebug(`couldn't start listening: ${e.message || e}`);
        currentMode = "idle";
    }
}

function startManualListening() {
    if (!recognition) return;

    if (currentMode === "wake") {
        // Pause wake listening first, then switch into manual mode once it stops.
        pendingMode = "manual";
        awaitingCommand = false;
        recognition.stop();
        return;
    }

    if (currentMode === "manual") return;

    currentMode = "manual";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.start();
}

if (SpeechRecognitionAPI) {
    recognition = new SpeechRecognitionAPI();
    recognition.lang = "en-US";
    recognition.maxAlternatives = 3; // check a few transcription guesses, not just the top one

    recognition.onstart = () => {
        if (currentMode === "manual") {
            micBtn.classList.add("listening");
            micBtn.textContent = "🔴";
        }
    };

    recognition.onerror = (event) => {
        logDebug(`error: ${event.error}`);

        if (event.error === "not-allowed" || event.error === "service-not-allowed") {
            wakeWordEnabled = false;
            wakeWordToggle.checked = false;
            showWakeIndicator(false);
            notifyWindow("error", "microphone permission denied");
            alert('NOVA needs microphone permission for the wake word to work. Check your browser\'s site settings (the padlock icon in the address bar) and allow the microphone, then try again.');
        } else if (event.error === "network") {
            notifyWindow("error", "no internet connection for voice recognition");
        }
        // Other errors (like "no-speech" during quiet moments) are normal
        // and expected constantly in the restart loop - onend handles the retry.
    };

    recognition.onend = () => {
        const finishedMode = currentMode;
        currentMode = "idle";
        micBtn.classList.remove("listening");
        micBtn.textContent = "🎤";

        if (pendingMode) {
            const next = pendingMode;
            pendingMode = null;
            if (next === "manual") {
                currentMode = "manual";
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.start();
            }
            return;
        }

        // This is the "restart loop": every time a cycle ends (whether it
        // caught speech, hit silence, or errored), immediately start a new
        // one if wake word listening is still turned on.
        if (wakeWordEnabled && (finishedMode === "wake" || finishedMode === "manual")) {
            setTimeout(startWakeListening, 250);
        }
    };

    recognition.onresult = (event) => {
        if (currentMode === "manual") {
            const transcript = event.results[0][0].transcript;
            sendMessage(transcript);
            return;
        }

        if (currentMode === "wake") {
            const alternatives = event.results[0];
            let transcript = alternatives[0].transcript.trim();
            let match = null;

            if (!awaitingCommand) {
                // Check every transcription guess for the wake word, not just
                // the top one - noise/accents often trip up the #1 guess
                // while a lower-ranked alternative still catches it.
                for (let i = 0; i < alternatives.length; i++) {
                    const altText = alternatives[i].transcript.trim();
                    const result = matchWakeWord(altText);
                    if (result.matched) {
                        transcript = altText;
                        match = result;
                        break;
                    }
                }
            }

            if (!transcript) return;
            logDebug(`heard: "${transcript}"`);

            if (!awaitingCommand) {
                if (match) {
                    logDebug(match.fuzzy
                        ? `wake word matched (fuzzy, ${Math.round(match.score * 100)}% similar)`
                        : "wake word matched (exact)");
                    notifyWindow("triggered", transcript);
                    playChime(880);
                    openChatScreen();

                    if (match.remainder) {
                        // Wake word + command said in one breath.
                        sendMessage(match.remainder);
                        notifyWindow("heard", match.remainder);
                        showWakeIndicator(false);
                    } else {
                        awaitingCommand = true;
                        showWakeIndicator(true);
                        notifyWindow("awaiting", "");
                    }
                }
            } else {
                sendMessage(transcript);
                notifyWindow("heard", transcript);
                awaitingCommand = false;
                showWakeIndicator(false);
            }
        }
    };

    micBtn.addEventListener("click", () => {
        if (currentMode === "manual") {
            recognition.stop();
        } else {
            startManualListening();
        }
    });

    wakeWordToggle.addEventListener("change", () => {
        wakeWordEnabled = wakeWordToggle.checked;

        if (wakeWordEnabled) {
            awaitingCommand = false;
            logDebug("wake word enabled");
            notifyWindow("listening", "");
            if (currentMode === "idle") startWakeListening();
        } else {
            awaitingCommand = false;
            showWakeIndicator(false);
            logDebug("wake word disabled");
            notifyWindow("idle", "");
            if (currentMode === "wake") recognition.stop();
        }
    });

} else {
    micBtn.disabled = true;
    micBtn.title = "Voice input isn't supported in this browser";
    wakeWordToggle.disabled = true;
    document.getElementById("wakeWordLabel").textContent =
        "Wake word isn't supported in this browser";
    logDebug("This browser doesn't support the Web Speech API at all (try Chrome or Edge).");
}
