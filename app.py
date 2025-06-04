import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import json
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import math
from collections import defaultdict

id_to_name = {
    5503: 'Messi',
    20055: 'Ter Stegen',
    6374: 'Semedo',
    5213: 'Pique',
    5492: 'Umtiti',
    5211: 'J.Alba',
    5203: 'Busquets',
    5470: 'Rakitic',
    6379: 'S.Roberto',
    5477: 'Dembele',
    5246: 'Suarez'
}

id_to_role = {
    20055: 'GK',
    5213: 'DF',
    5492: 'DF',
    5211: 'DF',
    6374: 'DF',
    5203: 'MF',
    5470: 'MF',
    6379: 'MF',
    5477: 'FW',
    5246: 'FW',
    5503: 'FW'
}

role_to_color = {
    'GK': '#DC143C',
    'DF': '#1E90FF',
    'MF': '#32CD32',
    'FW': '#FFA500'
}

@st.cache_data
def load_data():
    with open('events.json','r', encoding='utf-8') as f:
        data = json.load(f)
    return pd.json_normalize(data)

df = load_data()

st.sidebar.title("Paramètres du Pass Map")

team_list = df['team.name'].dropna().unique().tolist()
default_team = 'Barcelona' if 'Barcelona' in team_list else team_list[0]
selected_team = st.sidebar.selectbox("Équipe", options=team_list, index=team_list.index(default_team))

display_mode = st.sidebar.selectbox(
    "Mode de visualisation",
    ["Échanges totaux", "Passes faites (flèches)", "Passes reçues (flèches)"]
)

min_pass_count = st.sidebar.slider("Afficher liens à partir de X passes", 1, 10, 1)

df_starting = df[(df['type.id'] == 35) & (df['team.name'] == selected_team)]
players_in_lineup_ids = set()
for lineup_list in df_starting['tactics.lineup'].dropna():
    for player_info in lineup_list:
        players_in_lineup_ids.add(player_info['player']['id'])

titulaires_sorted = sorted(players_in_lineup_ids, key=lambda x: id_to_name.get(x, f"ID {x}"))
selected_player = st.sidebar.selectbox(
    "Voir les stats détaillées d’un joueur",
    options=[None] + titulaires_sorted,
    format_func=lambda x: id_to_name.get(x, f"ID {x}") if x else "---"
)

df_pass = df[(df['type.id'] == 30) & (df['team.name'] == selected_team)].copy()
df_pass['passeur_id'] = df_pass['player.id']
df_pass['receveur_id'] = df_pass['pass.recipient.id']

df_pass = df_pass[
    df_pass['passeur_id'].isin(players_in_lineup_ids) &
    df_pass['receveur_id'].isin(players_in_lineup_ids)
]

df_pass['x_debut'] = df_pass['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
df_pass['y_debut'] = df_pass['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
df_pass['x_fin']   = df_pass['pass.end_location'].apply(lambda x: x[0] if isinstance(x, list) else None)
df_pass['y_fin']   = df_pass['pass.end_location'].apply(lambda x: x[1] if isinstance(x, list) else None)

df_pass['distance'] = np.sqrt((df_pass['x_fin'] - df_pass['x_debut'])**2 
                              + (df_pass['y_fin'] - df_pass['y_debut'])**2)
df_pair_counts = (
    df_pass
    .groupby(['passeur_id','receveur_id'], as_index=False)
    .size()
    .rename(columns={'size':'count'})
)

df_distance_passeur = (
    df_pass
    .groupby('passeur_id', as_index=False)
    .agg({'distance':'mean', 'id':'count'})
    .rename(columns={'passeur_id':'player_id','distance':'avg_pass_distance','id':'total_passes_made'})
)

df_distance_receveur = (
    df_pass
    .groupby('receveur_id', as_index=False)
    .agg({'distance':'mean'})
    .rename(columns={'receveur_id':'player_id','distance':'avg_receiving_distance'})
)

if display_mode == "Échanges totaux":
    from collections import defaultdict
    df_directed = df_pair_counts.copy()
    undirected_dict = defaultdict(int)
    for row in df_directed.itertuples():
        a, b, c = row.passeur_id, row.receveur_id, row.count
        key = (min(a,b), max(a,b))
        undirected_dict[key] += c
    data_undirected = []
    for (a,b), total in undirected_dict.items():
        data_undirected.append({'playerA':a, 'playerB':b, 'count_sum': total})
    df_undirected = pd.DataFrame(data_undirected)
    df_passeur_pos = df_pass[['passeur_id','x_debut','y_debut']].rename(columns={
        'passeur_id':'player_id','x_debut':'x','y_debut':'y'
    })
    df_receveur_pos = df_pass[['receveur_id','x_fin','y_fin']].rename(columns={
        'receveur_id':'player_id','x_fin':'x','y_fin':'y'
    })
    df_allpos = pd.concat([df_passeur_pos, df_receveur_pos], ignore_index=True)
    df_allpos.dropna(subset=['x','y'], inplace=True)

    df_positions = (
        df_allpos
        .groupby('player_id', as_index=False)
        .agg({'x':'mean','y':'mean'})
    )
    df_positions['short_name'] = df_positions['player_id'].map(id_to_name)
    df_positions['role'] = df_positions['player_id'].map(id_to_role)
    df_made_sum = df_pair_counts.groupby('passeur_id', as_index=False)['count'].sum()
    df_made_sum.rename(columns={'passeur_id':'player_id','count':'passes_made'}, inplace=True)
    df_received_sum = df_pair_counts.groupby('receveur_id', as_index=False)['count'].sum()
    df_received_sum.rename(columns={'receveur_id':'player_id','count':'passes_received'}, inplace=True)
    df_merge = pd.merge(df_made_sum, df_received_sum, on='player_id', how='outer').fillna(0)
    df_merge['total_involved'] = df_merge['passes_made'] + df_merge['passes_received']
    df_positions = pd.merge(df_positions, df_merge[['player_id','total_involved']], on='player_id', how='left').fillna(0)
    df_positions['marker_size'] = df_positions['total_involved'].apply(lambda v: 20 + 5*v)
    st.title(f"Pass Map (Échanges totaux) : {selected_team}")
    pitch = Pitch(pitch_color='white', line_color='black', stripe=False, pad_bottom=0.05)
    fig, ax = pitch.draw(figsize=(10, 6))

    for _, rowp in df_positions.iterrows():
        color = role_to_color.get(rowp['role'], 'gray')
        pitch.scatter(
            rowp['x'], rowp['y'],
            s=rowp['marker_size'],
            edgecolors='black',
            color=color, alpha=0.9, ax=ax
        )
        ax.text(
            rowp['x']+2, rowp['y'], 
            rowp['short_name'] if pd.notna(rowp['short_name']) else rowp['player_id'],
            ha='left', va='center', color='black', fontsize=10, fontweight='bold'
        )

    if not df_undirected.empty:
        pass_values = df_undirected['count_sum'].values
        vmin, vmax = pass_values.min(), pass_values.max()
        norm = Normalize(vmin=vmin, vmax=vmax, clip=True)
        cmap = cm.get_cmap('coolwarm')

        for rowu in df_undirected.itertuples():
            a, b, c = rowu.playerA, rowu.playerB, rowu.count_sum
            if c < min_pass_count:
                continue
            pa = df_positions[df_positions['player_id'] == a]
            pb = df_positions[df_positions['player_id'] == b]
            if pa.empty or pb.empty:
                continue
            x1, y1 = pa.iloc[0]['x'], pa.iloc[0]['y']
            x2, y2 = pb.iloc[0]['x'], pb.iloc[0]['y']

            lw = 1 + (c*0.15)
            color_link = cmap(norm(c))
            pitch.lines(x1, y1, x2, y2, lw=lw, color=color_link, alpha=0.7, ax=ax)

            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(
                mid_x, mid_y, str(c),
                color='black', fontsize=6, fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", fc='white', ec='none', alpha=0.6)
            )

    st.pyplot(fig)

elif display_mode == "Passes faites (flèches)":

    df_pos_passeurs = (
        df_pass
        .groupby('passeur_id', as_index=False)
        .agg({'x_debut':'mean','y_debut':'mean'})
        .rename(columns={'passeur_id':'player_id','x_debut':'x','y_debut':'y'})
    )
    all_pids = list(players_in_lineup_ids)
    existing_pids = df_pos_passeurs['player_id'].tolist()
    missing = [p for p in all_pids if p not in existing_pids]
    df_pos_missing = pd.DataFrame({'player_id':missing, 'x':np.nan, 'y':np.nan})
    df_pos_passeurs = pd.concat([df_pos_passeurs, df_pos_missing], ignore_index=True)
    df_pos_passeurs['short_name'] = df_pos_passeurs['player_id'].map(id_to_name)
    df_pos_passeurs['role'] = df_pos_passeurs['player_id'].map(id_to_role)

    df_made_sum = df_pass.groupby('passeur_id', as_index=False).size().rename(columns={'passeur_id':'player_id','size':'passes_made'})
    df_pos_passeurs = pd.merge(df_pos_passeurs, df_made_sum, on='player_id', how='left').fillna(0)
    df_pos_passeurs['marker_size'] = df_pos_passeurs['passes_made'].apply(lambda v: 20 + 5*v)

    df_made = df_pair_counts.rename(columns={'count':'nb_passes'})
    df_made = df_made[df_made['nb_passes'] >= min_pass_count]

    st.title(f"Pass Map (Passes faites) : {selected_team}")
    pitch = Pitch(pitch_color='white', line_color='black', stripe=False, pad_bottom=0.05)
    fig, ax = pitch.draw(figsize=(10, 6))

    for _, rowp in df_pos_passeurs.iterrows():
        color = role_to_color.get(rowp['role'], 'gray')
        x_, y_ = rowp['x'], rowp['y']
        if pd.isna(x_) or pd.isna(y_):
            continue
        pitch.scatter(
            x_, y_,
            alpha=0.9,
            s=rowp['marker_size'],
            edgecolors='black',
            color=color,
            ax=ax
        )
        label = rowp['short_name'] if pd.notna(rowp['short_name']) else f"ID {rowp['player_id']}"
        ax.text(
            x_+2, y_,
            label,
            ha='left', va='center',
            color='black', fontsize=10, fontweight='bold'
        )

    if not df_made.empty:
        pass_values = df_made['nb_passes'].values
        vmin, vmax = pass_values.min(), pass_values.max()
        norm = Normalize(vmin=vmin, vmax=vmax, clip=True)
        cmap = cm.get_cmap('coolwarm')

        for rowf in df_made.itertuples():
            pidA, pidB, c = rowf.passeur_id, rowf.receveur_id, rowf.nb_passes
            pa = df_pos_passeurs[df_pos_passeurs['player_id'] == pidA]
            pb = df_pos_passeurs[df_pos_passeurs['player_id'] == pidB]
            if pa.empty or pb.empty:
                continue
            x1, y1 = pa.iloc[0]['x'], pa.iloc[0]['y']
            x2, y2 = pb.iloc[0]['x'], pb.iloc[0]['y']
            if pd.isna(x1) or pd.isna(y1) or pd.isna(x2) or pd.isna(y2):
                continue

            lw = 1 + (c*0.1)
            color_link = cmap(norm(c))

            pitch.arrows(
                x1, y1, x2, y2,
                width=lw,
                headwidth=lw*1.5,
                headlength=lw*1.5,
                color=color_link,
                alpha=0.7,
                ax=ax
            )

            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(
                mid_x, mid_y, str(c),
                color='black', fontsize=8, fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", fc='white', ec='none', alpha=0.6)
            )

    st.pyplot(fig)

else:

    df_pos_receveurs = (
        df_pass
        .groupby('receveur_id', as_index=False)
        .agg({'x_fin':'mean','y_fin':'mean'})
        .rename(columns={'receveur_id':'player_id','x_fin':'x','y_fin':'y'})
    )
    all_pids = list(players_in_lineup_ids)
    existing_pids = df_pos_receveurs['player_id'].tolist()
    missing = [p for p in all_pids if p not in existing_pids]
    df_pos_missing = pd.DataFrame({'player_id':missing, 'x':np.nan, 'y':np.nan})
    df_pos_receveurs = pd.concat([df_pos_receveurs, df_pos_missing], ignore_index=True)
    df_pos_receveurs['short_name'] = df_pos_receveurs['player_id'].map(id_to_name)
    df_pos_receveurs['role'] = df_pos_receveurs['player_id'].map(id_to_role)

    df_received_sum = df_pass.groupby('receveur_id', as_index=False).size().rename(columns={'receveur_id':'player_id','size':'passes_received'})
    df_pos_receveurs = pd.merge(df_pos_receveurs, df_received_sum, on='player_id', how='left').fillna(0)
    df_pos_receveurs['marker_size'] = df_pos_receveurs['passes_received'].apply(lambda v: 20 + 5*v)

    df_received = df_pair_counts.rename(columns={'count':'nb_passes'})
    df_received = df_received[df_received['nb_passes'] >= min_pass_count]

    st.title(f"Pass Map (Passes reçues) : {selected_team}")
    pitch = Pitch(pitch_color='white', line_color='black', stripe=False, pad_bottom=0.05)
    fig, ax = pitch.draw(figsize=(10, 6))

    for _, rowp in df_pos_receveurs.iterrows():
        color = role_to_color.get(rowp['role'], 'gray')
        x_, y_ = rowp['x'], rowp['y']
        if pd.isna(x_) or pd.isna(y_):
            continue
        pitch.scatter(
            x_, y_,
            alpha=0.9,
            s=rowp['marker_size'],
            edgecolors='black',
            color=color,
            ax=ax
        )
        label = rowp['short_name'] if pd.notna(rowp['short_name']) else f"ID {rowp['player_id']}"
        ax.text(
            x_+2, y_,
            label,
            ha='left', va='center',
            color='black', fontsize=10, fontweight='bold'
        )

    if not df_received.empty:
        pass_values = df_received['nb_passes'].values
        vmin, vmax = pass_values.min(), pass_values.max()
        norm = Normalize(vmin=vmin, vmax=vmax, clip=True)
        cmap = cm.get_cmap('coolwarm')

        for rowr in df_received.itertuples():
            pidA, pidB, c = rowr.passeur_id, rowr.receveur_id, rowr.nb_passes
            pa = df_pos_receveurs[df_pos_receveurs['player_id'] == pidA]
            pb = df_pos_receveurs[df_pos_receveurs['player_id'] == pidB]
            if pa.empty or pb.empty:
                continue
            x1, y1 = pa.iloc[0]['x'], pa.iloc[0]['y']
            x2, y2 = pb.iloc[0]['x'], pb.iloc[0]['y']
            if pd.isna(x1) or pd.isna(y1) or pd.isna(x2) or pd.isna(y2):
                continue

            lw = 1 + (c*0.1)
            color_link = cmap(norm(c))

            pitch.arrows(
                x1, y1, x2, y2,
                width=lw,
                headwidth=lw*1.5,
                headlength=lw*1.5,
                color=color_link,
                alpha=0.7,
                ax=ax
            )

            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(
                mid_x, mid_y, str(c),
                color='black', fontsize=8, fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", fc='white', ec='none', alpha=0.6)
            )

    st.pyplot(fig)

if selected_player:
    st.subheader(f"Infos sur le joueur : {id_to_name.get(selected_player, f'ID {selected_player}')}")
    row_dist_passeur = df_distance_passeur[df_distance_passeur['player_id'] == selected_player]
    total_made = 0
    avg_dist = 0.0
    if not row_dist_passeur.empty:
        total_made = int(row_dist_passeur.iloc[0]['total_passes_made'])
        avg_dist = float(row_dist_passeur.iloc[0]['avg_pass_distance'])

    st.write(f"- **Passes totales effectuées** : {total_made}")
    st.write(f"- **Distance moyenne de ses passes** : {avg_dist:.2f}")
    df_pairs_player = df_pair_counts[((df_pair_counts['passeur_id'] == selected_player) | 
                                      (df_pair_counts['receveur_id'] == selected_player))].copy()
    df_pairs_player['other'] = df_pairs_player.apply(
        lambda r: r['receveur_id'] if r['passeur_id'] == selected_player else r['passeur_id'],
        axis=1
    )
    dict_exch = defaultdict(int)
    for rowp in df_pairs_player.itertuples():
        o = rowp.other
        c = rowp.count
        key = (min(selected_player,o), max(selected_player,o))
        dict_exch[key] += c

    final_exch = []
    for (a,b), c in dict_exch.items():
        if a == selected_player:
            other_id = b
        else:
            other_id = a
        final_exch.append((other_id, c))
    final_exch.sort(key=lambda x: x[1], reverse=True)
    top3_exch = final_exch[:3]

    st.write("**Top 3 coéquipiers avec qui il a le plus échangé** :")
    for i, (co_id, n) in enumerate(top3_exch, start=1):
        st.write(f"{i}. {id_to_name.get(co_id, co_id)} : {n} échanges")

    df_made_player = df_pair_counts[df_pair_counts['passeur_id'] == selected_player].copy()
    df_made_player.sort_values(by='count', ascending=False, inplace=True)
    top3_made = df_made_player.head(3)

    st.write("**Top 3 joueurs à qui il a fait le plus de passes** :")
    for i, rowx in enumerate(top3_made.itertuples(), start=1):
        rid = rowx.receveur_id
        ct = rowx.count
        st.write(f"{i}. {id_to_name.get(rid, rid)} : {ct} passes")

    df_received_player = df_pair_counts[df_pair_counts['receveur_id'] == selected_player].copy()
    df_received_player.sort_values(by='count', ascending=False, inplace=True)
    top3_recv = df_received_player.head(3)

    st.write("**Top 3 joueurs qui lui ont fait le plus de passes** :")
    for i, rowx in enumerate(top3_recv.itertuples(), start=1):
        pid = rowx.passeur_id
        ct = rowx.count
        st.write(f"{i}. {id_to_name.get(pid, pid)} : {ct} passes")
