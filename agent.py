# ============================================================
# CAREER COMPASS AGENT
# Built by Melissa van den Brink-Romero
#
# What this does:
# This agent runs all five Career Compass tools automatically,
# in the right order, without you having to prompt each step.
#
# You answer questions about your background once.
# It handles the rest and saves a full report to your computer.
#
# How to run it:
# 1. Open Terminal (Mac) or Command Prompt (Windows)
# 2. Navigate to this folder
# 3. Type: python agent.py
# 4. Answer the questions
# 5. Find your report saved as a .txt file in the same folder
# ============================================================


# "import" means: go borrow this tool from somewhere else
# Think of it like pulling ingredients off a shelf before cooking

import os                          # lets us read things saved on your computer
from datetime import datetime      # lets us add today's date to the report filename

# anthropic is the official Python package for talking to Claude via the API
# This is what uses your API key and sends/receives messages
import anthropic

# These are OUR five tools, borrowed from the server.py file we already built
# "from server import" means: go into server.py and bring me these five functions
from server import (
    build_profile,
    discover_roles,
    discover_companies,
    analyze_fit,
    generate_report
)


# ============================================================
# THE MESSENGER FUNCTION
# ============================================================
# This small function does one job: send a prompt to Claude
# and bring back the answer.
#
# Every tool we built (build_profile, discover_roles, etc.)
# produces a prompt (a set of instructions for Claude).
# This function is what actually runs that prompt through Claude
# and returns the result.

def call_claude(client, prompt):
    """Send a prompt to Claude and return the response."""

    message = client.messages.create(
        model="claude-sonnet-4-6",   # the Claude model doing the thinking
        max_tokens=4096,             # maximum length of the response
                                     # 4096 tokens is roughly 3,000 words
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # message.content is a list, [0] gets the first item, .text gets the words
    return message.content[0].text


# ============================================================
# THE MAIN AGENT FUNCTION
# ============================================================
# This is the agent. It collects your information,
# runs all five tools in sequence, and saves your report.

def run_career_compass():

    # ── Get your API key ──────────────────────────────────────
    # First we check if you have stored your API key on your computer
    # as an environment variable (the secure way).
    # If not, we simply ask you to type it in.
    #
    # To store it securely on Mac, open Terminal and type:
    # export ANTHROPIC_API_KEY="your-key-here"
    # Then run this script in the same Terminal window.

    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("\nNo API key found in environment.")
        api_key = input("Paste your Anthropic API key here: ").strip()

    # This opens the connection to Claude using your API key
    client = anthropic.Anthropic(api_key=api_key)

    # ── Welcome ───────────────────────────────────────────────
    print("\n")
    print("=" * 60)
    print("  CAREER COMPASS")
    print("  Your personal career intelligence session")
    print("=" * 60)
    print("\nTake your time with each answer.")
    print("The more honest you are, the better the results.\n")

    # ── Collect your information ──────────────────────────────
    # The agent asks you questions one at a time.
    # Your answers become the input for build_profile.

    print("─" * 60)
    print("STEP 1 OF 6: YOUR BACKGROUND")
    print("─" * 60)
    resume = input(
        "\nPaste your resume text, or describe your career history\n"
        "in your own words. Include roles, companies, achievements.\n\n> "
    )

    print("\n─" * 60)
    print("STEP 2 OF 6: WHERE YOU WANT TO GO")
    print("─" * 60)
    aspirations = input(
        "\nWhat do you want your work life to feel like in 3 years?\n"
        "What kind of impact matters to you?\n"
        "Be honest, not polished.\n\n> "
    )

    print("\n─" * 60)
    print("STEP 3 OF 6: WHAT YOU LOVE")
    print("─" * 60)
    passions = input(
        "\nWhat are your passions and interests, inside and outside work?\n"
        "What makes you lose track of time?\n"
        "Include personal interests too.\n\n> "
    )

    print("\n─" * 60)
    print("STEP 4 OF 6: YOUR ENERGY")
    print("─" * 60)
    energizers = input(
        "\nWhat kinds of work, interactions, or environments make you come alive?\n"
        "(e.g. being the expert in the room, teaching others, building from zero)\n\n> "
    )

    drains = input(
        "\nWhat consistently depletes you, even when you are good at it?\n"
        "(e.g. heavy politics, repetitive execution, managing up constantly)\n\n> "
    )

    print("\n─" * 60)
    print("STEP 5 OF 6: WHO YOU ARE (optional)")
    print("─" * 60)
    print("Press Enter to skip any of these.\n")

    clifton = input(
        "Clifton Strengths top themes:\n> "
    ).strip() or None

    mbti = input(
        "\nMBTI type (e.g. ENTJ, INFP):\n> "
    ).strip() or None

    other = input(
        "\nAny other self-knowledge? Enneagram, colors, 360 feedback,\n"
        "things people always say about you:\n> "
    ).strip() or None

    print("\n─" * 60)
    print("STEP 6 OF 6: WHAT YOU ARE LOOKING FOR")
    print("─" * 60)

    company_prefs = input(
        "\nDescribe the type of company you want.\n"
        "(e.g. PE-backed, mid-size, less bureaucracy, consumer-facing)\n\n> "
    )

    location = input(
        "\nLocation and remote preferences:\n"
        "(e.g. Twin Cities metro or fully remote)\n\n> "
    )

    industries = input(
        "\nAny industries you are curious about beyond your home industry?\n"
        "Press Enter to skip.\n\n> "
    ).strip() or None

    target_company = input(
        "\nIs there a specific company you are drawn to?\n"
        "The agent will analyze your fit and give you a 90-day bridge plan.\n"
        "Press Enter to skip.\n\n> "
    ).strip() or None

    target_role = None
    if target_company:
        target_role = input(
            f"\nWhat kind of role are you interested in at {target_company}?\n"
            "Press Enter to let the agent decide.\n\n> "
        ).strip() or None

    # ── Run the tools ─────────────────────────────────────────
    # This is where the agent takes over.
    # Each step calls a tool, sends the prompt to Claude,
    # gets the result, and passes it into the next step.

    print("\n")
    print("=" * 60)
    print("  CAREER COMPASS IS RUNNING")
    print("  This takes about 2 minutes. Grab a coffee.")
    print("=" * 60)

    # Step 1: Build the full profile from everything you told us
    print("\n[1/5] Building your Career Compass profile...")
    profile_prompt = build_profile(
        resume_or_career_history=resume,
        aspirations=aspirations,
        passions_and_interests=passions,
        what_energizes_you=energizers,
        what_drains_you=drains,
        clifton_strengths=clifton,
        mbti_type=mbti,
        other_assessments=other
    )
    profile = call_claude(client, profile_prompt)
    print("    Done.")

    # Step 2: Discover roles using the full profile
    print("\n[2/5] Discovering roles you have probably never considered...")
    roles_prompt = discover_roles(
        career_compass_profile=profile
    )
    roles = call_claude(client, roles_prompt)
    print("    Done.")

    # Step 3: Find companies that match
    print("\n[3/5] Finding companies that match what you want...")
    companies_prompt = discover_companies(
        career_compass_profile=profile,
        company_type_preferences=company_prefs,
        location=location,
        industries_open_to=industries
    )
    companies = call_claude(client, companies_prompt)
    print("    Done.")

    # Step 4: Analyze fit with a specific company (if named)
    fit = None
    if target_company:
        print(f"\n[4/5] Analyzing your real fit with {target_company}...")
        fit_prompt = analyze_fit(
            career_compass_profile=profile,
            company_name=target_company,
            target_role_type=target_role
        )
        fit = call_claude(client, fit_prompt)
        print("    Done.")
    else:
        print("\n[4/5] No target company named. Skipping fit analysis.")

    # Step 5: Compile everything into a final report
    print("\n[5/5] Generating your Career Compass Report...")
    report_prompt = generate_report(
        career_compass_profile=profile,
        discovered_roles=roles,
        discovered_companies=companies,
        fit_analysis=fit
    )
    report = call_claude(client, report_prompt)
    print("    Done.")

    # ── Save the report ───────────────────────────────────────
    # The report saves as a .txt file in the same folder as this script.
    # The filename includes today's date and time so you can run it
    # multiple times without overwriting previous reports.

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"career_compass_report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("CAREER COMPASS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(report)

    # ── Done ──────────────────────────────────────────────────
    print("\n")
    print("=" * 60)
    print("  YOUR CAREER COMPASS REPORT IS READY")
    print(f"  Saved as: {filename}")
    print("  It is in the same folder as this script.")
    print("=" * 60)
    print("\nHere is a preview of the first section:\n")
    print(report[:600])
    print("\n[...full report saved to file]\n")


# ============================================================
# START HERE
# ============================================================
# This runs the agent when you type: python agent.py
# "if __name__ == '__main__'" means: only run this if someone
# is starting this file directly, not importing it elsewhere.

if __name__ == "__main__":
    run_career_compass()
