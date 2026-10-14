# Seed: WhatsApp bridge drops image captions; auto-pull images for chosen chats (14 Oct 2026)

## The bug (verified)
`whatsapp-bridge/main.go:177` `extractTextContent()` reads only `Conversation` and
`ExtendedTextMessage`. Captions on images, videos and documents are thrown away, so those
messages are stored with empty `content`. On 13 Oct, Emily's two questions (Google OAuth, and
"do we need two thank-you pages/merge tags in XG") came as screenshot captions, and Claude
reported them as missing.

## Fix 1: store captions
Add `GetImageMessage().GetCaption()`, `GetVideoMessage().GetCaption()` and
`GetDocumentMessage().GetCaption()` to `extractTextContent`. Also check whether `messages.db`
should backfill earlier ones. It probably can't, since history sync only re-sends what WhatsApp gives it.

## Fix 2: auto-download images for an allowlist of chats (Paul: "probably not all images for all chats")
- Allowlist: Emily (`150311490576411@lid`) and Paul's "Tall Paul Cowen" self-chat, which he uses to send screenshots. Look up its JID.
- On receipt, download the media to the existing `store/<jid>/` path, the same place `download_media` writes.
- Keep the allowlist in a config file, not in code.

## Care
- The bridge is a live session. A restart can need a QR re-scan (memory `whatsapp-companion-logout-after-14-days`). `whatsapp.db` is credentials (memory `whatsapp-db-is-credentials-not-data`).
- After the restart, check that port 8080 sends work, not just that reads do (memory `whatsapp-bridge-silent-send-failure`).
- Test: send an image with a caption to the self-chat, then confirm `content` holds the caption and the file is on disk.
