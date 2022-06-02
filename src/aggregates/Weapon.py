from enum import Enum, auto, unique


@unique
class WeaponType(Enum):
    pistol = auto()
    shotgun = auto()
    grenade = auto()


class Weapons:

    def __init__(self):
        self.__current_weapon = WeaponType.pistol
        self.__in_chamber = [8, 4, 3]
        self.__packs = [20, 10, 3]

    def update_current_weapon(self, weapon_type):
        self.__current_weapon = weapon_type

    def updated_ammo_packs(self, weapon_type, x):
        self.__packs[weapon_type.value - 1] += x

    def update_in_chamber(self, x):
        self.__in_chamber[self.__current_weapon.value-1] = x

    def reload(self):
        if self.__current_weapon == WeaponType.pistol:
            self.__in_chamber[WeaponType.pistol.value-1] = 8
        elif self.__current_weapon == WeaponType.shotgun:
            self.__in_chamber[WeaponType.shotgun.value-1] = 4
        else:
            self.__in_chamber[WeaponType.grenade.value - 1] = 3

    def set_next_weapon(self):
        if self.__current_weapon == WeaponType.pistol:
            self.__current_weapon = WeaponType.grenade
        elif self.__current_weapon == WeaponType.grenade:
            self.__current_weapon = WeaponType.shotgun
        else:
            self.__current_weapon = WeaponType.pistol

    def set_prev_weapon(self):
        if self.__current_weapon == WeaponType.pistol:
            self.__current_weapon = WeaponType.shotgun
        elif self.__current_weapon == WeaponType.grenade:
            self.__current_weapon = WeaponType.pistol
        else:
            self.__current_weapon = WeaponType.grenade

    @property
    def in_chamber(self):
        return self.__in_chamber[self.__current_weapon.value-1]

    @property
    def packs(self):
        return self.__packs[self.__current_weapon.value-1]

    @property
    def current_weapon(self):
        return self.__current_weapon
