#!/bin/bash
# fix-deepseek-wrapper.sh - Idempotent script to update DeepSeek Claude wrapper with optimal settings
# Author: Claude Code Assistant
# Date: 2026-03-04

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 DeepSeek Wrapper Fix Script${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if running with sudo privileges
if [[ $EUID -ne 0 ]]; then
    echo -e "${YELLOW}⚠️  This script requires sudo privileges to modify /usr/local/bin${NC}"
    echo -e "Please run with: ${GREEN}sudo bash $0${NC}"
    exit 1
fi

WRAPPER_PATH="/usr/local/bin/deepseek-claude"
BACKUP_DIR="/usr/local/bin/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_PATH="${BACKUP_DIR}/deepseek-claude.backup.${TIMESTAMP}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Define the new wrapper content
NEW_WRAPPER_CONTENT='#!/bin/bash
# DeepSeek Claude Wrapper - Optimized for 131k token limit
# Updated: 2026-03-04

# Your API key
export DEEPSEEK_API_KEY="sk-ab95b69cfd9348f19ffd3cdd13f168d2"

# Core API configuration - Updated endpoint
export ANTHROPIC_BASE_URL="https://api.deepseek.com/v1"
export ANTHROPIC_AUTH_TOKEN="$DEEPSEEK_API_KEY"
export ANTHROPIC_MODEL="deepseek-chat"

# ===== CRITICAL FIX: Token Management =====
# DeepSeek maximum context is 131,072 tokens
export ANTHROPIC_MAX_TOKENS="8192"           # Limit output to 8k tokens
export ANTHROPIC_COMPACT_THRESHOLD="70"      # Auto-compact at 70% usage
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE="70"  # Same as above for Claude Code

# Claude Code specific optimizations
export CLAUDE_CODE_MAX_OUTPUT_TOKENS="8192"  # Match the above
export MAX_THINKING_TOKENS="4096"            # Limit thinking tokens

# Prevent timeouts on long responses
export API_TIMEOUT_MS="600000"  # 10 minutes
export ANTHROPIC_TIMEOUT_MS="600000"

# Disable non-essential traffic to maximize context
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"

# Context monitoring warning (calculated based on typical token counts)
export CLAUDE_CODE_CONTEXT_WARNING_THRESHOLD="80"

# Display configuration
echo "🔧 DeepSeek Professional Configuration"
echo "========================================"
echo "📡 Model: DeepSeek-V3.1 (131k context)"
echo "📤 Max Output: 8,192 tokens (saves ~24k for conversation)"
echo "🔄 Auto-compact at: 70% of limit"
echo "⚠️  Context warning at: 80% usage"
echo "⏱️  Timeout: 10 minutes"
echo "========================================"
echo -e "💡 ${YELLOW}Tip: Use /save command in Claude Code to save your session${NC}"
echo ""

# Run Claude with all arguments
exec claude "$@"
'

# Function to compare existing wrapper with desired content
wrapper_needs_update() {
    local existing_content
    if [[ ! -f "$WRAPPER_PATH" ]]; then
        return 0  # File doesn't exist, needs creation
    fi

    existing_content=$(cat "$WRAPPER_PATH" 2>/dev/null || true)
    if [[ "$existing_content" == "$NEW_WRAPPER_CONTENT" ]]; then
        return 1  # Content matches, no update needed
    else
        return 0  # Content differs, needs update
    fi
}

# Check if update is needed
if wrapper_needs_update; then
    echo -e "${YELLOW}📦 Backing up existing wrapper...${NC}"
    cp "$WRAPPER_PATH" "$BACKUP_PATH" 2>/dev/null || echo -e "${YELLOW}No existing wrapper to backup${NC}"
    echo -e "Backup saved to: ${GREEN}$BACKUP_PATH${NC}"

    echo -e "${YELLOW}✏️  Writing new wrapper...${NC}"
    echo "$NEW_WRAPPER_CONTENT" > "$WRAPPER_PATH"
    chmod +x "$WRAPPER_PATH"

    echo -e "${GREEN}✅ Wrapper updated successfully!${NC}"
else
    echo -e "${GREEN}✅ Wrapper already up-to-date. No changes needed.${NC}"
fi

# Display verification
echo -e "\n${BLUE}📋 Verification:${NC}"
ls -la "$WRAPPER_PATH"
echo -e "\n${BLUE}📄 First 10 lines of wrapper:${NC}"
head -10 "$WRAPPER_PATH"

# Create session helper script
SESSION_HELPER_PATH="/usr/local/bin/deepseek-session-helper"
SESSION_HELPER_CONTENT='#!/bin/bash
# DeepSeek Session Helper - Tips for managing long conversations
# This script provides guidance on saving and managing Claude Code sessions

echo "🔧 DeepSeek Session Management Helper"
echo "========================================"
echo ""
echo "📚 SESSION SAVING OPTIONS:"
echo "1. In Claude Code, use: /save"
echo "   Saves current conversation to a file"
echo ""
echo "2. Manual save:"
echo "   Copy conversation text and paste into a text file"
echo ""
echo "3. Reset context when approaching limits:"
echo "   Use /clear or start a new conversation"
echo ""
echo "⚠️  WARNING SIGNS OF CONTEXT LIMIT:"
echo "   - API errors about token limits"
echo "   - Slow response times"
echo "   - Truncated responses"
echo ""
echo "🔄 RECOMMENDED WORKFLOW:"
echo "   - Save important work every 50-60k tokens"
echo "   - Use /save before complex operations"
echo "   - Consider splitting long conversations into multiple sessions"
echo "========================================"
'

echo -e "\n${YELLOW}📝 Creating session helper script...${NC}"
echo "$SESSION_HELPER_CONTENT" > "$SESSION_HELPER_PATH"
chmod +x "$SESSION_HELPER_PATH"
echo -e "Helper script created: ${GREEN}$SESSION_HELPER_PATH${NC}"
echo -e "Run with: ${GREEN}deepseek-session-helper${NC}"

# Summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Your DeepSeek wrapper has been optimized with:"
echo -e "  • ${GREEN}8k output tokens${NC} (was 32k)"
echo -e "  • ${GREEN}70% auto-compact threshold${NC}"
echo -e "  • ${GREEN}Correct API endpoint${NC} (api.deepseek.com/v1)"
echo -e "  • ${GREEN}Context warning at 80% usage${NC}"
echo -e "  • ${GREEN}Session helper script${NC}"
echo -e "\nNext time you run ${GREEN}deepseek-claude${NC}, the new settings will apply."
echo -e "\n${YELLOW}⚠️  Important:${NC} If you still encounter token limit errors,"
echo -e "consider using ${GREEN}/save${NC} more frequently or starting a new session."
echo -e "\n${BLUE}For help: deepseek-session-helper${NC}"