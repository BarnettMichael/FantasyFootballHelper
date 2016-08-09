from Tkinter import *
import tkSimpleDialog

import FantasyFootballHelper
import utils
import Opponent


# class ffhUI(Frame):
#     """
#     UI for Fantasy Football Helper
#     """
#
#     def __init__(self, parent, draftgame):
#         self.game = draftgame
#         self.parent = parent
#         Frame.__init__(self, parent)
#         self.grid()
#         self.__initUI()
#
#     # def __initUI(self):
#     #     self.__draw_new_draft_window(self.parent)
#
#     def __MainUI(self):
#         self.parent.title("Fantasy Football Helper")
#
#         for widget in self.parent.winfo_children():
#             widget.destroy()
#
#         #self.__draw_menu()
#         print "opponents", self.game.numberofopponents
#         print "rounds", self.game.numberofrounds
#         print "position", self.game.draftposition
#         print "style", self.game.draftstyle
#
#         print self.game.current_team
#         self.__draw_recommended_list(self.parent)
#         self.__draw_valuable_list(self.parent)
#         self.__draw_current_team(self.parent)
#         self.__draw_team_requirements(self.parent)
#         self.__draw_current_choice(self.parent)
#         #self.__draw_other_player_teams()
#
#
#     def __draw_current_choice(self, parent):
#
#         choice = IntVar()
#         otherplayer = StringVar()
#         recommended = self.game.most_recommended_player_remaining()
#         valuable = self.game.get_best_player_remaining()
#
#         recommendedbutton = Radiobutton(parent, text=recommended, variable=choice, value=1)
#         valuablebutton = Radiobutton(parent, text=valuable, variable=choice, value=2)
#         otherbutton = Radiobutton(parent, text="", variable=choice, takefocus=0, value=3)
#         othertext = Entry(parent, textvariable=otherplayer)
#
#         def textfocus(event):
#             otherbutton.select()
#
#         othertext.bind("<Button-1>", textfocus)
#
#
#         def pickplayer():
#             decision = choice.get()
#
#             if decision == 1:
#                 print "Recommended Chosen"
#                 self.game.add_player_to_team(self.game.most_recommended_player_remaining())
#                 utils.remove_player_from_possible_players(self.game.get_best_player_remaining(), self.game.connection, self.game.cursor)
#
#             elif decision == 2:
#                 print "MVP chosen"
#                 self.game.add_player_to_team(self.game.get_best_player_remaining())
#                 utils.remove_player_from_possible_players(self.game.get_best_player_remaining(), self.game.connection, self.game.cursor)
#
#             elif decision == 3:
#                 print "Other Player being chosen"
#                 player = otherplayer.get()
#                 print player
#                 self.game.add_player_to_team(player)
#                 utils.remove_player_from_possible_players(player, self.game.connection, self.game.cursor)
#
#             self.game.clear_finished_tables()
#
#         Label(parent, text="Recommended Player").grid(sticky=W, row=0)
#         recommendedbutton.grid(sticky=W, row=0, column=1, columnspan=2)
#
#         Label(parent, text="Most Valuable Player").grid(sticky=W, row=1)
#         valuablebutton.grid(sticky=W, row=1, column=1, columnspan=2)
#
#         Label(parent, text="Choose other Player").grid(sticky=W, row=2)
#         otherbutton.grid(sticky=W, row=2, column=1)
#         othertext.grid(row=2, column=2, sticky=W)
#
#         pickbutton = Button(parent, text="Pick", command=pickplayer).grid(
#             row=3, columnspan=3, sticky=NE)
#
#     def __draw_recommended_list(self, parent):
#
#         recommendedlist = self.game.get_list_recommended_players("10")
#         recommendedlistbox = Text(parent, height=10, width=35)
#
#         Label(parent, text="List of Recommended Players").grid(row=0, column=3)
#         recommendedlistbox.grid(row=1, column=3, rowspan=4, sticky=N)
#         for player in recommendedlist:
#             index = str(recommendedlist.index(player) + 1)
#             recommendedlistbox.insert(END, index + ":"
#                                            + player[0] + " "
#                                            + player[2] + " "
#                                            + format(player[1], '.2f') + "\n"
#                                    )
#
#         recommendedlistbox.config(state=DISABLED)
#
#     def __draw_valuable_list(self, parent):
#
#         valuablelist = self.game.get_list_of_best_players("10")
#         valuablelistbox = Text(parent, height=10, width=35)
#
#         Label(parent, text="List of Most Valuable Players").grid(row=0, column=4)
#         valuablelistbox.grid(row=1, column=4, rowspan=4, sticky=N)
#         for player in valuablelist:
#             index = str(valuablelist.index(player) + 1)
#             valuablelistbox.insert(END, index + ":"
#                                         + player[0] + " "
#                                         + player[2] + " "
#                                         + format(player[1], '.2f') + "\n"
#                                    )
#
#         valuablelistbox.config(state=DISABLED)
#
#     def __draw_team_requirements(self, parent):
#
#         requirements = self.game.check_current_team_needs()
#         requirementlist = []
#
#         for key in requirements.keys():
#             keystring = "%d%s" % (requirements[key], key)
#             requirementlist.append(keystring)
#
#         Label(parent, text = "Still Need: " + ", ".join(requirementlist)).grid(
#             row = 4, columnspan = 3, sticky=W)
#
#     def __draw_current_team(self, parent):
#
#         currentteam = self.game.current_team
#         teamlist = []
#
#         for key in currentteam.keys():
#             playerstring = "%s %s" % (key, currentteam[key])
#             teamlist.append(playerstring)
#
#         currentteamstring = (", ".join(teamlist[0:len(teamlist) / 2 + 1])
#                              + "\n" + ", ".join(teamlist[len(teamlist) / 2 + 1:]))
#
#         Label(parent, text = "Current Team: ").grid(
#             row=5)
#         Label(parent, text = currentteamstring).grid(
#             row=5, column=1, columnspan=4)
#
#     def __draw_new_opponent_choice_window(self, parent, opponentindex):
#
#
#         self.parent.title("Opponent %d Pick" % (opponentindex))
#
#         for widget in self.parent.winfo_children():
#             widget.destroy()
#
#         pick = StringVar()
#         pickbox = Entry(parent, textvariable=pick)
#
#         def opponentpick():
#
#             opppick = pick.get()
#
#             self.game.opponentteams[opponentindex - 1].append(opppick)
#             if utils.get_player_position(opppick, self.game.cursor) != None:
#                 utils.remove_player_from_possible_players(opppick, self.game.connection, self.game.cursor)
#
#             self.__MainUI()
#
#         Label(parent, text="Opponent Pick").grid()
#         pickbox.grid(row=0, column=1)
#         Button(parent, text="OK", command=opponentpick).grid(column=1)

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
        style.set("Linear") ## Just for testing, should be Snake in release

        opponentlabel = Label(parent, text="Opponents")
        opponententry = Entry(parent, width=5)
        
        positionlabel = Label(parent, text="Draft Position")
        positionentry = Entry(parent, width=5)
        
        roundslabel = Label(parent, text="Number of Rounds")
        roundsentry = Entry(parent, width=5)
        
        stylelable = Label(parent, text="Draft Style")
        stylemenu = OptionMenu(parent, style, "Snake", "Linear")
        
        def begin_draft():
            """
            initializes variables to control the flow of the draft
            calls the first window of the draft.
            """
            self.game.numberofopponents = int(opponententry.get())
            self.game.draftposition = int(positionentry.get())
            self.game.numberofrounds = int(roundsentry.get())
            self.game.draftstyle = style.get()
            
            self.game.opponents = []
            self.game.currentposition = 1
            self.game.currentround = 1
            
            for x in xrange(self.game.numberofopponents):
                self.game.opponents.append(Opponent.Opponent(x))
            
            # if self.game.draftstyle == "Linear":
            #     if self.game.draftposition == 1:
            #         MainUI(self.parent, self.game)
            #     else:
            #         OpponentChoiceUI(self.parent, self.game, 1)
            #
            # elif self.game.draftstyle == "Snake":
            #     if self.game.draftposition == 1:
            #         MainUI(self.parent, self.game)
            #     else:
            #         OpponentChoiceUI(self.parent, self.game, 1)

            MainUI(self.parent, self.game)
            
        okbutton = Button(parent, text="OK", command=begin_draft)
        
        opponentlabel.grid(row=0)
        opponententry.grid(row=0, column=1)
        positionlabel.grid(row=1)
        positionentry.grid(row=1, column=1)
        roundslabel.grid(row=2)
        roundsentry.grid(row=2, column=1)
        stylelable.grid(row=3)
        stylemenu.grid(row=3, column=1)
        okbutton.grid(row=4, column=1, sticky=E)
        
class MainUI(Frame):
    """
    Main UI window for draft
    """
    
    def __init__(self, parent, draftgame):
        self.current_opponent_id = 0

        self.userpickmade = BooleanVar()
        self.userpickmade.set(False)
        self.game = draftgame
        self.parent = parent
        Frame.__init__(self, parent)
        self.grid()        
        self.__MainUI()
        self.draft_logic()

    def draft_logic(self):

        if self.game.draftstyle == "Linear":
            self.LinearDraft()

        elif self.game.draftstyle == "Snake":
            self.SnakeDraft()

    def LinearDraft(self):
        while self.game.currentround <= self.game.numberofrounds:
            if self.game.draftposition != self.game.currentposition:
                self.opponent_pick_logic(self.current_opponent_id)
                self.current_opponent_id += 1
                self.increment_position()
            else:
                self.user_pick_logic()
                self.increment_position()

    def SnakeDraft(self):
        print "Snake Draft"
        while self.game.currentround <= self.game.numberofrounds:
            if self.game.draftposition != self.game.currentposition:
                self.opponent_pick_logic(self.current_opponent_id)
                self.current_opponent_id += 1
                self.increment_position()
            else:
                print "USER PICK HAPPENS"
                self.user_pick_logic()
                self.increment_position()

    def increment_position(self):

        self.game.currentposition += 1

        if self.game.currentposition > self.game.numberofopponents + 1:
            self.game.currentround += 1
            self.game.currentposition = 1
            self.current_opponent_id = 0

    def user_pick_logic(self):

        self.userpickmade.set(False)

        while not self.userpickmade.get():
            self.wait_variable(name=self.userpickmade)
            self.__MainUI()

    def opponent_pick_logic(self, opponent_id):
        pickmade = False

        pick = tkSimpleDialog.askstring(
            "Opponent's pick",
            "Who did your opponent pick?\nCurrent Pick: Round {0}: Pick {1}" \
                .format(self.game.currentround, self.game.currentposition))

        while not pickmade:

            if utils.get_player_position(pick, self.game.cursor) != None:
                utils.remove_player_from_possible_players(pick, self.game.connection, self.game.cursor)
                opponent = [opponent for opponent in self.game.opponents if opponent_id == opponent.id][0]
                opponent.team.append(pick)
                self.__MainUI()
                pickmade = True

            else:
                pick = tkSimpleDialog.askstring(
                    "Opponent's pick",
                    "Not a valid pick, please select again\nCurrent Pick: Round {0}: Pick {1}" \
                        .format(self.game.currentround, self.game.currentposition))

    def __MainUI(self):
    
        self.parent.title("Fantasy Football Helper")
               
        for widget in self.parent.winfo_children():
            widget.destroy()
                
        #self.__draw_menu()
        self.__draw_recommended_list(self.parent)
        self.__draw_valuable_list(self.parent)
        self.__draw_current_team(self.parent)
        self.__draw_team_requirements(self.parent)
        self.__draw_current_choice(self.parent)
        #self.__draw_other_player_teams()
        
    def __draw_current_choice(self, parent):
        
        choice = IntVar()
        otherplayer = StringVar()
        recommended = self.game.most_recommended_player_remaining()
        valuable = self.game.get_best_player_remaining()
        
        recommendedbutton = Radiobutton(parent, text=recommended, variable=choice, value=1)
        valuablebutton = Radiobutton(parent, text=valuable, variable=choice, value=2)
        otherbutton = Radiobutton(parent, text="", variable=choice, takefocus=0, value=3)
        othertext = Entry(parent, textvariable=otherplayer)
        
        def textfocus(event):
            otherbutton.select()
        
        othertext.bind("<Button-1>", textfocus)
        
        
        def pickplayer():

            print "Button Press Did something"

            decision = choice.get()

            if decision == 1:
                self.game.add_player_to_team(self.game.most_recommended_player_remaining())
                utils.remove_player_from_possible_players(self.game.get_best_player_remaining(), self.game.connection, self.game.cursor)

            elif decision == 2:
                self.game.add_player_to_team(self.game.get_best_player_remaining())
                utils.remove_player_from_possible_players(self.game.get_best_player_remaining(), self.game.connection, self.game.cursor)

            elif decision == 3:
                player = otherplayer.get()
                self.game.add_player_to_team(player)
                utils.remove_player_from_possible_players(player, self.game.connection, self.game.cursor)

            self.game.clear_finished_tables()
            self.userpickmade.set(True)



        Label(parent, text="Recommended Player").grid(sticky=W, row=0)
        recommendedbutton.grid(sticky=W, row=0, column=1, columnspan=2)
        
        Label(parent, text="Most Valuable Player").grid(sticky=W, row=1)
        valuablebutton.grid(sticky=W, row=1, column=1, columnspan=2)
        
        Label(parent, text="Choose other Player").grid(sticky=W, row=2)
        otherbutton.grid(sticky=W, row=2, column=1)
        othertext.grid(row=2, column=2, sticky=W)
        
        pickbutton = Button(parent, text="Pick", command=pickplayer).grid(
            row=3, columnspan=3, sticky=NE)
        
    def __draw_recommended_list(self, parent):
        
        recommendedlist = self.game.get_list_recommended_players("10")
        recommendedlistbox = Text(parent, height=10, width=35)
        
        Label(parent, text="List of Recommended Players").grid(row=0, column=3)
        recommendedlistbox.grid(row=1, column=3, rowspan=4, sticky=N)
        for player in recommendedlist:
            index = str(recommendedlist.index(player) + 1)
            recommendedlistbox.insert(END, index + ":"
                                           + player[0] + " "
                                           + player[2] + " " 
                                           + format(player[1], '.2f') + "\n"
                                   )
           
        recommendedlistbox.config(state=DISABLED)
        
    def __draw_valuable_list(self, parent):
        
        valuablelist = self.game.get_list_of_best_players("10")
        valuablelistbox = Text(parent, height=10, width=35)
        
        Label(parent, text="List of Most Valuable Players").grid(row=0, column=4)
        valuablelistbox.grid(row=1, column=4, rowspan=4, sticky=N)
        for player in valuablelist:
            index = str(valuablelist.index(player) + 1)
            valuablelistbox.insert(END, index + ":" 
                                        + player[0] + " "
                                        + player[2] + " " 
                                        + format(player[1], '.2f') + "\n"
                                   )
                
        valuablelistbox.config(state=DISABLED)
            
    def __draw_team_requirements(self, parent):
        
        requirements = self.game.check_current_team_needs()
        requirementlist = []
        
        for key in requirements.keys():
            keystring = "%d%s" % (requirements[key], key)
            requirementlist.append(keystring)
        
        Label(parent, text = "Still Need: " + ", ".join(requirementlist)).grid(
            row = 4, columnspan = 3, sticky=W)
            
    def __draw_current_team(self, parent):
        
        currentteam = self.game.current_team
        teamlist = []
        
        for key in currentteam.keys():
            playerstring = "%s %s" % (key, currentteam[key])
            teamlist.append(playerstring)
        
        currentteamstring = (", ".join(teamlist[0:len(teamlist) / 2 + 1])
                             + "\n" + ", ".join(teamlist[len(teamlist) / 2 + 1:]))
        
        Label(parent, text = "Current Team: ").grid(
            row=5)
        Label(parent, text = currentteamstring).grid(
            row=5, column=1, columnspan=4)

# class OpponentChoiceUI(Frame):
#     """
#     Opponent Choice Window
#     Takes draft position as additional argument
#     """
#
#     def __init__(self, parent, draftgame, draftposition):
#         self.game = draftgame
#         self.parent = parent
#         self.draftposition = draftposition
#         Frame.__init__(self, self.parent)
#         self.grid()
#         self.__draw_opponent_choice_window(self.draftposition)
#
#     def __draw_opponent_choice_window(self, draftposition):
#
#         opp_choice_window = Toplevel()
#         opp_choice_window.grab_set()
#         opp_choice_window.title("Opponent %d Pick" % (draftposition))
#
#         for widget in self.parent.winfo_children():
#             widget.destroy()
#
#         MainUI(self.parent, self.game)
#
#         pick = StringVar()
#         pickbox = Entry(opp_choice_window, textvariable=pick)
#
#         def opponentpick():
#
#             opppick = pick.get()
#
#             self.game.opponentteams[draftposition - 1].append(opppick)
#             if utils.get_player_position(opppick, self.game.cursor) != None:
#                 utils.remove_player_from_possible_players(opppick, self.game.connection, self.game.cursor)
#
#             ##Call back to mainUI
#
#         Label(opp_choice_window, text="Opponent Pick").grid()
#         pickbox.grid(row=0, column=1)
#         Button(opp_choice_window, text="OK", command=opponentpick).grid(column=1)
        
        
ffhelper = FantasyFootballHelper.draftgame()       
        
root = Tk()
StartUpUI(root, ffhelper)
root.mainloop()