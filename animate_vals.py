from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
import matplotlib as plt
import pandas as pd
import plotly.graph_objs as go
from plotly.grid_objs import Grid, Column
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, iplot_mpl, plot
import math
import copy
import sys

pathval = sys.argv[1]

def makePlayerShapes(home,away,direction):
    dbs = []
    for i in range(len(home['x'])):

        if(home['text'][i] == 'FS' or home['text'][i] == 'SS' or home['text'][i] == 'CB' or home['text'][i] == 'S'):
            dbs.append((home['x'][i],home['y'][i],home['text'][i]))
    for i in range(len(away['x'])):
        if(away['text'][i] == 'FS' or away['text'][i] == 'SS' or away['text'][i] == 'CB' or away['text'][i] == 'S'):
            dbs.append((away['x'][i],away['y'][i],away['text'][i]))
    #print(dbs)
    
    recs = []
    newthing = sorted(dbs,key= lambda qqq: qqq[1])
    #print(thing)
    
    t = []
    for lel in newthing:
        to_add = True
        for lel2 in newthing:
            if(abs(lel[1] - lel2[1]) < 7.5):
                if(direction == "GOING RIGHT"):
                    if(lel[0] < lel2[0]):
                        to_add = False
                else:
                    if(lel[0] > lel2[0]): 
                        to_add = False
        if(to_add): t.append(lel)
    thing = sorted(t,key= lambda qqq: qqq[1])
                    
    for i in range(len(thing)):
        if(i == 0):
            tnow = thing[i]
            try: 
                tnext = thing[i+1]
            except:
                tnext = None
            
            if(direction == "GOING RIGHT"):
            
                if(tnext != None): 
                    recs.append(  (tnow[0]-2,0,120,(tnow[1] +tnext[1])/2, tnow[2])   )
                else:
                    recs.append(  (tnow[0]-2,0,120,54, tnow[2])   )
            else:
                if(tnext != None):
                    recs.append(  (tnow[0]+2,0,0,(tnow[1] +tnext[1])/2, tnow[2])   )
                else:
                    recs.append(  (tnow[0]-2,0,0,54, tnow[2])   )
        elif(i == len(thing)-1):
            tnow = thing[i]
            tprev = thing[i-1]
            if(direction == "GOING RIGHT"):


                recs.append(   (tnow[0]-2,(tnow[1]+tprev[1])/2,120,54   , tnow[2]))
            else:
                
                recs.append(   (tnow[0]+2,(tnow[1]+tprev[1])/2,0,54   , tnow[2]))
        else:
            tnow = thing[i]
            tprev = thing[i-1]
            tnext = thing[i+1]
            if(direction == "GOING RIGHT"):
                
                recs.append(  (tnow[0]-2,(tnow[1]+tprev[1])/2,120,(tnow[1] +tnext[1])/2   , tnow[2]))
            else:
        
                recs.append(  (tnow[0]+2,(tnow[1]+tprev[1])/2,0,(tnow[1] +tnext[1])/2   , tnow[2]))
            
    shapes = []
    for x in recs:
        #print(x[4])
        color = 'rgb(127,187,34)' if "S" in x[4] else 'rgb(187,34,127)'
        rect = {
        'type': 'rect',
        'layer' : 'below',
        'x0': x[0],
        'y0': x[1],
        'x1': x[2],
        'y1': x[3],
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
        'fillcolor' : color,
        }
        shapes.append(rect)
    return shapes

def makeDefenseZones(LOS,direction,numzonesWide,numzonesDeep):
    shapes = []
    rect = {
        'type': 'rect',
        'layer' : 'below',
        'x0': 0,
        'y0': 54,
        'x1': LOS,
        'y1':  0,
        'line': {
            'color': 'rgba(0,0,255,1)',
            'width': 1
        }
        }
    shapes.append(rect)
    if(direction == "GOING LEFT"):
        
        color = 'rgb(127,187,34)'
        for x in range(1,numzonesWide):
            rect = {
                'type': 'rect',
                'layer' : 'below',
                'x0': 0,
                'y0': x*(54/numzonesWide),
                'x1': LOS,
                'y1':  x*(54/numzonesWide),
                'line': {
                    'color': 'rgba(255,105,180,1)',
                    'width': 1
                },
                'fillcolor' : color,
                }
            shapes.append(rect)

        if(LOS > 21):
            for x in range(1,numzonesDeep):
                rect = {
                'type': 'rect',
                'layer' : 'below',
                'x0': LOS-7*x,
                'y0': 0,
                'x1': LOS-7*x,
                'y1': 54,
                'line': {
                    'color': 'rgba(255,105,180,1)',
                    'width': 1
                },
                'fillcolor' : color,
                }
                shapes.append(rect)
        color = 'rgb(127,187,34)'
    else:
        for x in range(1,numzonesWide):
            rect = {
                'type': 'rect',
                'layer' : 'below',
                'x0': LOS,
                'y0': x*(54/numzonesWide),
                'x1': 120,
                'y1':  x*(54/numzonesWide),
                'line': {
                    'color': 'rgba(255,105,180,1)',
                    'width': 1
                }
                }
            shapes.append(rect)

        if(120 - LOS > 21):
            for x in range(1,numzonesDeep):
                rect = {
                'type': 'rect',
                'layer' : 'below',
                'x0': LOS+7*x,
                'y0': 0,
                'x1': LOS+7*x,
                'y1': 54,
                'line': {
                    'color': 'rgba(255,105,180,1)',
                    'width': 1
                },
                }
                shapes.append(rect)

    return shapes


plays_df = pd.read_csv(pathval + '/pass_plays.csv')
games_df = pd.read_csv(pathval + '/games.csv')
player_info = pd.read_csv(pathval + '/players.csv')


#@interact(PLAYVAL="10")
opts = [x for x in range(len(plays_df))]
def g(PLAYVAL):
    midpoint_trace = go.Scatter(
    x = [60],
    y = [53.3/2]
    )
    outer_shape = {
        'type': 'rect',
        'layer' : 'below',
        'x0': 0,
        'y0': 0,
        'x1': 120,
        'y1': 53.3,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
        'fillcolor' : 'rgb(61,204,132)',
    }


    left_goal = {
        'type': 'rect',
        'layer' : 'below',
        'x0': 0,
        'y0': 0,
        'x1': 10,
        'y1': 53.3,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
        'fillcolor' : 'rgb(0,0,127)',
    }

    right_goal = {
        'type': 'rect',
        'layer' : 'below',
        'x0': 110,
        'y0': 0,
        'x1': 120,
        'y1': 53.3,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
        'fillcolor' : 'rgb(0,0,127)',
    }


    _shapes = [
        outer_shape,
        left_goal,
        right_goal,
    ]

    for x in range(1,13):
        temp_shape = {
        'type': 'rect',
            'layer' : 'below',
        'x0': x*10,
        'y0': 0,
        'x1': x*10,
        'y1': 53.3,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
        }
        _shapes.append(temp_shape)


    layout = go.Layout(
        title = 'Football Field',
        shapes = _shapes,
    )
    xs = []
    ys = []
    ts = []
    for i in range(1,10):
        x = (i+1) * 10 - 1
        xs.append(x)
        y = 10
        ys.append(y)
        tt = i if i < 5 else 10 -i 
        ts.append(tt)

        x = (i+1) * 10 + 1
        xs.append(x)
        y = 10
        ys.append(y)
        ts.append(0)


    yardlabels = go.Scatter(
        x=xs,
        y=ys,
        mode='text',
        name='Lines, Markers and Text',
        text=ts,
    )

    #play = plays_df.iloc[int(PLAYVAL)]
    kk1 = input("Enter gameId \n")
    kk2 = input("Enter playId \n")
    play = plays_df[(plays_df['gameId'] == kk1) & (plays_df['playId'] == kk2)].iloc[0]
    print(play)

    playId = play['playId']
    gameId = play['gameId']
    bigLos = play['LOS']
    gameInfo = games_df.query('gameId == %s' % gameId)
    trackingfilename = '/tracking_gameId_' + str(gameId) + '.csv'

    game_df = pd.read_csv(pathval + trackingfilename)
    game_play_df = game_df.query('playId == %s' % playId)
    direction = play["POSS_DIR"]
    print(game_play_df['event'].unique())


    sett = set()

    play_info ={}
    lastname = ''
    playlengthframes = 0
    home_team = gameInfo['homeTeamAbbr'].iloc[0]
    away_team = gameInfo['visitorTeamAbbr'].iloc[0]

    layout = {'xaxis': {'range': [0, 120], 'autorange': False, 'showgrid':False, 'showticklabels': False},
                     'yaxis': {'range': [0, 53.3], 'autorange': False,'showgrid':False,'showticklabels': False} ,
                     'title': 'GameID ' + str(gameId) + ', PlayID ' + str(playId) + '\n' + play['playDescription'],
                     #'shapes': _shapes,
                     
                     'updatemenus': [{'type': 'buttons',
                                      'buttons': [{'label': 'Play',
                                                   'method': 'animate',
                                            
                                                   'args': [None, {'frame': {'redraw': True, 'duration': 100}, 'fromcurrent': True}]},
                                                  
                                                   {
                                                    'args': [[None], {'frame': {'duration': 75, 'redraw': True}, 'mode': 'immediate',
                                                    'transition': {'duration': 0}}],
                                                    'label': 'Pause',
                                                    'method': 'animate'
                                                }
                                                 
                                                 
                                                 ]}]
                    }


    for x in range(len(game_play_df)):
        try: playerInfo  = player_info[player_info['nflId'] == game_play_df.iloc[x]['nflId']].iloc[0]
        except: playerInfo = player_info[player_info['nflId'] == game_play_df.iloc[0]['nflId']].iloc[0]
    
        currname = game_play_df.iloc[x]['displayName']
        #print(game_play_df.iloc[x]['team'])
        if(currname == lastname):
            play_info[currname].append((game_play_df.iloc[x]['x'],
                                        game_play_df.iloc[x]['y'],
                                        game_play_df.iloc[x]['team'],
                                        game_play_df.iloc[x]['jerseyNumber'],
                                        game_play_df.iloc[x]['event'],playerInfo['PositionAbbr']))
        else:
            if(lastname != ''): 
                playlengthframes = len(play_info[lastname])
            play_info[currname] = [(game_play_df.iloc[x]['x'],
                                    game_play_df.iloc[x]['y'],
                                    game_play_df.iloc[x]['team'],
                                    game_play_df.iloc[x]['jerseyNumber'],
                                    game_play_df.iloc[x]['event'],playerInfo['PositionAbbr'])]

        lastname = currname
        
    
    los = None
    frames = []
    ball_thrown = False
    for c in range(playlengthframes):
        frame = {'data' : [], 'name': c}
        home = {'x' : [], 'y' : [], 'text' : []}
        away = {'x' : [], 'y' : [], 'text' : []}
        ball = {'x' : [], 'y' : [], 'text' : []}
        frameInfo = {'x' : [], 'y' : [], 'text' : []}
        checkevent = False
        player_shapes = []

        for p in sorted(play_info):
            if(checkevent == False):
                try:
                    b = math.isnan(play_info[p][c][4])
                except:
                    b = False
                if(b):
                    frameInfo['x'].append(85)
                    frameInfo['y'].append(8)
                    frameInfo['text'].append('Frame %s' % c)
                    frameInfo['mode'] = 'text'
                    frameInfo['name'] = 'frameInfo'
                    frameInfo['textfont']=dict(
                        size=15,
                        color='#ffffff')
                else:
                    if(play_info[p][c][4] == 'pass_forward'):
                        print("BALL THROWN")
                        ball_thrown = True
                    frameInfo['x'].append(85)
                    frameInfo['y'].append(8)
                    frameInfo['text'].append(play_info[p][c][4])
                    frameInfo['mode'] = 'text'
                    frameInfo['textfont']=dict(
                        size=10,
                        color='#ffffff')
                checkEvent = True
            if play_info[p][c][2] == 'home':
                home['x'].append(play_info[p][c][0])
                home['y'].append(play_info[p][c][1])
                home['text'].append(int(play_info[p][c][3]))
                home['mode'] = 'markers+text'
                home['marker'] = {'color' : 'blue', 'size' : 20}
                home['name'] = home_team
                home['textfont']=dict(
                        size=10,
                        color='#ffffff'
                )
            elif play_info[p][c][2] == 'away': 
                away['x'].append(play_info[p][c][0])
                away['y'].append(play_info[p][c][1])
                away['text'].append(int(play_info[p][c][3]))
                away['mode'] = 'markers+text'
                away['name'] = away_team
                away['marker'] = {'color' : 'red', 'size' : 20}
                away['textfont']=dict(
                        size=10,
                        color='#ffffff'
                )
                
            else:
                if los == None:
                    los = (play_info[p][c][0],play_info[p][c][1])
                ball['x'].append(play_info[p][c][0])
                ball['y'].append(play_info[p][c][1])
                ball['mode'] = 'markers'
                ball['marker'] = {'color' : 'brown', 'size' : 10}
                ball['name'] = 'Ball'
        
        if (not ball_thrown):
            player_shapes = makePlayerShapes(home,away,direction)
        else:
            player_shapes = []
        
        #defense_Zones = makeDefenseZones(bigLos, direction,4,4)
        tempshapes = copy.deepcopy(_shapes)
        tempshapes.extend(player_shapes)
        #tempshapes.extend(defense_Zones)
        #layout['shapes'] = tempshapes
        frame = {'data' : [home,away,ball],'layout':{'shapes' : tempshapes}}
        frames.append(frame)

    #print(los)

   
    figure = {
          
          'layout': layout,
          'frames': frames,
          'data' : [{'x' : [1], 'y' : [1]},{'x' : [1], 'y' : [1]},{'x' : [1], 'y' : [1]},yardlabels]
          #'data' : [yardlabels]
    }

    plot(figure)
    return (PLAYVAL)

g(2)