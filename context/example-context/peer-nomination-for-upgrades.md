# Product Brief: Peer Nomination for Upgrades

## What problem are you solving and why?

Right now, users on free Viewer seats don't know they need an upgrade until they hit a limitation. By that point, they're frustrated and the request feels like friction. Meanwhile, paid Pro Editor users already know who on their team would benefit from editing access - they're sharing docs with Viewers who clearly need more capabilities.

We're targeting teams where Pro Editors are actively collaborating with Viewer users. The insight: peer recommendations convert better than self-serve prompts because they come with social proof and context. If a trusted teammate suggests you need editing access, you're more likely to request it (and admins are more likely to approve it).

We should win here because we have the collaboration graph - we know who's sharing what with whom, and which Viewers are trying to do Editor-level work.

## What are you thinking of building?

When a Pro Editor shares a document with a Viewer user, we show a lightweight "Suggest upgrade" option in the share modal or as a follow-up action. When clicked, the Pro Editor can add a quick note ("Sarah needs editing access to help with the Q4 roadmap") and send a suggestion.

The Viewer receives a notification: "Alex suggested you upgrade to Editor to collaborate on [Doc Name]." They can request the upgrade with one click, with the peer endorsement attached to the request.

For admins, the approval request now includes context: "Sarah requested Editor access (suggested by Alex for collaboration on Q4 Roadmap doc)."

User journey:
1. Pro Editor shares doc with Viewer → sees "Suggest upgrade for this person?"
2. Pro Editor adds quick context → suggestion sent
3. Viewer gets notification → clicks to request upgrade
4. Admin sees request with peer endorsement → approves faster/more confidently

## Why might you not build this?

**Controversial bit:** We're asking Pro Editors to do extra work (suggest upgrades) that creates more costs for their company. Some might see this as Figma being pushy about upsells.

**Risks:**
- Could create awkward team dynamics if suggestions feel like peer pressure
- Admins might get annoyed by increased request volume if it's not thoughtful
- Pro Editors might not want to "nominate" colleagues for fear of seeming like they're trying to spend company money
- If the suggestions are low-quality (just spam everyone), admins will lose trust

**Most scared of:** Building a feature that Pro Editors ignore because it feels awkward, or that increases request volume but tanks approval rates because requests aren't actually better-informed.

## What does success look like?

| Goal | Measured by | Target | Rationale |
|---|---|---|---|
| Increase upgrade request volume | Requests per 1000 Viewer users (monthly) | +30% | Peer suggestions surface upgrade needs earlier in collaboration |
| Maintain or improve approval rate | % requests approved within 7 days | No regression (<-5%) | Better context should help, not hurt, admin decisions |
| Adoption of suggestion feature | % of Pro Editors who suggest ≥1 upgrade (monthly) | 15% | Need meaningful adoption to drive volume impact |
| Request quality (guardrail) | % of peer-suggested requests approved | ≥ baseline approval rate | Ensure suggestions don't degrade request quality |

## What's next?

**Effort:** ~3-4 months for 1 PM + 2-3 engineers + 1 designer

**Timeline:** Target GA for Q1 2026 (Jan-Mar)

**Milestones:**
- Dec 2025: Design review with leadership
- Jan 2026: Build and internal dogfood
- Feb 2026: Beta to 10% of Pro Editor users
- Mar 2026: Full GA launch

**Affected areas:**
- Sharing flows (adding suggestion CTA)
- Notification system (new notification type for Viewers)
- Admin dashboard (showing peer endorsements in approval UI)
- Analytics/metrics (tracking suggestion → request → approval funnel)

**Reviewer** | **Are you aligned?** | **How should you be involved?** | **Feedback / comments**
---|---|---|---
Alicia Xiong | TBD | Review before design |
Ben Stern | TBD | Review before build kickoff |
Design lead | TBD | Own design execution |
Eng lead | TBD | Scoping and feasibility |
