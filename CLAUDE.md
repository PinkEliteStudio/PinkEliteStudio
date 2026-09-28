# CLAUDE.md — Project context for Claude

Read this first in every session. It records what we're building and the rules we've agreed on,
so the user doesn't have to re-explain them.

## Who I'm working with
- A 1099 independent agent who sells **mortgage protection / life insurance** (brand: FaithShield).
- Faith-based brand (✝️ 🙏 💕). Pink visual style (Pink Elite Studio).
- Not a developer. Explain things in **simple, plain words** and give **one task at a time** with
  numbered click-by-click steps. Ask for a **screenshot** to confirm each step before moving on.
- Deploys by **drag-and-drop to Netlify** from a computer.

## This repo
Static marketing pages for Pink Elite Studio (landing, playbook, email swipe, ad scripts, intake
form, payment, scheduling, webinar, KPI tracker). Hosted on Netlify (`_headers`, `_redirects`).

## Main project: DreamTeam AI (lead qualification + AI calling CRM)
An AI assistant that calls the user's leads, vets and qualifies them, and hands over warm leads
for the user to call and close. It's **our own build**, not a copy of Orion AI Solutions, SalesApe,
Connex or NextLM (their systems are private; we only match what they do).

- **Live site:** dreamteam-faithshield.netlify.app
- **Code location:** was delivered as a zip (`dreamteam-ai` folder) and deployed manually to
  Netlify. **It is not in this repo yet.** If work is needed on it, ask the user to upload the
  folder here first.
- **Features:** private lead dashboard behind an access code; add leads one at a time or upload a CSV;
  "Call with AI" for one lead or the whole list; after each call it shows the summary, qualifying
  answers, transcript and recording; hot leads are flagged in pink.
  An Email tab has templates and "Send test".
- **Stack:**
  - **Vapi** is the AI voice/calling engine. Billing is per minute, and it can transfer a hot lead
    to the user's cell.
  - **Netlify Functions** (`call`, `status`) connect the site to Vapi.
  - **Resend** sends email. The API key is named "DreamTeam CRM".
  - **Secrets live only in Netlify environment variables.** Never put keys in the code or in this file.

## Compliance rules (keep these in the product)
- The FCC ruled in 2024 that AI voices count as "artificial voice" calls under the TCPA. They need
  **prior express written consent**, and fines are $500 to $1,500 per call. Florida's FTSA is also strict.
- The dashboard **blocks AI calls to any lead not marked as opted in**. Keep that checkbox.
- The AI says up front that it is an AI assistant calling for the user.
- The user scrubs every list against **DNC**. Only leads whose form consents to automated calls get
  AI calls; the user dials everyone else by hand.

## Copy/script rules
- **"WHEN, never IF"**: write "when something happens to you", never "if something happened to you".
- Scripts put the **pain first, then the solution**, matching the user's phone script.

## Progress log
- Task 1: deploy the site to Netlify and confirm the `call` + `status` functions. Done.
- Tasks 2–7: Vapi account/number setup and later steps. Covered in the original chat; details not
  recorded here.
- Task 8: rotated the Resend API key; a test email arrived in the Inbox with the pink design. Done.
- Task 9: deleted the old Resend key; only "DreamTeam CRM" remains. Done.
- **Next:** rewrite all 3 starter email templates to follow the WHEN-never-IF rule. The template
  "Would your spouse have to move?" still says "If something happened to you tomorrow...".
- Pending: write the AI caller script (pain first, then solution) if it isn't done yet.
