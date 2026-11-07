# Making the iPhone the WhatsApp primary — recommendation + cheat sheet (9 Oct 2026)

Seed: `docs/SEED-iphone-primary-2026-10-09.md`. Research only — nothing on the bridge or phones was changed.

## Recommendation

**One fact decides this: the official Android→iPhone WhatsApp transfer only works on a factory-new or freshly erased iPhone.**
WhatsApp states it in plain terms: "Your iPhone must be factory new or factory reset", and "If you want to get back your old message history, you need to wipe your new device and start over. It's not possible to merge" ([WhatsApp FAQ 686469079565350](https://faq.whatsapp.com/686469079565350), [1195710084347483](https://faq.whatsapp.com/1195710084347483)). Apple's guide also says that if setup is already finished, you must erase the iPhone ([Apple 118670](https://support.apple.com/en-us/118670)).

| Your situation | Do this |
|---|---|
| **The iPhone is new, or you can erase it** (its contents are in iCloud, or there's nothing on it) | **Path A — Move to iOS.** Full history moves across. The iPhone becomes primary, and the 14-day logout risk effectively disappears because you use that phone every day. |
| **The iPhone is your daily phone and erasing it is too costly** | **Path B — keep the Android as primary and treat it as a home base.** Keep it charged on Wi-Fi and open WhatsApp on it at least weekly (set a recurring reminder). You can optionally link the iPhone as a companion phone. |
| Not recommended | Registering WhatsApp fresh on the iPhone without a transfer loses all history on the phone. Third-party transfer tools (Tenorshare, MobileTrans, etc.) are something WhatsApp says "isn't supported and may cause loss of chats". |

Path B works because the 14-day rule is about **using** the primary, not about which phone the primary is. The rule only bit because you were in hospital for more than 14 days and the Android sat untouched.

## Answers to the four questions

**1. Official path.** Use Apple's **Move to iOS** app on the Android, during the iPhone's setup. Requirements: Android 5+, iOS 15.5+, latest WhatsApp on both, the same phone number, both phones on power and the same Wi-Fi (or the iPhone's hotspot), and a factory-new or reset iPhone ([WhatsApp FAQ](https://faq.whatsapp.com/686469079565350)).
- **What moves:** account info, profile photo, individual, group and community chats, media, and settings.
- **What is lost:** call history, display name, peer-to-peer payment messages, and media received via Channels. The transfer also does not work for the WhatsApp Business app.
- **Linked devices:** the Android is signed out of WhatsApp at step 5 and the account is re-registered on the iPhone. WhatsApp's pages don't say explicitly that linked devices get dropped. **[Unverified, but plan for it]:** assume the bridge, Mac, iPad and any other linked devices will need relinking from the iPhone. Only the primary can link devices ([FAQ 378279804439436](https://faq.whatsapp.com/378279804439436)).
- **Newer options:** Apple now supports a USB-C cable, and an Android-17 "Transfer without App" flow. WhatsApp's FAQ names the Move to iOS **app** and says "other data migration apps … will cause migration issues", so use the app.

**2. The 14-day timeout.** It still applies after the switch. It is tied to whichever phone is primary: "Linked devices … will log out if your phone is unused for over 14 days". There is also a separate rule that a *linked device* is disconnected after **30 days of its own inactivity** ([FAQ 378279804439436](https://faq.whatsapp.com/378279804439436), [1046791737425017](https://faq.whatsapp.com/1046791737425017)). With the iPhone as your daily phone, the 14-day rule would only trigger if you went two weeks without opening WhatsApp at all. The bridge is connected around the clock, so the 30-day rule doesn't affect it.

**3. Bridge re-pairing and history.**
- **Expect to re-pair.** On a fresh link, the primary sends "an end-to-end encrypted copy of your **most recent** message history", and "not all messages and chats are synced" ([FAQ 653480766448040](https://faq.whatsapp.com/653480766448040)).
- **messages.db is safe as it stands.** I checked the code. A re-pair only replaces `store/whatsapp.db` (the credentials file); `store/messages.db` is not touched.
  - History-sync rows go through `StoreMessage` (`whatsapp-bridge/main.go:112-126`), which uses `INSERT OR REPLACE` and skips anything with no text and no media. Re-delivered history therefore overwrites matching rows with the same content and adds missing ones; it does not delete.
  - Remaining risk: a re-delivered copy of a media message can replace the stored media URL and key fields with fresh ones. That should be harmless, but it is a change.
- **The gap to watch.** Anything you send between the Android being signed out and the bridge being re-paired only reaches the DB if the iPhone's initial history sync includes it. Keep that window to minutes, and re-pair the bridge immediately after WhatsApp is activated on the iPhone.
- **On-demand backfill is switched off.** `requestHistorySync` (`main.go:1539`) is disabled, so the bridge can't ask the phone for more history afterwards. Fixing it means using `BuildHistorySyncRequest` with a real anchor message, which is a separate piece of work.

**4. The "last ~6 days of sent messages missing on linked devices" symptom.** I found no published fix. WhatsApp currently carries a banner on its linked-device pages: "**There is a known issue for some linked devices not displaying up to one year of chat history. We're working to fix this**" ([FAQ 378279804439436](https://faq.whatsapp.com/378279804439436), [1046791737425017](https://faq.whatsapp.com/1046791737425017)). That fits what you're seeing: the gap is in the **initial history sync sent to a newly linked device**, not in the live stream. The bridge DB proves the live stream is complete. It records 42–249 sent messages a day from 26 Sep to 9 Oct (`sqlite3 store/messages.db "select date(timestamp), sum(is_from_me) …"`, run 9 Oct 20:05).
- **Practical stance:** treat the bridge DB as the system of record and avoid unnecessary relinks.
- **[Speculative]:** a move to an iOS primary *might* change the symptom, because a different client builds the sync. Don't count on it. Keep the support ticket open.

**4a. What the WhatsApp Support chat adds.** The chat is ticket **1398598115722339**, read from `messages.db`, `chat_jid = 255735573270728@lid`.
- **Who answered:** it was an AI agent. It said it would "escalate" several times, then the ticket auto-closed at 18:22 and 18:42. There's no sign a human ever saw it. Its only concrete advice was update, check the connection and restart, and you'd already done all three.
- **What the screenshots pin down:** the missing sent messages show as **"Waiting for this message"** placeholders on companion devices. That is a decryption-key problem, not missing history. WhatsApp's own FAQ lists "Switch to your primary device" and "Unlink and relink" as the fixes ([FAQ 3398056720476987](https://faq.whatsapp.com/3398056720476987)), and it says the sender must be online for the message to come through.
- **[Inference — worth a 5-minute test]** A placeholder like that on a linked device is filled when the **primary phone answers a resend request**. Your old Samsung mostly sits idle, so it may never answer. The test:
  1. Open WhatsApp on the Samsung, on Wi-Fi.
  2. Leave it in the foreground for a few minutes.
  3. Scroll through your self-chat on the iPhone or Mac and see whether the "Waiting" messages fill in.

  If they do, that's the mechanism, and an iPhone primary you use every day would largely make the problem go away.
- **Result (Paul, 14 Oct):** the Samsung has been left on and online for long stretches, and the placeholders have never resolved. That rules out the idle-primary theory: this is WhatsApp's bug. Follow-up ticket **1454403296568821** was opened 9 Oct at 20:15. **Decision: still switching to an iPhone primary (Path A)**, because that is what stops the 14-day logouts.
- **To reach a human:** reply in the same Support chat with the ticket number. Ask for the placeholder-resend failure to be escalated to engineering as a **bug**, not a how-to question.

---

## Cheat sheet — Path A (Move to iOS). You do the phone steps; I do the Mac steps.

**Before you start (on the Mac):**
1. Take a fresh DB snapshot. The 20:01 backup predates tonight's messages. Ask me, or run:
   `sqlite3 ~/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/messages.db ".backup '$HOME/WhatsAppBackups/pre-iphone-$(date +%Y%m%d-%H%M%S).db'"`
2. Don't copy or share `whatsapp.db`; it holds credentials.

**On the Android:**
3. Update WhatsApp from the Play Store, then install **Move to iOS**.
4. Optional fallback: Settings → Chats → Chat backup → **Back up**, to Google Drive. Only an Android can restore from this backup, but it's a safety net.

**On the iPhone (it must be new or erased):**
5. If it's in use, back it up first (iCloud or the Mac), then Settings → General → Transfer or Reset → **Erase All Content and Settings**. Restoring that iCloud backup later would mean erasing again and losing the WhatsApp transfer, which is why Path A is only right if the iPhone is new or you can live without its old contents.
6. Plug both phones into power and put them on the same Wi-Fi.
7. iPhone setup → Quick Start → **Set Up Without Another Apple Device** → Transfer Your Apps & Data → **From Android** → **Transfer with App**.
8. Open Move to iOS on the Android, enter the code shown on the iPhone, and join the temporary Wi-Fi when asked.
9. On the Transfer Data screen, tick **WhatsApp** plus anything else you want. Tap **Start** in the WhatsApp prompt and wait while it prepares; the Android is signed out of WhatsApp at this point. Then **Next** → **Continue**.
10. Leave both phones untouched until the iPhone's progress bar finishes. No calls, and don't switch apps on the Android.
11. Install WhatsApp from the App Store, log in with the **same number**, tap **Start** to import, and finish activation.

**Straight after, to keep the gap short:**
12. Tell me "iPhone active". I'll restart the bridge to show a QR code. On the iPhone: Settings → **Linked Devices** → **Link a Device** → scan it.
13. Relink the Mac and iPad apps and any other devices the same way.
14. I'll check that the bridge stored the post-switch messages and compare row counts against the snapshot from step 1.
15. Keep the Android and **don't wipe it** until you've spot-checked chats on the iPhone. Its local WhatsApp data stays on the phone until you delete it.

## Cheat sheet — Path B (keep Android primary)
1. Keep the Android on charge and on home Wi-Fi permanently.
2. Set a recurring reminder: **every Sunday, open WhatsApp on the Android**. That gives a 7-day margin against the 14-day cutoff.
3. Optional: link the iPhone as a companion phone. Install WhatsApp on the iPhone → three-dot / ⋯ menu → **Link as companion device**. On the Android: ⋮ → Linked devices → Link a device → scan. Menu labels vary by version ([WABetaInfo](https://wabetainfo.com/whatsapp-for-ios-23-10-76-whats-new/), [folk.app guide](https://www.folk.app/articles/how-to-link-whatsapp-to-another-phone-without-switching-accounts)). This uses one of the four linked-device slots, and the bridge uses another.
4. If you ever go into hospital again, bring the Android, or have someone open WhatsApp on it once a week.

## Sources
- WhatsApp — [Move chats Android → iPhone](https://faq.whatsapp.com/686469079565350) · [Can't move chats](https://faq.whatsapp.com/1195710084347483) · [About linked devices](https://faq.whatsapp.com/378279804439436) · [Message history on linked devices](https://faq.whatsapp.com/653480766448040) · [Second phone](https://faq.whatsapp.com/1046791737425017) · [Changing phones](https://faq.whatsapp.com/1197347060992858)
- Apple — [Move from Android to iPhone](https://support.apple.com/en-us/118670)
- whatsmeow behaviour on reconnect — [slidge-whatsapp commit](https://git.deuill.org/deuill/slidge-whatsapp/commit/8a1e30648433715d1a09deb8e35004e0d4721ed2) · [wacli](https://github.com/UAEpro/wacli)
