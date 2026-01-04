import json
from datetime import datetime


class Hero:
    def __init__(self, name, hero_class, level=1):
        self.name = name
        self.hero_class = hero_class
        self.level = level
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.experience = 0
        self.inventory = []
        self.artifacts = []
        self.skills = []
        self.gold = 50
        self.is_alive = True

        # Инициализация в зависимости от класса
        self._init_class_stats()

    def _init_class_stats(self):
        if self.hero_class == "Воин":
            self.health = 150
            self.max_health = 150
            self.mana = 30
            self.max_mana = 30
            self.skills = ["Удар мечом", "Щит"]
        elif self.hero_class == "Маг":
            self.health = 80
            self.max_health = 80
            self.mana = 100
            self.max_mana = 100
            self.skills = ["Огненный шар", "Щит маны"]
        elif self.hero_class == "Лучник":
            self.health = 100
            self.max_health = 100
            self.mana = 60
            self.max_mana = 60
            self.skills = ["Точный выстрел", "Уклонение"]

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return self.is_alive

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def restore_mana(self, amount):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def add_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 20
        self.max_mana += 10
        self.health = self.max_health
        self.mana = self.max_mana
        print(f"\n✨ {self.name} достиг {self.level} уровня!")
        print(f"Здоровье: {self.max_health}, Мана: {self.max_mana}")

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        # Применяем бонусы артефакта
        if "Здоровье" in artifact.effects:
            self.max_health += artifact.effects["Здоровье"]
            self.health += artifact.effects["Здоровье"]
        if "Мана" in artifact.effects:
            self.max_mana += artifact.effects["Мана"]
            self.mana += artifact.effects["Мана"]

    def remove_artifact(self, artifact):
        if artifact in self.artifacts:
            self.artifacts.remove(artifact)
            # Убираем бонусы
            if "Здоровье" in artifact.effects:
                self.max_health -= artifact.effects["Здоровье"]
                if self.health > self.max_health:
                    self.health = self.max_health
            if "Мана" in artifact.effects:
                self.max_mana -= artifact.effects["Мана"]
                if self.mana > self.max_mana:
                    self.mana = self.max_mana

    def to_dict(self):
        return {
            "name": self.name,
            "hero_class": self.hero_class,
            "level": self.level,
            "health": self.health,
            "max_health": self.max_health,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "experience": self.experience,
            "inventory": self.inventory,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "skills": self.skills,
            "gold": self.gold,
            "is_alive": self.is_alive
        }

    @classmethod
    def from_dict(cls, data):
        hero = cls(data["name"], data["hero_class"], data["level"])
        hero.health = data["health"]
        hero.max_health = data["max_health"]
        hero.mana = data["mana"]
        hero.max_mana = data["max_mana"]
        hero.experience = data["experience"]
        hero.inventory = data["inventory"]
        hero.skills = data["skills"]
        hero.gold = data["gold"]
        hero.is_alive = data["is_alive"]
        return hero

    def show_stats(self):
        print(f"\n=== Статистика героя ===")
        print(f"Имя: {self.name}")
        print(f"Класс: {self.hero_class}")
        print(f"Уровень: {self.level}")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Мана: {self.mana}/{self.max_mana}")
        print(f"Опыт: {self.experience}/{(self.level) * 100}")
        print(f"Золото: {self.gold}")
        print(f"Артефакты: {len(self.artifacts)}")
        print(f"Навыки: {', '.join(self.skills)}")


class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.is_alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return self.is_alive

    def show_stats(self):
        print(f"{self.name}: Здоровье {self.health}/{self.max_health}, Урон {self.damage}")