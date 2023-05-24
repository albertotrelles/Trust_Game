from otree.api import *
import random 
roleA = random.randint(1,2)   #si roleA == 2, P2 recibe la dotación. 

doc = """
Simple trust game
"""

#####################################################################################################
## MODELS                                                                                          ##
#####################################################################################################
class C(BaseConstants):
    NAME_IN_URL = 'trust_simple'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(5)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    send = models.CurrencyField(min=cu(0), max=C.ENDOWMENT, label="Si fueras el jugador A ¿cuánto enviarías al jugador B?")
    
    sb1 = models.CurrencyField(min=cu(0) , max=cu(C.MULTIPLIER*1), label="Si fueras el jugador B y recibieras 3 puntos ¿cuánto enviarías de vuelta al Jugador A?")
    sb2 = models.CurrencyField(min=cu(0) , max=cu(C.MULTIPLIER*2), label="Si fueras el jugador B y recibieras 6 puntos ¿cuánto enviarías de vuelta al Jugador A?")
    sb3 = models.CurrencyField(min=cu(0) , max=cu(C.MULTIPLIER*3), label="Si fueras el jugador B y recibieras 9 puntos ¿cuánto enviarías de vuelta al Jugador A?")
    sb4 = models.CurrencyField(min=cu(0) , max=cu(C.MULTIPLIER*4), label="Si fueras el jugador B y recibieras 12 puntos ¿cuánto enviarías de vuelta al Jugador A?")
    sb5 = models.CurrencyField(min=cu(0) , max=cu(C.MULTIPLIER*5), label="Si fueras el jugador B y recibieras 15 puntos ¿cuánto enviarías de vuelta al Jugador A?")

    nature = models.IntegerField(initial=roleA)

    final_sb = models.CurrencyField(initial=cu(0))
    
#####################################################################################################
## FUNCTIONS                                                                                       ##
#####################################################################################################
def creating_session(subsession):
    matrix = subsession.get_group_matrix()

    if roleA == 2:
        for row in matrix:
            row.reverse()
    else:
        pass
    subsession.set_group_matrix(matrix)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    if roleA == 2:                              #si P2 recibe la dotación    
        #sent_amount = p2.send 
        mylist = [p1.sb1, p1.sb2, p1.sb3, p1.sb4, p1.sb5]

        for i in range(5):
            if cu(i) == p2.send:
                p2.payoff = max(C.ENDOWMENT - p2.send + mylist[i-1], 0)
                p1.payoff = max(p2.send * C.MULTIPLIER - mylist[i-1], 0)                  #p2.payoff = C.ENDOWMENT - p.2send - p1.sb`k` donde `k`=p2.send
                p1.final_sb = mylist[i-1]            
            else:
                pass 

    else:
        #sent_amount = p1.send
        mylist = [p2.sb1, p2.sb2, p2.sb3, p2.sb4, p2.sb5]

        for i in range(5):
            if cu(i) == p1.send:
                p1.payoff = max(C.ENDOWMENT - p1.send + mylist[i-1], cu(0))
                p2.payoff = max(p1.send * C.MULTIPLIER - mylist[i-1], cu(0))
                p2.final_sb = mylist[i-1]
            else:
                pass


def other_player(player: Player):                #para hacer referencias a p1.var y p2.var en vars_for_templates
    return player.get_others_in_group()[0]
def self_player(player: Player):
    return player

#####################################################################################################
## PAGES                                                                                           ##
#####################################################################################################
class P1_Choice(Page):
    form_model = 'player'
    form_fields = ['send', 'sb1', 'sb2', 'sb3', 'sb4', 'sb5']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class P2_Choice(Page):
    form_model = 'player'
    form_fields = ['send', 'sb1', 'sb2', 'sb3', 'sb4', 'sb5']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod                                          
    def vars_for_template(player: Player):
        return dict(other_sb=other_player(player).final_sb, other_send=other_player(player).send, your_sb=self_player(player).final_sb, 
                    your_send=self_player(player).send, your_received=other_player(player).send*C.MULTIPLIER, other_received=self_player(player).send*C.MULTIPLIER)


class Results2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
    
    @staticmethod                                          
    def vars_for_template(player: Player):
        return dict(other_sb=other_player(player).final_sb, other_send=other_player(player).send, your_sb=self_player(player).final_sb, 
                    your_send=self_player(player).send, your_received=other_player(player).send*C.MULTIPLIER, other_received=self_player(player).send*C.MULTIPLIER)



page_sequence = [P1_Choice, P2_Choice, ResultsWaitPage, Results1, Results2]
