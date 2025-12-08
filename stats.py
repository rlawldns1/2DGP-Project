class Stats:
    def __init__(self, max_hp, attack, defense):
        self.max_hp = max_hp
        self.cur_hp = max_hp
        self.attack = attack
        self.defense = defense

    def set_stats(self, max_hp, attack, defense):
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.cur_hp = max_hp


    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.cur_hp = max(0, self.cur_hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.cur_hp > 0

    def heal(self, amount):
        self.cur_hp = min(self.max_hp, self.cur_hp + amount)

    def full_heal(self):
        self.cur_hp = self.max_hp

    def upgrade_hp(self, amount = 20):
        self.max_hp += amount
        self.cur_hp += amount

    def upgrade_attack(self, amount = 5):
        self.attack += amount

    def upgrade_defense(self, amount = 5):
        self.defense += amount