from Tkinter import Tk, StringVar, BooleanVar, IntVar, Text, Radiobutton, OptionMenu
from ttk import Button, Frame, Label, Entry
import tkSimpleDialog
import tkMessageBox

import FantasyFootballHelper
import utils
import Opponent


class StartUpUI(Frame):
    """
    UI object for new draft window
    """
    
    def __init__(self, parent, draftgame):
        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()        
        self.__initUI()
        
    def __initUI(self):
        self.__draw_new_draft_window(self.parent)
        
    def __draw_new_draft_window(self, parent):

        self.parent.title("New Draft")

        style = StringVar()
        style.set("Snake")

        opponent_label = Label(parent, text="Opponents")
        opponent_entry = Entry(parent, width=5)
        
        position_label = Label(parent, text="Draft Position")
        position_entry = Entry(parent, width=5)
        
        rounds_label = Label(parent, text="Number of Rounds")
        rounds_entry = Entry(parent, width=5)
        
        style_label = Label(parent, text="Draft Style")
        style_menu = OptionMenu(parent, style, "Snake", "Linear")
        
        def begin_draft():
            """
            initializes variables to control the flow of the draft
            calls the first window of the draft.
            """
            self.game.number_of_opponents = int(opponent_entry.get())
            self.game.draft_position = int(position_entry.get())
            self.game.number_of_rounds = int(rounds_entry.get())
            self.game.draft_style = style.get()
            
            self.game.opponents = []
            self.game.current_position = 1
            self.game.current_round = 1
            
            for x in xrange(self.game.number_of_opponents):
                self.game.opponents.append(Opponent.Opponent(x))

            if self.game.draft_position <= self.game.number_of_opponents + 1:
                MainUI(self.parent, self.game)
            else:
                tkMessageBox.showinfo("Error",
                                      "Draft position too high!\nYou would never get to pick a player"
                                      )

        def begin_button(event):
            begin_draft()

        ok_button = Button(parent, text="OK", command=begin_draft)
        self.parent.bind("<Return>", begin_button)
        
        opponent_label.grid(row=0, pady=5)
        opponent_entry.grid(row=0, column=1, pady=5)
        position_label.grid(row=1)
        position_entry.grid(row=1, column=1)
        rounds_label.grid(row=2, pady=5)
        rounds_entry.grid(row=2, column=1, pady=5, padx=5)
        style_label.grid(row=3)
        style_menu.grid(row=3, column=1)
        ok_button.grid(row=4, column=1, sticky="se", pady=5, padx=5)

        
class MainUI(Frame):
    """
    Main UI window for draft
    """
    
    def __init__(self, parent, draftgame):

        self.current_opponent_id = 0
        self.user_pick_made = BooleanVar()
        self.user_pick_made.set(False)

        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()        
        self.__MainUI()

        self.draft_logic()

    def draft_logic(self):

        if self.game.draft_style == "Linear":
            self.linear_draft()

        elif self.game.draft_style == "Snake":
            self.snake_draft()

        FinalUI(self.parent, self.game)

    def linear_draft(self):
        while self.game.current_round <= self.game.number_of_rounds:
            if self.game.draft_position != self.game.current_position:
                self.opponent_pick_logic(self.current_opponent_id)
                self.current_opponent_id += 1
                self.increment_position()
            else:
                self.user_pick_logic()
                self.increment_position()

    def snake_draft(self):
        while self.game.current_round <= self.game.number_of_rounds:
            if self.game.current_round % 2 != 0:
                if self.game.draft_position != self.game.current_position:
                    self.opponent_pick_logic(self.current_opponent_id)
                    self.current_opponent_id += 1
                    self.increment_position()
                else:
                    self.user_pick_logic()
                    self.increment_position()
            else:
                if self.game.draft_position != \
                                        self.game.number_of_opponents \
                                        - self.game.current_position + 2:
                    self.opponent_pick_logic(
                        self.game.number_of_opponents - self.current_opponent_id - 1
                    )
                    self.current_opponent_id += 1
                    self.increment_position()
                else:
                    self.user_pick_logic()
                    self.increment_position()

    def increment_position(self):

        self.game.current_position += 1

        if self.game.current_position > self.game.number_of_opponents + 1:
            self.game.current_round += 1
            self.game.current_position = 1
            self.current_opponent_id = 0

        self.__MainUI()

    def user_pick_logic(self):

        self.user_pick_made.set(False)

        while not self.user_pick_made.get():
            self.wait_variable(name=self.user_pick_made)

    def opponent_pick_logic(self, opponent_id):
        pick_made = False

        pick = tkSimpleDialog.askstring(
            "Opponent's pick",
            "Who did your opponent pick?\nCurrent Pick: Round {0}: Pick {1}"
            .format(self.game.current_round, self.game.current_position))

        while not pick_made:
            try:
                if utils.get_player_position(pick, self.game.cursor) is not None:
                    position = utils.get_player_position(pick, self.game.cursor).rstrip('0123456789 ').upper()
                    if utils.get_player_from_table(pick, position, self.game.cursor) is not None:
                        utils.remove_player_from_possible_players(pick, self.game.connection, self.game.cursor)
                        opponent = [opponent for opponent in self.game.opponents if opponent_id == opponent.id][0]
                        opponent.team.append(pick)
                        pick_made = True
                    else:
                        pick = tkSimpleDialog.askstring(
                            "Opponent's pick",
                            "NOT A VALID PICK: please select again\nCurrent Pick: Round {0}: Pick {1}"
                            .format(self.game.current_round, self.game.current_position))

                else:
                    pick = tkSimpleDialog.askstring(
                        "Opponent's pick",
                        "NOT A VALID PICK: please select again\nCurrent Pick: Round {0}: Pick {1}"
                        .format(self.game.current_round, self.game.current_position))
            except AttributeError:
                tkMessageBox.showinfo("Error", "Opponent must pick a valid player")
                pick = tkSimpleDialog.askstring(
                    "Opponent's pick",
                    "NOT A VALID PICK: please select again\nCurrent Pick: Round {0}: Pick {1}"
                    .format(self.game.current_round, self.game.current_position))

    def __MainUI(self):

        self.parent.title("Fantasy Football Helper")
               
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.__draw_round_label(self.parent)
        self.__draw_recommended_list(self.parent)
        self.__draw_valuable_list(self.parent)
        self.__draw_current_team(self.parent)
        self.__draw_team_requirements(self.parent)
        self.__draw_current_choice(self.parent)
        self.__draw_opponent_teams(self.parent)

    def __draw_round_label(self, parent):

        Label(parent, text="Round{0}: Pick{1}".format(self.game.current_round,
                                                      self.game.current_position)).grid(row=0)

    def __draw_current_choice(self, parent):
        
        choice = IntVar()
        other_player = StringVar()
        recommended = self.game.most_recommended_player_remaining()
        valuable = self.game.get_best_player_remaining()
        
        recommended_button = Radiobutton(parent, text=recommended, variable=choice, value=1)
        valuable_button = Radiobutton(parent, text=valuable, variable=choice, value=2)
        other_button = Radiobutton(parent, text="", variable=choice, takefocus=0, value=3)
        other_text = Entry(parent, textvariable=other_player)
        
        def text_focus(event):
            other_button.select()
        
        other_text.bind("<Button-1>", text_focus)

        def pick_player():

            decision = choice.get()

            if decision == 1:

                player = self.game.most_recommended_player_remaining()
                self.game.add_player_to_team(player)
                utils.remove_player_from_possible_players(
                    player,
                    self.game.connection,
                    self.game.cursor)
                self.user_pick_made.set(True)

            elif decision == 2:

                player = self.game.get_best_player_remaining()
                self.game.add_player_to_team(player)
                utils.remove_player_from_possible_players(
                    player,
                    self.game.connection,
                    self.game.cursor)
                self.user_pick_made.set(True)

            elif decision == 3:
                player = other_player.get()
                try:
                    self.game.add_player_to_team(player)
                    utils.remove_player_from_possible_players(
                        player,
                        self.game.connection,
                        self.game.cursor)
                    self.user_pick_made.set(True)
                except:
                    tkMessageBox.showinfo("Error", "Can't add that player to team, try again.")
                    self.user_pick_logic()

            else:
                tkMessageBox.showinfo("No Selection", "Please make a selection")
                self.user_pick_logic()

        def pick_player_button(event):
            pick_player()

        Label(parent, text="Recommended Player").grid(sticky="w", row=1)
        recommended_button.grid(sticky="w", row=1, column=1, columnspan=2)
        
        Label(parent, text="Most Valuable Player").grid(sticky="w", row=2)
        valuable_button.grid(sticky="w", row=2, column=1, columnspan=2)
        
        Label(parent, text="Choose other Player").grid(sticky="w", row=3)
        other_button.grid(sticky="w", row=3, column=1)
        other_text.grid(row=3, column=2, sticky="w", padx=5)
        
        pick_button = Button(parent, text="Pick", command=pick_player).grid(
            row=4, columnspan=3, sticky="ne", padx=5)
        self.parent.bind("<Return>", pick_player_button)
        
    def __draw_recommended_list(self, parent):
        
        recommended_list = self.game.get_list_recommended_players("10")
        recommended_listbox = Text(parent, height=10, width=35)
        
        Label(parent, text="List of Recommended Players").grid(row=1, column=3)
        recommended_listbox.grid(row=2, column=3, rowspan=4, sticky="n")
        for player in recommended_list:
            index = str(recommended_list.index(player) + 1)
            recommended_listbox.insert("end", "{0:>2}:{1:<20} {2} {3}\n".format(index,
                                                                                player[0],
                                                                                player[2],
                                                                                format(player[1], '.0f'))
                                       )
           
        recommended_listbox.config(state="disabled")
        
    def __draw_valuable_list(self, parent):
        
        valuable_list = self.game.get_list_of_best_players("10")
        valuable_listbox = Text(parent, height=10, width=35)
        
        Label(parent, text="List of Most Valuable Players").grid(row=1, column=4)
        valuable_listbox.grid(row=2, column=4, rowspan=4, sticky="n", padx=10)
        for player in valuable_list:
            index = str(valuable_list.index(player) + 1)
            valuable_listbox.insert("end",
                                    "{0:>2}:{1:<20} {2} {3}\n".format(index,
                                                                      player[0],
                                                                      player[2],
                                                                      format(player[1], '.0f'))
                                    )

        valuable_listbox.config(state="disabled")
            
    def __draw_team_requirements(self, parent):
        
        requirements = self.game.check_current_team_needs()
        requirement_list = []
        
        for key in requirements.keys():
            # key_string = "%d%s" % (requirements[key], key)
            requirement_list.append("{0}{1}".format(requirements[key], key))

        Label(parent, text="Still Need: " + ", ".join(requirement_list)).grid(
            row=5, columnspan=3, sticky="w")
            
    def __draw_current_team(self, parent):
        
        current_team = self.game.current_team
        team_list = []
        
        for key in current_team.keys():
            # player_string = "%s %s" % (key, current_team[key])
            team_list.append("{0}: {1}".format(key, current_team[key]))
        
        current_team_string = (", ".join(team_list[0:len(team_list) / 2 + 1])
                               + "\n" + ", ".join(team_list[len(team_list) / 2 + 1:]))
        
        Label(parent, text="Current Team: ").grid(
            row=6)
        Label(parent, text=current_team_string).grid(
            row=6, column=1, columnspan=4, pady=10)

    def __draw_opponent_teams(self, parent):

        opponents = self.game.opponents

        for opponent in opponents:
            Label(parent, text="Opponent{0}'s Team: ".format(opponent.id + 1)).grid(
                row=7 + opponent.id)
            Label(parent, text=str(opponent.team)).grid(
                row=7 + opponent.id,
                column=1, columnspan=4)


class FinalUI(Frame):
    """
    After draft results Screen
    """

    def __init__(self, parent, draftgame):
        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()
        self.__FinalUI()

    def __FinalUI(self):
        self.parent.title("Results")

        for widget in self.parent.winfo_children():
            widget.destroy()

        # self.__draw_menu()
        self.__draw_final_team(self.parent)
        self.__draw_opponent_teams(self.parent)

    def __draw_final_team(self, parent):
        final_team = self.game.current_team
        team_list = []

        for key in final_team.keys():
            player_string = "{0} {1}".format(key, final_team[key])
            team_list.append(player_string)

        final_team_string = (", ".join(team_list[0:len(team_list) / 2 + 1])
                             + "\n" + ", ".join(team_list[len(team_list) / 2 + 1:]))

        Label(parent, text="Final Team: ").grid(
            row=1)
        Label(parent, text=final_team_string).grid(
            row=1, column=1, columnspan=4)

    def __draw_opponent_teams(self, parent):

        opponents = self.game.opponents

        for opponent in opponents:
            Label(parent, text="Opponent{0}'s Team: ".format(opponent.id + 1)).grid(
                row=2 + opponent.id)
            Label(parent, text=str(opponent.team)).grid(
                row=2 + opponent.id,
                column=1, columnspan=4)

        
ffhelper = FantasyFootballHelper.DraftGame()
        
root = Tk()
StartUpUI(root, ffhelper)
root.mainloop()
