import json
import random


class Artifact:
    def __init__(self, name, description, effects):
        self.name = name
        self.description = description
        self.effects = effects

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "effects": self.effects
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["description"], data["effects"])

    def __str__(self):
        effects_str = ", ".join([f"{k}: {v}" for k, v in self.effects.items()])
        return f"{self.name}: {self.description} ({effects_str})"


class ArtifactVault:
    def __init__(self):
        self.available_artifacts = []
        self.hero_artifacts = []
        self._init_artifacts()

    def _init_artifacts(self):
        # Артефакты Dota 2
        artifacts_data = [
            {"name": "Эгида бессмертия", "description": "Легендарный щит",
             "effects": {"Здоровье": 50, "Защита": 10}},
            {"name": "Сфера Аганима", "description": "Усиливает способности",
             "effects": {"Мана": 30, "Урон": 15}},
            {"name": "Клинок Раздора", "description": "Меч темного властелина",
             "effects": {"Урон": 25, "Критический удар": 5}},
            {"name": "Сердце Тарраске", "description": "Дарует невероятную регенерацию",
             "effects": {"Здоровье": 80, "Регенерация": 20}},
            {"name": "Посох чародея", "description": "Усиливает магические способности",
             "effects": {"Мана": 50, "Маг. урон": 20}},
            {"name": "Боевая фасция", "description": "Доспехи древнего воина",
             "effects": {"Защита": 25, "Здоровье": 40}},
            {"name": "Кольцо здоровья", "description": "Простое магическое кольцо",
             "effects": {"Здоровье": 20, "Регенерация": 5}},
            {"name": "Перо Феникса", "description": "Дает шанс на возрождение",
             "effects": {"Возрождение": 1, "Мана": 10}},
        ]

        for artifact in artifacts_data:
            self.available_artifacts.append(Artifact(**artifact))

    def get_random_artifact(self):
        if not self.available_artifacts:
            self.generate_new_artifacts()

        artifact = random.choice(self.available_artifacts)
        self.available_artifacts.remove(artifact)
        return artifact

    def generate_new_artifacts(self):
        print("\n⚡ Все артефакты собраны! Генерирую новые...")
        new_artifacts = [
            {"name": "Око тени", "description": "Артефакт теневого демона",
             "effects": {"Мана": 40, "Невидимость": 10}},
            {"name": "Клык Скади", "description": "Ледяное оружие",
             "effects": {"Урон": 20, "Замедление": 15}},
            {"name": "Руна мастера", "description": "Древняя магическая руна",
             "effects": {"Все параметры": 10}},
            {"name": "Плащ иллюзий", "description": "Создает иллюзорные копии",
             "effects": {"Уклонение": 25, "Мана": 15}},
            {"name": "Сапфировый жезл", "description": "Жезл из чистой маны",
             "effects": {"Мана": 60, "Маг. защита": 20}},
        ]

        for artifact in new_artifacts:
            self.available_artifacts.append(Artifact(**artifact))

        print("⚡ Новые артефакты созданы!")

    def return_artifact(self, artifact):
        self.available_artifacts.append(artifact)

    def save_state(self):
        state = {
            "available": [a.to_dict() for a in self.available_artifacts],
            "hero": [a.to_dict() for a in self.hero_artifacts]
        }
        with open("vault_state.json", "w") as f:
            json.dump(state, f)

    def load_state(self):
        try:
            with open("vault_state.json", "r") as f:
                state = json.load(f)
                self.available_artifacts = [Artifact.from_dict(a) for a in state["available"]]
                self.hero_artifacts = [Artifact.from_dict(a) for a in state["hero"]]
        except FileNotFoundError:
            self._init_artifacts()

    def show_available_artifacts(self):
        print("\n=== Доступные артефакты ===")
        for i, artifact in enumerate(self.available_artifacts, 1):
            print(f"{i}. {artifact}")