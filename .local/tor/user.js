/**************************************
 * 🧙🏾‍♂️ Kris Yotam's GOD-TIER user.js *
 * Tor Browser hardening and tuning   *
 **************************************/

/** 🚫 Disable WebRTC (prevents IP leaks via STUN/ICE) **/
user_pref("media.peerconnection.enabled", false);

/** 🕵️‍♂️ Fingerprinting Resistance **/
user_pref("privacy.resistFingerprinting", true); // Enable general RFP
user_pref("privacy.resistFingerprinting.reduceTimerPrecision", true); // Lower resolution of JS timers
user_pref("privacy.resistFingerprinting.reduceTimerPrecision.microseconds", 1000); // Coarsen to 1ms
user_pref("privacy.resistFingerprinting.letterboxing", true); // Avoid screen-size fingerprinting

/** ⏰ Timezone & Locale Spoofing **/
user_pref("privacy.resistFingerprinting.screen_resolution", [1000, 1000]); // Fake screen res
user_pref("privacy.resistFingerprinting.randomizedNames.enabled", true);

/** 🌍 Use DuckDuckGo Onion as Homepage **/
user_pref("browser.startup.homepage", "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/");

/** 🔥 Disable Disk Cache (no residual data saved) **/
user_pref("browser.cache.disk.enable", false);
user_pref("browser.cache.memory.enable", false);
user_pref("browser.cache.offline.enable", false);
user_pref("network.http.use-cache", false);

/** 🧼 Disable Browsing History & Form Data **/
user_pref("places.history.enabled", false);
user_pref("browser.formfill.enable", false);
user_pref("signon.rememberSignons", false);

/** 🔒 Enforce Private Browsing Mode **/
user_pref("browser.privatebrowsing.autostart", true);

/** 🧠 Disable Telemetry, Experiments, and Studies **/
user_pref("toolkit.telemetry.enabled", false);
user_pref("toolkit.telemetry.unified", false);
user_pref("toolkit.telemetry.archive.enabled", false);
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("app.shield.optoutstudies.enabled", false);

/** 📡 Disable Battery Status API **/
user_pref("dom.battery.enabled", false);

/** 🖼️ Disable WebGL (defends against fingerprinting) **/
user_pref("webgl.disabled", true);

/** 📸 Disable canvas readout (prevents pixel fingerprinting) **/
user_pref("privacy.resistFingerprinting.block_mozAddonManager", true);
user_pref("canvas.capturestream.enabled", false);
user_pref("gfx.offscreencanvas.enabled", false);

/** 🧠 Disable clipboard snooping **/
user_pref("dom.event.clipboardevents.enabled", false);

/** 🔇 Disable Speech Recognition & Input APIs **/
user_pref("media.webspeech.recognition.enable", false);
user_pref("media.webspeech.synth.enabled", false);

/** 🔕 Disable Notifications & Push **/
user_pref("dom.push.enabled", false);
user_pref("dom.webnotifications.enabled", false);

/** 🧱 Block all forms of speculative connections (preloading, etc) **/
user_pref("network.dns.disablePrefetch", true);
user_pref("network.prefetch-next", false);
user_pref("network.http.speculative-parallel-limit", 0);
user_pref("network.predictor.enabled", false);

/** 🧭 Enforce SOCKS DNS (no DNS leaks) **/
user_pref("network.proxy.socks_remote_dns", true);

/** 🕳️ Disable DNS-over-HTTPS (we're using Tor DNS!) **/
user_pref("network.trr.mode", 5);

/** 📦 Disable all telemetry pings from extensions **/
user_pref("extensions.getAddons.cache.enabled", false);
user_pref("extensions.webservice.discoverURL", "");

/** 💣 Kill all autoplay **/
user_pref("media.autoplay.default", 5); // Block all autoplay media
user_pref("media.autoplay.allow-extension-background-pages", false);

/** 🔐 Hide internal IPs from JS (especially in WebRTC leaks) **/
user_pref("media.peerconnection.ice.no_host", true);

/** 🦺 Enforce First-Party Isolation (already default in Tor, but here anyway) **/
user_pref("privacy.firstparty.isolate", true);

/** 🧪 Optional: Disable JavaScript on non-onion sites (breaks things, but ultra-paranoid) **/
// user_pref("javascript.enabled", false);

/** 🎁 Bonus: Set blank new tab **/
user_pref("browser.newtabpage.enabled", false);
user_pref("browser.newtab.url", "about:blank");

/** ⚠️ Disable auto-updates (if you want to manage them manually) **/
user_pref("app.update.auto", false);

/** ✋ Disable Pocket garbage **/
user_pref("extensions.pocket.enabled", false);

/** 👁️‍🗨️ Optional: Show Tor circuit info automatically **/
// user_pref("extensions.torbutton.display_circuit", true);

/** 🧩 Block all extensions except verified Tor Browser ones **/
user_pref("xpinstall.signatures.required", true);
user_pref("extensions.autoDisableScopes", 15);

/** 🎯 Maximize content process isolation **/
user_pref("security.sandbox.content.level", 5);

/** 🧃 Extra Juice: Make Firefox *say no* to ping tracking **/
user_pref("browser.send_pings", false);
user_pref("browser.send_pings.require_same_host", true);

/**************************************
 * End of GOD-TIER user.js            *
 * You are now operating in ghostmode *
 **************************************/
