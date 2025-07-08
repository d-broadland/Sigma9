from dataclasses import dataclass, field
from typing import Dict, List, Optional
from api.index import TheShowAPI

api = TheShowAPI()

@dataclass
class LineupCard:
    name: str
    ovr: int
    position: str
    bats: str  # R, L, or S
    team: str
    quirks: List[str]
    stats: Dict[str, int]
    is_boosted_by_royce: bool = False
    is_boosted_by_kaat: bool = False
    boosted_stats: Dict[str, int] = field(default_factory=dict)

def fetch_card_by_name_and_ovr(name: str, ovr: int) -> Optional[Dict]:
    for item in api.iter_inventory("mlb_card"):
        if name.lower() in item.get("name", "").lower() and item.get("overall") == ovr:
            return item
    return None

def build_lineup_card(name: str, ovr: int, position: str, bats: str) -> LineupCard:
    raw = fetch_card_by_name_and_ovr(name, ovr)
    if not raw:
        raise ValueError(f"Card not found: {name} {ovr}")

    team = raw.get("team", "")
    quirks = raw.get("quirks", [])
    stats = raw.get("attributes", {})

    is_twins = team == "Minnesota Twins"
    under_95 = ovr <= 95

    is_boosted_by_royce = is_twins and under_95
    is_boosted_by_kaat = is_twins and under_95

    boosted_stats = stats.copy()

    if is_boosted_by_royce:
        for k in ("power_r", "power_l", "plate_vision"):
            boosted_stats[k] = boosted_stats.get(k, 0) + 8
    if is_boosted_by_kaat:
        for k in ("contact_r", "contact_l", "clutch"):
            boosted_stats[k] = boosted_stats.get(k, 0) + 8

    return LineupCard(
        name=name,
        ovr=ovr,
        position=position,
        bats=bats,
        team=team,
        quirks=quirks,
        stats=stats,
        is_boosted_by_royce=is_boosted_by_royce,
        is_boosted_by_kaat=is_boosted_by_kaat,
        boosted_stats=boosted_stats,
    )

def build_full_lineup() -> List[LineupCard]:
    raw_lineup = [
        ("Byron Buxton", 92, "CF", "R"),
        ("Joe Mauer", 96, "C", "L"),
        ("Royce Lewis", 91, "3B", "R"),
        ("Kody Clemens", 92, "1B", "L"),
        ("Brian Dozier", 93, "DH", "R"),
        ("Carlos Correa", 89, "2B", "R"),
        ("Willi Castro", 92, "SS", "S"),
        ("Harrison Bader", 91, "LF", "R"),
        ("Matt Wallner", 75, "RF", "L"),
    ]

    return [build_lineup_card(*entry) for entry in raw_lineup]


# Test block to print the full lineup in markdown format
if __name__ == "__main__":
    lineup = build_full_lineup()
    print("# 📋 Boosted Lineup Scroll\n")
    for card in lineup:
        print(f"### {card.name} ({card.ovr}) — {card.position}")
        print(f"- **Bats:** {card.bats}")
        print(f"- **Team:** {card.team}")
        print(f"- **Boosted by Royce:** {'✅' if card.is_boosted_by_royce else '❌'}")
        print(f"- **Boosted by Kaat:** {'✅' if card.is_boosted_by_kaat else '❌'}")
        print(f"- **Base Stats:** `{card.stats}`")
        print(f"- **Boosted Stats:** `{card.boosted_stats}`\n")
