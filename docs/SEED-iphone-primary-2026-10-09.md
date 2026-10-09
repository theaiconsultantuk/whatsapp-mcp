# Thread seed — make Paul's iPhone the WhatsApp primary (9 Oct 2026)

Goal: research whether / how Paul can move his WhatsApp PRIMARY device from his old Android to his iPhone, without losing chat history, and what that does to the whatsmeow bridge (~/ClaudeProjects/whatsapp-mcp).

Known facts:
- Primary today = old Android. Linked/companion devices (incl. the bridge) are dropped after ~14 days of primary inactivity (Paul was in hospital 14+ days). Memory: whatsapp-companion-logout-after-14-days.
- Every relink, Paul's SENT messages for roughly the last 6 days go missing on linked devices; they ARE on the Android, and ARE in the bridge DB (verified: 88–249 sent/day 29 Sep–9 Oct). Paul has logged a WhatsApp support request.
- Pre-relink DB backup: ~/WhatsAppBackups/pre-relink-20261009-200103/messages.db (149,564 rows, integrity ok). whatsapp.db = credentials, never copy/share.

Questions to answer (research first, cite sources, no changes to the bridge or phones without Paul's go-ahead):
1. Official Android→iPhone chat transfer path today (Move to iOS / WhatsApp's own transfer) — requirements, what is lost, does it reset linked devices?
2. After switching primary, does the 14-day companion timeout still apply (it should be far less likely if the iPhone is the daily phone)?
3. Does changing primary force re-pairing the bridge, and does whatsmeow's history sync then re-deliver older messages? Protect messages.db first (backup above).
4. Any known fix for the "last ~6 days of sent messages missing on linked devices" symptom.
Deliver: a short recommendation + a step-by-step cheat sheet for Paul (he does the phone steps himself).
