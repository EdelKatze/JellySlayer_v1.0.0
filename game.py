import pygame as pg
from conf import Config
from ply import Player
from ani import animes, Anime
from stg import Stage
from obj import Object, State, jelly_state, platform_state
from stage_moving import CameraMoving
from switch_drawing import Switch
import pickle
from maker.input import main
from maker.option import mainloop
from maker.delete import delete
from ent import Jelly, BossJelly, Entity
from str import Platform, Portal
from interactions import Text_play
from gui import DisplayBar

pg.init()
pg.display.set_caption("JellySlayer")


class Game:

    def __init__(self):
        print("Game created")

    @staticmethod
    def bgm_change(current_stage, next_stage):
        for bgm in current_stage.bgms.values():
            if Config.SOUND.background_is_playing[bgm]:
                Config.SOUND.sound_stop(bgm)
        Config.SOUND.sound_play(next_stage.bgms["general"])

    @staticmethod
    def main():
        from stg import stages
        count = 10

        current_stage = "forest"
        is_stage_changed = False
        player = Player(
            img_name="player_idle",
            size=Config.player_size,
        )

        objects = stages[current_stage].objs
        objects.append(player)

        enemies = []
        structures = []

        def get_combinations(objects):
            __objects = objects[1:][::-1]
            func_num = 0
            result = []
            used_list = []
            classes = [Object, Platform]
            for obj1 in __objects:
                for obj2 in __objects:
                    if obj1.name != obj2.name and obj2.name not in used_list:
                        if type(obj1) in classes and type(obj2) in classes:
                            continue
                        result.append([obj1, obj2])
                        func_num += 1
                used_list.append(obj1.name)
            return result

        def get_player_combinations():
            result = {}
            __player = player

            result["enemy"] = [[player, __enemy] for __enemy in enemies]
            result["structure"] = [[player, __structure] for __structure in structures]

            return result


        lighted_enemies = []

        def light_hitbox():
            player.is_damage_immune = False
            player.plus_ap(-20)
            player.can_moving = False
            hitbox_pos = player.pos
            hitbox = pg.Rect(hitbox_pos[0], hitbox_pos[1],
                             Config.player_width + Config.light_length, Config.light_size[1])
            for _enemy in enemies:
                if _enemy.hitbox.box.colliderect(hitbox):
                    _enemy.can_moving = False
                    lighted_enemies.append(_enemy)
            player.is_damage_immune = True
            player.hit_count = player.hit_count_constant
            player.can_moving = True

        def light_move1():
            if player.direction:
                player.pos[0] += Config.player_width
            else:
                player.pos[0] -= Config.player_width

        def light_move2():
            if player.direction:
                player.pos[0] += Config.light_length
            else:
                player.pos[0] -= Config.light_length

        def falsing():
            player.is_lighting = False
            player.can_moving = True

            for _enemy in lighted_enemies:
                _enemy.can_moving = True
                _enemy.manage_dmg(player.lighting_damage)
                lighted_enemies.remove(_enemy)

        def atk():
            if player.direction:
                rect = player.img.get_rect(topleft=player.animation.apply_offset(1))
            else:
                rect = player.img.get_rect(topleft=player.animation.apply_offset(0))

            for _enemy in enemies:
                if rect.colliderect(_enemy.hitbox.box):
                    _enemy.can_moving = False
                    _enemy.is_hit = True

        def atk_falsing():
            player.is_attacking = False
            for _enemy in enemies:
                if _enemy.is_hit:
                    _enemy.is_hit = False
                    _enemy.can_moving = True
                    _enemy.manage_dmg(player.attack_damage, screen=Config.screen)
                    _enemy.knock_back(player.stage_pos, True, player.direction)


        animes["player_attack"] = Anime(name="player_attack", size=Config.player_attack, fmc=3,
                                        offset_left=(21, 10),
                                        offset_right=(3, 10),
                                        end_func=atk_falsing,
                                        frame_func=atk)
        animes["player_light"] = Anime(name="player_light", size=Config.player_light, fmc=5,
                                       offset_left=(17, -1),
                                       offset_right=(5, -1),
                                       start_func=light_hitbox,
                                       middle_func=[
                                           light_move1,
                                           light_move2,
                                       ],
                                       end_func=falsing)


        Config.SOUND.sound_play(stages[current_stage].bgms["general"], -1)
        try:
            Config.SOUND.sounds[stages[current_stage].bgms["general"]].sound.set_volume(0.5)
        except:
            Config.SOUND.sounds["@"].sound.set_volume(0.5)

        stages[current_stage].obj_states["player"] = State(attackable=False,
                                                           interactive=False,
                                                           can_be_damaged=False,
                                                           can_step=False,
                                                           can_underthrough=True)


        def img_none(objs):
            for i in objs:
                i.img = None
                try:
                    i.font = None
                    i.text = None
                except:
                    pass
            return objs

        def img_surface(objs):
            for i in objs:
                i.img = Config.IMAGE.images[i.img_name][0].image
                i.img = pg.transform.scale(i.img, i.size)


            return objs



        combinations = get_combinations(objects)
        clock = pg.time.Clock()
        background = objects.pop(0)

        switch = Switch(player_pos=[0, 660],
                        stage_size=stages[current_stage].stage_size,
                        projectile_obj=[],
                        obj=objects)
        camera = CameraMoving(screen_player_pos=[0, 660],
                              drawn_obj=switch.drawn_obj,
                              stage_size=switch.stage_size,
                              stage_player_pos=[0, 660])

        objects.insert(0, background)
        protection_bar = DisplayBar(
            "protection",
            [0, 0]
        )
        anima_bar = DisplayBar(
            "anima",
            [0, Config.bar_size[1] + 10]
        )

        stages[current_stage].objs = img_none(stages[current_stage].objs)

        bind = [stages[current_stage], switch, camera, player]

        stages[current_stage].objs = img_surface(stages[current_stage].objs)

        is_debugging = False

        player_combinations = get_player_combinations()

        def loading(stagename: str, player):
            original_direction = player.direction

            with open(f"stage.p", "rb") as f:
                binding = pickle.load(f)

            stages[current_stage], switch, camera, player, player_combinations = (
                binding[0], binding[1], binding[2], binding[3], binding[4])

            camera.drawn_obj = img_surface(camera.drawn_obj)
            stages[current_stage].objs = img_surface(stages[current_stage].objs)
            switch.undrawn_obj = img_surface(switch.undrawn_obj)
            switch.drawn_obj = img_surface(switch.drawn_obj)
            for i in player_combinations:
                x = 0
                for j in player_combinations[i]:
                    player_combinations[i][x] = img_surface(j)
                    x += 1

            print("WTESTING")
            player.direction = original_direction
            player.going_direction = [False, False]
            player.rotate()

            return camera, stages, switch, player, player_combinations


        def object_remove(object):
            for list in lists_using_objects:
                for obj in list:
                    if obj.name == object.name:
                        list.remove(obj)

            for comb in player_combinations["enemy"]:
                if comb[1].name == object.name:
                    player_combinations["enemy"].remove(comb)

        while True:
            # background separation
            background = objects.pop(0)
            # 키 설정
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return

                # Keyboard event handling
                if event.type == pg.KEYDOWN:
                    # Key press
                    if event.key == pg.K_LEFT:
                        player.going_direction[0] = True
                    if event.key == pg.K_RIGHT:
                        player.going_direction[1] = True
                    if event.key == pg.K_SPACE:
                        if player.vertical_speed == 0 and not player.is_lighting:
                            player.jumping()
                    if event.key == pg.K_l:
                        stages[current_stage].obj_states["jelly1"].can_be_damaged = not stages[current_stage].obj_states["jelly1"].can_be_damaged
                    if event.key == pg.K_q:
                        player.pos[1] -= 500
                        player.stage_pos[1] -= 500
                    if event.key == pg.K_e:
                        player.pos[1] += 100
                        player.stage_pos[1] += 100
                    if event.key == pg.K_t:
                        player.hitbox.obj_tracking = not player.hitbox.obj_tracking

                    if event.key == pg.K_c:
                        if Config.SOUND.background_is_playing[stages[current_stage].bgms["general"]]:
                            Config.SOUND.sound_stop(stages[current_stage].bgms["general"])
                        else:
                            Config.SOUND.sound_play(stages[current_stage].bgms["general"], -1)

                    if event.key == pg.K_z:
                        for obj in stages[current_stage].objs:
                            if obj.name is not player.name:
                                if (stages[current_stage].check_collide([obj, player]) and
                                        stages[current_stage].obj_states[obj.name].interactive):
                                    obj.interact()

                    if event.key == pg.K_x:
                        player.attack()

                    if event.key == pg.K_LSHIFT:
                        if player.vertical_speed == 0 and player.can_lighting:
                            player.light()


                    if event.key == pg.K_F1:
                        is_debugging = not is_debugging

                    if event.key == pg.K_d:
                        var = Text_play(["wow sans", "and wow papirus"])
                        var.main(background)


                    if is_debugging:
                        if event.key == pg.K_d and pg.key.get_mods() & pg.KMOD_CTRL:
                            # damaging test
                            player.manage_dmg(121)

                        if event.key == pg.K_l and pg.key.get_mods() & pg.KMOD_CTRL:
                            # load
                            with open("stage.p", "rb") as f:
                                binding = pickle.load(f)

                            stages[current_stage], switch, camera, player, player_combinations = (
                                binding[0], binding[1], binding[2], binding[3], binding[4])

                            camera.drawn_obj = img_surface(camera.drawn_obj)
                            stages[current_stage].objs = img_surface(stages[current_stage].objs)
                            switch.undrawn_obj = img_surface(switch.undrawn_obj)
                            switch.drawn_obj = img_surface(switch.drawn_obj)
                            objects = stages[current_stage].objs
                            loading("test", player)

                        if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                            # save

                            stages[current_stage].objs = img_none(stages[current_stage].objs)
                            stages[current_stage].objs = img_none(stages[current_stage].objs)
                            switch.undrawn_obj = img_none(switch.undrawn_obj)
                            switch.drawn_obj = img_none(switch.drawn_obj)
                            camera.drawn_obj = img_none(camera.drawn_obj)
                            player = img_none([player])[0]
                            player.going_direction = [False, False]
                            for i in player_combinations:
                                x = 0
                                for j in player_combinations[i]:
                                    print(x)
                                    player_combinations[i][x] = img_none(j)
                                    x += 1


                            bind = [stages[current_stage], switch, camera, player, player_combinations]

                            with open("stage.p", 'wb') as file:
                                pickle.dump(bind, file)

                            stages[current_stage].objs = img_surface(stages[current_stage].objs)
                            switch.undrawn_obj = img_surface(switch.undrawn_obj)
                            switch.drawn_obj = img_surface(switch.drawn_obj)
                            camera.drawn_obj = img_surface(camera.drawn_obj)
                            player = img_surface([player])[0]
                            for i in player_combinations:
                                x = 0
                                for j in player_combinations[i]:
                                    print(x)
                                    player_combinations[i][x] = img_surface(j)
                                    x += 1

                        if event.key == pg.K_EQUALS and pg.key.get_mods() & pg.KMOD_CTRL:  # object addition
                            var = mainloop([Jelly, Platform, BossJelly])
                            def location(empty, pos:list):
                                pass

                            position = main(location)[0]
                            foo = None
                            state = None
                            if var == Jelly:
                                foo = ["jelly"f'{count}', Config.jelly_size, position]
                                state = jelly_state
                            if var == Platform:
                                foo = ["platform"f'{count}', [176, 96], position]
                                state = platform_state

                            if var == BossJelly:
                                foo = [f"jellyboss{count}", Config.boss_jelly_size, position, player, objects,
                                       stages[current_stage].obj_states, count, Jelly, Jelly, Jelly, Jelly]
                                state = jelly_state
                            count += 1
                            entity = var(*foo)
                            objects.append(entity)
                            stages[current_stage].obj_states[foo[0]] = state
                            try:
                                entity = var(*foo)
                                objects.append(entity)
                                stages[current_stage].obj_states[foo[0]] = state

                            except:
                                print("failed")



                        if event.key == pg.K_BACKSPACE and pg.key.get_mods() & pg.KMOD_CTRL:  # object deletion
                            objects = delete(objects)
                            combinations = get_combinations(objects)
                            for enemy in objects:
                                if enemy.species == "enemy":
                                    enemies.append(enemy)
                            player_combinations = get_player_combinations()

                        if event.key == pg.K_t and pg.key.get_mods() & pg.KMOD_CTRL:  # State addition
                            def name_input(empty_whatever, name: str) -> None:
                                pass

                            state_name = main(name_input)
                            state = list(main(State))
                            x = 0
                            for i in state:
                                if state[x] == "True":

                                    state[x] = True

                                else:
                                    state[x] = False

                                x += 1
                            print(state_name)
                            stages[current_stage].obj_states[state_name[0]] = State(*state)
                        if event.key == pg.K_v:
                            camera, stages, switch, player, player_combinations = loading("test", player)
                        if event.key == pg.K_n:
                            def stg_input(self, name):
                                pass
                            next_stage = main(stg_input)[0]

                        if event.key == pg.K_F5:
                            if is_debugging:
                                for obj in objects:
                                    if "Entity" in [o.__name__ for o in obj.__class__.mro()]:
                                        if obj.species == "enemy":
                                            obj.can_moving = True

                        if event.key == pg.K_F6:
                            foo = [f"jellyboss{count}", Config.boss_jelly_size, [1200, 123], player, objects,
                                   stages[current_stage].obj_states, count, Jelly, Jelly, Jelly, Jelly]
                            state = jelly_state
                            try:
                                entity = BossJelly(*foo)
                                objects.append(entity)
                                stages[current_stage].obj_states[foo[0]] = state
                                print(stages[current_stage].obj_states, foo[0])

                            except:
                                print("failed")

                            count += 1
                        if event.key == pg.K_F7:
                            foo = ["jellyboss"f'{count}', Config.boss_jelly_size, [800, 123]]
                            state = jelly_state
                            try:
                                entity = Jelly(*foo)
                                objects.append(entity)
                                stages[current_stage].obj_states[foo[0]] = state
                                print(stages[current_stage].obj_states, foo[0])

                            except:
                                print("failed")

                            count += 1


                if event.type == pg.KEYUP:
                    # Key release
                    if event.key == pg.K_LEFT:
                        player.going_direction[0] = False
                    if event.key == pg.K_RIGHT:
                        player.going_direction[1] = False

            for obj in objects:
                if obj.stage_pos[0] + obj.size[0] > stages[current_stage].size[0]:
                    obj.stage_pos[0] = stages[current_stage].size[0] - obj.size[0]

                if obj.stage_pos[0] < 0:
                    obj.stage_pos[0] = 0
                if "Entity" in [o.__name__ for o in obj.__class__.mro()] and obj.name != "protection_bar":
                    obj.falling(objects, 0, stages[current_stage].obj_states)
                    obj.stop_going(objects, 0, stages[current_stage].obj_states)
                    if obj.species == "enemy":
                        if obj.get_protect_point() <= 0:
                            del stages[current_stage].obj_states[obj.name]
                            object_remove(obj)

                        obj.determinate(player.stage_pos)
                        obj.movement()

            player.movement()
            player.pos[0] = max(0, min(player.pos[0], Config.width - player.size[0]))
            player.pos[1] = max(0, min(player.pos[1], Config.height - player.size[1]))
            player.skill_count()
            player.can_moving = not player.is_attacking
            if player.is_attacking and player.is_lighting:
                player.is_attacking = False

            x = 0
            # position rearrange and object management
            objects = switch.switch()
            switch.objectupdate(objects)
            switch.player_pos_update(player.stage_pos)
            player.stage_pos = camera.stage_player_pos

            structures = []
            enemies = []

            for structure in objects:
                if structure.species == "structure":
                    structures.append(structure)
            structures = list(filter(lambda obj: obj.species == "enemy", objects))
            enemies = list(filter(lambda obj: isinstance(obj, Entity) and obj.species == "enemy", objects))

            player_combinations = get_player_combinations()

            lists_using_objects = [
                objects,
                lighted_enemies,
                stages[current_stage].objs,
            ]


            # background insert
            if is_debugging:
                for obj in objects:
                    if "Entity" in [o.__name__ for o in obj.__class__.mro()]:
                        if obj.species == "enemy":

                                obj.can_moving = False


            objects.insert(0, background)

            # Screen update
            Config.screen.fill((0, 0, 0))
            # Re-draw objects


            for obj in objects:
                obj.update()
            protection_bar.update(player)
            anima_bar.update(player)

            background = objects.pop(0)

            for combination in player_combinations["enemy"]:
                if Stage.check_collide(combination):

                    if stages[current_stage].obj_states[combination[1].name].can_be_damaged:
                        if not player.is_damage_immune:
                            player.knock_back(combination[1].stage_pos, True, combination[1].going_direction[1])
                            player.manage_dmg(combination[1].attack_damage, screen=Config.screen)

            player.knock_back([0,0], False, True)
            player.manage_dmg(screen=Config.screen)

            # Create separate lists/dictionaries for entities and portals
            entity_objects = enemies
            portal_objects = [obj for obj in objects if isinstance(obj, Portal)]

            # Iterate through entity objects
            for entity in entity_objects:

                entity.manage_dmg(screen=Config.screen)
                entity.knock_back(player.stage_pos, False, player.direction)

            # Iterate through portal objects
            for portal in portal_objects:
                if portal.switch:
                    if not enemies:
                        print("LLL")
                        camera, stages, switch, player, player_combinations = loading(next_stage, player)
                    else:
                        portal.switch = False

            objects, player.pos, background = camera.obj_update(
                drawn_obj=objects, screen_player_pos=player.pos, background=background, width=switch.stage_size[0],
                player=player)
            objects.insert(0, background)


            if is_stage_changed:
                objects = stages[current_stage].objs
                is_stage_changed = False

            pg.display.flip()

            # 초당 프레임 조정
            clock.tick(Config.fps)
