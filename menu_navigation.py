from melee.menuhelper import MenuHelper
import melee

class MenuNavigation:

    def __init__(self, gamestate):
        self.MenuHelper = MenuHelper()
        self.gamestate = gamestate

    def navigate(self):
    # If we're at the character select screen, choose our character
        if self.gamestate.menu_state in [melee.enums.Menu.CHARACTER_SELECT, melee.enums.Menu.SLIPPI_ONLINE_CSS]:
            if self.gamestate.submenu == melee.enums.SubMenu.NAME_ENTRY_SUBMENU:
                MenuHelper.name_tag_index = MenuHelper.enter_direct_code(gamestate=self.gamestate,
                                                           controller=controller,
                                                           connect_code=connect_code,
                                                           index=MenuHelper.name_tag_index)
            else:
                MenuHelper.choose_character(character=character_selected,
                                            gamestate=self.gamestate,
                                            controller=controller,
                                            cpu_level=cpu_level,
                                            costume=costume,
                                            swag=swag,
                                            start=autostart)
        # If we're at the postgame scores screen, spam START
        elif self.gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
            MenuHelper.skip_postgame(controller=controller)
        # If we're at the stage select screen, choose a stage
        elif self.gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
            MenuHelper.choose_stage(stage=stage_selected,
                                    gamestate=self.gamestate,
                                    controller=controller)
        elif self.gamestate.menu_state == melee.enums.Menu.MAIN_MENU:
            if connect_code:
                MenuHelper.choose_direct_online(gamestate=self.gamestate, controller=controller)
            else:
                MenuHelper.choose_versus_mode(gamestate=self.gamestate, controller=controller)