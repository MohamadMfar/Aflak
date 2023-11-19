import os
import time
import sqlite3
import io
# from gestures4kivy import CommonGestures
import kivy
from kivy import platform, Config
from kivy.graphics import Rectangle, RoundedRectangle
from kivy.graphics.context_instructions import Rotate, PushMatrix, PopMatrix, Color
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
import threading
import random
import numpy as np
import numpy
import arabic_reshaper
from bidi.algorithm import get_display
import itertools
import operator
import pickle
import math
from math import pi
from functools import partial

current_dir=os.getcwd()
keyboard_state=True

sound=dict()
sound['music_bg']=SoundLoader.load(current_dir+'/assets/'+'Menu.ogg')

try:
    save_game = pickle.load(open(current_dir + '/save', 'rb'))
    save_game['nth_time']+=1
except:
    save_game={}
    save_game['nth_time'] = 1
    save_game['score'] = 0
    save_game['xp'] = 0
    save_game['win'] = 0
    save_game['lose'] = 0
    save_game['storylvl'] = 0
    pickle.dump(save_game, open(current_dir + '/save', 'wb'))

print(save_game)
Window.size= (720,1280)

planet_scale = int(Window.width / 8)
planet_qscale = int(Window.width / 8)

globals()['font_scale'] = (26 / 600) * Window.width
globals()['characters_limit'] = 30

globals()['characters_hold'] = {'a': 'ا'}

globals()['characters'] = {
    'b': 'ب',
    'p': 'پ',
    't': 'ت',
    'th': 'ث',
    'j': 'ج',
    'ch': 'چ',
    'hj': 'ح',
    'kh': 'خ',
    'd': 'د',
    'zd': 'ذ',
    'r': 'ر',
    'z': 'ز',
    'zh': 'ژ',
    's': 'س',
    'sh': 'ش',
    'sz': 'ص',
    'zs': 'ض',
    'tz': 'ط',
    'zt': 'ظ',
    'eyn': 'ع',
    'gheyn': 'غ',
    'f': 'ف',
    'ghaf': 'ق',
    'k': 'ک',
    'g': 'گ',
    'l': 'ل',
    'm': 'م',
    'n': 'ن',
    'v': 'و',
    'h': 'ه',
    'y': 'ی',
    'hamze': 'ئ',
    # ,'ئ' :() ,'آ' :() ,'أ' :() , 'ؤ':()
}

globals()['alphabets_hold'] = {'a': (Window.width * 0.495, Window.height * .12)}

globals()['alphabets'] = {
    'b': (Window.width * 0.32, Window.height * .12),
    'p': (Window.width * 0.69, Window.height * .078),
    't': (Window.width * 0.582, Window.height * .12),
    'th': (Window.width * 0.215, Window.height * .165),
    'j': (Window.width * 0.865, Window.height * .165),
    'ch': (Window.width * 0.945, Window.height * .165),
    'hj': (Window.width * 0.785, Window.height * .165),
    'kh': (Window.width * 0.705, Window.height * .165),
    'd': (Window.width * 0.60, Window.height * .078),
    'zd': (Window.width * 0.515, Window.height * .078),
    'r': (Window.width * 0.428, Window.height * .078),
    'z': (Window.width * 0.345, Window.height * .078),
    'zh': (Window.width * 0.87, Window.height * .078),
    's': (Window.width * 0.15, Window.height * .12),
    'sh': (Window.width * 0.063, Window.height * .12),
    'sz': (Window.width * 0.135, Window.height * .165),
    'zs': (Window.width * 0.055, Window.height * .165),
    'tz': (Window.width * 0.26, Window.height * .078),
    'zt': (Window.width * 0.175, Window.height * .078),
    'eyn': (Window.width * 0.540, Window.height * .165),
    'gheyn': (Window.width * 0.460, Window.height * .165),
    'f': (Window.width * 0.375, Window.height * .165),
    'ghaf': (Window.width * 0.295, Window.height * .165),
    'k': (Window.width * 0.84, Window.height * .12),
    'g': (Window.width * 0.93, Window.height * .12),
    'l': (Window.width * 0.41, Window.height * .12),
    'm': (Window.width * 0.755, Window.height * .12),
    'n': (Window.width * 0.667, Window.height * .12),
    'v': (Window.width * 0.774, Window.height * .078),
    'h': (Window.width * 0.62, Window.height * .165),
    'y': (Window.width * 0.235, Window.height * .12),
    'hamze': (Window.width * 0.09, Window.height * .078),
    # ,'ئ' :() ,'آ' :() ,'أ' :() , 'ؤ':()
}

globals()['alphabets_size'] = {'ا': (int(Window.width / 7), int(Window.width / 7)),
                               'ب': (int(Window.width / 7), int(Window.width / 7)),
                               'پ': (int(Window.width / 7), int(Window.width / 7)),
                               'ت': (int(Window.width / 7), int(Window.width / 7)),
                               'ث': (int(Window.width / 7), int(Window.width / 7)),
                               'ج': (int(Window.width / 7), int(Window.width / 7)),
                               'چ': (int(Window.width / 7), int(Window.width / 7)),
                               'ح': (int(Window.width / 7), int(Window.width / 7)),
                               'خ': (int(Window.width / 7), int(Window.width / 7)),
                               'د': (int(Window.width / 7), int(Window.width / 7)),
                               'ذ': (int(Window.width / 7), int(Window.width / 7)),
                               'ر': (int(Window.width / 7), int(Window.width / 7)),
                               'ز': (int(Window.width / 7), int(Window.width / 7)),
                               'ژ': (int(Window.width / 7), int(Window.width / 7)),
                               'س': (int(Window.width / 7), int(Window.width / 7)),
                               'ش': (int(Window.width / 7), int(Window.width / 7)),
                               'ص': (int(Window.width / 7), int(Window.width / 7)),
                               'ض': (int(Window.width / 7), int(Window.width / 7)),
                               'ط': (int(Window.width / 7), int(Window.width / 7)),
                               'ظ': (int(Window.width / 7), int(Window.width / 7)),
                               'ع': (int(Window.width / 7), int(Window.width / 7)),
                               'غ': (int(Window.width / 7), int(Window.width / 7)),
                               'ف': (int(Window.width / 7), int(Window.width / 7)),
                               'ق': (int(Window.width / 7), int(Window.width / 7)),
                               'ک': (int(Window.width / 7), int(Window.width / 7)),
                               'گ': (int(Window.width / 7), int(Window.width / 7)),
                               'ل': (int(Window.width / 7), int(Window.width / 7)),
                               'م': (int(Window.width / 7), int(Window.width / 7)),
                               'ن': (int(Window.width / 7), int(Window.width / 7)),
                               'و': (int(Window.width / 7), int(Window.width / 7)),
                               'ه': (int(Window.width / 7), int(Window.width / 7)),
                               'ی': (int(Window.width / 7), int(Window.width / 7)),
                               'ء': (int(Window.width / 7), int(Window.width / 7)),
                               'ئ': (int(Window.width / 7), int(Window.width / 7)),
                               'آ': (int(Window.width / 7), int(Window.width / 7)),
                               'أ': (int(Window.width / 7), int(Window.width / 7)),
                               'ؤ': (int(Window.width / 7), int(Window.width / 7))}

globals()['texts'] = {1: 'یک رمز تصادفی برایت انتخاب شد\n حدست شروع کاوشت خواهد بود',
                      2: 'حدست بیش از یک معنا دارد\n کدام معنا منظور تو بود؟',
                      3: ''}

globals()['tuts'] = {1: 'کلمه حدست را وارد کن و دستگیره را فشار بده.\n برای وارد کردن «آ» الف را نگه دار',
                     2: 'روی فلش ها بزن تا معنای بعدی را ببینی.\n دسته را بکش تا شروع کنی',
                     3: 'کلمه ای که وارد کردی را پیدا نکردم.\n دوباره امتحان کن'}

scale = .3

globals()['texts_ingame'] = {1: 'کلمات نزدیکت را ببین و حدس بزن تا کمی سوخت بگیری',
                             2: 'بنویس ردر تا از رادارت کمک بگیری',
                             3: 'میتوانی هر کلمه ای که دوست داری را هم امتحان کنی',
                             4: 'دور سیاهچاله را روشن کن تا معنای آن را ببینی'
                             }

globals()['tuts_ingame'] = {1: '',
                            2: 'آفرین! حدست درست بود. جایزه کشفت کمی سوخت اضافه است',
                            3: 'کلمه ای که نوشتی را پیدا نکردم. دوباره امتحان کن',
                            4: 'بر روی فلش ها بزن تا معنای مورد نظرت را پیدا کنی'
                            }


class Aflak(App):
    def build(self):
        usr_dir = self.user_data_dir + '/app/assets/'
        usr_dir = 'assets/'

        con = sqlite3.connect(usr_dir + 'aflak.db', check_same_thread=False)
        self.root = MainFrame(usr_dir=usr_dir, conn=con)
        return self.root

    def on_pause(self):
        return True


class MainFrame(Widget):
    def __init__(self, usr_dir, conn, **kwargs):
        super().__init__(**kwargs)
        #initial values
        self._last_answer=''
        self._keyboard = dict()
        self._state_menu = None
        self.nofe = None
        self.answer = ''
        self._just_pressed_gloss = False
        self.destination_id_random = None
        self._switched = None
        self._locked_on_index = None
        self._search_results = []
        self._locked_on_id = None
        self.conn = conn
        self.sp_diff = None
        self.usr_dir = usr_dir
        self._state_menu = 1
        # sound['music1'] = SoundLoader.load(current_dir + 'Menu.wav')
        sound['music_bg'].loop=True
        sound['music_bg'].volume=1

        #fix bugs from restarting main menu
        try:
            del (self._challenge_map)
            self.clear_widgets()
            self._splash_screen.center = (Window.width / 2, Window.height / 2)
            self._splash_screen.allow_stretch = True
            self._splash_screen.size = Window.size
            self._splash_screen.center = Window.center
            self._splash_screen.source = self.usr_dir + 'loading_down.zip'
        except:
            pass

        # initialize sub-widgets
        self.frame = Image(source=self.usr_dir + 'frame.png', size=(Window.width * 1, Window.height * 1),
                           center=(Window.width * .5, Window.height * .5),
                           allow_stretch=True, keep_ratio=False)

        self._text_display = ChallengeMenu2(usr_dir=self.usr_dir, size=Window.size)
        self._text_display.left_arrow.color[3] = 0
        self._text_display.right_arrow.color[3] = 0

        self._menu_bg = MenuBG(usr_dir=self.usr_dir, size=Window.size, keep_ratio=False, allow_stretch=True,
                               anim_delay=1 / 22)

        self.tut = Tutorial(usr_dir=self.usr_dir, size=Window.size, center=self.center)
        self.tut.center = self.center

        self._splash_screen = LoadingInit(usr_dir=self.usr_dir, size=(Window.size[0] * .5, Window.size[1] * .5),
                                          keep_ratio=False, allow_stretch=False, anim_delay=1 / 12)

        self.nofe = Image(source=self.usr_dir + 'nofe.zip', size=(Window.width * 1, Window.height * 1),
                          center=(Window.width * .5, Window.height * .5),
                          allow_stretch=True, keep_ratio=False, color=[1, 1, 1, .5], anim_delay=1 / 20)

        self.mainmenu = MainMenu(usr_dir=self.usr_dir)
        self.mainmenu.size = (Window.width, Window.height )


        #initialize buttons
        self.tuticon = Tuticon(usr_dir=self.usr_dir)
        # self.tuticon.bind(on_press=self.tuticonpress)

        self._back_button = BackButton(usr_dir=self.usr_dir, size=(planet_qscale * .55, planet_qscale * .55),
                                       pos=(Window.width * .01, Window.height * .94),color=[.46,.54,.6,.8])
        self._back_button.bind(on_press=self.back_btn)
        self.mainmenu.red_bottun.bind(on_press=self.red_press)

        #Animations
        self.remove_mm_anim = Animation( center_y=-Window.height * scale * 1.2, duration=0.6, t='in_back')
        self.add_sp_anim = Animation(duration=.4) + Animation(x=0, y=0, duration=.8, t='out_back')
        self.add_back_anim = Animation(duration=.4) + Animation(x=Window.width * .002, y=Window.height * .94,
                                                                duration=.8, t='in_back')
        self.add_mm_anim = Animation(duration=.2) + Animation(center_y=Window.height * .5, duration=.8, t='out_back')
        self._add_challenge_menu = Animation(duration=.1) + Animation(x=Window.width * .05, y=0, duration=.5,
                                                                      t='in_back')
        self._remove_challenge_menu = Animation(x=0, y=-Window.height, duration=.4, t='in_out_circ')
        self._search_add_anim = Animation(x=Window.width * .1, y=Window.height * .5, duration=1)

        self.remove_tuticon = Animation(center_y=-Window.height / 6, duration=.4)
        self.add_tuticon = Animation(center_y=Window.height / 10)
        self.cancel_layout = Animation(x=-Window.width, y=0, duration=.8, t='out_back')
        self.cancel_back = Animation(x=Window.width * .04, y=Window.height * 1.06, duration=.6, t='out_back')

        # self.text_btn_search=TextBtn(self.usr_dir,'',center_y=Window.height*.45,size=(Window.width*.65,Window.height*.12))
        self._text_display.text_btn.bind(on_release=self.textbtn_press)
        Clock.schedule_once(self.loading_mainframe, -1)
        # self.music_bg.play()
        self.mainmenu.settings.bind(on_press=self.settings_turnon)
        self.mainmenu.profile_icon.bind(on_press=self.profile_turnon)

    def bring_menu_back(self,dt):
        for child in self.mainmenu.children:
            _anim =Animation(d=.2)+ Animation(center_y=child.center_y + Window.height)
            _anim.start(child)

    def profile_turnon(self,dt):
        self.mainmenu.profile_icon.unbind(on_press=self.profile_turnon)

        _animation = Animation(d=.2,center_y=Window.height*.185)
        _animation.start(self.mainmenu.profile_btn)
        _animation.bind(on_complete=self.profile_binder)

        pass

    def profile_binder(self,dt,dx):
        self.mainmenu.profile_btn.bind(on_press=self.profile_press_main)
        pass

    def profile_press_main(self,dt):
        self.mainmenu.profile_btn.unbind(on_press=self.profile_press_main)
        self.mainmenu.profile_icon.bind(on_press=self.profile_turnon)
        _animation2=Animation(center=(self.center_x*1.25,Window.height*.5*.575),d=.1)
        _animation2.start(self.mainmenu.profile_btn)
        for child in self.mainmenu.children:
            _anim =Animation(d=.1)+ Animation(center_y=child.center_y - Window.height)
            _anim.start(child)
        _anim.bind(on_complete=self.profile_menu_bring)
        pass

    def profile_menu_bring(self,dt,dx):

        print('xxx')
        _animation2=Animation(center=(self.center_x*1.25,Window.height*.5*.5-Window.height),d=.001)
        _animation2.start(self.mainmenu.profile_btn)
        self.profile_window=ProfileMenu(usr_dir=self.usr_dir)
        self.add_widget(self.profile_window)
        pass

    def settings_turnon(self,dt):
        self.mainmenu.settings.unbind(on_press=self.settings_turnon)
        _animation2=Animation(center_y=self.mainmenu.settings.center_y+self.mainmenu.settings.size[1]/3
                              ,center_x=self.mainmenu.settings.center_x-self.mainmenu.settings.size[0]/3,d=.1)
        _animation2.start(self.mainmenu.settings)
        _animation2.bind(on_complete=self.setting_binder)

        pass

    def setting_binder(self,dt,dx):
        self.mainmenu.settings.bind(on_press=self.setting_press_main)

    def setting_press_main(self,dt):
        self.mainmenu.settings.unbind(on_press=self.setting_press_main)
        self.mainmenu.settings.bind(on_press=self.settings_turnon)

        for child in self.mainmenu.children:
            _anim =Animation(d=.1)+ Animation(center_y=child.center_y - Window.height)
            _anim.start(child)
        _anim.bind(on_complete=self.settings_menu_bring)
        pass

    def settings_menu_bring(self,dt,dx):
        print('xxx')
        _animation2=Animation(center_y=self.mainmenu.settings.center_y-self.mainmenu.settings.size[1]/3
                              ,center_x=self.mainmenu.settings.center_x+self.mainmenu.settings.size[0]/3,d=.01)
        _animation2.start(self.mainmenu.settings)
        self.settings_window=SettingMenu(usr_dir=self.usr_dir)
        self.add_widget(self.settings_window)

        pass

    def menu_isback(self,dt,dx):
        self.mainmenu.settings.my_rotate.angle=0

    def back_btn(self, dt):
        if self._state_menu == 2:
            for child in self.mainmenu.children:
                _anim = Animation(center_y=child.center_y+Window.height)
                _anim.start(child)
            _anim.bind(on_complete=self.menu_isback)
            Clock.schedule_once(self.fade_in,0)
            for alph in self._keyboard:
                self.remove_widget(self._keyboard[alph])
            self.remove_widget(self.frame)
            self._keyboard = dict()
            self.remove_widget(self.nofe)
            self._text_display.left_arrow.color[3] = 0
            self._text_display.right_arrow.color[3] = 0
            self.remove_widget(self._text_display)
            self._state_menu = 1

        elif self._state_menu == 3:
            # self.remove_widget(self.text_btn_search)
            self._state_menu = 2
            self._text_display.text_btn.disabled=True
            self._text_display.text_btn.text=''
            self._text_display.text_btn_bg.color[3]=0
            self.answer = ''
            # self._text_display._counter.str = ''
            # self._text_display._counter.text = ''
            self._text_display.left_arrow.color[3] = 0
            self._text_display.right_arrow.color[3] = 0
            # self._text_display._tutorial.str = ''
            # self._text_display._tutorial.text = ''
            # self._text_display._message_text.str = ''
            # self._text_display._message_text.text = ''
            self._text_display._gloss_text.str = ''
            self._text_display._gloss_text.text = ''
            self._text_display._input_text.str = ''
            self._text_display._input_text.text = ''
            # Clock.schedule_once(partial(self._text_writer_init, globals()['texts'][1]), 0)
            # Clock.schedule_once(partial(self._tut_writer_init, globals()['tuts'][1]), 0)
        pass

    def create_keyboard(self, dt):
        for alph in globals()['alphabets']:
            self._keyboard[alph] = KeyboardBtn(usr_dir=self.usr_dir, alphabet=alph,
                                               size=(int(Window.width / 12), int(Window.height / 25)))
            self._keyboard[alph].center = globals()['alphabets'][alph]
            self.add_widget(self._keyboard[alph])

        for alph in globals()['alphabets_hold']:
            self._keyboard[alph] = KeyboardBtnHold(usr_dir=self.usr_dir, alphabet=alph,
                                                   size=(int(Window.width / 12), int(Window.height / 25)))
            self._keyboard[alph].center = globals()['alphabets_hold'][alph]
            self.add_widget(self._keyboard[alph])
        self._keyboard['space'] = KeyboardSpc(usr_dir=self.usr_dir, center=(.380 * Window.width, .049 * Window.height),
                                              size=(int(Window.width / 2.5), int(Window.width / 14))
                                              , keep_ratio=False, allow_stretch=True)
        self._keyboard['space'].center = (.48 * Window.width, .03 * Window.height)

        self.add_widget(self._keyboard['space'])
        self._keyboard['backspace'] = KeyboardBspc(usr_dir=self.usr_dir,
                                                   size=(int(Window.width / 5), int(Window.width / 11)))
        self._keyboard['backspace'].center = (.160 * Window.width, .03 * Window.height)
        self.add_widget(self._keyboard['backspace'])
        self._keyboard['enter'] = KeyboardEnter(usr_dir=self.usr_dir,
                                                size=(int(Window.width / 5), int(Window.width / 10)))
        self._keyboard['enter'].center = (.80 * Window.width, .03 * Window.height)
        self._keyboard['enter'].bind(on_release=self.challenge_b_press)
        self.add_widget(self._keyboard['enter'])


    def left_arrow_press(self, dt):
        self._just_pressed = True
        self._text_display.right_arrow.disabled = False
        self._text_display.right_arrow.color = [.28, .72, .54]
        self._locked_on_index += 1
        self._text_display._gloss_text.str = ''
        self._text_display._gloss_text.text = ''
        Clock.schedule_once(partial(self.gloss_writer_new,
                                    self._text_matcher_menu(self._search_results[self._locked_on_index])), 0)

        if self._locked_on_index == len(self._search_results) - 1:
            self._text_display.left_arrow.disabled = True
            # self._text_display.right_arrow.disabled = False
            self._text_display.left_arrow.color = [.5, .5, .54]

    def right_arrow_press(self, dt):
        self._just_pressed = True
        self._text_display.left_arrow.disabled = False
        self._text_display.left_arrow.color = [.28, .72, .54]
        # self._text_display._counter.str = ''
        # self._text_display._counter.text = ''
        self._locked_on_index -= 1
        self._text_display._gloss_text.str = ''
        self._text_display._gloss_text.text = ''

        Clock.schedule_once(partial(self.gloss_writer_new,
                                    self._text_matcher_menu(self._search_results[self._locked_on_index])), 0)

        if self._locked_on_index == 0:
            self._text_display.right_arrow.disabled = True
            self._text_display.right_arrow.color = [.5, .5, .5, 1]

    def textbtn_press(self,dt):
        self._text_display.remove_widget(self._text_display.text_btn)
        self._text_display.remove_widget(self._text_display.text_btn_bg)
        self._last_answer = self.answer
        self._locked_on_id = self._search_results[self._locked_on_index]
        Clock.schedule_once(partial(self.initialize_challenge, self._locked_on_id), 0.1)
        pass

    def challenge_b_press(self, dt):

        self._last_answer = self.answer
        self.answer = self._text_display._input_text.str
        if self.answer.strip(' ') == '':
            if len(self._search_results) > 1:
                # self._locked_on_id = self._search_results[self._locked_on_index]
                # Clock.schedule_once(partial(self.initialize_challenge, self._locked_on_id), 0.1)
                pass
        else:
            self._text_display._input_text.str = ''
            self._text_display._input_text.text = ''
            _results = word_search_db(self.answer, self.conn)
            self._search_results = clean_search_db(_results, self.answer)
            if len(self._search_results) == 0:
                # self._text_display._icon.source = self.usr_dir + 'envelope.png'
                # self._search_results = None
                self._locked_on_id = 0
                # self._text_display._counter.str = ''
                # self._text_display._counter.text = ''
                self._text_display.left_arrow.color[3] = 0
                self._text_display.right_arrow.color[3] = 0
                # self._text_display._tutorial.str = ''
                # self._text_display._tutorial.text = ''
                # self._text_display._message_text.str = ''
                # self._text_display._message_text.text = ''
                self._text_display._gloss_text.str = ''
                self._text_display._gloss_text.text = ''
                self._text_display._input_text.str = ''
                self._text_display._input_text.text = ''
                Clock.schedule_once(partial(self._tut_writer_init, globals()['tuts'][3]), 1 / 120)
                Clock.schedule_once(partial(self._text_writer_init, globals()['texts'][1]), 1 / 120)

                pass
            if len(self._search_results) == 1:
                self._last_answer = self.answer
                # self._text_display._counter.str = ''
                # self._text_display._counter.text = ''
                self._text_display.left_arrow.color[3] = 0
                self._text_display.right_arrow.color[3] = 0
                self._locked_on_index = 0
                self._locked_on_id = self._search_results[0]
                Clock.schedule_once(partial(self.initialize_challenge, self._search_results[0]), .1)
                # Clock.schedule_once(partial(self.initialize_challenge,self._search_results[0]),0)
            elif len(self._search_results) > 1:
                self._text_display.right_arrow.disabled = True
                self._text_display.left_arrow.disabled = False
                try:
                    self._text_display.add_widget(self._text_display.text_btn)
                    self._text_display.add_widget(self._text_display.text_btn_bg,index=2)
                except kivy.uix.widget.WidgetException:
                    pass
                # Clock.schedule_interval(partial(self._counter_text_writer, f'{1} از {len(self._search_results)}'),
                #                         1 / 120)
                self._text_display.left_arrow.color = [.5, .5, .5]
                self._text_display.right_arrow.color = [.5, .5, .5]
                # self._text_display._icon.source = self.usr_dir + 'safineh.jpg'
                # self._text_display._icon._do_press()
                self._locked_on_index = 0

                self._text_display.left_arrow.color = [.28, .72, .54]
                self._text_display.left_arrow.color[3] = 1
                self._text_display.right_arrow.color[3] = 1
                self._text_display.left_arrow.bind(on_press=self.left_arrow_press)
                self._text_display.right_arrow.bind(on_press=self.right_arrow_press)
                self._state_menu = 3
                # self._text_display._tutorial.str = ''
                # self._text_display._tutorial.text = ''
                # self._text_display._message_text.str = ''
                # self._text_display._message_text.text = ''
                self._text_display._input_text.str = ''
                self._text_display._input_text.text = ''
                Clock.schedule_once(partial(self._text_writer_init, globals()['texts'][2]), 0)
                Clock.schedule_once(partial(self._tut_writer_init, globals()['tuts'][2]), 0)
                self._text_display._input_text.focus = False
                self._text_display._gloss_text.str = ''
                self._text_display._gloss_text.text = ''
                # Clock.schedule_once(partial(self.gloss_writer_new, self._text_matcher_menu(self._search_results[0])), 0)
                self._text_display.text_btn.disabled=False
                self._text_display.text_btn_bg.color[3]=.8
                self._text_display.text_btn.text = get_display(arabic_reshaper.reshape(self._text_matcher_menu(self._search_results[0])))
                # self.add_widget(self.text_btn_search,index=70)


    def initialize_challenge(self, ids, dt):
        #self.clear_widgets()
        self._splash_screen = Loading(usr_dir=self.usr_dir, size=(Window.size[0]*.9,Window.size[1]*.8), keep_ratio=False,
                                      allow_stretch=True, anim_delay=1 / 23,center=(self.center_x,self.center_y*1.2))
        self.add_widget(self._splash_screen,index=40)
        t2 = threading.Thread(target=self.start_loading_random
                              , kwargs={'ids': ids}
                              )
        t2.start()

    def finish_loading_challenge(self, dt):
        # self._challenge_map =   Scatter(do_translation=False,do_scale=True,size=self.size,center=self.center,)
        self._challenge_map = MapChallengeNormal(usr_dir=self.usr_dir, midline=[self._mid_line],
                                                 destination_id=self.destination_id_random,
                                                 chosen_id=self._locked_on_id,
                                                 anchors=self._anchors, conn=self.conn, encodings=self.emb,
                                                 data=self.data, size=(Window.width*12,Window.size[1]*10),
                                                 answer_text=self._last_answer,center=self.center)

        # self.add_widget(self._challenge_map)
        Clock.schedule_once(self.remove_splash, .1)

    #     # self.remove_widget(self._splash_screen)
    def remove_splash(self, dt):
        self.add_widget(self._challenge_map)

        self.remove_widget(self._splash_screen)

    def start_loading_random(self, ids):
        pool=[]
        random.seed(a=None,version=2)

        if self.sp_diff == 'ez':
            pool=random.choice([5,6,7,8,])
        else:
            pool=random.choice([1,2,3,4])
        print(pool)
        self.candids = pickle.load(open(self.usr_dir + f'candids_th{pool}', 'rb'))
        # random.seed(a=None,version=2)
        self.destination_id_random = random.choice(self.candids)
        cur = self.conn.cursor()
        cur.execute(f'''SELECT id, score FROM wordb WHERE id IN {tuple(set(self.candids))}''')
        _emb = cur.fetchall()
        self.emb = {}
        for line in _emb:
            self.emb[line[0]] = convert_array(line[1])
        self._anchors = self._find_anchors(self.destination_id_random, self._locked_on_id)
        # print(self.data[self.destination_id_random]['syn_search'])
        # for idss in self._mid_line:
        #     print(self.data[idss]['syn_search'])
        # print(self.data[ids]['syn_search'])

        Clock.schedule_once(self.finish_loading_challenge, 0)

    def _find_anchors(self, id1, id2):
        print('heyhey')
        _nodes = [id1, id2]
        _score_dict = {}
        # conn = sqlite3.connect(self.usr_dir+'pythonsqlite3.db')
        cur = self.conn.cursor()
        # init_ids = []
        init_emb = {}
        for ids in _nodes:
            # print(ids)
            try:
                init_emb[ids] = convert_array(
                    list(cur.execute(f'''SELECT id, score FROM wordb WHERE id={ids}'''))[0][1])
            except sqlite3.OperationalError:
                print(ids)
        cur.close()

        sum_dist = {}
        pool=[]
        random.seed(a=None,version=2)

        pool = random.choices(list(self.emb.keys()),k=350)
        for ids in pool:
            if ids not in _nodes:
                d1 = eucliddean_distance(self.emb[ids], init_emb[id1])
                d2 = eucliddean_distance(self.emb[ids], init_emb[id2])
                if d1 + d2 < 42:
                    sum_dist[ids] = d1 + d2
                if abs(d1 - d2) < 1:
                    _score_dict[ids] = d1 + d2
        print('2')
        _sorted = dict(sorted(sum_dist.items(), key=operator.itemgetter(1)), reverse=True)
        _sorted.pop('reverse')

        print(list(_sorted.keys())[0:10])
        final = list(_sorted.keys())[0:10]
        random.seed(a=None,version=2)

        self._mid_line = random.choice(final)
        for ids in _nodes:
            self.emb[ids] = init_emb[ids]
        _nodes.append(self._mid_line)
        _sorted = {}
        _sorted = dict(sorted(_score_dict.items(), key=operator.itemgetter(1)), reverse=True)
        print(list(_sorted.keys())[0:20])
        _sorted.pop('reverse')
        max_quad = 0
        final_quad = None
        for quad in itertools.combinations(list(_sorted.keys())[0:25], 4):
            _dist = 0
            for double in itertools.combinations(quad, 2):
                # print(double)
                _dist += eucliddean_distance(self.emb[double[0]], self.emb[double[1]])
            if _dist > max_quad:
                max_quad = _dist
                final_quad = quad
        return list(final_quad)

    def _text_matcher_menu(self, ids):
        gettext_raw = ''
        og_text = self.data[ids]['gloss2']
        for char in og_text:
            gettext_raw += char
            if len(gettext_raw.split('\n')[-1]) > globals()['characters_limit'] * 1 and char == ' ':
                gettext_raw += '\n'
        return gettext_raw

    def loading_mainframe(self, dt):
        self.add_widget(self._splash_screen)
        self.data = pickle.load(open(self.usr_dir + 'data', 'rb'))
        pickle.dump(save_game, open(current_dir + 'save', 'wb'))
        # t1 = threading.Thread(target=self.finish_loading_mainframe)
        # t1.start()
        #self.add_widget(self.tuticon)
        sound['music_bg'].play()
        # self.add_widget(self.introvid,index=0)
        self.add_widget(self._menu_bg, index=24)
        self.add_widget(self.mainmenu, index=1)
        self.remove_widget(self._splash_screen)

    def fade_in_step(self,dt):
        self._menu_bg.color[0]+=1/15
        self._menu_bg.color[1]+=1/15
        self._menu_bg.color[2]+=1/15
        if  self._menu_bg.color[0]>=1:
            return False

    def fade_in(self,dt):
        #self.add_widget(self.tuticon)
        self.remove_widget(self._back_button)

        self.add_widget(self._menu_bg,index=4)
        Clock.schedule_interval(self.fade_in_step,1/60)

    def fade_out_step(self,dt):
        self._menu_bg.color[0]-=1/15
        self._menu_bg.color[1]-=1/15
        self._menu_bg.color[2]-=1/15
        if  self._menu_bg.color[0]<=0:
            Clock.schedule_once(self.create_keyboard, -1)
            self.add_widget(self.frame, index=2)
            self.remove_widget(self._menu_bg)
            self._state_menu = 2
            self.add_widget(self.nofe, index=3)
            self.add_widget(self._text_display, index=4)
            self.add_widget(self._back_button)
            _text = globals()['texts'][1]
            _text_tut = globals()['tuts'][1]
            # self._text_display._tutorial.str = ''
            # self._text_display._tutorial.text = ''
            # self._text_display._message_text.str = ''
            # self._text_display._message_text.text = ''
            self._text_display._gloss_text.str = ''
            self._text_display._gloss_text.text = ''
            self._text_display._input_text.str = ''
            self._text_display._input_text.text = ''
            # Clock.schedule_once(partial(self._tut_writer_init,_text_tut),0)
            # Clock.schedule_once(partial(self._text_writer_init,_text),0)
            # self.game_mode=GameModeSelection(usr_dir=self.usr_dir)
            # self.game_mode.center=Window.center
            # self.add_widget(self.game_mode,index=4)

            return False

    def fade_out(self,dt,dtt):
        #self.remove_widget(self.tuticon)
        Clock.unschedule(self.fade_out_step)
        Clock.schedule_interval(self.fade_out_step,1/60)


    def red_press(self, dt):
        if self.mainmenu._toggle_state == 2:


            mode='nl'
            self.mainmenu.settings.my_rotate.angle=0
            for child in self.mainmenu.children:
                _anim = Animation(center_y=child.center_y-Window.height)

                _anim.start(child)
            _anim.bind(on_complete=self.fade_out)
            self.sp_diff = mode

            pass

        elif self.mainmenu._toggle_state == 1:
            mode='ez'
            self.mainmenu.settings.my_rotate.angle=0
            for child in self.mainmenu.children:
                _anim = Animation(center_y=child.center_y-Window.height)

                _anim.start(child)
            _anim.bind(on_complete=self.fade_out)
            self.sp_diff = mode

    def tuticonpress(self, dt):
        try:
            self.add_widget(self.tut)
        except:
            pass

    def gloss_effect_fadein(self,dt):
        self._text_display.text_btn_bg.color[3]+=.2

        if self._just_pressed:
            return False
        if self._text_display.text_btn_bg.color[3]>=.8:
            return False

    def gloss_effect_fade(self,txt,dt):
        self._text_display.text_btn_bg.color[3]-=.2

        if self._just_pressed:
            self._text_display.text_btn.text = get_display(arabic_reshaper.reshape(txt))
            self._text_display.text_btn.str = get_display(arabic_reshaper.reshape(txt))
            Clock.schedule_interval(self.gloss_effect_fadein,0)
            return False
        if self._text_display.text_btn_bg.color[3]<=0 :
            self._text_display.text_btn.text = get_display(arabic_reshaper.reshape(txt))
            self._text_display.text_btn.str = get_display(arabic_reshaper.reshape(txt))
            Clock.schedule_interval(self.gloss_effect_fadein,0)
            return False

    def gloss_writer_new(self,text,dt):
        self._just_pressed = False
        Clock.schedule_interval(partial(self.gloss_effect_fade,text),0)
        pass

    def finish_loading_mainframe(self):
        self.data = pickle.load(open(self.usr_dir + 'data', 'rb'))
        pickle.dump(save_game, open(current_dir + 'save', 'wb'))


    def _tut_writer_init(self, text, dt):
        self._just_pressed = False
        # self._text_display._tutorial.text = ''
        Clock.schedule_interval(partial(self._text_writer, text, 'tut'), 1 / 120)
        pass

    def _text_writer_init(self, text, dt):
        self._just_pressed = False
        # self._text_display._message_text.text = ''
        Clock.schedule_interval(partial(self._text_writer, text, 'text'), 1 / 120)
        pass

    def _text_writer(self, txt, mode, dt):
        if self._just_pressed:
            return False
        # if mode == 'tut':
        #     if self._text_display._tutorial.text == get_display(arabic_reshaper.reshape(txt)):
        #         return False
        #     else:
        #         try:
        #             self._text_display._tutorial.insert_text(
        #                 txt[len(self._text_display._tutorial.text)] + txt[len(self._text_display._tutorial.text) + 1])
        #         except IndexError:
        #             try:
        #                 self._text_display._tutorial.insert_text(txt[len(self._text_display._tutorial.text)])
        #             except IndexError:
        #                 return False
        #     pass
        # elif mode == 'text':
        #     if self._text_display._message_text.text == get_display(arabic_reshaper.reshape(txt)):
        #         return False
        #     else:
        #         try:
        #             self._text_display._message_text.insert_text(
        #                 txt[len(self._text_display._message_text.text)] + txt[
        #                     len(self._text_display._message_text.text) + 1])
        #         except IndexError:
        #             try:
        #                 self._text_display._message_text.insert_text(txt[len(self._text_display._message_text.text)])
        #             except IndexError:
        #                 return False
        elif mode == 'gloss':
            if self._text_display._gloss_text.text == get_display(arabic_reshaper.reshape(txt)):
                # self._text_display.right_arrow.disabled = False
                # self._text_display.left_arrow.disabled = False
                return False
            else:
                try:
                    self._text_display._gloss_text.insert_text(txt[len(self._text_display._gloss_text.text)] + txt[
                        len(self._text_display._gloss_text.text) + 1] + txt[
                                                                   len(self._text_display._gloss_text.text) + 2])
                except IndexError:
                    try:
                        # self._text_display.right_arrow.disabled = False
                        # self._text_display.left_arrow.disabled = False
                        self._text_display._gloss_text.insert_text(txt[len(self._text_display._gloss_text.text)] + txt[
                            len(self._text_display._gloss_text.text) + 1])
                    except IndexError:
                        try:
                            self._text_display._gloss_text.insert_text(txt[len(self._text_display._gloss_text.text)])
                        except:
                            # self._text_display.right_arrow.disabled = False
                            # self._text_display.left_arrow.disabled = False
                            return False
                        pass


class MapChallengeNormal(Widget):

    def __init__(self, usr_dir, chosen_id, destination_id, midline, anchors, conn, encodings, data, answer_text,
                 **kwargs):
        super().__init__(**kwargs)

        self.help_layout = None
        self.answer_iterator = ''
        self.scatter_layout=Scatter(size=self.size,do_translation=False,do_rotation=False,do_scale=False,do_collide_after_children=False
                                    ,auto_bring_to_front=False)
        self.add_widget(self.scatter_layout,index=0)

        self.moving_layout=Scatter(scale_min=.35, scale_max=1.7,scale=.9,size=(Window.width*4,Window.height*5),do_translation=True,do_rotation=False,do_scale=True,do_collide_after_children=False
                                    ,auto_bring_to_front=False)
        self.add_widget(self.moving_layout,index=3)
        self.moving_layout.center_x-=Window.width*1.3
        self._found_one = False
        self._just_pressed = False
        self._bait_pos2 = None
        # self._safineh_moving
        self.connection = conn
        self._bait_pos1 = None
        self._locked_on_index = int()
        self._locked_on_id = int()
        self._search_results = list()
        self.answer = ''
        self._last_planet = chosen_id
        self.chosen_id = chosen_id
        self.midline = midline
        self.destination_id = destination_id
        self.anchors = anchors
        self.encodings = encodings
        self.time_limit = 300
        self._final_click = None
        self._safineh_moving = False
        self._keyboard = dict()
        self._fuel = 100
        self._chosen_text = answer_text
        self.usr_dir = usr_dir
        self._planets_moving = True
        self._camera_bul_moving = False
        self.quit_bul = False
        self.reset_bul = False
        self.planet_labels = {}
        self.quit_btn = QuitButton(usr_dir=self.usr_dir)
        self.quit_btn.center = (Window.width * .94, Window.height * .98)
        self.quit_btn.bind(on_release=self.quit_to_main)
        self.back_btn = BackButtonInGame(usr_dir=self.usr_dir)
        self.back_btn.center = (Window.width * .06, Window.height * .98)
        self.back_btn.bind(on_release=self.pause_menu)

        self._fuel_icon=Image(source=self.usr_dir+'fuel.png',allow_stretch=True,keep_ratio=False,size=(planet_qscale/3,planet_qscale/3),center=(Window.width * .15, Window.height * .93))
        self.scatter_layout.add_widget(self._fuel_icon)
        self._fuel_counter = Label(font_name=self.usr_dir + 'B Elm_0.ttf', font_size=globals()['font_scale']*1.2,
                                   center=(Window.width * .207, Window.height * .927),color=[.28, .72, .54],
                                   text=get_display(arabic_reshaper.reshape(f'{self._fuel}')))
        self.scatter_layout.add_widget(self._fuel_counter)

        self._time = time.perf_counter()

        time_display = self.time_limit - int(time.perf_counter() - self._time)

        self.timer = Label(font_name=self.usr_dir + 'B Elm_0.ttf', font_size=globals()['font_scale'] * 1,base_direction='rtl',
                           center=(Window.width * .18, Window.height * .895),color=[.28, .72, .54],halign='center',
                           text=get_display(arabic_reshaper.reshape(
                               f'{int(time_display/60)}:{time_display%60}')))

        self.scatter_layout.add_widget(self.timer)
        self.data = data
        self._word_objects = {}
        self._planet_size = (planet_scale, planet_scale)
        self._planet_qsize = (planet_qscale, planet_qscale)

        with self.moving_layout.canvas.before:
            self._bg = Image(source=self.usr_dir + 'back back.jpg', size=(Window.size[0] * 7, Window.size[1] * 5),
                             color=[1, 1, 1, 1])
            self._bg.keep_ratio = False
            self._bg.allow_stretch = True
            self._bg.center = (self.center[0]*5,self.center_y*2)
        self._text_display = ChallengeMenu2(usr_dir=self.usr_dir, size=Window.size)
        self.add_widget(self._text_display)
        self._text_display.left_arrow.disabled = True
        self._text_display.right_arrow.disabled = True
        # self._safineh_aflak.my_rotate.angle=90
        self._text_display.left_arrow.color[3] = 0
        self._text_display.right_arrow.color[3] = 0
        self._text_display.left_arrow.bind(on_press=self.left_arrow_press)
        self._text_display.right_arrow.bind(on_press=self.right_arrow_press)
        self.nofe = Image(source=self.usr_dir + 'nofe.zip', size=(Window.width * 1, Window.height * 1),
                          center=(Window.width * .5, Window.height * .5),
                          allow_stretch=True, keep_ratio=False, color=[1, 1, 1, .4], anim_delay=1 / 18)
        self.add_widget(self.nofe,index=2)
        # with self.canvas:
        self.frame = Image(source=self.usr_dir + 'frame.png', size=(Window.width * 1, Window.height * 1),
                           center=(Window.width * .5, Window.height * .5),
                           allow_stretch=True, keep_ratio=False)
        self.safineh = SafineAflak(usr_dir=self.usr_dir)
        self.moving_layout.add_widget(self.safineh, index=0)
        self.safineh_audio = SoundLoader.load(self.usr_dir+'spin.ogg')
        self.safineh_audio.play()
        self.safineh_audio.loop=True
        self.safineh_audio.volume=1
        self.radar=RadarBtn(usr_dir=self.usr_dir)
        self.radar.bind(on_release=self.give_tip)
        self.moving_layout.bind(on_transform_with_touch=self.moving_scatter_bind)

        # Clock.schedule_interval(partial(self._text_writer, globals()['tuts_ingame'][1], 'tut'), 1 / 120)
        Clock.schedule_interval(partial(self._text_writer, globals()['texts_ingame'][1], 'text'), 1 / 120)
        Clock.schedule_once(self._initialize_map, -1)
        Clock.schedule_once(self.create_keyboard, -1)
        self.main_event=Clock.schedule_interval(self._callback_main, 1 / 60)
        self.scatter_layout.add_widget(self.frame, index=0)
        self._text_display.text_btn.bind(on_release=self.text_btn_press)

        self.scatter_layout.add_widget(self.radar,index=5)
        self.pause_bg=StoryButton(usr_dir=self.usr_dir, size=(Window.width * .8, Window.height * .4),
                                            center=(Window.width * .5, Window.height * .7), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
        self.pause_msg=Label(center=self.pause_bg.center)
        self.pause_msg.font_name = self.usr_dir + 'Aflak Bold(1).ttf'
        self.pause_msg.font_size = int(globals()['font_scale'] * .91)
        self.pause_msg.halign = 'center'
        self.pause_msg.text = get_display(
            arabic_reshaper.reshape('برای خروج یا تکرار مرحله گزینه های زیر را بزن\n دکمه منو را دوباره بزن تا به بازی برگردی'))

        self.pause_dobare_btn = StoryResetButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                           center=(Window.width * .35, Window.height * .4), allow_stretch=True,
                                           keep_ratio=False, color=[.23, .4, .85, .99])

        self.pause_exit_btn = StoryExitButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                        center=(Window.width * .65, Window.height * .4), allow_stretch=True,
                                        keep_ratio=False, color=[.23, .4, .85, .99])

        self.pause_dobare_btn.bind(on_release=self.reset_init)
        self.pause_exit_btn.bind(on_release=self.quit_to_main)

    # def on_transform_with_touch(self, touch):
    #     print(touch)
    #     print(self.moving_layout.center)

    def moving_scatter_bind(self, touch, dx):
        if self.moving_layout.center[0] > Window.width*3.1*self.moving_layout.scale:
            self.moving_layout.center_x -= 40
        elif self.moving_layout.center[0] < -.9*Window.width*self.moving_layout.scale:
            self.moving_layout.center_x += 40

        if self.moving_layout.center[1] > Window.height*3.9*self.moving_layout.scale:
            self.moving_layout.center_y -= 40
        elif self.moving_layout.center[1] < 1.0*Window.height*self.moving_layout.scale:
            self.moving_layout.center_y += 40

    def pause_menu(self,dt):
        try:
            self.add_widget(self.pause_exit_btn, index=0)
            self.add_widget(self.pause_dobare_btn, index=0)
            self.add_widget(self.pause_bg, index=0)
            self.add_widget(self.pause_msg, index=0)
            # add pause menu
        except:
            self.remove_widget(self.pause_exit_btn)
            self.remove_widget(self.pause_dobare_btn)
            self.remove_widget(self.pause_bg)
            self.remove_widget(self.pause_msg)
            # remove pause menu
            pass

    def text_btn_release(self,dt):
        self._text_display.remove_widget(self._text_display.text_btn)
        self._text_display.remove_widget(self._text_display.text_btn_bg)

    def text_btn_press(self,dt):

        self._last_written = self.answer
        self._text_display.text_btn_bg.color[3]=0
        self._text_display.text_btn.color[3]=0
        self._text_display.text_btn.disabled=True
        self._text_display._gloss_text.str = ''
        self._text_display._gloss_text.text = ''
        self._text_display._input_text.str = ''
        self._text_display._input_text.text = ''
        # self._text_display._counter.str = ''
        # self._text_display._counter.text = ''
        self._text_display.left_arrow.color[3] = 0
        self._text_display.right_arrow.color[3] = 0

        self._locked_on_id = self._search_results[self._locked_on_index]
        Clock.schedule_once(self.init_create, 0.01)
        self._text_display.remove_widget(self._text_display.text_btn)
        self._text_display.remove_widget(self._text_display.text_btn_bg)

        pass

    def _callback_main(self, dt):
        self.frame.center=(Window.width/2,Window.height/2)
        self.safineh.my_rotate2.origin = self.safineh.center
        self.safineh.my_rotate.origin = (self.safineh.center_x, self.safineh.center_y - planet_scale * .7)
        if not self._safineh_moving:
            self.safineh.my_rotate.angle += self.safineh.step

        # Check if I`ve quit
        if self.quit_bul:
            self.safineh_audio.stop()
            return False
        if self.reset_bul:
            self.safineh_audio.stop()
            return False
        # self.timer.center=(Window.width * .18, Window.height * .895)
        # Update and check Fuel and Timer
        self._fuel_counter.text = get_display(arabic_reshaper.reshape(f'{int(self._fuel)}'))
        if int(self._fuel) < .01:
            Clock.schedule_once(partial(self.finish_game, 'lose_f'), .1)
            self.safineh_audio.stop()

            return False
        time_display = self.time_limit - int(time.perf_counter() - self._time)
        self.timer.text = get_display(arabic_reshaper.reshape(
                               f'{int(time_display/60)}:{time_display%60}'))
        if self.time_limit - int(time.perf_counter() - self._time) < .1:
            Clock.schedule_once(partial(self.finish_game, 'lose_t'), .1)
            self.safineh_audio.stop()

            return False

        _moving = set()

        # Update displayed info on planets
        for ids in self._word_objects:
            if self._word_objects[ids].type == 'on':
                self._word_objects[ids].info_ratio = 1
            elif self._word_objects[ids].type == 'off':
                self._word_objects[ids].info_ratio = .1
                if eucliddean_distance(
                        np.asarray((self.safineh.center[0], self.safineh.center[1] - .7 * planet_qscale)),
                        np.asarray(self._word_objects[ids].center)) < 5 * planet_qscale:
                    self._word_objects[ids].info_ratio = .22
                for ww in self._word_objects:
                    if ww != ids and eucliddean_distance(self._word_objects[ww].center,
                                                         self._word_objects[ids].center) <= 5 * planet_qscale:
                        self._word_objects[ids].info_ratio += .22
            else:
                _radial = eucliddean_distance((self.safineh.center[0], self.safineh.center[1] - .7 * planet_qscale),
                                              self._word_objects[ids].center)
                if _radial > 7 * planet_qscale:
                    self._word_objects[ids].info_ratio = .15
                else:
                    self._word_objects[ids].info_ratio = 1

        # Position updater
        moving_words = list()
        for pairs in itertools.combinations(list(self._word_objects.keys()), 2):
            if eucliddean_distance(np.asarray(list(self._word_objects[pairs[0]].pos)),
                                   np.asarray(list(self._word_objects[pairs[1]].pos))) < 2 * self._planet_size[0]:
                if self._last_planet == pairs[0]:
                    moving_words.append(pairs[1])
                    dx, dy = self._math_position(pairs[1])
                    self._word_objects[pairs[1]].center_x += dx
                    self._word_objects[pairs[1]].center_y += dy
                    if pairs[1] in self.planet_labels:
                        self.planet_labels[pairs[1]].center_x += dx
                        self.planet_labels[pairs[1]].center_y += dy

                    pass
                elif self._last_planet == pairs[1]:
                    moving_words.append(pairs[0])
                    dx, dy = self._math_position(pairs[0])
                    self._word_objects[pairs[0]].center_x += dx
                    self._word_objects[pairs[0]].center_y += dy
                    if pairs[0] in self.planet_labels:
                        self.planet_labels[pairs[0]].center_x += dx
                        self.planet_labels[pairs[0]].center_y += dy
                    pass
                elif self._last_planet not in pairs:
                    if pairs[0] in moving_words:
                        moving_words.append(pairs[1])
                        dx, dy = self._math_position_dynamic(pairs[1], pairs[0])
                        self._word_objects[pairs[1]].center_x += dx
                        self._word_objects[pairs[1]].center_y += dy
                        if pairs[1] in self.planet_labels:
                            self.planet_labels[pairs[1]].center_x += dx
                            self.planet_labels[pairs[1]].center_y += dy
                    elif pairs[1] in moving_words:
                        moving_words.append(pairs[0])
                        dx, dy = self._math_position_dynamic(pairs[0], pairs[1])
                        self._word_objects[pairs[0]].center_x += dx
                        self._word_objects[pairs[0]].center_y += dy
                        if pairs[0] in self.planet_labels:
                            self.planet_labels[pairs[0]].center_x += dx
                            self.planet_labels[pairs[0]].center_y += dy
                    else:
                        moving_words.append(pairs[1])
                        dx, dy = self._math_position_dynamic(pairs[1], pairs[0])
                        self._word_objects[pairs[1]].center_x += dx
                        self._word_objects[pairs[1]].center_y += dy
                        if pairs[1] in self.planet_labels:
                            self.planet_labels[pairs[1]].center_x += dx
                            self.planet_labels[pairs[1]].center_y += dy

    def _math_position_dynamic(self, id1, id2):
        delta_x = self._word_objects[id1].center_x - self._word_objects[id2].center_x
        delta_y = self._word_objects[id1].center_y - self._word_objects[id2].center_y
        return (delta_x + 1) / (abs(delta_x + delta_y) + 1), (delta_y + 1) / (abs(delta_x + delta_y) + 1)

    def _math_position(self, ids):
        delta_x = self._word_objects[ids].center_x - self._word_objects[self._last_planet].center_x
        delta_y = self._word_objects[ids].center_y - self._word_objects[self._last_planet].center_y
        return (delta_x + 1) / (abs(delta_x + delta_y) + 1), (delta_y + 1) / (abs(delta_x + delta_y) + 1)

    def gloss_effect_fadein(self,dt):
        self._text_display.text_btn_bg.color[3]+=.2

        if self._just_pressed:
            return False
        if self._text_display.text_btn_bg.color[3]>=.8:
            return False

    def gloss_effect_fade(self,txt,dt):
        self._text_display.text_btn_bg.color[3]-=.2

        if self._just_pressed:
            self._text_display.text_btn.text = get_display(arabic_reshaper.reshape(txt))
            self._text_display.text_btn.str = get_display(arabic_reshaper.reshape(txt))
            Clock.schedule_interval(self.gloss_effect_fadein,0)
            return False
        if self._text_display.text_btn_bg.color[3]<=0 :
            self._text_display.text_btn.text = get_display(arabic_reshaper.reshape(txt))
            self._text_display.text_btn.str = get_display(arabic_reshaper.reshape(txt))
            Clock.schedule_interval(self.gloss_effect_fadein,0)
            return False

    def gloss_writer_new(self,text,dt):
        self._just_pressed = False
        Clock.schedule_interval(partial(self.gloss_effect_fade,text),0)
        pass

    def _gloss_writer_init_ingame(self, text, dt):
        self._just_pressed = False
        self._text_display._gloss_text.text = ''
        Clock.schedule_interval(partial(self._text_writer, text, 'gloss'), 1 / 120)
        pass

    def _text_writer(self, txt, mode, dt):
        if self._just_pressed:
            return False
        # if mode == 'tut':
        #     if self._text_display._tutorial.text == get_display(arabic_reshaper.reshape(txt)):
        #         return False
        #     else:
        #         try:
        #             self._text_display._tutorial.insert_text(
        #                 txt[len(self._text_display._tutorial.text)] + txt[len(self._text_display._tutorial.text) + 1])
        #         except IndexError:
        #             try:
        #                 self._text_display._tutorial.insert_text(txt[len(self._text_display._tutorial.text)])
        #             except IndexError:
        #                 return False
        #     pass
        # elif mode == 'text':
        #     if self._text_display._message_text.text == get_display(arabic_reshaper.reshape(txt)):
        #         return False
        #     else:
        #         try:
        #             self._text_display._message_text.insert_text(
        #                 txt[len(self._text_display._message_text.text)] + txt[
        #                     len(self._text_display._message_text.text) + 1])
        #         except IndexError:
        #             try:
        #                 self._text_display._message_text.insert_text(txt[len(self._text_display._message_text.text)])
        #             except IndexError:
        #                 return False
        if mode == 'gloss':
            if self._text_display._gloss_text.text == get_display(arabic_reshaper.reshape(txt)):
                # self._text_display.right_arrow.disabled = False
                # self._text_display.left_arrow.disabled = False
                return False
            else:
                try:
                    self._text_display._gloss_text.insert_text(txt[len(self._text_display._gloss_text.text)] + txt[
                        len(self._text_display._gloss_text.text) + 1] + txt[
                                                                   len(self._text_display._gloss_text.text) + 2])
                except IndexError:
                    try:
                        # self._text_display.right_arrow.disabled = False
                        # self._text_display.left_arrow.disabled = False
                        self._text_display._gloss_text.insert_text(txt[len(self._text_display._gloss_text.text)] + txt[
                            len(self._text_display._gloss_text.text) + 1])
                    except IndexError:
                        try:
                            self._text_display._gloss_text.insert_text(txt[len(self._text_display._gloss_text.text)])
                        except:
                            # self._text_display.right_arrow.disabled = False
                            # self._text_display.left_arrow.disabled = False
                            return False
                        pass

    def _label_planet_puter(self, _text, ids, dt):
        self.planet_labels[ids] = Label(font_name=self.usr_dir + 'Aflak Bold(1).ttf',
                                        font_size=int(globals()['font_scale'] * 1), color=[.23, .24, .82, .8])
        self.planet_labels[ids].center = self._word_objects[ids].center
        self.planet_labels[ids].text = get_display(arabic_reshaper.reshape(_text))
        Clock.schedule_once(partial(self.add_planet_label, ids), 1.7)
        self.answer_iterator+=" , "+_text
        pass

    def add_planet_label(self, ids, dt):
        self.moving_layout.add_widget(self.planet_labels[ids], index=0)

    def _initialize_map(self, dt):
        self._word_objects[self.chosen_id] = WordsPlanetOn(usr_dir=self.usr_dir,
                                                           size=self._planet_size)
        self._word_objects[self.chosen_id].center = (Window.width * 2, Window.height * .6)
        self.moving_layout.add_widget(self._word_objects[self.chosen_id], index=0)

        self._word_objects[self.destination_id] = WordsPlanetOff(usr_dir=self.usr_dir, size=self._planet_size)
        self._word_objects[self.destination_id].center = (Window.width * 2,
                                                          25* (
                                                                          planet_scale / 2) + Window.height * .45
                                                              )
        self.moving_layout.add_widget(self._word_objects[self.destination_id], index=0)

        Clock.schedule_once(partial(self._label_planet_puter, self._chosen_text, self.chosen_id), 0)

        pos_mid, pos_gusheh = self._position_maker()

        for ii in range(len(pos_mid)):
            self._word_objects[self.midline[ii]] = WordsPlanetQuestion(usr_dir=self.usr_dir)
            self._word_objects[self.midline[ii]].center = pos_mid[ii]
            self._word_objects[self.midline[ii]].size = self._planet_qsize
            self.moving_layout.add_widget(self._word_objects[self.midline[ii]], index=0)

        for ii in range(len(pos_gusheh)):
            self._word_objects[self.anchors[ii]] = WordsPlanetQuestion(usr_dir=self.usr_dir)
            self._word_objects[self.anchors[ii]].center = pos_gusheh[ii]
            self._word_objects[self.anchors[ii]].size = self._planet_qsize
            self.moving_layout.add_widget(self._word_objects[self.anchors[ii]], index=0)
        self.safineh.center_x = self._word_objects[self.chosen_id].center_x
        self.safineh.center_y = self._word_objects[self.chosen_id].center_y + planet_scale * .7
        for word in self._word_objects:
            self._word_objects[word].bind(on_press=partial(self.press_planet, word))
            self._word_objects[word].bind(on_release=self.release_planet)
        # self.add_widget(self.quit_btn, index=0)
        self.scatter_layout.add_widget(self.back_btn, index=0)

    def _position_maker(self):
        pos_list_mid = list()
        self._mid_point = [self._word_objects[self.chosen_id].center_x,
                           self._word_objects[self.chosen_id].center_y + ((self._word_objects[
                                                                               self.destination_id].center_y -
                                                                           self._word_objects[
                                                                               self.chosen_id].center_y) * .5)]

        mid_up = [self._word_objects[self.chosen_id].center_x,
                  (self._mid_point[1] + self._word_objects[self.destination_id].center_y) * .5]

        mid_down = [self._word_objects[self.chosen_id].center_x,
                    (self._mid_point[1] + self._word_objects[self.chosen_id].center_y) * .5]

        mid_down_down = [self._word_objects[self.chosen_id].center_x,
                         (mid_down[1] + self._word_objects[self.chosen_id].center_y) * .5
                         ]
        # mid_down_down_down = [self._word_objects[self.chosen_id].center_x,
        #              (mid_down_down[1] + self._word_objects[self.chosen_id].center_y) * .5
        #              ]

        # pos_list_mid.append(mid_up)
        pos_list_mid.append(self._mid_point)
        # pos_list_mid.append(mid_down)
        # pos_list_mid.append(mid_down_down)
        # pos_list_mid.append(mid_down_down_down)

        anchors = []

        right_up = [self._word_objects[self.destination_id].center_x + (
                self._word_objects[self.destination_id].center_y - self._word_objects[
            self.chosen_id].center_y) * .5,
                    self._word_objects[self.destination_id].center_y - (
                            self._word_objects[self.destination_id].center_y - self._word_objects[
                        self.chosen_id].center_y) * .15]

        left_up = [self._word_objects[self.destination_id].center_x - (
                self._word_objects[self.destination_id].center_y - self._word_objects[
            self.chosen_id].center_y) * .5,
                   self._word_objects[self.destination_id].center_y - (
                           self._word_objects[self.destination_id].center_y - self._word_objects[
                       self.chosen_id].center_y) * .15]

        right_down = [self._word_objects[self.chosen_id].center_x + (
                self._word_objects[self.destination_id].center_y - self._word_objects[
            self.chosen_id].center_y) * .5,
                      self._word_objects[self.chosen_id].center_y + ((self._word_objects[
                                                                          self.destination_id].center_y -
                                                                      self._word_objects[
                                                                          self.chosen_id].center_y) * .15)]

        left_down = [self._word_objects[self.chosen_id].center_x - (
                self._word_objects[self.destination_id].center_y - self._word_objects[
            self.chosen_id].center_y) * .5,
                     self._word_objects[self.chosen_id].center_y + ((self._word_objects[
                                                                         self.destination_id].center_y -
                                                                     self._word_objects[
                                                                         self.chosen_id].center_y) * .15)]

        anchors.append(left_up)
        anchors.append(right_up)
        anchors.append(left_down)
        anchors.append(right_down)
        return pos_list_mid, anchors

    def create_keyboard(self, dt):
        for alph in globals()['alphabets']:
            self._keyboard[alph] = KeyboardBtn(usr_dir=self.usr_dir, alphabet=alph,
                                               size=(int(Window.width / 12), int(Window.height / 25)))
            self._keyboard[alph].center = globals()['alphabets'][alph]
            self.add_widget(self._keyboard[alph])

        for alph in globals()['alphabets_hold']:
            self._keyboard[alph] = KeyboardBtnHold(usr_dir=self.usr_dir, alphabet=alph,
                                                   size=(int(Window.width / 12), int(Window.height / 25)))
            self._keyboard[alph].center = globals()['alphabets_hold'][alph]
            self.add_widget(self._keyboard[alph])
        self._keyboard['space'] = KeyboardSpc(usr_dir=self.usr_dir, center=(.380 * Window.width, .049 * Window.height),
                                              size=(int(Window.width / 2.5), int(Window.width / 14))
                                              , keep_ratio=False, allow_stretch=True)
        self._keyboard['space'].center = (.48 * Window.width, .03 * Window.height)

        self.add_widget(self._keyboard['space'])
        self._keyboard['backspace'] = KeyboardBspc(usr_dir=self.usr_dir,
                                                   size=(int(Window.width / 5), int(Window.width / 11)))
        self._keyboard['backspace'].center = (.160 * Window.width, .03 * Window.height)
        self.add_widget(self._keyboard['backspace'])
        self._keyboard['enter'] = KeyboardEnter(usr_dir=self.usr_dir,
                                                size=(int(Window.width / 5), int(Window.width / 10)))
        self._keyboard['enter'].center = (.80 * Window.width, .03 * Window.height)
        self._keyboard['enter'].bind(on_release=self.challenge_b_press_ingame)
        self.add_widget(self._keyboard['enter'])

    def quit_to_main(self, dt):
        self.quit_bul = True
        try:
            self.end_audio.stop()
        except:
            pass
        if self.parent._state_menu == 3:
            Clock.schedule_once(self.parent.back_btn,-1)
            # self.parent.clear_widgets()
        # self.parent.__init__(usr_dir=self.usr_dir, conn=self.parent.conn)
        self.parent._last_answer=self._chosen_text
        self.parent.answer=self._chosen_text
        self.parent.remove_widget(self)

        del(self)

    def give_tip(self, dt):
        try:
            self.scatter_layout.remove_widget(self.help_layout)
        except:
            pass
        self.help_layout = None
        ans = set()
        self._fuel -= 7
        _potential=set()
        for ids in self._word_objects:
            if self._word_objects[ids].type != 'on' and eucliddean_distance(self._word_objects[ids].center,
                                                                            self._word_objects[
                                                                                self._last_planet].center)< 6 * \
                    self._planet_size[0]*(1/self.moving_layout.scale):
                _nodes = [self._last_planet, ids]

                _score_dict = {}
                # conn = sqlite3.connect(self.usr_dir+'pythonsqlite3.db')
                cur = self.connection.cursor()
                # init_ids = []
                init_emb = {}
                for node in _nodes:
                    # print(ids)
                    try:
                        init_emb[node] = convert_array(
                            list(cur.execute(f'''SELECT id, score FROM wordb WHERE id={node}'''))[0][1])
                    except sqlite3.OperationalError:
                        print(node)
                cur.close()
                print('heyyy')
                sum_dist = {}
                random.seed(a=None, version=2)
                pool = random.choices(list(self.encodings.keys()),k=450)
                for enc in pool:
                    if enc not in _nodes:
                        d1 = eucliddean_distance(self.encodings[enc], init_emb[self._last_planet])
                        d2 = eucliddean_distance(self.encodings[enc], init_emb[ids])
                        sum_dist[enc] = d1 + d2

                print('2')
                _sorted = dict(sorted(sum_dist.items(), key=operator.itemgetter(1)), reverse=False)
                _sorted.pop('reverse')

                _final = list(_sorted.keys())[0:10]
                _index = 0
                while True:
                    if _final[_index] not in list(self._word_objects.keys()):
                        ans.add(_final[_index])
                        break
                    else:
                        _index += 1
        ans=list(ans)
        cur = self.connection.cursor()
        for ids in self._word_objects:
            if self._word_objects[ids].type != 'on' and eucliddean_distance(self.encodings[ids], convert_array(
                            list(cur.execute(f'''SELECT id, score FROM wordb WHERE id={self._last_planet}'''))[0][1]))<12:
                print(eucliddean_distance(self.encodings[ids], convert_array(
                            list(cur.execute(f'''SELECT id, score FROM wordb WHERE id={self._last_planet}'''))[0][1])))
                _potential.add(ids)

        if len(_potential)>0:
            random.seed(a=None, version=2)
            ans.remove(random.choice(ans))
            ans.append(random.choice(list(_potential)))

        random.shuffle(ans)
        for nn in ans:
            print(self.data[nn]['syn_search'])

        self.help_layout = Accordion(center=(Window.width*.5,Window.height*.5), size=(Window.width * .8, Window.height * .2))
        self.help_layout.center = (self.center[0], self.center[1] * .8)
        self.help_layout.padding = 0
        for nn in ans:
            item = AccordionItem(title='Title %d' % nn,background_normal=self.usr_dir+'btntut.png')
            # item.size=(100,100)
            item.add_widget(TextBtn( string=self.data[nn]['syn_search'].split(',')[0],
                                               on_press=partial(self.help_press, nn),
                                               usr_dir=self.usr_dir))
            self.help_layout.add_widget(item)
        self.scatter_layout.add_widget(self.help_layout)
        pass

    def help_press(self, ids, dt):
        if ids in self._word_objects:
            if self._word_objects[ids].type == 'q':
                self._found_one = True
                _pos = self._word_objects[ids].center
                self.moving_layout.remove_widget(self._word_objects[ids])
                self._word_objects[ids] = WordsPlanetOn(usr_dir=self.usr_dir,
                                                               size=self._planet_size,
                                                               center=_pos)
                self._word_objects[ids].source = self.usr_dir + 'planet_found.zip'
                self._word_objects[ids].anim_delay = 1 / 4
                self._word_objects[ids].bind(on_press=partial(self.press_planet, ids))
                self.moving_layout.add_widget(self._word_objects[ids], index=0)

                Clock.schedule_once(partial(self._label_planet_puter, self.data[ids]['words'].split(',')[0], ids), 0)
                Clock.schedule_interval(partial(self._move_camera, ids), 1 / 60)
            elif self._word_objects[ids].type == 'off':
                Clock.schedule_once(partial(self.finish_game, 'win'), .1)
                self.main_event.cancel()
                pass


            self.scatter_layout.remove_widget(self.help_layout)
            self.help_layout = None
            pass
        else:
            self._locked_on_id = ids
            self._last_written = self.data[ids]['words'].split(',')[0]

            Clock.schedule_once(self.init_create, 0)
            self.scatter_layout.remove_widget(self.help_layout)
            self.help_layout = None
        pass

    def press_planet(self, ids, dt):
        self._text_display.left_arrow.disabled = True
        self._text_display.left_arrow.color[3] = 0
        self._text_display.right_arrow.disabled = True
        self._text_display.right_arrow.color[3] = 0
        self._text_display._gloss_text.text = get_display(arabic_reshaper.reshape(self._text_matcher(ids)))
        self._text_display._gloss_text.str = get_display(arabic_reshaper.reshape(self._text_matcher(ids)))
        # Clock.schedule_once(partial(self.radar, self._last_planet, ids), 0)
        print(self.data[ids]['syn_search'])
        pass

    def radar(self, id1, id2, dt):
        _nodes = [id1, id2]
        _score_dict = {}
        # conn = sqlite3.connect(self.usr_dir+'pythonsqlite3.db')
        cur = self.connection.cursor()
        # init_ids = []
        init_emb = {}
        for ids in _nodes:
            # print(ids)
            try:
                init_emb[ids] = convert_array(
                    list(cur.execute(f'''SELECT id, score FROM wordb WHERE id={ids}'''))[0][1])
            except sqlite3.OperationalError:
                print(ids)
        cur.close()
        print('heyyy')
        sum_dist = {}
        for ids in self.encodings:
            if ids not in _nodes:
                d1 = eucliddean_distance(self.encodings[ids], init_emb[id1])
                d2 = eucliddean_distance(self.encodings[ids], init_emb[id2])
                if d1 + d2 < 40:
                    sum_dist[ids] = d1 + d2

        print('2')
        _sorted = dict(sorted(sum_dist.items(), key=operator.itemgetter(1)), reverse=False)
        _sorted.pop('reverse')
        print(f'kalameye to:\n {self.data[id1]["syn_search"]}')
        print(f'kalameye hadaf:\n {self.data[id2]["syn_search"]}')

        final = list(_sorted.keys())[0:10]
        for ids in final:
            print(self.data[ids]['syn_search'])

    def release_planet(self, dt):
        self._text_display._gloss_text.text = ''
        self._text_display._gloss_text.str = ''
        pass

    def _text_matcher(self, ids):
        gettext_raw = ''
        info_ratio = self._word_objects[ids].info_ratio
        # print(info_ratio)
        og_text = self.data[ids]['gloss2']
        words = set(og_text.split())
        if info_ratio == 0:
            return '..... ...... ...... ......'
        else:
            random.seed(17)
            deleted_words = set()
            while len(deleted_words) <= int((1 - info_ratio) * len(words) - 1):

                deleted_words.add(random.choice(list(words)))
            # print(deleted_words)
            for w in deleted_words:
                _tmp = ''
                for char in w:
                    _tmp += '.'
                og_text = og_text.replace(f' {w} ', f' {_tmp} ')
            for char in og_text:
                gettext_raw += char
                if len(gettext_raw.split('\n')[-1]) > globals()['characters_limit'] * 1.4 and char == ' ':
                    gettext_raw += '\n'

        for syn in self.data[ids]['syn_search'].split(','):
            gettext_raw = gettext_raw.replace(syn, '***')
        return gettext_raw
    #
    # def on_touch_move(self, touch):
    #
    #     # self.safineh.my_rotate.origin = (self.safineh.center_x, self.safineh.center_y - planet_scale * .7)
    #     if self._final_click is not None and not self._camera_bul_moving:
    #         step_size = 1
    #         self.safineh.center_x -= (self._final_click[0] - touch.pos[0]) * 1
    #         self.safineh.center_y -= (self._final_click[1] - touch.pos[1]) * 1
    #         if not self._safineh_moving:
    #             self.safineh.my_rotate2.origin = self.safineh.center
    #             self.safineh.my_rotate.origin = (self.safineh.center_x, self.safineh.center_y - planet_scale * .7)
    #
    #         # self.safineh.my_rotate.origin = self.safineh.center
    #         if eucliddean_distance(self._final_click, touch.pos) < 400:
    #             if self._safineh_moving:
    #                 self._bait_pos1[0] -= (self._final_click[0] - touch.pos[0]) * step_size
    #                 self._bait_pos1[1] -= (self._final_click[1] - touch.pos[1]) * step_size
    #
    #                 self._bait_pos2[0] -= (self._final_click[0] - touch.pos[0]) * step_size
    #                 self._bait_pos2[1] -= (self._final_click[1] - touch.pos[1]) * step_size
    #
    #             for ids in self.planet_labels:
    #                 self.planet_labels[ids].center_x -= (self._final_click[0] - touch.pos[0]) * step_size
    #                 self.planet_labels[ids].center_y -= (self._final_click[1] - touch.pos[1]) * step_size
    #
    #             for word in self._word_objects:
    #                 self._word_objects[word].center_x -= (self._final_click[0] - touch.pos[0]) * step_size
    #                 self._word_objects[word].center_y -= (self._final_click[1] - touch.pos[1]) * step_size
    #     self._final_click = touch.pos
    #
    # def on_touch_up(self, touch):
    #     self._final_click = None

    # def _check_pos(self,pos,ids,dt):
    #     for words in self._word_objects:
    #         if words != ids :
    #             if 2*planet_qscale>eucliddean_distance(pos,self._word_objects[words])>0:
    #                 pass
    #     pass

    def init_create(self, dt):
        # print(f'{self._locked_on_id}')
        self._text_display.text_btn_bg.color[3]=0
        self._text_display.text_btn.color[3]=0
        _chart = {}
        cur = self.connection.cursor()
        self.encodings[self._locked_on_id] = convert_array(
            list(cur.execute(f'''SELECT id, score FROM wordb WHERE id={self._locked_on_id}'''))[0][1])
        for words in self._word_objects.keys():
            _chart[words] = eucliddean_distance(self.encodings[words], self.encodings[self._locked_on_id])
        _chart = dict(sorted(_chart.items(), key=operator.itemgetter(1), reverse=False))
        list_id = list(_chart.keys())[0:3]
        _position = self._triple_circle(list_id, self._locked_on_id)
        _position = [_position[0] + random.choice([50, -5]), _position[1] + random.choice([50, -50])]
        # Clock.schedule_once(partial(self._check_pos,_position,self._locked_on_id),0)
        # print(f'{eucliddean_distance(_position,self._word_objects[self.chosen_id].center)}')
        if self._locked_on_id not in self._word_objects:
            self._word_objects[self._locked_on_id] = WordsPlanetOn(usr_dir=self.usr_dir, center=_position,
                                                                   size=self._planet_qsize)

            self.moving_layout.add_widget(self._word_objects[self._locked_on_id], index=0)
            self._word_objects[self._locked_on_id].bind(on_press=partial(self.press_planet, self._locked_on_id))

            Clock.schedule_once(partial(self._label_planet_puter, self._last_written, self._locked_on_id), 0)

        if abs(_position[0] - Window.width / 2) > Window.width / 2 or abs(
                _position[1] - Window.height / 2) > Window.height / 2:
            self._camera_bul_moving = True
            # delta_x=_position[0]-Window.width/2
            # delta_y=_position[1]-Window.height/2
            self.safineh_audio.stop()
            self.safineh_audio = SoundLoader.load(self.usr_dir+'movesafineh.ogg')
            self.safineh_audio.loop=True
            self.safineh_audio.volume=.7
            self.safineh_audio.play()
            self.safineh.moving = True
            self._safineh_moving = True
            Clock.schedule_interval(partial(self._move_camera, self._locked_on_id), 1 / 60)
        else:
            self._camera_bul_moving = False
            Clock.unschedule(self._start_move_safineh)
            Clock.unschedule(self.move_bait2)
            Clock.unschedule(self._move_bait1)
            Clock.schedule_once(partial(self.create_bait, self._locked_on_id), -1)
            Clock.schedule_interval(partial(self._move_bait1, self._locked_on_id), 1 / 60)
            Clock.schedule_interval(partial(self._start_move_safineh, self._locked_on_id), 1 / 120)
            self.safineh.moving = True
            self._safineh_moving = True
            self._last_planet = self._locked_on_id

    def create_bait(self, ids, dt):
        distance = eucliddean_distance((self.safineh.center_x, self.safineh.center_y - planet_scale * .7),
                                       self._word_objects[ids].center)

        self._bait_pos1 = [math.cos(math.radians(self.safineh.my_rotate.angle)) * distance * .6 + self.safineh.center[0],
                           math.sin(math.radians(self.safineh.my_rotate.angle)) * distance * .6 + self.safineh.center[1]- planet_scale * .7]

        try:

            x1, y1, x2, y2 = get_intersections(self.safineh.pos[0] + 1, self.safineh.pos[1], distance + 1,
                                               self._word_objects[ids].pos[0], self._word_objects[ids].pos[1] + 1,
                                               distance + 1)

        except TypeError:

            x1, y1, x2, y2 = Window.width / 2, Window.height / 2, Window.width / 2, Window.height / 2

        if eucliddean_distance(self._bait_pos1, [x1, y1]) > eucliddean_distance(
                self._bait_pos1, [x2, y2]):

            self._bait_pos2 = [x2, y2]
        else:
            self._bait_pos2 = [x1, y1]

    def _move_bait1(self, ids, dt):
        _dist = eucliddean_distance(self._bait_pos1, self._bait_pos2)

        step_x = (-self._bait_pos1[0] + self._bait_pos2[0] + 1) / (_dist + 1)
        step_y = (-self._bait_pos1[1] + self._bait_pos2[1] + 1) / (_dist + 1)

        self._bait_pos1[0] += int(step_x * 11)
        self._bait_pos1[1] += int(step_y * 11)

        if _dist < 10:
            Clock.schedule_interval(partial(self.move_bait2, ids), 1 / 60)
            return False
        pass

    def move_bait2(self, ids, dt):

        _dist = eucliddean_distance(self._bait_pos1, (
        self._word_objects[ids].center_x, self._word_objects[ids].center_y - planet_scale * .7))

        step_x = (-self._bait_pos1[0] + self._word_objects[ids].center_x + 1) / (_dist)

        step_y = (-self._bait_pos1[1] + self._word_objects[ids].center_y - planet_scale * .7 + 1) / (_dist)

        self._bait_pos1[0] += int(step_x * 12)
        self._bait_pos1[1] += int(step_y * 12)

        if _dist < 10:
            self._bait_pos1 = [int(self._word_objects[ids].center_x),
                               int(self._word_objects[ids].center_y + planet_scale * .7)]
            return False

    def _start_move_safineh(self, ids, dt):
        if self.reset_bul:
            return False
        if self._fuel < 0:
            return False
        # if not self._found_one:
        self._fuel -= 1 / 40
        step_x = (self._bait_pos1[0] - self.safineh.center[0] + 1) / (
                    eucliddean_distance(self._bait_pos1, self.safineh.center) + 1)

        step_y = (self._bait_pos1[1] - self.safineh.center[1] + 1) / (
                    eucliddean_distance(self._bait_pos1, self.safineh.center) + 1)

        try:
            anggle = (math.degrees(math.atan((self._bait_pos1[1] - self.safineh.pos[1] + 1) / (
                    self._bait_pos1[0] - self.safineh.pos[0] + 1))))
        except:
            anggle = 0
        if (self._bait_pos1[0] - self.safineh.pos[0]) < 0:
            anggle += 180

        self.safineh.my_rotate.angle = anggle
        self.safineh.my_rotate.origin = self.safineh.center

        # print(self._safineh_aflak.my_rotate.angle)

        self.safineh.center[0] += int(step_x * 8)
        self.safineh.center[1] += int(step_y * 8)

        if eucliddean_distance(self._bait_pos1, self.safineh.center) < 10:
            if self._found_one:
                self._fuel += 15
            self.safineh.center = (
            self._word_objects[ids].center[0], self._word_objects[ids].center[1] + .7 * planet_qscale)
            self.safineh.my_rotate2.origin = self.safineh.center
            self._safineh_moving = False
            self.safineh.moving = False
            self._found_one = False
            self.safineh_audio.stop()
            self.safineh_audio = SoundLoader.load(self.usr_dir+'spin.ogg')
            self.safineh_audio.loop=True
            self.safineh_audio.volume=.8
            self.safineh_audio.play()
            return False
        pass

    def _move_camera(self, ids, dt):
        # step_x = (self._word_objects[ids].center_x - Window.width / 2 + 1) / (
        #             eucliddean_distance(self._word_objects[ids].center, (Window.width / 2, Window.height / 2)) + 1)
        #
        # step_y = (self._word_objects[ids].center_y - Window.height / 2 + 1) / (
        #             eucliddean_distance(self._word_objects[ids].center, (Window.width / 2, Window.height / 2)) + 1)

        # self.safineh.my_rotate.origin = self.safineh.center
        # self.safineh.center_x -= int(step_x * 30)
        # self.safineh.center_y -= int(step_y * 30)
        # for words in self._word_objects.keys():
        #     self._word_objects[words].center_x -= int(step_x * 30)
        #     self._word_objects[words].center_y -= int(step_y * 30)
        # for words in self.planet_labels:
        #     self.planet_labels[words].center = self._word_objects[words].center
        # if eucliddean_distance((Window.width / 2, Window.height / 2), self._word_objects[ids].center) < 50:
        self._camera_bul_moving = False
        Clock.unschedule(self._start_move_safineh)
        Clock.unschedule(self.move_bait2)
        Clock.unschedule(self._move_bait1)

        Clock.schedule_once(partial(self.create_bait, ids), -1)
        Clock.schedule_interval(partial(self._move_bait1, ids), 1 / 60)
        Clock.schedule_interval(partial(self._start_move_safineh, ids), 1 / 60)
        self.safineh.moving = True
        self._safineh_moving = True
        self._last_planet = ids
        return False

    def _triple_circle(self, id_list, id_player_word):

        _info = {
            'very_close': 0,
            'close': 0,
            'kinda_close': 0,
            'kinda_far': 0,
            'far': 0,
            'very_far': 0}

        _radial_points = dict()
        for ids in id_list:
            if eucliddean_distance(self.encodings[ids], self.encodings[id_player_word]) < 12:
                _info['very_close'] += 1
            elif eucliddean_distance(self.encodings[ids], self.encodings[id_player_word]) < 15:
                _info['close'] += 1
            elif eucliddean_distance(self.encodings[ids], self.encodings[id_player_word]) < 18:
                _info['kinda_close'] += 1
            elif eucliddean_distance(self.encodings[ids], self.encodings[id_player_word]) < 22:
                _info['kinda_far'] += 1
            elif eucliddean_distance(self.encodings[ids], self.encodings[id_player_word]) < 25:
                _info['far'] += 1
            else:
                _info['very_far'] += 1

        # for id in id_list:
        #     print(self.data[id]['syn_search'])
        # print(_info)
        if _info['close'] + _info['kinda_close'] + _info['very_close'] == 0:
            _pos = self._very_far(id_list, id_player_word)
            return _pos
        elif _info['very_close'] > 1:
            _pos = self._very_close(id_list, id_player_word)
            return _pos
        elif _info['close'] + _info['kinda_close'] + _info['very_close'] == 3:
            return self._center_triple_point(id_list)
        else:
            _pos = self._center_triple_point(id_list)
            return _pos

    def _center_triple_point(self, id_list):
        x = 0
        y = 0
        for ids in id_list:
            x += self._word_objects[ids].center[0] / 3
            y += self._word_objects[ids].center[1] / 3
        return (x, y)

    def _very_close(self, id_list, id_word_player):
        _closest = None
        _dist = 100
        for ids in id_list:
            if eucliddean_distance(self.encodings[ids], self.encodings[id_word_player]) < _dist:
                _closest = ids
                _dist = eucliddean_distance(self.encodings[ids], self.encodings[id_word_player])
        _2nd_closest = None
        _dist = 100
        for ids in id_list:
            if ids != _closest:
                if eucliddean_distance(self.encodings[ids], self.encodings[id_word_player]) < _dist:
                    _2nd_closest = ids
                    _dist = eucliddean_distance(self.encodings[ids], self.encodings[id_word_player])

        points = _circle_points(self._word_objects[_closest].center, (_dist * Window.height) / 120, 40)
        _final_point = None
        min_dist = 100000

        for point in points:
            _temp_dist = 0
            _temp_dist = eucliddean_distance(numpy.asarray(self._word_objects[_2nd_closest].center),
                                             numpy.asarray(point))
            if _temp_dist < min_dist:
                min_dist = _temp_dist,
                _final_point = point
        return _final_point

    def _very_far(self, id_list, id_word_player):
        _closest = None
        _dist = 100
        for ids in self.anchors:
            if eucliddean_distance(self.encodings[ids], self.encodings[id_word_player]) < _dist:
                _closest = ids
                _dist = eucliddean_distance(self.encodings[ids], self.encodings[id_word_player])
        points = _circle_points(self._word_objects[_closest].center, (_dist * Window.height) / 60, 40)
        _furthest = None
        max_dist = 0

        for point in points:
            _temp_dist = 0
            for words in self._word_objects.keys():
                if words != _closest and words != id_word_player:
                    _temp_dist += eucliddean_distance(numpy.asarray(self._word_objects[words].center),
                                                      numpy.asarray(point))
            if _temp_dist > max_dist:
                max_dist = _temp_dist
                _furthest = point
        return _furthest

    def left_arrow_press(self, dt):
        self._just_pressed = True
        self._text_display.right_arrow.disabled = False
        # self._text_display._counter.str = ''
        # self._text_display._counter.text = ''
        self._text_display.right_arrow.color = [.28, .72, .54]
        # self._text_display.right_arrow.disabled = False
        self._locked_on_index += 1
        # Clock.schedule_interval(partial(self._counter_text_writer, f'{self._locked_on_index+1} از {len(self._search_results)}'), 1 / 120)

        # self._text_display._gloss_text.str = ''
        # self._text_display._gloss_text.text = ''
        Clock.schedule_once(partial(self.gloss_writer_new,
                                    self._text_matcher_menu(self._search_results[self._locked_on_index])), 0)

        if self._locked_on_index == len(self._search_results) - 1:
            self._text_display.left_arrow.disabled = True
            # self._text_display.right_arrow.disabled = False

            self._text_display.left_arrow.color = [.5, .5, .54]

    def right_arrow_press(self, dt):
        self._just_pressed = True
        self._text_display.left_arrow.disabled = False

        # self._text_display.left_arrow.disabled = False
        self._text_display.left_arrow.color = [.28, .72, .54]
        # self._text_display.left_arrow.disabled = False
        # self._text_display._counter.str = ''
        # self._text_display._counter.text = ''
        self._locked_on_index -= 1
        # Clock.schedule_interval(partial(self._counter_text_writer, f'{self._locked_on_index+1} از {len(self._search_results)}'), 1 / 120)

        # self._text_display._gloss_text.str = ''
        # self._text_display._gloss_text.text = ''

        Clock.schedule_once(partial(self.gloss_writer_new,
                                    self._text_matcher_menu(self._search_results[self._locked_on_index])), 0)

        if self._locked_on_index == 0:
            self._text_display.right_arrow.disabled = True
            # self._text_display.left_arrow.disabled = False
            self._text_display.right_arrow.color = [.5, .5, .5, 1]

    def text_matcher_widget(self,text):
        og_text = text
        gettext_raw = ''
        for char in og_text:
            gettext_raw += char
            if len(gettext_raw.split('\n')[-1]) > globals()['characters_limit'] * 1 and char == ' ':
                gettext_raw += '\n'
        return gettext_raw
        pass

    def _text_matcher_menu(self, ids):
        gettext_raw = ''
        og_text = self.data[ids]['gloss2']
        for char in og_text:
            gettext_raw += char
            if len(gettext_raw.split('\n')[-1]) > globals()['characters_limit'] * 1 and char == ' ':
                gettext_raw += '\n'
        return gettext_raw

    def finish_game(self, mode, dt):
        if mode == 'lose_f':
            save_game['xp']+=1
            save_game['lose'] += 1
            pickle.dump(save_game, open(current_dir + 'save', 'wb'))
            self.end_audio=SoundLoader.load(self.usr_dir+'Lose Massage .ogg')
            self.end_audio.play()
            self._win_message = StoryButton(usr_dir=self.usr_dir, size=(Window.width * .8, Window.height * .4),
                                            center=(Window.width * .5, Window.height * .7), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self._win_text = Label(center=self._win_message.center)
            self._win_text.font_name = self.usr_dir + 'Aflak Bold(1).ttf'
            self._win_text.font_size = int(globals()['font_scale'] * 1)
            self._win_text.halign = 'center'
            self._win_text.text = get_display(
                arabic_reshaper.reshape('متاسفانه سوخت سفینه تموم شد و باختی\n یک بار دیگه تلاش کن'))
            self.add_widget(self._win_message, index=0)
            self.add_widget(self._win_text, index=0)

            self.dobare_btn=StoryResetButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                            center=(Window.width * .35, Window.height * .4), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self.add_widget(self.dobare_btn, index=0)

            self.exit_btn = StoryExitButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                            center=(Window.width * .65, Window.height * .4), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self.add_widget(self.exit_btn, index=0)

            self.dobare_btn.bind(on_release=self.reset_init)
            self.exit_btn.bind(on_release=self.quit_to_main)

        elif mode == 'lose_t':
            self.end_audio=SoundLoader.load(self.usr_dir+'Lose Massage .ogg')
            self.end_audio.play()
            save_game['xp']+=1
            save_game['lose'] += 1
            self._win_message = StoryButton(usr_dir=self.usr_dir, size=(Window.width * .8, Window.height * .4),
                                            center=(Window.width * .5, Window.height * .7), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self._win_text = Label(center=self._win_message.center)
            self._win_text.font_name = self.usr_dir + 'Aflak Bold(1).ttf'
            self._win_text.font_size = int(globals()['font_scale'] * 1)
            self._win_text.halign = 'center'
            self._win_text.text = get_display(
                arabic_reshaper.reshape('متاسفانه زمانت تموم شد و باختی\n یک بار دیگه تلاش کن'))
            self.add_widget(self._win_message, index=0)
            self.add_widget(self._win_text, index=0)
            self.dobare_btn=StoryResetButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                            center=(Window.width * .35, Window.height * .4), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self.add_widget(self.dobare_btn, index=0)

            self.exit_btn = StoryExitButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                            center=(Window.width * .65, Window.height * .4), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self.add_widget(self.exit_btn, index=0)
            self.dobare_btn.bind(on_release=self.reset_init)
            self.exit_btn.bind(on_release=self.quit_to_main)
            pass
        elif mode == 'win':
            self.end_audio=SoundLoader.load(self.usr_dir+'Winning.ogg')
            self.end_audio.play()
            _score =5+ int((self._fuel/12 )* ((self.time_limit - int(time.perf_counter() - self._time))/60) )
            save_game['xp']+=_score
            save_game['win'] += 1
            pickle.dump(save_game, open(current_dir + 'save', 'wb'))

            self._win_message = StoryButton(usr_dir=self.usr_dir, size=(Window.width * .8, Window.height * .4),
                                            center=(Window.width * .5, Window.height * .7), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self._win_text = Label(center=self._win_message.center)
            self._win_text.font_name = self.usr_dir + 'Aflak Bold(1).ttf'
            self._win_text.font_size = int(globals()['font_scale'] * 1)
            self._win_text.halign = 'center'
            self._win_text.text = get_display(
                arabic_reshaper.reshape(
                    f'تبریک! تو برنده این مرحله شدی.\n مرحله های متنوع دیگه منتظرتن \n امتیاز تو   {_score}'))


            self._win_text.text = get_display(
                arabic_reshaper.reshape(
                    f' تبریک تو برنده این مرحله شدی! \n امتیاز تو  {_score}\n گزارش  {self.text_matcher_widget(self.answer_iterator)}'))


            self.add_widget(self._win_message, index=0)
            self.add_widget(self._win_text, index=0)
            self.dobare_btn=StoryResetButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                            center=(Window.width * .35, Window.height * .4), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self.add_widget(self.dobare_btn, index=0)

            self.exit_btn = StoryExitButton(usr_dir=self.usr_dir, size=(Window.width * .2, Window.height * .12),
                                            center=(Window.width * .65, Window.height * .4), allow_stretch=True,
                                            keep_ratio=False, color=[.23, .4, .85, .99])
            self.add_widget(self.exit_btn, index=0)
            self.dobare_btn.bind(on_release=self.reset_init)
            self.exit_btn.bind(on_release=self.quit_to_main)
            pass

    def reset_init(self, dt):
        self.reset_bul = True
        self.safineh.brake = True
        try:
            self.end_audio.stop()
        except:
            pass
            Clock.schedule_once(self.reset_game, 0)
        pass

    def reset_game(self, dt):
        self._word_objects = {}
        del (self.safineh)
        self.clear_widgets()
        self.__init__(usr_dir=self.usr_dir, midline=self.midline, conn=self.connection,
                      destination_id=self.destination_id, chosen_id=self.chosen_id,
                      anchors=self.anchors, encodings=self.encodings,
                      data=self.data, size=self.size, answer_text=self._chosen_text)

    def challenge_b_press_ingame(self, dt):
        # print(self.parent)
        self._last_written = self.answer
        self.answer = self._text_display._input_text.str
        self._text_display.left_arrow.color[3] = 0
        self._text_display.right_arrow.color[3] = 0
        if self.answer == 'ردر':
            self._text_display._input_text.str = ''
            self._text_display._input_text.text = ''
            pass
        elif self.answer == '':
            if len(self._search_results) > 1:
                self._text_display.left_arrow.disabled = True
                self._text_display.right_arrow.disabled = True

                pass
            else:
                pass
            pass
        else:
            self._text_display._input_text.str = ''
            self._text_display._input_text.text = ''

            self._search_results = word_search2(self.data, self.answer)

            if len(self._search_results) == 0:
                # self._text_display._tutorial.str = ''
                # self._text_display._tutorial.text = ''
                # self._text_display._message_text.str = ''
                # self._text_display._message_text.text = ''
                self._text_display._gloss_text.str = ''
                self._text_display._gloss_text.text = ''
                self._text_display._input_text.str = ''
                self._text_display._input_text.text = ''
                # self._text_display._icon.source =self.usr_dir +'envelope.png'
                # self._search_results = None
                self._locked_on_id = 0
                # self._text_display._counter.str = ''
                # self._text_display._counter.text = ''
                self._text_display.left_arrow.color[3] = 0
                self._text_display.right_arrow.color[3] = 0
                # self._text_display._tutorial.str = ''
                # self._text_display._tutorial.text = ''
                # self._text_display._message_text.str = ''
                # self._text_display._message_text.text = ''
                self._text_display._gloss_text.str = ''
                self._text_display._gloss_text.text = ''
                self._text_display._input_text.str = ''
                self._text_display._input_text.text = ''
                # Clock.schedule_interval(partial(self._text_writer, globals()['tuts'][3], 'text'), 1 / 120)
                # Clock.schedule_interval(partial(self._text_writer, globals()['texts_ingame'][1], 'tut'), 1 / 120)
            else:
                _shared = set()
                for ww in self._search_results:
                    if ww in list(self._word_objects.keys()):
                        if self._word_objects[ww].type != 'on':
                            _shared.add(ww)

                if len(_shared) > 0:
                    self._found_one = True
                    _shared = list(_shared)
                    if self.destination_id in _shared:
                        Clock.schedule_once(partial(self.finish_game, 'win'), .1)
                        self.main_event.cancel()
                        pass
                    else:
                        if len(_shared) == 1:
                            if self._word_objects[_shared[0]].type == 'q':
                                # self._fuel += 10
                                _pos = self._word_objects[_shared[0]].center
                                self.moving_layout.remove_widget(self._word_objects[_shared[0]])
                                self._word_objects[_shared[0]] = WordsPlanetOn(usr_dir=self.usr_dir,
                                                                               size=self._planet_size,
                                                                               center=_pos)
                                self._word_objects[_shared[0]].source = self.usr_dir + 'planet_found.zip'
                                self._word_objects[_shared[0]].anim_delay = 1 / 4
                                self._word_objects[_shared[0]].bind(on_press=partial(self.press_planet, _shared[0]))
                                self.moving_layout.add_widget(self._word_objects[_shared[0]], index=0)

                                Clock.schedule_once(partial(self._label_planet_puter, self.answer, _shared[0]), 0)
                            Clock.schedule_interval(partial(self._move_camera, _shared[0]), 1 / 60)

                            pass
                        elif len(_shared) > 1:
                            for w_w in _shared:
                                if w_w not in self._word_objects:
                                    # self._fuel += 10
                                    self.time_limit += 10

                                    _pos = self._word_objects[w_w].center
                                    self.moving_layout.remove_widget(self._word_objects[w_w])
                                    self._word_objects[w_w] = WordsPlanetOn(usr_dir=self.usr_dir,
                                                                            size=self._planet_size,
                                                                            center=_pos)
                                    self._word_objects[w_w].source = self.usr_dir + 'planet_found.zip'
                                    self._word_objects[w_w].bind(on_press=partial(self.press_planet, w_w))

                                    self._word_objects[w_w].anim_delay = 1 / 4
                                    self.moving_layout.add_widget(self._word_objects[w_w], index=0)

                                    Clock.schedule_once(partial(self._label_planet_puter, self.answer, w_w), 0)
                            Clock.schedule_interval(partial(self._move_camera, _shared[-1]), 1 / 60)
                            pass
                        pass
                else:

                    if len(self._search_results) == 1:
                        self._last_written = self.answer
                        self._text_display._gloss_text.str = ''
                        self._text_display._gloss_text.text = ''
                        self._text_display._input_text.str = ''
                        self._text_display._input_text.text = ''
                        # self._text_display._counter.str = ''
                        # self._text_display._counter.text = ''
                        self._text_display.left_arrow.color[3] = 0
                        self._text_display.right_arrow.color[3] = 0
                        self._locked_on_index = 0
                        self._locked_on_id = self._search_results[0]
                        Clock.schedule_once(self.init_create, 0)
                        # Clock.schedule_once(partial(self.initialize_challenge,self._search_results[0]),0)

                    elif len(self._search_results) > 1:
                        self._last_written = self.answer
                        self._text_display.text_btn.disabled=False
                        self._text_display.text_btn_bg.color[3]=.8
                        self._text_display.text_btn.color[3]=.8
                        self._text_display.right_arrow.disabled = True
                        # self._text_display._counter.str = ''
                        # self._text_display._counter.text = ''
                        # Clock.schedule_interval(partial(self._counter_text_writer, f'{1} از {len(self._search_results)}'),1/120)
                        self._text_display.left_arrow.color = [.5, .5, .5]
                        self._text_display.right_arrow.color = [.5, .5, .5]
                        # self._text_display._icon.source = self.usr_dir +'safineh.jpg'
                        # self._text_display._icon._do_press()
                        self._locked_on_index = 0
                        self._locked_on_id = self._search_results[0]
                        # self._keyboard['space'].bind(on_press=self.space_switch)
                        self._text_display.left_arrow.disabled = False
                        self._text_display.left_arrow.color = [.28, .72, .54]
                        self._text_display.left_arrow.color[3] = 1
                        self._text_display.right_arrow.color[3] = 1

                        # self._text_display.left_arrow.bind(on_press=self.left_arrow_press)
                        # self._text_display.right_arrow.bind(on_press=self.right_arrow_press)

                        # self._text_display._tutorial.str = ''
                        # self._text_display._tutorial.text = ''
                        # self._text_display._message_text.str = ''
                        # self._text_display._message_text.text = ''
                        self._text_display.add_widget(self._text_display.text_btn)
                        self._text_display.add_widget(self._text_display.text_btn_bg, index=1)
                        self._text_display._input_text.str = ''
                        self._text_display._input_text.text = ''
                        # Clock.schedule_interval(partial(self._text_writer, globals()['texts'][2], 'text'), 1 / 120)
                        # Clock.schedule_interval(partial(self._text_writer, globals()['tuts'][2], 'tut'), 1 / 120)
                        self._text_display._input_text.focus = False
                        self._text_display._gloss_text.str = ''
                        self._text_display._gloss_text.text = ''
                        self._text_display.text_btn.text=get_display(arabic_reshaper.reshape(self.parent._text_matcher_menu(self._search_results[0])))


class ChallengeMenu2(Widget):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.text = ''

        self._input_text = ArText3(center=(Window.width * 0.5, Window.height * .27), halign='right',
                                   font_name=usr_dir + 'Aflak Bold(1).ttf', base_direction='ltr',
                                   font_size=int(globals()['font_scale'] * 1.6), background_color=[.0, .0, .0,.0]
                                   )
        self._input_text.center = (Window.width * 0.5, Window.height * .27)
        # self._input_text.base_direction = 'rtl'
        # self._message_text = ArText2(halign='right', font_name=usr_dir + 'Aflak Bold(1).ttf', base_direction='ltr',
        #                              font_size=int(globals()['font_scale'] * .7), color=[.28, .72, .54]
        #                              # ,background_color=[0,0,0,0]
        #                              )
        # self._message_text.center = (Window.width * 0.5, Window.height * .89)

        self._gloss_text = ArText2(halign='right',
                                   font_name=usr_dir + 'Aflak Bold(1).ttf', base_direction='ltr',
                                   font_size=int(globals()['font_scale'] * .9), color=[.28, .72, .54]
                                   # ,background_color=[0,0,0,0]
                                   )
        self._gloss_text.center = (Window.width * 0.5, Window.height * .85)

        # self._tutorial = ArTextTut(center=(Window.width * 0.5, Window.height * .4), halign='right',
        #                            font_name=usr_dir + 'Aflak Bold(1).ttf', base_direction='weak_rtl',
        #                            font_size=int(globals()['font_scale'] * .8), background_color=[.0, .0, .0,.0]
        #                            )
        #
        # self._tutorial.center = (Window.width * 0.5, Window.height * .31)
        # self._tutorial.base_direction = 'weak_rtl'
        #
        # self._counter = ArText2(halign='center',
        #                         font_name=usr_dir + 'Aflak Bold(1).ttf', base_direction='rtl',
        #                         font_size=int(globals()['font_scale'] * .8), color=[.28, .72, .54])
        # self._counter.center = (Window.width * 0.5, Window.height * .65)

        # self._icon = Icon(usr_dir=self.usr_dir,size=(planet_scale*1.5,1.5*planet_scale),source=self.usr_dir+'envelope.png')
        # self._icon.center = (Window.width * 0.5, Window.height * .75)

        self.left_arrow = ArrowSearch(usr_dir=self.usr_dir, orientation='left',
                                      )
        self.left_arrow.center = (Window.width * 0.1, Window.height * .47)

        self.right_arrow = ArrowSearch(usr_dir=self.usr_dir, orientation='right',
                                       )
        self.right_arrow.center = (Window.width * 0.9, Window.height * .47)

        self._input_text.foreground_color = [1, 1, 1, 1]
        # self._layout.add_widget(self._monitor)
        self.text_btn=TextBtnChallenge(self.usr_dir,'',center_y=Window.height*.45,size=(Window.width*.65,Window.height*.12))
        self.text_btn_bg=Image(center_x=Window.width*.5,center_y=Window.height*.45,
                               size=(Window.width*.66,Window.height*.12),color=[.28, .72, .59,0])
        self.text_btn_bg.center_x= self.center_x
        self.text_btn.disabled=True
        # self.add_widget(self.text_btn)
        # self.add_widget(self.text_btn_bg,index=1)
        self.add_widget(self.right_arrow)
        self.add_widget(self.left_arrow)
        # self.add_widget(self._message_text)

        # self.add_widget(self._counter)

        self.add_widget(self._input_text)
        # self.add_widget(self._message_text)
        # self.add_widget(self._tutorial)
        # self.add_widget(self._icon)
        self.add_widget(self._gloss_text)


class Tutorial(Widget):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.mode = 1
        self.tut_message = Image(source=self.usr_dir + f'tut{self.mode}.png', size=Window.size, center=Window.center,
                                 allow_stretch=True, keep_ratio=False)
        self.add_widget(self.tut_message)
        self.tut_btn = Tutbtn(usr_dir=self.usr_dir, center=(Window.width / 2, Window.height / 6),
                              size=(planet_qscale * 2, planet_qscale))
        self.tut_btn.center = (Window.width / 2, Window.height / 6)
        self.add_widget(self.tut_btn)
        self.tut_btn.bind(on_release=self.press_btn)

    def press_btn(self, dt):
        if self.mode < 6:
            self.mode += 1
            self.tut_message.source = self.usr_dir + f'tut{self.mode}.png'
        else:
            self.mode = 1
            self.tut_message.source = self.usr_dir + f'tut{self.mode}.png'
            self.parent.remove_widget(self)


class MainMenu(Widget):

    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.center=(Window.width*.5,Window.height*.5)
        self._toggle_state = 1
        # self._layout = FloatLayout(size=self.size, pos=(0, .2 * Window.height))
        # self.add_widget(sel61f._layout)
        self._toggle_button = FlipButton(usr_dir=usr_dir, size=(planet_qscale*.3, planet_qscale*.8), center=(self.center_x*1.41,self.center_y*.72)
                                         , keep_ratio=False, allow_stretch=True)
        self.panel_bg = Image(size=(Window.width*.75, Window.height*.25), source=usr_dir + 'frame3.png'
                              , keep_ratio=False, allow_stretch=True
                              , center=(self.center_x,self.center_y*.8), color=(1, 1, 1, 1))

        self._text_label = ArText2( font_name=usr_dir + 'Aflak Bold(1).ttf'
                                   , center=(self.center_x,self.center_y*.92),
                                   font_size=int(globals()['font_scale'] * 1.5), color=[.28, .72, .54])
        self._text_label.text = get_display(arabic_reshaper.reshape('حالت معمولی'))
        self._text_label.str = get_display(arabic_reshaper.reshape('حالت معمولی'))
        self.red_bottun = RedButton(usr_dir=usr_dir, size=(planet_qscale*.65, planet_qscale*.5), center=(self.center_x*.711,self.center_y*.715)
                                     , always_release=True)

        self._toggle_button.bind(on_press=self.toggle_press)
        # self.red_bottun.bind(on_press=self.red_press)
        self.add_widget(self.panel_bg)
        self.add_widget(self._text_label)
        self.add_widget(self._toggle_button)
        self._start_sp = False
        self.audio=SoundLoader.load(self.usr_dir+'Joy Stick .ogg')
        self.settings=SettingsBtn(usr_dir=self.usr_dir, center=(self.center_x*.45,Window.height*.5*.97))
        self.add_widget(self.red_bottun)

        self.profile_icon=ProfileIcon(usr_dir=self.usr_dir, center=(self.center_x*1.25,Window.height*.5*.575))
        self.profile_icon.size=(planet_scale,planet_scale*.2)
        self.profile_icon.color[3]=.0
        self.profile_icon.color[1]=.70
        self.add_widget(self.settings,index=7)

        self.profile_btn=ProfileIcon(usr_dir=self.usr_dir, center=(self.center_x*1.25,Window.height*.5*.575))
        self.add_widget(self.profile_btn,index=10)
        self.add_widget(self.profile_icon,index=0)

        for child in self.children:
            child.center_y-=.08*Window.height

    def toggle_press(self, dt):
        self.audio.play()
        if self._toggle_button.state == 'down':
            self._toggle_button.source = self.usr_dir + 'toggledown(1).png'
            self._toggle_state = 2
            self._text_label.source = self.usr_dir + 'mp1.png'

            self._text_label.text = get_display(arabic_reshaper.reshape('حالت دشوار'))
            self._text_label.str = get_display(arabic_reshaper.reshape('حالت دشوار'))
        else:
            self._text_label.text = get_display(arabic_reshaper.reshape('حالت معمولی'))
            self._text_label.str = get_display(arabic_reshaper.reshape('حالت معمولی'))

            self._toggle_button.source = self.usr_dir + 'toggleup(1).png'
            self._text_label.source = self.usr_dir + 'sp1.png'
            self._toggle_state = 1


class ProfileIcon(ButtonBehavior,Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.source = usr_dir + 'profile.png'
        self.allow_stretch=True
        self.keep_ratio=False
        self.size=(planet_scale,planet_scale)


class QuitButton(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.source = usr_dir + 'exit.png'
        self.center = (Window.width * .94, Window.height * .98)
        self.allow_stretch = True
        self.keep_ratio = False
        self.size = (planet_qscale / 2, planet_qscale / 2)

    def on_press(self):
        self.center = (Window.width * .94, Window.height * .98)
        self.size[0] += 10
        self.size[1] += 10

    def on_release(self):
        self.center = (Window.width * .94, Window.height * .98)
        self.size[0] -= 10
        self.size[1] -= 10


class BackButtonInGame(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.source = usr_dir + 'DSC_0621.png'
        self.center = (Window.width * .06, Window.height * .98)
        self.allow_stretch = True
        self.keep_ratio = False
        self.size = (planet_qscale / 2, planet_qscale / 2)
        self.color = [.5, .5, .5, .7]

    def on_press(self):
        self.center = (Window.width * .06, Window.height * .98)
        self.size[0] += 10
        self.size[1] += 10

    def on_release(self):
        self.center = (Window.width * .06, Window.height * .98)
        self.size[0] -= 10
        self.size[1] -= 10


class ArText2(Label):
    max_chars = NumericProperty(200)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(ArText2, self).__init__(**kwargs)
        self.text = ''
        self.base_direction = 'rtl'
        self.halign = 'right'

    def on_touch_down(self, touch):

        pass

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str + substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        substring = ""

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str) - 1]

        self.text = get_display(arabic_reshaper.reshape(self.str))


class ArText3(TextInput):
    max_chars = NumericProperty(200)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(ArText3, self).__init__(**kwargs)
        self.text = ''
        self.size=[Window.width*.95,Window.height*.07]
        self.base_direction = 'rtl'
        self.halign = 'right'
        self.padding=[planet_qscale/2,6]
        # self.border = (8,8,8,8)
        # self.
        self.background_color=[.0, .0, .0,.0]
        self.foreground_color = [.28, .72, .54]
        self.use_bubble =False
        self.use_handles = False
        self.selection_color =[0,0,0,0]

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str + substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        substring = ""
        super(ArText3, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str) - 1]
        self.text = get_display(arabic_reshaper.reshape(self.str))

    def _on_focus(self, instance, value, *largs):
        if value:
            self.focus=False
            self.keyboard=False


class ArTextTut(TextInput):
    max_chars = NumericProperty(200)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(ArTextTut, self).__init__(**kwargs)
        self.text = ''
        self.padding=[int(planet_qscale)/4,6]
        self.size=[Window.width*.9,Window.height*.07]
        self.base_direction = 'rtl'
        self.halign = 'right'
        # self.border = (8,8,8,8)
        # self.
        self.foreground_color = [.28, .72, .54]
        self.use_bubble =False
        self.use_handles = False
        self.selection_color =[0,0,0,0]

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str + substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        substring = ""
        super(ArTextTut, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str) - 1]
        self.text = get_display(arabic_reshaper.reshape(self.str))

    def _on_focus(self, instance, value, *largs):
        if value:
            self.focus=False
            self.keyboard=False


class Ar_text(TextInput):
    max_chars = NumericProperty(200)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(Ar_text, self).__init__(**kwargs)
        self.text = ''
        self.cursor_color = [.51, 1, 1, 1]
        self.text_validate_unfocus = False
        self.cursor_width = 2
        self.keyboard_mode = 'managed'

        self.size = [Window.width * .75, Window.height * .2]
        self.base_direction = 'rtl'
        self.halign = 'right'

    def on_touch_down(self, touch):
        pass

    def on_double_tap(self):
        pass

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str + substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        self.focus = True
        self.do_cursor_movement(action='cursor_end', control=True, alt=True)

        substring = ""
        # super(Ar_text, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str) - 1]
        self.text = get_display(arabic_reshaper.reshape(self.str))


class WordsPlanetQuestion(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        file = 'planet_off.zip'
        self.type = 'q'

        self.source = usr_dir + f'{file}'
        # if file == 'orange.zip' :
        # self.color=[random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255]
        self.color = [.6, .6, .6]
        self.anim_delay = random.choice([1 / 10, 1 / 6, 1 / 4, 1 / 3])
        self.info_ratio = 0

        # with self.canvas.before:
        #     PushMatrix()
        #     self.my_rotate=Rotate()
        #     self.my_rotate.angle = random.randint(0,30)
        #     self.my_rotate.origin = self.center
        #     self.my_rotate.axis = (0, 0, 1)
        # with self.canvas.after:
        #     PopMatrix()


class WordsPlanetOff(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.source = usr_dir + 'blackhole.zip'
        self.info_ratio = 0
        self.type = 'off'
        self.audio = SoundLoader.load(usr_dir+'holdplanet.ogg')
        self.audio.volume=.9

    def on_press(self):
        self.audio.play()

    def on_release(self):
        self.audio.stop()

class WordsPlanetOn(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.source = usr_dir + 'planet_create_full.zip'
        self.anim_delay = 1 / 30
        # self.label=Label(center=self.center,font_name=usr_dir+'Aflak Bold(1).ttf',text=get_display(arabic_reshaper.reshape('سلام')))
        # self.add_widget(self.label,index=0)
        self.info_ratio = 1
        self.anim_loop = 1
        self.type = 'on'
        Clock.schedule_once(partial(self.change_source, usr_dir), 2)

    def on_press(self):
        print('xxxxxx')

    def change_source(self, usr_dir, dt):
        self.source = usr_dir + 'planet_on.zip'
        self.anim_delay = 1 / 10
        self.anim_loop = 0


class QuitPlanet(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.source = usr_dir + 'DSC_0621.png'

    def on_press(self):
        print('xxxxxx')


class SafineAflak(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        # self.angle=0
        self.step = -.5
        self.moving = False
        self.brake = False
        self.source = usr_dir + 'harkat.zip'
        self.size = (int(Window.width / 10), int(Window.width / 10))
        with self.canvas.before:
            PushMatrix()
            self.my_rotate2 = Rotate()
            self.my_rotate2.angle = 0
            self.my_rotate2.origin = self.center
            self.my_rotate2.axis = (0, 0, 1)
        with self.canvas.after:
            PopMatrix()


class RadarBtn(ButtonBehavior,Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'rdr1.png'
        self.anim_delay=1/10
        self.size= (planet_scale*1.1,planet_scale*1.1)
        self.center=(Window.width*.85,Window.height*.93)
        self.allow_stretch=True
        self.keep_ratio=False
        with self.canvas.before:
            PushMatrix()
            self.my_rotate = Rotate()
            self.my_rotate.angle = 45
            self.my_rotate.origin = self.center
            self.my_rotate.axis = (0, 0, 1)
        with self.canvas.after:
            PopMatrix()

    def on_press(self):
        self.source = self.usr_dir + 'rdr1.png'
        self.source = self.usr_dir + 'rdr.zip'
        self.anim_loop=1


class FlipButton(ToggleButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'toggleup(1).png'

    def on_state(self, widget, value):
        pass


class RedButton(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.allow_stretch=True
        self.keep_ratio=False
        self.source = self.usr_dir + 'buttom_off_firstpage.png'
        # self.always_release=True
        self.audio=SoundLoader.load(self.usr_dir+'Joy Stick .ogg')

    def on_press(self):
        self.audio.play()

        self.source = self.usr_dir + 'buttom_on_firstpage.png'
        # print ('pressed')

    def on_release(self):
        self.source = self.usr_dir + 'buttom_off_firstpage.png'


class BackButton(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        self.usr_dir = usr_dir
        super().__init__(**kwargs)
        self.source = self.usr_dir + 'DSC_0621.png'

    def on_press(self):
        pass


class Tuticon(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.size = (planet_qscale, planet_qscale)
        self.source = self.usr_dir + 'tuticon.png'
        self.center = (Window.width / 2, Window.height / 10)
        self.color = [.5, .5, .5]


class LoadingInit(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'loading_fire.zip'
        self.center = (Window.width / 2, Window.height / 4)


class Tutbtn(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'btntut.png'
        self.keep_ratio = False
        self.allow_stretch = True

    def on_press(self):
        self.color = [.5, .5, .5, 1]

    def on_release(self):
        self.color = [1, 1, 1, 1]


class TextBtn(ButtonBehavior,Label):
    def __init__(self, usr_dir, string, **kwargs):
        super().__init__(**kwargs)
        self.text = get_display(arabic_reshaper.reshape(string))
        self.font_name= usr_dir+'Aflak Bold(1).ttf'
        self.font_size = globals()['font_scale']*1.1
        self.width = Window.width*.1
        self.base_direction='rtl'
        self.halign='center'
        self.valign='center'
        # self.height = Window.height*.08
        self.color=[.28, .72, .59, 1]
        # self.center_x=Window.width/2
        # self.texture_update()
        # with self.canvas.before:
        #     Color(rgba=[0, 0, 0.71])
        #     RoundedRectangle(size=self.size, center=self.center)
        # self.texture_update()

    def on_press(self):
        self.color = [.28, .72, .59, 1]
        # with self.canvas.before:
        #     Color(rgba=[.0, .0, .0,1])
        #     RoundedRectangle(size=self.size, pos=self.pos)

    def on_release(self):
        self.color = [.0, .0, .0,1]
        # with self.canvas.before:
        #     Color(rgba=[.28, .72, .59,1])
        #     RoundedRectangle(size=self.size, pos=self.pos)


class TextBtnChallenge(ButtonBehavior,Label):
    def __init__(self, usr_dir, string, **kwargs):
        super().__init__(**kwargs)
        self.text = get_display(arabic_reshaper.reshape(string))
        self.font_name= usr_dir+'Aflak Bold(1).ttf'
        self.font_size = globals()['font_scale']*1
        # self.width = Window.width*.37
        self.base_direction='rtl'
        self.halign='center'
        self.valign='center'
        # self.height = Window.height*.08
        self.color=[.0,.0,.0,.8]
        self.center_x=Window.width/2
        # self.texture_update()
        # with self.canvas.before:
        #     Color(rgba=[.28, .72, .59,1])
        #     RoundedRectangle(size=self.size, pos=self.pos)
        # self.texture_update()

    def on_press(self):
        self.color = [.28, .72, .59, 1]
        self.parent.text_btn_bg.color[3]=0
        # with self.canvas.before:
        #     Color(rgba=[.0, .0, .0,1])
        #     RoundedRectangle(size=self.size, pos=self.pos)

    def on_release(self):
        self.color = [.0, .0, .0,.8]
        # self.parent.text_btn_bg.color[3]=.8

        # with self.canvas.before:
        #     Color(rgba=[.28, .72, .59,1])
        #     RoundedRectangle(size=self.size, pos=self.pos)



class GameModeSelection(Widget):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.size=Window.size
        self.center=Window.center
        self.story=TextBtn(center=(Window.width/2,Window.height*.85),usr_dir=self.usr_dir,string='حالت داستانی')
        # self.story.center=(Window.center[0],Window.center[1]*.35)
        self.daily_challenge=TextBtn(center=(Window.width/2,Window.height*.7),usr_dir=self.usr_dir,string='چالش روزانه')
        # self.daily_challenge.center=(Window.center[0],Window.center[1]*1)

        self.random_challenge=TextBtn(center=(Window.width/2,Window.height*.55),usr_dir=self.usr_dir,string='چالش تصادفی')
        # self.random_challenge.center=(Window.center[0],Window.center[1]*.65)



        self.add_widget(self.story,index=60)
        self.add_widget(self.daily_challenge,index=60)
        self.add_widget(self.random_challenge,index=60)
        # self.daily_mode.bind(on_press=)


class Icon(ButtonBehavior, Image):

    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        # self.source=self.usr_dir+'buttonoff2.png'

    def on_press(self):
        # print('xxxxxxxxxxxx')
        self.size[0] += 30
        self.size[1] += 30
        self.center = (Window.width * 0.5, Window.height * .75)

    def on_release(self):
        self.size[0] -= 30
        self.size[1] -= 30
        self.center = (Window.width * 0.5, Window.height * .75)


class MenuBG(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'loop_frames.zip'


class ArrowSearch(ButtonBehavior, Image):
    def __init__(self, usr_dir, orientation, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.size = (int(Window.width / 12), int(Window.width / 12))
        self.source = self.usr_dir + f'arrow_{orientation}.png'
        self.color = [.5, .5, .5, 1]
        self.audio = SoundLoader.load(self.usr_dir + 'arrow.ogg')
        self.audio.volume = .3

    def on_press(self):
        # self.color = [.5, .5, .5, 1]
        self.audio.play()

        pass

    def on_release(self):
        # self.color = [.28, .72, .54]
        pass


class KeyboardBtn(ButtonBehavior, Image):
    def __init__(self, usr_dir, alphabet, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.alphabet = alphabet
        self.source = self.usr_dir + f'{self.alphabet}.png'
        self.allow_stretch=True
        self.keep_ratio=False
        self.audio = SoundLoader.load(self.usr_dir + 'Keyboard1.ogg')

    def on_press(self):
        self.audio.pitch = 1
        self.audio.play()
        self.source = self.usr_dir + f'{self.alphabet}2.png'

    def on_release(self):

        self.source = self.usr_dir + f'{self.alphabet}.png'

        try:
            self.parent._text_display._input_text.insert_text(globals()['characters'][self.alphabet])
        except AttributeError:
            pass
        # self.parent._search_panel_ingame._input_text.text += self.alphabet


class KeyboardSpc(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.alphabet = 'space'
        self.source = self.usr_dir + f'{self.alphabet}.png'
        self.allow_stretch=True
        self.keep_ratio=False
        self.audio = SoundLoader.load(self.usr_dir + 'Keyboard1.ogg')

    def on_press(self):
        self.audio.play()

        self.source = self.usr_dir + f'{self.alphabet}2.png'

    def on_release(self):
        self.source = self.usr_dir + f'{self.alphabet}.png'
        if self.parent._text_display._input_text.text != '':
            # self.unbind(on_press=self.parent.space_switch)
            self.parent._text_display._input_text.insert_text(' ')
        # self.parent._search_panel_ingame._input_text.text += self.alphabet


class KeyboardBspc(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.alphabet = 'bspace'
        self.source = self.usr_dir + f'{self.alphabet}.png'
        self.allow_stretch=True
        self.keep_ratio=False
        self.audio = SoundLoader.load(self.usr_dir + 'Keyboard1.ogg')

    def on_press(self):

        self.audio.play()
        self.source = self.usr_dir + f'{self.alphabet}2.png'

    def on_release(self):
        self.source = self.usr_dir + f'{self.alphabet}.png'
        self.parent._text_display._input_text.do_backspace()
        # self.parent._search_panel_ingame._input_text.text += self.alphabet


class KeyboardEnter(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.alphabet = 'daste'
        self.source = self.usr_dir + f'{self.alphabet}1.png'
        # self.anim_loop=0
        self.anim_delay = 1 / 10
        self.allow_stretch=True
        self.keep_ratio=False
        self.audio = SoundLoader.load(self.usr_dir + 'Joy Stick .ogg')

    def on_press(self):
        self.audio.play()
        self.source = self.usr_dir + f'{self.alphabet}1.png'
        self.source = self.usr_dir + f'{self.alphabet}.zip'
        self.anim_loop = 1

    def on_release(self):
        pass


class KeyboardBtnHold(ButtonBehavior, Image):
    def __init__(self, usr_dir, alphabet, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.alphabet = alphabet
        self.source = self.usr_dir + f'{self.alphabet}.png'
        self.start = None
        self.end = None
        self.elapsed = None
        self.allow_stretch=True
        self.keep_ratio=False
        self.audio = SoundLoader.load(self.usr_dir + 'Keyboard1.ogg')

    def on_press(self):
        self.audio.play()
        self.source = self.usr_dir + f'{self.alphabet}2.png'
        self.start = time.time()

    def on_release(self):
        self.end = time.time()
        self.elapsed = (self.end - self.start)
        self.source = self.usr_dir + f'{self.alphabet}.png'
        if self.elapsed < .6:
            try:
                self.parent._text_display._input_text.insert_text(globals()['characters_hold'][self.alphabet])
            except AttributeError:
                pass
        else:
            try:
                self.parent._text_display._input_text.insert_text('آ')
            except AttributeError:
                pass

def eucliddean_distance(u, v):
    # print(f' u: {len(u)}')
    # print(f' v: {len(v)}')

    return np.linalg.norm(np.asarray(u) - np.asarray(v))

def word_search_db(word, conn):
    curor = conn.cursor()
    results = list(curor.execute(f'''SELECT id, syn_search, gloss, pos FROM wordb WHERE words LIKE '%{word}%' '''))
    curor.close()
    return results


def clean_search_db(results, word):
    _fin = set()
    for res in results:
        if word in res[1].split(','):
            _fin.add(res[0])
    return list(_fin)


class SettingsBtn(ButtonBehavior,Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'settings.png'
        self.keep_ratio=False
        self.allow_stretch=True
        self.size=(planet_scale*.7,planet_scale*.7)
        with self.canvas.before:
            PushMatrix()
            self.my_rotate = Rotate()
            self.my_rotate.angle = 0
            self.my_rotate.origin = self.center
            self.my_rotate.axis = (0, 0, 1)

        with self.canvas.after:
            PopMatrix()


class Loading(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'loading_up.zip'
        # self.color[3]=.65


def word_search2(data, word):
    candids = []
    for id in data.keys():
        if word in data[id]['syn_search'].split(','):
            candids.append(id)
    return candids


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


class StoryResetButton(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'again.png'

    def on_press(self):
        # self.color=[.9,.9,.9,1]
        pass


class ProfileMenu(Widget):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.center=(Window.width/2,Window.height/2)
        self.return_tomain=TextBtn(center_y=Window.height*.2,center_x=Window.width*.5,usr_dir=self.usr_dir,string='بازگشت')
        self.add_widget(self.return_tomain)
        self.return_tomain.bind(on_press=self.return_press)

        self.runs=TextBtn(center_y=Window.height*.25,center_x=Window.width*.5,usr_dir=self.usr_dir,string=f'تعداد ورود {save_game["nth_time"]}')
        self.add_widget(self.runs)
        self.xp=TextBtn(center_y=Window.height*.3,center_x=Window.width*.5,usr_dir=self.usr_dir,string=f'میزان تجربه  {save_game["xp"]}')
        self.add_widget(self.xp)

        self.win=TextBtn(center_y=Window.height*.35,center_x=Window.width*.5,usr_dir=self.usr_dir,string=f'تعداد برد  {save_game["win"]}')
        self.add_widget(self.win)

        self.lose=TextBtn(center_y=Window.height*.4,center_x=Window.width*.5,usr_dir=self.usr_dir,string=f'تعداد باخت  {save_game["lose"]}')
        self.add_widget(self.lose)

    def return_press(self,dt):
        Clock.schedule_once(self.parent.bring_menu_back)
        self.parent.remove_widget(self.parent.profile_window)


class SettingMenu(Widget):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.center=(Window.width/2,Window.height/2)
        self.return_tomain=TextBtn(center=self.center,usr_dir=self.usr_dir,size=(planet_qscale,planet_qscale),string='بازگشت')
        self.add_widget(self.return_tomain)
        self.return_tomain.bind(on_press=self.return_press)

    def return_press(self,dt):
        Clock.schedule_once(self.parent.bring_menu_back)
        self.parent.remove_widget(self.parent.settings_window)


class StoryExitButton(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'exit_end.png'

    def on_press(self):
        # self.color=[.9,.9,.9,1]
        pass

class StoryButton(ButtonBehavior, Image):
    def __init__(self, usr_dir, **kwargs):
        super().__init__(**kwargs)
        self.usr_dir = usr_dir
        self.source = self.usr_dir + 'background2.png'

    def on_press(self):
        # self.color=[.9,.9,.9,1]
        pass


def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d
        return x3, y3, x4, y4


def _circle_points(center, r, n):
    return [
        (
            center[0] + int(math.cos(2 * pi / n * x) * r),  # x
            center[1] + int(math.sin(2 * pi / n * x) * r)  # y

        ) for x in range(0, n)]



if __name__ == "__main__":
    app = Aflak()

    app.run()
