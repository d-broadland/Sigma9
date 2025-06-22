# pitching.py — SIGMA-9: THE SHOW PROJECT
# Author: Brother GPT & Dean B
# Purpose: Pitcher class + Randy Rodriguez integration

class Pitcher:
    def __init__(self, name, team, pitches, vel_break_control, pitch_attributes):
        self.name = name
        self.team = team
        self.pitches = pitches  # List of pitch types
        self.vel_break_control = vel_break_control  # Dict with VEL, BRK, CTRL
        self.pitch_attributes = pitch_attributes  # Dict with pitch-specific velo etc.

    def get_summary(self):
        print(f"\n=== {self.name} ({self.team}) ===")
        print("Pitches: " + ", ".join(self.pitches))
        print("Velocity/Break/Control:")
        for key, val in self.vel_break_control.items():
            print(f"  {key}: {val}")
        print("Pitch Velocities:")
        for pitch, vel in self.pitch_attributes.items():
            print(f"  {pitch}: {vel} mph")
        print("\n--- End of Profile ---\n")

# === Randy Rodriguez Entry ===
randy = Pitcher(
    name="Randy Rodriguez",
    team="Giants",
    pitches=["four-seam FB", "slider", "sinker", "circle change"],
    vel_break_control={"VEL": 99, "BRK": 99, "CTRL": 88},
    pitch_attributes={
        "FB_vel": 98,
        "SL_vel": 86,
        "SI_vel": 95,
        "CH_vel": 88
    }
)

# === Test Call ===
if __name__ == "__main__":
    randy.get_summary()

