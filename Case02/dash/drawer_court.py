from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def adjust_color_intensity(value):
    if value < 30:
        return (1, 1, 0.6)  # Amarelo mais claro
    elif 30 <= value < 45:
        return (1, 1, 0.4)  # Laranja claro
    elif 45 <= value < 60:
        return (1, 0.9, 0.2)  # Laranja médio
    else:
        return (1, 0.7, 0)  # Laranja escuro
    

def draw_court(df, name):
    # Probabilidades do Dataframe   
    df = df.loc[df['PLAYER_NAME'] == name]
    player_card_text = f"Jogador: {name}"
    restricted_area_pct = df['FG_PCT_Restricted_Area'].iloc[0]
    restricted_area_text = f'{restricted_area_pct:.1f}%'

    in_the_paint_pct = df['FG_PCT_In_The_Paint_(Non-RA)'].iloc[0]
    in_the_paint_pct_text = f'{in_the_paint_pct:.1f}%'

    left_corner_pct = df['FG_PCT_Left_Corner_3'].iloc[0]
    left_corner_pct_text = f'{left_corner_pct:.1f}%'

    right_corner_pct = df['FG_PCT_Right_Corner_3'].iloc[0]
    right_corner_pct_text = f'{right_corner_pct:.1f}%'

    mid_range_pct = df['FG_PCT_Mid-Range'].iloc[0]
    mid_range_pct_text = f'{mid_range_pct:.1f}%'

    above_break_3_pct = df['FG_PCT_Above_the_Break_3'].iloc[0]
    above_break_3_pct_text = f'{above_break_3_pct:.1f}%'     

    cmap_name = 'light_to_dark'
    n_bins = 100
    
    # Criar uma figura e eixo
    fig, ax = plt.subplots(figsize=(12, 6))

    # Adicionar retângulo externo da quadra
    outer_box = patches.Rectangle((0, 0), 60, 47, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(outer_box)

    # Adicionar arco de três pontos
    three_point_arc = patches.Arc((25, 0), 44, 50, theta1=0, theta2=180, linewidth=2, edgecolor='black')
    ax.add_patch(three_point_arc)   

    # Adicionar círculo do garrafão
    paint_circle = patches.Circle((25, 19), radius=6, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(paint_circle)

    # Adicionar retângulo da área restrita
    restricted_area = patches.Rectangle((19, 0), 12, 19, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(restricted_area)

    # Adicionar heatmap na área restrita
#     heatmap_data = np.array([[restricted_area_pct]])
    heatmap_data = np.array([
        [restricted_area_pct],
        [in_the_paint_pct],
        [left_corner_pct],
        [right_corner_pct],
        [mid_range_pct],
        [above_break_3_pct]
    ])
    adjusted_colors = [adjust_color_intensity(value) for value in heatmap_data.flatten()]      
    cmap = LinearSegmentedColormap.from_list(cmap_name, adjusted_colors, N=n_bins)
    
    heatmap = ax.imshow(heatmap_data, cmap=cmap, interpolation='bilinear', aspect='auto', extent=(0, 50, 0, 47))

    # Adicionar barra de cores
    cbar = plt.colorbar(heatmap, ax=ax, pad=0.02)
    cbar.set_label('Field Goal Percentage', rotation=270, labelpad=15)

    # Adicionar linhas laterais
    ax.plot([0, 0], [0, 47], color='black')
    ax.plot([50, 50], [0, 47], color='black')

    # Adicionar texto indicando as zonas
    ax.text(3, 17, right_corner_pct_text, fontsize=12, ha='center', va='center')
    ax.text(1, 8, 'Right Corner 3', fontsize=10, ha='center', va='center', rotation='vertical')    
    
    ax.text(25, 36, above_break_3_pct_text, fontsize=12, ha='center', va='center')
    ax.text(25, 40, 'Above the Break 3', fontsize=10, ha='center', va='center')    
    
    ax.text(47, 17, left_corner_pct_text, fontsize=12, ha='center', va='center')
    ax.text(49, 8, 'Left Corner 3', fontsize=10, ha='center', va='center', rotation='vertical')
    
    ax.text(10, 4, in_the_paint_pct_text, fontsize=12, ha='center', va='center')
    ax.text(10, 2, 'In The Paint (Non-RA)', fontsize=10, ha='center', va='center')
    
    ax.text(40, 4, in_the_paint_pct_text, fontsize=12, ha='center', va='center')
    ax.text(40, 2, 'In The Paint (Non-RA)', fontsize=10, ha='center', va='center')   
    
    ax.text(25, 5, restricted_area_text, fontsize=12, ha='center', va='center')
    ax.text(25, 2, 'Restricted Area', fontsize=10, ha='center', va='center')   
    
    ax.text(25, 20, mid_range_pct_text, fontsize=12, ha='center', va='center')
    ax.text(25, 22, 'Mid-Range', fontsize=10, ha='center', va='center')    
    
    ax.text(58, 45, player_card_text, fontsize=12, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
       
    
    # Outras variáveis do card
    usg_pct = f"Eficiência por Jogo: {round(df['USG_PCT'].iloc[0], 2)}%"
    dreb_pct = f"Rebote Defensivo por Jogo: {round(df['DREB_PCT'].iloc[0], 2)}%"
    min_per_gp = f"Minutos por Jogo: {round(df['MIN_PER_GP'].iloc[0], 2)}"
    blk_per_gp = f"Bloqueios por Jogo: {round(df['BLK_PER_GP'].iloc[0], 2)}"
    ast_pct_per_gp = f"Assistência por Jogo: {round(df['AST_PER_GP'].iloc[0], 2)}"
    
    ax.text(58, 40, usg_pct, fontsize=12, ha='left', va='center')
    ax.text(58, 35, dreb_pct, fontsize=12, ha='left', va='center')
    ax.text(58, 30, min_per_gp, fontsize=12, ha='left', va='center')
    ax.text(58, 25, blk_per_gp, fontsize=12, ha='left', va='center')
    ax.text(58, 20, ast_pct_per_gp, fontsize=12, ha='left', va='center')

    # Adicionar linhas pontilhadas para demarcar as zonas
    ax.plot([0, 0], [0, 19], color='black', linestyle='dotted')
    ax.plot([50, 50], [0, 19], color='black', linestyle='dotted')
    ax.plot([19, 19], [19, 47], color='black', linestyle='dotted')
    ax.plot([31, 31], [19, 47], color='black', linestyle='dotted')

    # Definir limites do eixo
    ax.set_xlim(0, 50)
    ax.set_ylim(-15, 47)

    # Desativar eixos
    ax.set_axis_off()

    # Exibir a quadra
    # plt.show()
    return fig



def draw_court_team(df, name):
    # Probabilidades do Dataframe   
    df = df.loc[df['TEAM_NAME'] == name]
    team_card_text = f"Time: {name}"
    restricted_area_pct = df['FG_PCT_Restricted_Area_PER_GP'].iloc[0]
    restricted_area_text = f'{restricted_area_pct:.1f}%'

    in_the_paint_pct = df['FG_PCT_In_The_Paint_(Non-RA)_PER_GP'].iloc[0]
    in_the_paint_pct_text = f'{in_the_paint_pct:.1f}%'

    left_corner_pct = df['FG_PCT_Left_Corner_3_PER_GP'].iloc[0]
    left_corner_pct_text = f'{left_corner_pct:.1f}%'

    right_corner_pct = df['FG_PCT_Right_Corner_3_PER_GP'].iloc[0]
    right_corner_pct_text = f'{right_corner_pct:.1f}%'

    mid_range_pct = df['FG_PCT_Mid-Range_PER_GP'].iloc[0]
    mid_range_pct_text = f'{mid_range_pct:.1f}%'

    above_break_3_pct = df['FG_PCT_Above_the_Break_3_PER_GP'].iloc[0]
    above_break_3_pct_text = f'{above_break_3_pct:.1f}%'     

    cmap_name = 'light_to_dark'
    n_bins = 100
    
    # Criar uma figura e eixo
    fig, ax = plt.subplots(figsize=(12, 6))

    # Adicionar retângulo externo da quadra
    outer_box = patches.Rectangle((0, 0), 60, 47, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(outer_box)

    # Adicionar arco de três pontos
    three_point_arc = patches.Arc((25, 0), 44, 50, theta1=0, theta2=180, linewidth=2, edgecolor='black')
    ax.add_patch(three_point_arc)   

    # Adicionar círculo do garrafão
    paint_circle = patches.Circle((25, 19), radius=6, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(paint_circle)

    # Adicionar retângulo da área restrita
    restricted_area = patches.Rectangle((19, 0), 12, 19, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(restricted_area)

    # Adicionar heatmap na área restrita
#     heatmap_data = np.array([[restricted_area_pct]])
    heatmap_data = np.array([
        [restricted_area_pct],
        [in_the_paint_pct],
        [left_corner_pct],
        [right_corner_pct],
        [mid_range_pct],
        [above_break_3_pct]
    ])
    adjusted_colors = [adjust_color_intensity(value) for value in heatmap_data.flatten()]      
    cmap = LinearSegmentedColormap.from_list(cmap_name, adjusted_colors, N=n_bins)
    
    heatmap = ax.imshow(heatmap_data, cmap=cmap, interpolation='bilinear', aspect='auto', extent=(0, 50, 0, 47))

    # Adicionar barra de cores
    cbar = plt.colorbar(heatmap, ax=ax, pad=0.02)
    cbar.set_label('Field Goal Percentage', rotation=270, labelpad=15)

    # Adicionar linhas laterais
    ax.plot([0, 0], [0, 47], color='black')
    ax.plot([50, 50], [0, 47], color='black')

    # Adicionar texto indicando as zonas
    ax.text(3, 17, right_corner_pct_text, fontsize=12, ha='center', va='center')
    ax.text(1, 8, 'Right Corner 3', fontsize=10, ha='center', va='center', rotation='vertical')    
    
    ax.text(25, 36, above_break_3_pct_text, fontsize=12, ha='center', va='center')
    ax.text(25, 40, 'Above the Break 3', fontsize=10, ha='center', va='center')    
    
    ax.text(47, 17, left_corner_pct_text, fontsize=12, ha='center', va='center')
    ax.text(49, 8, 'Left Corner 3', fontsize=10, ha='center', va='center', rotation='vertical')
    
    ax.text(10, 4, in_the_paint_pct_text, fontsize=12, ha='center', va='center')
    ax.text(10, 2, 'In The Paint (Non-RA)', fontsize=10, ha='center', va='center')
    
    ax.text(40, 4, in_the_paint_pct_text, fontsize=12, ha='center', va='center')
    ax.text(40, 2, 'In The Paint (Non-RA)', fontsize=10, ha='center', va='center')   
    
    ax.text(25, 5, restricted_area_text, fontsize=12, ha='center', va='center')
    ax.text(25, 2, 'Restricted Area', fontsize=10, ha='center', va='center')   
    
    ax.text(25, 20, mid_range_pct_text, fontsize=12, ha='center', va='center')
    ax.text(25, 22, 'Mid-Range', fontsize=10, ha='center', va='center')    
    
    ax.text(58, 45, team_card_text, fontsize=12, ha='left', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
       
    
    # Outras variáveis do card
    win_pct = f"Percentual de Vitória: {df['WinPCT'].iloc[0]}%"
    home = f"Jogando em Casa: {df['HOME'].iloc[0]}%"    
    road = f"Jogando Fora: {df['ROAD'].iloc[0]}"

    
    ax.text(58, 40, win_pct, fontsize=12, ha='left', va='center')
    ax.text(58, 35, home, fontsize=12, ha='left', va='center')
    ax.text(58, 30, road, fontsize=12, ha='left', va='center')
 

    # Adicionar linhas pontilhadas para demarcar as zonas
    ax.plot([0, 0], [0, 19], color='black', linestyle='dotted')
    ax.plot([50, 50], [0, 19], color='black', linestyle='dotted')
    ax.plot([19, 19], [19, 47], color='black', linestyle='dotted')
    ax.plot([31, 31], [19, 47], color='black', linestyle='dotted')

    # Definir limites do eixo
    ax.set_xlim(0, 50)
    ax.set_ylim(-15, 47)

    # Desativar eixos
    ax.set_axis_off()

    # Exibir a quadra
    # plt.show()  
    return fig  