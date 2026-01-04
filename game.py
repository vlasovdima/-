import json
import os
import sys
import time
from player import Hero, Enemy
from artifact_vault import ArtifactVault


class DotaDNDGame:
    def __init__(self):
        self.player = None
        self.vault = ArtifactVault()
        self.current_location = "Начало"
        self.game_running = True
        self.save_file = "save_game.txt"
        self.cred_file = "credentials.txt"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_title(self):
        print("=" * 60)
        print("          DOTA 2 скачать на андроид")
        print("=" * 60)
        print("    здравствуйте")
        print("=" * 60)

    def register_user(self):
        print("\n=== РЕГИСТРАЦИЯ ===")
        username = input("Введите имя пользователя: ").strip()
        password = input("Введите пароль: ").strip()

        with open(self.cred_file, "a") as f:
            f.write(f"{username}:{password}\n")

        print("Регистрация успешна!")
        time.sleep(1)
        return username

    def login_user(self):
        print("\n=== ВХОД ===")
        username = input("Имя пользователя: ").strip()
        password = input("Пароль: ").strip()

        try:
            with open(self.cred_file, "r") as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(":")
                    if stored_user == username and stored_pass == password:
                        print(f"Добро пожаловать, {username}!")
                        time.sleep(1)
                        return username
        except FileNotFoundError:
            pass

        print("Неверные учетные данные!")
        return None

    def auth_menu(self):
        while True:
            self.clear_screen()
            self.print_title()
            print("\n1. Войти")
            print("2. Зарегистрироваться")
            print("3. Выйти")

            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                username = self.login_user()
                if username:
                    return username
            elif choice == "2":
                username = self.register_user()
                return username
            elif choice == "3":
                print("До свидания!")
                sys.exit(0)
            else:
                print("Неверный выбор!")
                time.sleep(1)

    def create_hero(self, username):
        self.clear_screen()
        print("\n=== СОЗДАНИЕ ГЕРОЯ ===")
        print(f"Игрок: {username}")

        name = input("Введите имя вашего героя: ").strip() or "Безымянный"

        print("\nВыберите класс героя:")
        print("1. Воин - высокое здоровье, малый урон")
        print("2. Маг - высокая мана, магические атаки")
        print("3. Лучник - баланс, дальние атаки")

        class_choice = input("Ваш выбор (1-3): ").strip()

        classes = ["Воин", "Маг", "Лучник"]
        hero_class = classes[int(class_choice) - 1] if class_choice in ["1", "2", "3"] else "Воин"

        self.player = Hero(name, hero_class)
        print(f"\nГерой {name} ({hero_class}) создан!")
        time.sleep(2)

    def save_game(self, ask_confirmation=True):
        if ask_confirmation:
            print("\n⚠️ Вы уверены, что хотите сохранить игру?")
            print("1. Да, сохранить и продолжить")
            print("2. Нет, вернуться в игру")

            choice = input("Выберите: ").strip()
            if choice != "1":
                return False

        save_data = {
            "player": self.player.to_dict(),
            "location": self.current_location,
            "artifacts_in_vault": [a.to_dict() for a in self.vault.available_artifacts],
            "timestamp": time.time()
        }

        with open(self.save_file, "w") as f:
            json.dump(save_data, f)

        # Сохраняем артефакты в копилке
        self.vault.save_state()

        print("\n✅ Игра сохранена!")
        time.sleep(1)
        return True

    def load_game(self):
        try:
            with open(self.save_file, "r") as f:
                save_data = json.load(f)

            self.player = Hero.from_dict(save_data["player"])
            self.current_location = save_data["location"]

            # Загружаем артефакты
            self.vault.load_state()

            print("\n✅ Игра загружена!")
            time.sleep(1)
            return True
        except FileNotFoundError:
            print("\n❌ Файл сохранения не найден!")
            time.sleep(1)
            return False
        except Exception as e:
            print(f"\n❌ Ошибка загрузки: {e}")
            time.sleep(1)
            return False

    def campfire(self):
        print("\n🔥 Вы нашли костер!")
        print("У костра можно отдохнуть и восстановить силы.")

        while True:
            print("\n1. Отдохнуть (восстановить здоровье и ману)")
            print("2. Сохранить игру")
            print("3. Осмотреть инвентарь")
            print("4. Продолжить путь")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self.player.heal(self.player.max_health)
                self.player.restore_mana(self.player.max_mana)
                print("\n✅ Вы отдохнули у костра!")
                print(f"Здоровье: {self.player.health}/{self.player.max_health}")
                print(f"Мана: {self.player.mana}/{self.player.max_mana}")
                time.sleep(2)
            elif choice == "2":
                self.save_game()
            elif choice == "3":
                self.player.show_stats()
                if self.player.artifacts:
                    print("\nАртефакты:")
                    for artifact in self.player.artifacts:
                        print(f"  - {artifact}")
            elif choice == "4":
                print("\nВы продолжаете свой путь...")
                time.sleep(1)
                break

    def battle(self, enemy):
        print(f"\n⚔️ БИТВА С {enemy.name.upper()}! ⚔️")

        while self.player.is_alive and enemy.is_alive:
            self.clear_screen()
            print(f"\n=== ХОД БИТВЫ ===")
            self.player.show_stats()
            enemy.show_stats()

            print(f"\nВаши действия:")
            print("1. Атаковать")
            print("2. Использовать навык")
            print("3. Попытаться сбежать")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                # Простая атака
                damage = self.player.level * 10
                if self.player.hero_class == "Воин":
                    damage += 5
                elif self.player.hero_class == "Маг":
                    damage -= 2

                print(f"\n⚔️ Вы атакуете {enemy.name} и наносите {damage} урона!")
                if not enemy.take_damage(damage):
                    print(f"✅ {enemy.name} побежден!")
                    reward_exp = enemy.max_health // 10
                    reward_gold = enemy.damage * 5
                    self.player.add_experience(reward_exp)
                    self.player.gold += reward_gold
                    print(f"Получено: {reward_exp} опыта и {reward_gold} золота!")

                    # Шанс получить артефакт
                    if len(self.player.artifacts) < 5 and len(self.vault.available_artifacts) > 0:
                        if input("\nНайти артефакт? (д/н): ").lower() == 'д':
                            artifact = self.vault.get_random_artifact()
                            self.player.add_artifact(artifact)
                            print(f"🎁 Вы получили: {artifact}")

                    time.sleep(3)
                    return True

            elif choice == "2":
                # Использование навыка
                print(f"\nВаши навыки: {', '.join(self.player.skills)}")
                skill_choice = input("Выберите навык (введите номер): ")
                if skill_choice in ["1", "2"]:
                    skill_index = int(skill_choice) - 1
                    skill = self.player.skills[skill_index]

                    if skill == "Огненный шар" and self.player.mana >= 20:
                        damage = 30
                        self.player.mana -= 20
                        print(f"🔥 Вы используете Огненный шар! Нанесено {damage} урона!")
                        if not enemy.take_damage(damage):
                            print(f"✅ {enemy.name} побежден!")
                            self.player.add_experience(50)
                            time.sleep(3)
                            return True
                    elif skill == "Удар мечом":
                        damage = 25
                        print(f"⚔️ Вы используете Удар мечом! Нанесено {damage} урона!")
                        if not enemy.take_damage(damage):
                            print(f"✅ {enemy.name} побежден!")
                            self.player.add_experience(50)
                            time.sleep(3)
                            return True
                    else:
                        print("Недостаточно маны или навык недоступен!")
                else:
                    print("Неверный выбор навыка!")

            elif choice == "3":
                # Попытка побега
                escape_chance = 40  # 40% шанс
                if self.player.hero_class == "Лучник":
                    escape_chance = 60

                import random
                if random.randint(1, 100) <= escape_chance:
                    print("\n✅ Вам удалось сбежать!")
                    time.sleep(2)
                    return False
                else:
                    print("\n❌ Не удалось сбежать!")

            # Атака врага
            if enemy.is_alive:
                enemy_damage = enemy.damage
                print(f"\n{enemy.name} атакует вас и наносит {enemy_damage} урона!")
                if not self.player.take_damage(enemy_damage):
                    print("\n💀 Вы пали в бою...")
                    time.sleep(2)
                    return False

            time.sleep(2)

        return False

    def main_story_branch_1(self):
        print("\n=== ЛЕС ТЕНИ ===")
        print("Вы вошли в мрачный лес, где царит вечная тьма.")
        print("1. Идти по тропинке")
        print("2. Исследовать руины")
        print("3. Вернуться назад")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            print("\nВы идете по тропинке и встречаете Разбойника!")
            enemy = Enemy("Лесной разбойник", 80, 15)
            if self.battle(enemy):
                print("\nПродвигаясь дальше, вы находите древний алтарь.")
                print("На алтаре лежит странный артефакт...")
                artifact = self.vault.get_random_artifact()
                self.player.add_artifact(artifact)
                print(f"🎁 Вы получаете: {artifact}")
        elif choice == "2":
            print("\nВ руинах вы находите сундук с сокровищами!")
            self.player.gold += 100
            print(f"💰 Найдено 100 золота! Всего: {self.player.gold}")
        elif choice == "3":
            print("\nВы возвращаетесь назад...")
            return

        time.sleep(2)

    def main_story_branch_2(self):
        print("\n=== ГОРЫ ГРОМА ===")
        print("Вы поднимаетесь в заснеженные горы.")
        print("1. Подняться на пик")
        print("2. Исследовать пещеру")
        print("3. Разжечь костер")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            print("\nНа вершине вас ждет Ледяной дракон!")
            enemy = Enemy("Ледяной дракон", 150, 25)
            if self.battle(enemy):
                print("\nВы победили дракона и нашли его сокровищницу!")
                artifact = self.vault.get_random_artifact()
                self.player.add_artifact(artifact)
                print(f"🎁 Вы получаете: {artifact}")
        elif choice == "2":
            print("\nВ пещере вы находите гнома-торговца.")
            print("1. Купить зелье здоровья (50 золота)")
            print("2. Купить зелье маны (30 золота)")
            print("3. Уйти")

            trade = input("Ваш выбор: ").strip()
            if trade == "1" and self.player.gold >= 50:
                self.player.gold -= 50
                self.player.heal(50)
                print("✅ Зелье здоровья куплено!")
            elif trade == "2" and self.player.gold >= 30:
                self.player.gold -= 30
                self.player.restore_mana(30)
                print("✅ Зелье маны куплено!")
            else:
                print("❌ Недостаточно золота!")
        elif choice == "3":
            self.campfire()

        time.sleep(2)

    def main_story_branch_3(self):
        print("\n=== БОЛОТА СКОРБИ ===")
        print("Вы вступаете в зловонные болота.")
        print("1. Перейти через трясину")
        print("2. Обойти болото")
        print("3. Искать растения")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            print("\nВас атакует Болотный тролль!")
            enemy = Enemy("Болотный тролль", 120, 20)
            if self.battle(enemy):
                print("\nЗа троллем вы находите логово с артефактами.")
                artifact = self.vault.get_random_artifact()
                self.player.add_artifact(artifact)
                print(f"🎁 Вы получаете: {artifact}")
        elif choice == "2":
            print("\nОбходя болото, вы находите заброшенный храм.")
            print("В храме можно отдохнуть...")
            self.campfire()
        elif choice == "3":
            print("\nВы находите редкое целебное растение!")
            heal_amount = 30
            self.player.heal(heal_amount)
            print(f"✅ Вы восстановили {heal_amount} здоровья!")

        time.sleep(2)

    def final_battle(self):
        print("\n" + "=" * 60)
        print("          ФИНАЛЬНАЯ БИТВА")
        print("=" * 60)
        print("\nВы достигли трона Властелина Бездны!")

        # Создаем босса в зависимости от уровня игрока
        boss_health = 200 + (self.player.level * 20)
        boss_damage = 30 + (self.player.level * 5)
        boss = Enemy("Властелин Бездны", boss_health, boss_damage)

        print(f"\n⚡ {boss.name} появляется перед вами! ⚡")
        print(f"Здоровье: {boss.health}, Урон: {boss.damage}")

        input("\nНажмите Enter, чтобы начать битву...")

        if self.battle(boss):
            print("\n" + "=" * 60)
            print("          ПОБЕДА!")
            print("=" * 60)
            print(f"\n🎉 Вы победили {boss.name} и спасли мир Dota 2!")
            print(f"Ваш герой {self.player.name} стал легендой!")

            # Финальная награда
            self.player.level_up()
            self.player.gold += 500
            print(f"\n🏆 Награда: 500 золота и повышение уровня!")

            return True
        else:
            print("\n💀 Вы пали в финальной битве...")
            return False

    def main_game_loop(self):
        self.clear_screen()
        print("\n=== НАЧАЛО ПУТИ ===")
        print("Вы стоите на перекрестке трех дорог:")

        story_progress = 0

        while self.game_running and self.player.is_alive and story_progress < 3:
            self.clear_screen()
            self.player.show_stats()

            print(f"\n=== ГЛАВА {story_progress + 1}/3 ===")
            print("Куда отправитесь?")
            print("1. Лес Теней")
            print("2. Горы Грома")
            print("3. Болота Скорби")
            print("4. К костру (сохранение/отдых)")
            print("5. Сохранить и выйти")

            if story_progress > 0:
                print("6. Пойти к Властелину Бездны (финальная битва)")

            choice = input("\nВаш выбор: ").strip()

            if choice == "1":
                self.main_story_branch_1()
                story_progress = max(story_progress, 1)
            elif choice == "2":
                self.main_story_branch_2()
                story_progress = max(story_progress, 2)
            elif choice == "3":
                self.main_story_branch_3()
                story_progress = max(story_progress, 3)
            elif choice == "4":
                self.campfire()
            elif choice == "5":
                if self.save_game():
                    print("\nИгра сохранена. Возвращайтесь скорее!")
                    time.sleep(2)
                    break
            elif choice == "6" and story_progress >= 3:
                if self.final_battle():
                    print("\n🎮 КОНЕЦ ИГРЫ 🎮")
                    input("\nНажмите Enter для возвращения в меню...")
                    break
                else:
                    print("\nИгра окончена...")
                    time.sleep(2)
                    break

        if not self.player.is_alive:
            print("\n💀 ВАШ ГЕРОЙ ПОГИБ")
            print("\nХотите начать заново?")
            print("1. Да, начать новую игру")
            print("2. Нет, выйти в меню")

            choice = input("Выберите: ").strip()
            if choice == "1":
                return True
            else:
                return False

        return True

    def start(self):
        while True:
            self.clear_screen()
            self.print_title()

            print("\nГЛАВНОЕ МЕНЮ:")
            print("1. Новая игра")
            print("2. Загрузить игру")
            print("3. Выход")

            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                username = self.auth_menu()
                if username:
                    self.create_hero(username)
                    continue_game = self.main_game_loop()
                    if not continue_game:
                        break
            elif choice == "2":
                if self.load_game():
                    continue_game = self.main_game_loop()
                    if not continue_game:
                        break
            elif choice == "3":
                print("До свидания, герой!")
                break
            else:
                print("Неверный выбор!")
                time.sleep(1)


if __name__ == "__main__":
    game = DotaDNDGame()
    game.start()