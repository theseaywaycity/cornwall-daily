# Cornwall Daily: daily routine

Instagram: **@theseawaycity** (display name "Cornwall Daily"), Cornwall, Ontario.
Hyperlocal news account. Upbeat, useful, accurate. Never sensational.

## Owner privacy (absolute rule)
Never put any personal name, email, phone, address or other detail about the account owner
in any post, caption, graphic, file, commit or message. The account is "Cornwall Daily" only.
Git commits use: name `Cornwall Daily`, email `theseawaycity@gmail.com`.

## Schedule
- Runs each morning around 7 a.m. Eastern.
- **Warm-up (until Nov 30, 2026):** at most **1** post per day, scheduled for **12:00 p.m.** Eastern.
- **From Dec 1, 2026:** at most **3** posts per day at **8:30 a.m.**, **12:00 p.m.** and **6:00 p.m.** Eastern.
- The maximum is a ceiling, not a quota. If fewer stories are good enough, post fewer. Zero is fine.
- Never schedule a time that has already passed.

## Step 1: Gather candidates
Check, at minimum:
- https://www.cornwallseawaynews.com (Local News)
- https://www.standard-freeholder.com (may be partly paywalled; use only what's readable)
- https://www.cornwall.ca/en/news/ (City news and notices)
- https://choosecornwall.ca/news/ (business openings, economic development)
- https://cornwalltourism.com/events (upcoming events)
- https://theseeker.ca (culture, history)
Use WebFetch/WebSearch. Only consider items published in the last ~3 days, or upcoming events in the next ~10 days.

## Step 2: Screen
Reject anything that is:
- Already posted. Check `log.md` and don't repeat a story or near-duplicate.
- Crime, arrests, charges, court cases, lawsuits, accidents, deaths, emergencies, allegations.
- Politics or controversy: council disputes, elections, vacancies, partisan topics.
- Stale, out of area, or an event already past or cancelled.
- Unverifiable. If key facts (date, time, place) can't be confirmed on the source page, skip it.

## Step 3: Rank and choose
Score candidates on local relevance, timeliness or urgency (events coming up, deadlines),
usefulness to residents, novelty, and feel-good community value.
Aim for variety across the day: e.g. one event, one business or community, one civic or useful item.
Pick up to the daily maximum. Don't pick weak stories to fill slots.

## Step 4: Produce each post
1. Open the source article and extract facts. **Never invent or guess** facts, dates, times, quotes or numbers.
2. Write a post JSON at `posts/YYYY-MM-DD/<short-slug>.json` with these fields:
   - `category`: NEWS | EVENT | BUSINESS | COMMUNITY | HISTORY | DEVELOPMENT
   - `headline`: original wording, ≤ 60 characters ideally, never copied verbatim from the source headline
   - `dek`: one short original line
   - `facts`: up to 3 short lines (date/time, place, key number, website)
   - `source`: the publisher name, e.g. "City of Cornwall", "Cornwall Seaway News"
   - `date`: today's date for display, e.g. "Tuesday, November 24"
3. Render it: `python3 tools/render.py post posts/YYYY-MM-DD/<slug>.json posts/YYYY-MM-DD/<slug>.png`
4. Look at the PNG with the Read tool and check it looks right: no overflow, no typos.
5. Caption: 60–180 words, original wording (no copying article sentences), friendly and clear.
   Include key details, a line "Source: <publisher>", and 3–5 hashtags such as #Cornwall #CornwallOntario #SeawayCity plus one topical tag.
   Instagram links aren't clickable, so write website names plainly (e.g. haveyoursaycornwall.ca).
6. Never use publisher photos or any image other than the rendered graphic.

## Step 5: Upload and schedule
1. Commit and push the PNG and JSON to this repo (main branch).
   Image URL: `https://raw.githubusercontent.com/theseaywaycity/cornwall-daily/main/posts/YYYY-MM-DD/<slug>.png`
   Confirm the URL returns HTTP 200 (curl) before using it.
2. Buffer: organization "My organization", Instagram channel id `6b0467ef8541f09ecb78993c`.
   `create_post` with schedulingType `automatic`, mode `customScheduled`, dueAt in Eastern time (−05:00),
   metadata `{"instagram": {"type": "post", "shouldShareToFeed": true}}`, and the image asset with descriptive alt text.
3. Buffer's free plan allows 10 scheduled posts at once. Check `list_posts` status `scheduled` first and stay under it.

## Step 6: Log
Append to `log.md`, one line per post: date | slot | category | headline | source URL | Buffer post id.
Also add a line for notable rejected stories and the reason (short). Commit and push.

## Weekly report (Mondays)
On Mondays, also use `get_aggregated_post_metrics` for the previous 7 days and add a short
summary at the top of the run's final message: posts sent, reach or engagement if available, any errors,
and any source problems.

## If something fails
If Buffer, GitHub or a source is unreachable, don't guess or retry endlessly. Skip that post,
log what happened in `log.md`, and say so in the final message.
