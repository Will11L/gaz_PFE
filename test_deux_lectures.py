import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import time

# Paramètres
sample_rate = 20000  # Taux d'échantillonnage en Hz
duration = 0.01  # Durée d'acquisition en secondes
num_samples = int(sample_rate * duration)  # Nombre d'échantillons à lire

# Initialisation du graphique pour deux signaux
plt.ion()  # Mode interactif pour mise à jour du graphique en temps réel
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)  # Deux sous-graphes pour les deux canaux

xdata = np.linspace(0, duration, num_samples)
ydata1 = np.zeros(num_samples)
ydata2 = np.zeros(num_samples)
line1, = ax1.plot(xdata, ydata1, label='Canal ai0')
line2, = ax2.plot(xdata, ydata2, label='Canal ai1')

# Configuration des graphiques
ax1.set_ylim(-0.5, 6)  # Limites de tension pour ai0
ax2.set_ylim(-0.5, 6)  # Limites de tension pour ai1
ax1.set_ylabel('Tension ai0 [V]')
ax2.set_ylabel('Tension ai1 [V]')
ax2.set_xlabel('Temps [s]')
ax1.legend(loc="upper right")
ax2.legend(loc="upper right")
plt.suptitle('Lecture des signaux sur ai0 et ai1')

# Lire les données en temps réel
with nidaqmx.Task() as task:
    # Ajouter les canaux analogiques ai0 et ai1
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.DIFF)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config=TerminalConfiguration.DIFF)
    
    # Configurer la tâche pour lecture continue
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=num_samples)
    
    print("Lecture des données... Appuyez sur Ctrl+C pour arrêter.")

    try:
        while True:
            # Lire les échantillons pour tous les canaux dans la tâche
            data = task.read(number_of_samples_per_channel=num_samples)

            # Si data est une liste de deux sous-listes, chaque sous-liste correspond à un canal
            if isinstance(data, list) and len(data) == 2:
                data_ai0 = np.array(data[0])  # Données pour le canal ai0
                data_ai1 = np.array(data[1])  # Données pour le canal ai1
                print(f"data_ai0 : {data_ai0}")
                print(f"data_ai1 : {data_ai1}")
            else:
                # Si data est un tableau plat, le reconfigurer pour qu'il ait deux lignes (un par canal)
                data = np.array(data).reshape(2, num_samples)
                data_ai0, data_ai1 = data[0], data[1]

            # Afficher les valeurs moyennes pour chaque canal
            print(f"Moyenne ai0 : {np.mean(data_ai0)}, Moyenne ai1 : {np.mean(data_ai1)}")

            # Mise à jour des données sur les graphiques
            line1.set_ydata(data_ai0)
            line2.set_ydata(data_ai1)
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            time.sleep(0.1)  # Pause pour ne pas surcharger le processeur

    except KeyboardInterrupt:
        print("Lecture interrompue.")

# Fin du programme
print("Fin de la lecture des signaux.")
