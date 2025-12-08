import os
import django
from fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Initialise Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference3IA2.settings")
django.setup()

from ConferenceApp.models import Conference
from SessionApp.models import Session

# Create MCP server
mcp = FastMCP("Conference Assistant")


# a) Lister toutes les conférences
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    @sync_to_async
    def _get_conferences():
        return list(Conference.objects.all())

    conferences = await _get_conferences()

    if not conferences:
        return "No conferences found."

    return "\n".join(
        [f"- {c.name} ({c.start_date} to {c.end_date})" for c in conferences]
    )


# b) Détails d'une conférence par nom
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""

    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    conference = await _get_conference()

    if conference == "MULTIPLE":
        return (
            f"Multiple conferences found matching '{name}'. "
            "Please be more specific."
        )

    if not conference:
        return f"Conference '{name}' not found."

    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )


# c) Lister les sessions d'une conférence
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""

    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(
                name__icontains=conference_name
            )
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    result, conference = await _get_sessions()

    if result == "MULTIPLE":
        return (
            f"Multiple conferences found matching '{conference_name}'. "
            "Please be more specific."
        )

    if conference is None:
        return f"Conference '{conference_name}' not found."

    sessions = result
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."

    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    return "\n".join(session_list)


# d) Tool libre : filtrer les conférences par thème
@mcp.tool()
async def conferences_by_theme(theme: str) -> str:
    """
    List conferences filtered by theme (e.g. 'IA', 'Security', 'Cloud').
    """
    @sync_to_async
    def _get_conferences():
        # on filtre sur le champ theme (ou theme__icontains si tu veux partiel)
        return list(Conference.objects.filter(theme__icontains=theme))

    conferences = await _get_conferences()

    if not conferences:
        return f"No conferences found with theme matching '{theme}'."

    lines = [f"Conferences with theme '{theme}':"]
    for c in conferences:
        lines.append(
            f"- {c.name} ({c.start_date} to {c.end_date}) in {c.location}"
        )

    return "\n".join(lines)


# Lancement du serveur MCP
if __name__ == "__main__":
    mcp.run(transport="stdio")
