# ============================================================
# CAREER COMPASS MCP SERVER
# Built by Melissa van den Brink-Romero
#
# What this is: an MCP server that helps people find their
# career pattern, discover roles they didn't know existed,
# and bridge the gap to companies they're drawn to.
#
# Most career tools only look at what you have DONE.
# Career Compass triangulates four dimensions:
#   - What you have done (resume / career history)
#   - Who you are (personality: Clifton Strengths, MBTI)
#   - What you want (aspirations, passions, interests)
#   - What gives you energy (and what drains it)
#
# The intersection of all four is where the real answer lives.
#
# Five tools, used in sequence:
#   1. build_profile      -- synthesize everything into one rich picture
#   2. discover_roles     -- surface roles you never thought to search
#   3. discover_companies -- find companies that match what you want
#   4. analyze_fit        -- honest gap analysis + 90-day bridge plan
#   5. generate_report    -- compile everything into one shareable document
# ============================================================

from mcp.server.fastmcp import FastMCP
from typing import Optional

# This creates the MCP server.
# "Career Compass" is the name Claude sees when it connects.
mcp = FastMCP("Career Compass")


# ============================================================
# TOOL 1: BUILD PROFILE
# ============================================================
# This is the foundation. Everything else builds on this.
# The more honestly someone fills this in, the better
# every other tool performs.

@mcp.tool()
def build_profile(
    resume_or_career_history: str,
    aspirations: str,
    passions_and_interests: str,
    what_energizes_you: str,
    what_drains_you: str,
    clifton_strengths: Optional[str] = None,
    mbti_type: Optional[str] = None,
    other_assessments: Optional[str] = None
) -> str:
    """
    The starting point for everything in Career Compass.

    Takes the full picture of who someone is, what they have done,
    and what they want, then synthesizes it into a rich career profile
    that all other tools use.

    Most career tools only look at what you have done.
    This tool triangulates four dimensions at once:
    your history, your personality, your aspirations, and your energy.

    Args:
        resume_or_career_history: Paste your resume text, or write a
                                  description of your career in your own words.
                                  Titles, companies, key achievements.

        aspirations:              Where do you want to go? What do you want
                                  your work life to feel like in 3 years?
                                  What kind of impact matters to you?
                                  Be honest, not polished.

        passions_and_interests:   What do you love, inside or outside work?
                                  What makes you lose track of time?
                                  What topics do you read about without being
                                  asked to? Include personal interests too.

        what_energizes_you:       What kinds of work tasks, interactions,
                                  or environments make you come alive?
                                  (e.g. "being the expert in the room",
                                  "teaching others", "building from zero",
                                  "solving ambiguous problems")

        what_drains_you:          What kinds of work consistently deplete you,
                                  even when you are good at them?
                                  (e.g. "repetitive execution", "heavy politics",
                                  "managing up constantly", "pure admin")

        clifton_strengths:        Optional. Your top 5 CliftonStrengths themes.
                                  (e.g. "WOO, Activator, Includer,
                                  Communicator, Significance")

        mbti_type:                Optional. Your MBTI type.
                                  (e.g. "ENTJ", "INFP", "ENFP")

        other_assessments:        Optional. Any other self-knowledge worth
                                  including: Enneagram, DISC, 360 feedback
                                  themes, things people always say about you.

    Returns:
        A rich, synthesized career profile that all other Career Compass
        tools will use as their foundation.
    """

    personality_section = ""
    if clifton_strengths:
        personality_section += f"\nCliftonStrengths top themes: {clifton_strengths}"
    if mbti_type:
        personality_section += f"\nMBTI type: {mbti_type}"
    if other_assessments:
        personality_section += f"\nOther self-knowledge: {other_assessments}"

    profile_prompt = f"""
You are a career pattern analyst with deep expertise in human psychology,
organizational behavior, and career development.

Your job is to synthesize multiple dimensions of who someone is into
one clear, honest, and specific career profile. This is not a resume summary.
This is the full human picture that most career tools never look at.

Here is the raw input. Treat each dimension seriously.

CAREER HISTORY:
{resume_or_career_history}

ASPIRATIONS (where they want to go, what they want their work to feel like):
{aspirations}

PASSIONS AND INTERESTS (what they love, what makes them lose track of time):
{passions_and_interests}

WHAT ENERGIZES THEM AT WORK:
{what_energizes_you}

WHAT DRAINS THEM, EVEN WHEN THEY ARE GOOD AT IT:
{what_drains_you}
{personality_section}

Now produce a Career Compass Profile with these six sections:

1. THE REAL EXPERTISE
   Not their job titles. What do they actually know how to DO that
   most people cannot? Find the specific capability that appears across
   multiple roles, industries, and contexts. Name it precisely.

2. THE CAREER PATTERN
   What is the consistent thread running through everything they have done?
   What problem do they solve over and over, even when the industry changes?
   This should surprise them slightly. It is never just "marketing" or "sales".

3. THE PERSONALITY FIT
   Based on their strengths, MBTI, and energy signals, what kind of
   environment, role type, and working style fits who they actually are?
   Where would they thrive vs. slowly suffocate?
   Be specific and honest, especially about the suffocation part.

4. THE ASPIRATION ALIGNMENT
   Where do their stated aspirations align with their actual skills and energy?
   Where is there tension? (e.g. they want to teach but their history shows
   they have avoided it, or they say they want stability but their pattern
   shows they always leave when things get predictable)
   Name the tensions honestly.

5. THE TRANSFERABLE EDGE
   What 5-7 specific capabilities from their background would be
   genuinely valuable in contexts they have never worked in?
   Not generic strengths. Specific, named capabilities with examples.

6. THE PROFILE IN ONE PARAGRAPH
   Write a single, sharp paragraph that captures who this person is
   professionally. This is not a LinkedIn bio. It is an honest synthesis.
   Start with their core capability, connect it to their energy and
   aspirations, and end with what kind of role would actually make them
   come alive. Write it as if you know them well.
"""

    return profile_prompt


# ============================================================
# TOOL 2: DISCOVER ROLES
# ============================================================

@mcp.tool()
def discover_roles(
    career_compass_profile: str,
    roles_already_considered: Optional[str] = None
) -> str:
    """
    Surfaces 6-8 specific job roles the person has probably not considered
    or does not know exist, matched to their full Career Compass profile.

    The key difference from a job board: this tool looks at the intersection
    of what someone has done, who they are, and what they want.
    It finds roles that fit all three, not just their resume.

    At least 3 of the 6 suggestions will be roles they have likely
    never searched for, because they did not know the title existed.

    Args:
        career_compass_profile: The output from the build_profile tool.
                                Paste the full profile here.

        roles_already_considered: Optional. Roles they have already thought
                                  about, so we do not repeat the obvious.
                                  (e.g. "Marketing Director, CMO, Brand Manager")

    Returns:
        6-8 specific role matches with reasoning, where to find them,
        and exact LinkedIn search terms.
    """

    already_considered = (
        f"\nDo not suggest these roles they have already considered: {roles_already_considered}"
        if roles_already_considered
        else ""
    )

    discovery_prompt = f"""
You are a career navigator who specializes in finding the roles people
never knew to look for. You have access to deep knowledge of the job market
across industries, including roles that have emerged in the last 5 years
that most people with traditional careers have never encountered.

Here is the person's full Career Compass Profile:
{career_compass_profile}
{already_considered}

Your job is to surface 6-8 specific roles that fit this person's
full profile, not just their resume. The role must fit:
- What they have done (skills and experience)
- Who they are (personality, working style)
- What they want (aspirations and growth direction)
- What gives them energy (not just what they are capable of)

For each role, use this exact format:

ROLE TITLE: [exact title as it appears in real job postings]

WHY YOUR SKILLS FIT:
[Connect specific experiences from their history to what this role
actually demands in practice. Not surface-level. Deep.]

WHY YOUR PERSONALITY FIT:
[Connect their Clifton Strengths, MBTI, or energy signals to what
thrives in this role. What about who they are makes this a good match?]

WHY YOUR ASPIRATIONS FIT:
[How does this role move them toward what they said they want?]

WHERE THIS ROLE EXISTS:
[What kinds of companies hire for this? Industries? Size? Ownership type?
Be specific, not generic.]

THE HIDDEN MATCH:
[The one thing from their background that makes them unusually qualified,
that most candidates will not have.]

SEARCH TERMS FOR LINKEDIN:
[Write the exact search string to find this role.]

Rules you must follow:
- Do not suggest roles they obviously already know to look for
- At least 3 of the 6 must be roles they have probably never heard of
- Every suggestion must connect to something specific in their profile
- If there is a gap to bridge, name it honestly in one sentence
"""

    return discovery_prompt


# ============================================================
# TOOL 3: DISCOVER COMPANIES
# ============================================================

@mcp.tool()
def discover_companies(
    career_compass_profile: str,
    company_type_preferences: str,
    location: str,
    industries_open_to: Optional[str] = None
) -> str:
    """
    Finds specific companies that match what someone is looking for,
    based on their full profile and stated preferences.

    Goes beyond job boards to surface companies people would never find
    by searching Indeed or LinkedIn. Especially useful for PE-backed
    mid-market companies that do not advertise heavily.

    Args:
        career_compass_profile:   The output from the build_profile tool.

        company_type_preferences: What they want in a company.
                                  (e.g. "PE-backed, mid-size, less bureaucracy,
                                  results-driven, consumer-facing")

        location:                 Location and remote preferences.
                                  (e.g. "Twin Cities metro or fully remote")

        industries_open_to:       Optional. Industries they are curious about
                                  beyond their home industry.

    Returns:
        5-7 specific companies with reasoning and a self-serve search strategy.
    """

    industries_section = (
        f"\nIndustries they are open to exploring: {industries_open_to}"
        if industries_open_to
        else ""
    )

    discovery_prompt = f"""
You are a company intelligence analyst helping someone find the employer
that fits not just their resume, but their full profile.

Here is their Career Compass Profile:
{career_compass_profile}

What they want in a company:
{company_type_preferences}

Location and remote preferences:
{location}
{industries_section}

Produce two outputs:

OUTPUT 1: SPECIFIC COMPANIES (5-7)

For each company:

COMPANY: [name]

WHY YOUR BACKGROUND FITS THEM:
[Connect specific experience or skills from their profile to a real need
this company has. Not generic. Specific. Show you understand both sides.]

WHY THEY FIT WHAT YOU WANT:
[How does this company match the size, culture, ownership type,
and energy environment they are looking for?]

THE PERSONALITY FIT:
[Based on who they are, would they thrive in this culture?
What specifically about this company's environment suits them?]

THE DOOR IN:
[What is the most natural entry point? A specific role type?
A direct approach to leadership? A mutual connection angle?
An industry event? Be specific and practical.]

OUTPUT 2: YOUR SEARCH STRATEGY

Give 3 specific methods to find more companies like these on their own:
- Exact LinkedIn search strings (write them out fully)
- Specific PE firm portfolio pages worth browsing (name the firms)
- Industry associations, directories, or databases to check

Rules:
- Prioritize companies they would never find on a job board
- PE-backed mid-market companies are high priority
- Match the company culture to their personality signals, not just their resume
"""

    return discovery_prompt


# ============================================================
# TOOL 4: ANALYZE FIT
# ============================================================

@mcp.tool()
def analyze_fit(
    career_compass_profile: str,
    company_name: str,
    target_role_type: Optional[str] = None
) -> str:
    """
    Takes a specific company and maps the person's real fit against
    what that company actually needs.

    Names the gap precisely and honestly. Then produces a specific,
    ordered 90-day bridge plan to close it.

    This tool does not sugarcoat. Knowing the exact gap is the only
    way to close it. A vague reassurance helps no one.

    Args:
        career_compass_profile: The output from build_profile.

        company_name:           The specific company to analyze fit against.

        target_role_type:       Optional. The kind of role they are targeting.
                                (e.g. "Customer Success Senior Manager",
                                "VP Marketing", "Commercial Capability Lead")

    Returns:
        Honest fit assessment, precise gap analysis, a 90-day bridge plan,
        and a kill switch signal.
    """

    role_section = (
        f"They are targeting roles like: {target_role_type}"
        if target_role_type
        else "Identify the most relevant role type based on their full profile."
    )

    fit_prompt = f"""
You are a direct, honest career advisor. Your job is not to make someone
feel good. It is to help them succeed. That means naming the truth clearly,
including the uncomfortable parts, then giving them a real plan.

Here is their full Career Compass Profile:
{career_compass_profile}

Target company: {company_name}

{role_section}

First: Draw on what you know about {company_name}. Their business model,
culture, current strategic priorities, what they value in hires, what
challenges they are working through right now. If you do not know specifics,
say so clearly and work with what you do know.

Then produce four sections:

1. THE REAL FIT
   Where does this person's full profile genuinely match what {company_name}
   needs? Look beyond the obvious resume match. Consider their personality,
   their energy, their pattern. Where is the deep fit?

2. THE HONEST GAP
   What is the actual obstacle? Name it precisely.

   Is it a:
   - Skills gap: they have not done something this role requires
   - Vocabulary gap: they cannot yet speak this industry's language
   - Network gap: they do not have relationships in this world yet
   - Credibility gap: their background looks wrong on paper even if
     they are qualified in practice
   - Culture gap: something about who they are may clash with how
     this company actually operates

   Name which type. Be specific. Do not soften it.

3. THE 90-DAY BRIDGE PLAN
   Concrete, ordered actions. Not "build your network."

   Week 1 and 2: [specific actions]
   Week 3 and 4: [specific actions]
   Month 2: [specific actions]
   Month 3: [specific actions, including when and how to approach {company_name}]

   Every action must be specific enough that they can do it tomorrow.

4. THE KILL SWITCH
   What specific signal would tell them this path is not working and
   it is time to redirect energy to a different target?
   Not a feeling. A concrete, observable signal with a timeframe.
"""

    return fit_prompt


# ============================================================
# TOOL 5: GENERATE REPORT
# ============================================================

@mcp.tool()
def generate_report(
    career_compass_profile: str,
    discovered_roles: Optional[str] = None,
    discovered_companies: Optional[str] = None,
    fit_analysis: Optional[str] = None
) -> str:
    """
    Compiles everything from the Career Compass session into one
    clean, shareable report.

    Run this at the end of a Career Compass session to pull all
    the outputs together into a single document someone can save,
    share with a coach, or return to later.

    Args:
        career_compass_profile:  The output from build_profile.

        discovered_roles:        Optional. The output from discover_roles.

        discovered_companies:    Optional. The output from discover_companies.

        fit_analysis:            Optional. The output from analyze_fit.

    Returns:
        A clean, structured Career Compass Report covering all sections
        that were completed in this session.
    """

    roles_section = (
        f"\nROLE DISCOVERIES FROM THIS SESSION:\n{discovered_roles}"
        if discovered_roles
        else ""
    )

    companies_section = (
        f"\nCOMPANY DISCOVERIES FROM THIS SESSION:\n{discovered_companies}"
        if discovered_companies
        else ""
    )

    fit_section = (
        f"\nFIT ANALYSIS FROM THIS SESSION:\n{fit_analysis}"
        if fit_analysis
        else ""
    )

    report_prompt = f"""
You are compiling a Career Compass Report for someone who has just completed
a Career Compass session. Your job is to take all the outputs and turn them
into one clean, well-structured, easy-to-read document they can save and
return to.

Here are the session outputs:

CAREER COMPASS PROFILE:
{career_compass_profile}
{roles_section}
{companies_section}
{fit_section}

Produce a complete Career Compass Report with the following structure:

CAREER COMPASS REPORT
Generated: [today's date]

SECTION 1: WHO YOU ARE
[Clean summary of the profile: real expertise, career pattern,
personality fit, and the one-paragraph synthesis]

SECTION 2: ROLES TO EXPLORE
[If role discovery was done: clean list of the recommended roles
with a one-line reason for each]

SECTION 3: COMPANIES TO TARGET
[If company discovery was done: clean list of companies with
one-line context for each and the door-in approach]

SECTION 4: YOUR FIT ANALYSIS
[If fit analysis was done: the company name, the real fit, the gap
named clearly, and the 90-day plan in condensed form]

SECTION 5: YOUR NEXT THREE ACTIONS
[Based on everything in this session, what are the three most
important things this person should do in the next 7 days?
Make these specific and ordered by priority.]

CLOSING NOTE
[One honest, direct paragraph. What did this session reveal?
What should this person hold onto as they move forward?
No generic inspiration. Something specific to them.]
"""

    return report_prompt


# ============================================================
# START THE SERVER
# ============================================================
# This runs the server when someone starts the file directly.

if __name__ == "__main__":
    mcp.run()
