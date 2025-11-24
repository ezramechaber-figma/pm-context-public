# Fictional Docs Product - Seat Expansion Roadmap 2025+

## Product Context
**DocFlow** - A collaborative document editing platform
- **Seat Types**: Viewer (free), Editor ($12/mo), Pro Editor ($25/mo)
- **Goal**: Increase paid seat adoption through self-serve expansion
- **Key Metrics**: Request volume, Approval rate, Seat retention

---

## Active Experiments

### Currently Running (4 experiments)

#### 1. In-Document Upgrade Prompts
- **Status**: Fielding Experiment
- **Theme**: Request Volume
- **Hypothesis**: By showing upgrade prompts when users hit collaboration limits (e.g., simultaneous editors), we'll increase upgrade requests by 15%
- **Priority**: P0
- **Confidence**: Medium
- **Effort**: Medium
- **Start Date**: Nov 2025
- **Description**: Surface contextual upgrade CTAs when Viewer users attempt actions requiring Editor privileges

#### 2. Admin Approval Email Redesign
- **Status**: Fielding Experiment
- **Theme**: Request Approvals
- **Hypothesis**: By redesigning approval emails to include requester context and one-click approval, we'll improve admin response rate by 20%
- **Priority**: P1
- **Confidence**: High
- **Effort**: Small
- **Start Date**: Oct 2025
- **Description**: Streamline approval flow with improved email design showing requester activity history

#### 3. Seat Tier Comparison at Request
- **Status**: Fielding Experiment
- **Theme**: Request Volume
- **Hypothesis**: By showing Editor vs Pro Editor comparison when users request upgrades, we'll increase Pro Editor requests by 25%
- **Priority**: P0
- **Confidence**: Medium
- **Effort**: Medium
- **Start Date**: Nov 2025
- **Description**: Add comparison table at request flow to help users choose appropriate tier

#### 4. Downgrade Friction with Usage Data
- **Status**: Fielding Experiment
- **Theme**: Downgrades
- **Hypothesis**: By showing admins recent collaboration activity before confirming downgrades, we'll reduce unnecessary downgrades by 10%
- **Priority**: P0
- **Confidence**: High
- **Effort**: Large
- **Start Date**: Aug 2025
- **Description**: Add confirmation modal with 30-day usage summary when admins attempt to downgrade active users

---

## In Development (3 projects)

#### 5. Team-Based Provisioning
- **Status**: In Development
- **Theme**: Must Do
- **Priority**: P0
- **Description**: Enable admins to provision seats to entire teams at once rather than individual approvals
- **Target Release**: Q1 2026

#### 6. Usage Analytics Dashboard for Admins
- **Status**: In Development
- **Theme**: Must Do
- **Priority**: P0
- **Description**: Give admins visibility into team collaboration patterns to make better seat allocation decisions
- **Target Release**: Q1 2026

#### 7. Mobile App Seat Requests
- **Status**: In Development
- **Theme**: Request Volume
- **Priority**: P1
- **Description**: Enable users to request seat upgrades from mobile app when hitting limitations
- **Target Release**: Q2 2026

---

## In PRD/Design (5 projects)

#### 8. Peer Nomination for Upgrades
- **Status**: In PRD/Design
- **Theme**: Request Volume
- **Priority**: P0
- **Confidence**: High
- **Effort**: Large
- **Hypothesis**: By allowing Pro Editors to nominate team members for upgrades during document sharing, we'll increase request volume by 30%
- **Target Start**: Jan 2026
- **Description**: Add "Suggest upgrade" option when sharing documents with Viewer users who need editing access

#### 9. Smart Seat Recommendations
- **Status**: In PRD/Design
- **Theme**: Request Volume
- **Priority**: P1
- **Confidence**: Medium
- **Effort**: Large
- **Hypothesis**: By analyzing usage patterns and suggesting appropriate seat tiers, we'll reduce upgrade friction and improve tier selection
- **Target Start**: Q2 2026
- **Description**: ML-based recommendations shown to users based on collaboration frequency and feature usage

#### 10. Admin Dashboard Request Triage
- **Status**: In PRD/Design
- **Theme**: Request Approvals
- **Priority**: P1
- **Confidence**: Medium
- **Effort**: Medium
- **Hypothesis**: By adding bulk approval and filtering to admin dashboard, we'll improve approval throughput by 40%
- **Target Start**: Jan 2026
- **Description**: Redesign admin panel with request prioritization, bulk actions, and smart filtering

#### 11. Trial Period for Seat Requests
- **Status**: In PRD/Design
- **Theme**: Request Approvals
- **Priority**: P2
- **Confidence**: Low
- **Effort**: Large
- **Hypothesis**: By giving users 7-day trial access before requiring approval, we'll increase both requests and approvals by proving value
- **Target Start**: Q2 2026
- **Description**: Provisional access period where users can try Editor features before admin approval required

#### 12. Seat Type Education in Onboarding
- **Status**: In PRD/Design
- **Theme**: Request Volume
- **Priority**: P1
- **Confidence**: Medium
- **Effort**: Small
- **Hypothesis**: By better explaining seat types during onboarding, we'll increase appropriate upgrade requests by 20%
- **Target Start**: Jan 2026
- **Description**: Add seat tier explanation and benefits to new user onboarding flow

---

## Backlog / Needs Triage (6 ideas)

#### 13. Usage-Based Auto-Upgrades
- **Status**: Needs Triage
- **Theme**: Request Volume
- **Description**: Automatically upgrade users to paid seats after consistent usage patterns, with admin opt-in
- **Rationale**: Reduce friction for power users who should be on paid seats

#### 14. Approval Reminder Cadence
- **Status**: Needs Triage
- **Theme**: Request Approvals
- **Description**: Optimize reminder frequency for pending approval requests
- **Rationale**: Find balance between urgency and admin fatigue

#### 15. Seat Sharing for Teams
- **Status**: Needs Triage
- **Theme**: Request Volume
- **Description**: Allow teams to share a pool of Editor seats that users can claim when needed
- **Rationale**: Better utilize existing seats before requesting new ones

#### 16. Downgrade Path with Feature Retention
- **Status**: Needs Triage
- **Theme**: Downgrades
- **Description**: Offer "Editor Lite" tier to retain some paying users who would otherwise downgrade to free
- **Rationale**: Capture users between Viewer and Editor price points

#### 17. Document-Level Permissions Upgrade
- **Status**: Needs Triage
- **Theme**: Request Volume
- **Description**: Allow temporary Editor access for specific documents without full seat upgrade
- **Rationale**: Some users need editing on one doc but not organization-wide

#### 18. Admin Delegation
- **Status**: Needs Triage
- **Theme**: Request Approvals
- **Description**: Let admins delegate approval authority to team leads
- **Rationale**: Distribute approval load and improve response times

---

## Shipped Experiments (Results)

#### 19. In-App Request Button (Shipped Q4 2025)
- **Theme**: Request Volume
- **Result**: ✅ Increased request volume by 18% (target: 15%)
- **Description**: Added "Request Upgrade" button in feature limitation screens

#### 20. One-Click Email Approvals (Shipped Q3 2025)
- **Theme**: Request Approvals
- **Result**: ❌ No significant impact on approval rates (-2%, not statistically significant)
- **Description**: Added approve/deny buttons directly in email notifications

#### 21. Seat Type Badges in UI (Shipped Q3 2025)
- **Theme**: Request Volume
- **Result**: ✅ Increased upgrade awareness, 12% increase in requests (target: 10%)
- **Description**: Display user's current seat type in navigation bar with upgrade option

---

## Experiment Themes & Hypotheses

### Request Volume
**Goal**: Increase # of users requesting seat upgrades
- Make upgrade value more visible
- Reduce friction in request process
- Surface upgrades at point of need

### Request Approvals
**Goal**: Increase % of requests that admins approve
- Give admins better context
- Reduce time/effort to approve
- Surface approvals in admin workflow

### Downgrades
**Goal**: Reduce unnecessary seat downgrades
- Show usage/value before downgrade
- Offer alternative retention paths
- Create friction for harmful downgrades

### Must Do
Non-experimental work required by business/product needs

---

## Success Metrics

**North Star**: Monthly Paid Seats Added (net new)

**Supporting Metrics**:
- Request volume (requests per 1000 free users)
- Approval rate (% requests approved within 7 days)
- Time to approval (median days)
- Downgrade rate (% seats downgraded monthly)
- Seat retention (% seats retained after 6 months)

**Experiment Success Criteria**:
- Primary metric moves >5% (statistical significance)
- No regression in key guardrail metrics
- Positive qualitative feedback from users/admins
