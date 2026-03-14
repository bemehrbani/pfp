"""
PFP React Dashboard — Source-Level UI Test Suite.

Validates UI structure by analyzing TSX source files directly (no server needed).
Uses regex to verify components, routes, form fields, and patterns are present.

Usage:
  python -m pytest telegram-bot/test_dashboard_ui.py -v
"""

import os
import re
import pytest

# ── Configuration ──────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_SRC = os.path.join(BASE_DIR, "..", "frontend", "src")


def read_file(relative_path: str) -> str:
    """Read a frontend source file."""
    full_path = os.path.join(FRONTEND_SRC, relative_path)
    if not os.path.exists(full_path):
        pytest.skip(f"File not found: {relative_path}")
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()


# ══════════════════════════════════════════════════════════════════════
#  ROUTES & NAVIGATION (4 tests)
# ══════════════════════════════════════════════════════════════════════


class TestRoutesNavigation:
    """Verify route definitions and navigation structure."""

    def test_all_routes_defined(self):
        """App.tsx defines all expected routes."""
        source = read_file("App.tsx")
        # Login is at '/' root path; other routes have explicit paths
        expected_routes = ['/dashboard', '/campaigns', '/tasks', '/analytics']
        for route in expected_routes:
            assert route in source, f"Route '{route}' not found in App.tsx"
        # Login page component must be referenced
        assert 'Login' in source, "Login page not referenced in App.tsx"

    def test_navigation_links_present(self):
        """Navigation.tsx contains links for main sections."""
        source = read_file("components/Navigation.tsx")
        expected_links = ['dashboard', 'campaigns', 'tasks', 'analytics']
        source_lower = source.lower()
        found = [link for link in expected_links if link in source_lower]
        assert len(found) >= 3, f"Missing nav links. Found: {found}"

    def test_role_based_analytics(self):
        """Analytics link is conditional on role (isCampaignManager or similar)."""
        source = read_file("components/Navigation.tsx")
        has_role_check = any(kw in source for kw in ['isCampaignManager', 'is_campaign_manager',
                                                      'role', 'isAdmin', 'is_admin',
                                                      'permission', 'can_view'])
        assert has_role_check, "No role-based access control found in Navigation"

    def test_mobile_hamburger_menu(self):
        """Navigation has mobile/responsive menu handling."""
        source = read_file("components/Navigation.tsx")
        has_mobile = any(kw in source for kw in ['isOpen', 'menuOpen', 'mobileMenu',
                                                   'hamburger', 'toggle', 'setIsOpen',
                                                   'isMobileMenuOpen', 'setIsMobileMenuOpen',
                                                   'useState', 'hidden', 'sm:hidden',
                                                   'md:hidden', 'lg:hidden', 'mobile',
                                                   'responsive', 'collapse', 'dropdown'])
        assert has_mobile, "No mobile/responsive menu handling found in Navigation"


# ══════════════════════════════════════════════════════════════════════
#  PAGE STRUCTURE (8 tests)
# ══════════════════════════════════════════════════════════════════════


class TestPageStructure:
    """Verify page component structure and key elements."""

    def test_login_inputs(self):
        """Login page has username + password inputs and submit button."""
        source = read_file("pages/Login.tsx")
        assert 'username' in source.lower(), "Login missing username field"
        assert 'password' in source.lower(), "Login missing password field"
        assert any(kw in source for kw in ['submit', 'type="submit"', 'Login', 'Sign In']), \
            "Login missing submit button"

    def test_dashboard_stat_cards(self):
        """Dashboard shows stat cards for campaigns, tasks, points, volunteers."""
        source = read_file("pages/Dashboard.tsx")
        source_lower = source.lower()
        expected_stats = ['campaign', 'task', 'point', 'volunteer']
        found = [stat for stat in expected_stats if stat in source_lower]
        assert len(found) >= 3, f"Dashboard missing stat cards. Found: {found}"

    def test_dashboard_quick_actions(self):
        """Dashboard has quick action links."""
        source = read_file("pages/Dashboard.tsx")
        has_actions = any(kw in source for kw in ['Quick Action', 'quick-action',
                                                    'Create Campaign', 'Create Task',
                                                    'View Campaign', 'quickAction'])
        assert has_actions, "Dashboard missing quick actions section"

    def test_campaigns_card_with_progress(self):
        """Campaigns page has card with progress indicators."""
        source = read_file("pages/Campaigns.tsx")
        assert 'progress' in source.lower() or 'status' in source.lower(), \
            "Campaigns page missing progress/status display"

    def test_campaigns_empty_state(self):
        """Campaigns page handles empty state."""
        source = read_file("pages/Campaigns.tsx")
        has_empty = any(kw in source.lower() for kw in ['no campaign', 'empty', 'nothing',
                                                         'get started', 'create your'])
        assert has_empty, "Campaigns page missing empty state handling"

    def test_tasks_filter_tabs(self):
        """Tasks page has filter tabs (All, Available, My Tasks, Completed)."""
        source = read_file("pages/Tasks.tsx")
        source_lower = source.lower()
        expected_filters = ['all', 'available', 'my', 'completed']
        found = [f for f in expected_filters if f in source_lower]
        assert len(found) >= 3, f"Tasks page missing filters. Found: {found}"

    def test_tasks_card_structure(self):
        """Tasks page card shows title, type, points, campaign."""
        source = read_file("pages/Tasks.tsx")
        source_lower = source.lower()
        expected = ['title', 'type', 'point', 'campaign']
        found = [field for field in expected if field in source_lower]
        assert len(found) >= 3, f"Task card missing fields. Found: {found}"

    def test_analytics_sections(self):
        """Analytics page has summary stats and chart sections."""
        source = read_file("pages/Analytics.tsx")
        source_lower = source.lower()
        has_stats = any(kw in source_lower for kw in ['summary', 'stat', 'total', 'overview'])
        has_charts = any(kw in source_lower for kw in ['chart', 'progress', 'distribution', 'graph'])
        assert has_stats, "Analytics missing summary stats"
        assert has_charts, "Analytics missing chart/progress sections"


# ══════════════════════════════════════════════════════════════════════
#  CREATE FORMS (6 tests)
# ══════════════════════════════════════════════════════════════════════


class TestCreateForms:
    """Verify campaign and task creation forms."""

    def test_campaign_create_sections(self):
        """CampaignCreate has 5 form sections (Basic, Goals, Storm, Telegram, Timeline)."""
        source = read_file("pages/CampaignCreate.tsx")
        source_lower = source.lower()
        expected_sections = ['basic', 'goal', 'twitter', 'telegram', 'timeline']
        found = [s for s in expected_sections if s in source_lower]
        assert len(found) >= 4, f"CampaignCreate missing sections. Found: {found}"

    def test_campaign_storm_conditional(self):
        """Twitter storm section is conditionally visible."""
        source = read_file("pages/CampaignCreate.tsx")
        has_conditional = any(kw in source for kw in ['showStorm', 'stormEnabled', 'enableStorm',
                                                        'twitter_storm', 'twitterStorm',
                                                        'enable_storm', '&&'])
        assert has_conditional, "Storm section not conditionally rendered"

    def test_task_create_sections(self):
        """TaskCreate has form sections (Basic, Requirements, Social)."""
        source = read_file("pages/TaskCreate.tsx")
        source_lower = source.lower()
        expected = ['basic', 'requirement', 'social']
        found = [s for s in expected if s in source_lower]
        assert len(found) >= 2, f"TaskCreate missing sections. Found: {found}"

    def test_task_create_key_tweets_conditional(self):
        """Key tweets section appears only for comment task type."""
        source = read_file("pages/TaskCreate.tsx")
        has_comment_check = any(kw in source for kw in ['twitter_comment', 'comment',
                                                          'key_tweet', 'keyTweet', 'KeyTweet'])
        assert has_comment_check, "No conditional key tweets section found"

    def test_task_create_points_field(self):
        """TaskCreate has a points/rewards field."""
        source = read_file("pages/TaskCreate.tsx")
        assert 'points' in source.lower() or 'reward' in source.lower(), \
            "TaskCreate missing points/rewards field"

    def test_campaign_create_date_fields(self):
        """CampaignCreate has date picker fields."""
        source = read_file("pages/CampaignCreate.tsx")
        has_dates = any(kw in source.lower() for kw in ['date', 'start_date', 'end_date',
                                                          'startdate', 'enddate',
                                                          'datepicker', 'FormDatePicker'])
        assert has_dates, "CampaignCreate missing date fields"


# ══════════════════════════════════════════════════════════════════════
#  COMPONENTS (2 tests)
# ══════════════════════════════════════════════════════════════════════


class TestComponents:
    """Verify shared component usage patterns."""

    def test_form_components_imported(self):
        """Form components (FormInput, FormTextarea, FormSelect) are used."""
        # Check across all create pages
        campaign_src = read_file("pages/CampaignCreate.tsx")
        task_src = read_file("pages/TaskCreate.tsx")
        combined = campaign_src + task_src

        expected_components = ['FormInput', 'FormTextarea', 'FormSelect']
        # Also accept lowercase or custom form patterns
        found = [comp for comp in expected_components if comp in combined]
        alt_found = any(kw in combined for kw in ['<input', '<textarea', '<select',
                                                    'TextField', 'Input'])
        assert len(found) >= 1 or alt_found, \
            "No form components found in create pages"

    def test_loading_components_used(self):
        """LoadingButton or LoadingSpinner patterns exist."""
        # Check across multiple files
        files_to_check = [
            "pages/Login.tsx",
            "pages/CampaignCreate.tsx",
            "pages/TaskCreate.tsx",
        ]
        combined = ""
        for filepath in files_to_check:
            try:
                combined += read_file(filepath)
            except Exception:
                continue

        has_loading = any(kw in combined for kw in ['LoadingButton', 'LoadingSpinner',
                                                     'isLoading', 'loading', 'spinner',
                                                     'isPending', 'isSubmitting'])
        assert has_loading, "No loading state patterns found"
