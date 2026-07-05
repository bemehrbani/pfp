# PFP Campaign Manager — User Onboarding Guide

Welcome to the **People for Peace (PFP) Campaign Manager**. This guide walks you through getting started based on your role.

---

## 🔴 Admin Guide

> System administrators with full platform access.

### First Login

1. Navigate to `http://<server-ip>:8080`
2. Log in with the admin credentials provided by the system operator
3. You'll land on the **Dashboard** showing platform-wide statistics

### Key Capabilities

| Feature | Where to Find It |
|---------|-----------------|
| User management | Django Admin → Users |
| All campaigns overview | Campaigns page |
| System analytics | Analytics → System |
| Telegram bot config | Django Admin → Telegram settings |
| Database management | Django Admin (`/admin/`) |

### Setting Up the Platform

1. **Create Campaign Managers**: Django Admin → Users → Add User → Set role to `Campaign Manager`
2. **Configure Telegram Bot**: Django Admin → set the `TELEGRAM_BOT_TOKEN` environment variable
3. **Review System Health**: Visit `/api/health/` to verify all services are operational
4. **Monitor Analytics**: Dashboard shows active campaigns, user growth, and task completion rates

### Django Admin Access

Access the Django admin panel at `/admin/` for direct database management:
- Create/edit users and assign roles
- Manage campaigns directly
- View activity logs
- Configure system settings

---

## 🟡 Campaign Manager Guide

> Create and manage peace-building campaigns, assign tasks, and coordinate volunteers.

### Getting Started

1. Log in at `http://<server-ip>:8080`
2. Your Dashboard shows **your campaigns**, task progress, and volunteer activity
3. Click **Campaigns** in the sidebar to manage your campaigns

### Creating a Campaign

1. Go to **Campaigns** → **Create Campaign**
2. Fill in:
   - **Name**: A clear, compelling campaign title
   - **Description**: What the campaign aims to achieve
   - **Category**: Select the most fitting category
   - **Start/End Dates**: Campaign duration
   - **Targets**: Set member, activity, and social media post targets
   - **Region**: Where the campaign operates
3. Click **Create** to publish

### Managing Tasks

1. Navigate to your campaign → **Tasks** tab
2. Click **Create Task** to add work items:
   - **Title**: Clear action item (e.g., "Share campaign on Twitter")
   - **Task Type**: Social Media, Outreach, Content Creation, etc.
   - **Points**: Reward value for completion
   - **Priority**: Low / Medium / High / Urgent
   - **Deadline**: When the task should be completed
3. Tasks appear in the volunteer's task list once assigned

### Tracking Progress

- **Campaign Analytics**: Click on any campaign → **Analytics** tab
  - Member recruitment progress vs. target
  - Activity completion rates
  - Top-performing volunteers
  - Task type distribution
- **Dashboard**: Quick overview of all your campaigns' health

### Volunteer Coordination

- View volunteers assigned to your campaigns
- Review submitted task proofs before verifying
- Award points upon task verification
- Use the activity feed to monitor real-time progress

---

## 🟢 Volunteer Guide

> Browse campaigns, pick up tasks, submit proof, and earn points.

### Getting Started

1. Log in at `http://<server-ip>:8080`
2. Your Dashboard shows:
   - **My Tasks**: Tasks assigned to you
   - **Points Earned**: Your total reward points
   - **Active Campaigns**: Campaigns you've joined

### Joining a Campaign

1. Go to **Campaigns** in the sidebar
2. Browse available campaigns
3. Click on a campaign to see its details:
   - Description and goals
   - Available tasks
   - Current progress
4. Click **Join Campaign** to become a volunteer

### Completing Tasks

1. Go to **Tasks** in the sidebar (or find tasks within a campaign)
2. You'll see tabs:
   - **Available**: Tasks you can pick up
   - **In Progress**: Tasks you're working on
   - **Completed**: Tasks you've finished
3. Click on a task to view details
4. Click **Accept Task** to start working on it
5. Once complete, click **Submit Proof** and provide evidence (photo, link, or description)
6. Wait for a Campaign Manager to verify your submission

### Earning Points

- Each task has a **point value** visible before you accept it
- Points are awarded after a Campaign Manager **verifies** your submission
- Track your total points on the Dashboard
- Higher-point tasks typically require more effort

### Tips for Success

- **Start with low-point tasks** to learn the platform
- **Check deadlines** — tasks may expire if not completed in time
- **Provide clear proof** — screenshots, links, or photos help managers verify quickly
- **Stay active** — campaign managers can see your activity history

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|---------|
| Can't log in | Contact your admin to verify credentials |
| Page not loading | Check if the server is running (ask admin) |
| Task submission rejected | Review the task requirements and resubmit with clearer proof |
| Dashboard shows no data | You may not be assigned to any campaigns yet |

---

## API Access (Advanced Users)

The platform exposes a REST API:

- **API Docs**: `/swagger/` (Swagger UI) or `/redoc/` (ReDoc)
- **Auth**: POST `/api/auth/login/` with `{"username": "...", "password": "..."}` → returns JWT token
- **Campaigns**: GET/POST `/api/campaigns/`
- **Tasks**: GET/POST `/api/tasks/`
- **Analytics**: GET `/api/analytics/dashboard-stats/`

Include the JWT token in the `Authorization: Bearer <token>` header for authenticated requests.
